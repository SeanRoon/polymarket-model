"""Per-station day-of-year temperature climatology from the ERA5 reanalysis archive.

Purpose: give the calibration layer a seasonal anchor. EMOS (`calibration/emos.py`)
fits in *anomaly space* — actual minus climatology regressed on forecast minus
climatology — so its rolling 60-day window learns regime structure (marine-layer
shrinkage, spread inflation) instead of memorizing the current season's mean
temperature. Without the anchor, every seasonal transition forces the window to
re-learn the intercept over weeks; with it, the seasonal cycle drops out of the
regression entirely.

Source is Open-Meteo's free ERA5 archive API (one request per station covering
~20 years of daily Tmax/Tmin). Two deliberate approximations, both absorbed by the
EMOS intercept because they are (near-)constant offsets:

- ERA5 is a 0.25° grid-cell average, not the station observation. The *shape* of
  the seasonal cycle is what matters; a level offset is soaked up by EMOS `a`.
- Daily extremes use the station's IANA calendar day, not Kalshi's LST window.
  The one-hour summer shift changes a 30-year daily mean negligibly.

The smoothed climatology is written once to `data/station_climatology.parquet`
(committed; refresh with `polymarket fetch-climatology` maybe once a year) and
loaded by the recorder and `compute-emos` at startup.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import httpx
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger
from polymarket_model.weather.stations import StationInfo, get_station

log = get_logger(__name__)

DEFAULT_CLIMATOLOGY_PARQUET = settings.data_dir / "station_climatology.parquet"

# Circular smoothing half-width in days: the climatology for day-of-year d is the mean
# over all historical observations within +/- this many days of d (wrapping the year end).
DEFAULT_WINDOW_DAYS = 7

CLIMATOLOGY_PARQUET_SCHEMA = pa.schema([
    pa.field("station_id", pa.string(), nullable=False),
    pa.field("kind", pa.string(), nullable=False),          # 'high' | 'low'
    pa.field("doy", pa.int32(), nullable=False),            # 1..366
    pa.field("climo_f", pa.float64(), nullable=False),
    pa.field("n_obs", pa.int32(), nullable=False),
    pa.field("years_back", pa.int32(), nullable=False),
    pa.field("source", pa.string(), nullable=False),
    pa.field("computed_at_utc", pa.timestamp("us", tz="UTC"), nullable=False),
])


@dataclass(frozen=True)
class StationClimatology:
    """366-entry day-of-year climatology for one (station, kind)."""
    station_id: str
    kind: str
    climo_f: np.ndarray   # shape (366,), index = doy - 1
    n_obs: np.ndarray     # shape (366,)
    years_back: int
    source: str


_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


@retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
def _get_archive(params: dict) -> dict:
    headers = {"User-Agent": settings.http_user_agent, "Accept": "application/json"}
    with httpx.Client(timeout=max(settings.http_timeout_seconds, 60.0), headers=headers) as c:
        r = c.get(f"{settings.open_meteo_archive_base_url.rstrip('/')}/archive", params=params)
        r.raise_for_status()
        return r.json()


def fetch_daily_history(
    station_id: str,
    *,
    years_back: int = 20,
    station: StationInfo | None = None,
    now: date | None = None,
) -> dict[str, tuple[list[date], list[float]]]:
    """Fetch ~years_back years of ERA5 daily Tmax/Tmin (°F) for a station.

    Returns {'high': (dates, values), 'low': (dates, values)} with None rows dropped.
    One archive request per station; the range ends last Dec 31 so partial years
    can't tilt the day-of-year means.
    """
    station = station or get_station(station_id)
    today = now or datetime.now(UTC).date()
    end = date(today.year - 1, 12, 31)
    start = date(end.year - years_back + 1, 1, 1)
    params = {
        "latitude": station.latitude,
        "longitude": station.longitude,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": station.timezone,
    }
    data = _get_archive(params)
    daily = data.get("daily") or {}
    times = [date.fromisoformat(t) for t in daily.get("time") or []]
    out: dict[str, tuple[list[date], list[float]]] = {}
    for kind, key in (("high", "temperature_2m_max"), ("low", "temperature_2m_min")):
        vals = daily.get(key) or []
        ds: list[date] = []
        vs: list[float] = []
        for d, v in zip(times, vals, strict=True):
            if v is None:
                continue
            ds.append(d)
            vs.append(float(v))
        out[kind] = (ds, vs)
    return out


def doy_of(d: date) -> int:
    """Day-of-year 1..366. In non-leap years Dec 31 is 365; index 366 exists only in leap years."""
    return d.timetuple().tm_yday


def daily_series_to_doy_climatology(
    dates: list[date],
    values: list[float],
    *,
    window_days: int = DEFAULT_WINDOW_DAYS,
) -> tuple[np.ndarray, np.ndarray]:
    """Reduce a multi-year daily series to a smoothed 366-entry day-of-year climatology.

    climo[d] = mean of all observations whose day-of-year is within +/- window_days of
    d+1, wrapping circularly across the year boundary (so early January borrows from
    late December and vice versa). Feb 29 (doy 60 in leap years) is thin on raw counts
    but the window fills it from neighboring days. Returns (climo[366], n_obs[366]);
    entries with zero observations in the window are NaN.
    """
    sums = np.zeros(366)
    counts = np.zeros(366)
    for d, v in zip(dates, values, strict=True):
        sums[doy_of(d) - 1] += v
        counts[doy_of(d) - 1] += 1

    climo = np.full(366, np.nan)
    n_obs = np.zeros(366, dtype=int)
    offsets = np.arange(-window_days, window_days + 1)
    for i in range(366):
        idx = (i + offsets) % 366
        c = counts[idx].sum()
        n_obs[i] = int(c)
        if c > 0:
            climo[i] = sums[idx].sum() / c
    return climo, n_obs


def build_station_climatology(
    station_id: str,
    *,
    years_back: int = 20,
    window_days: int = DEFAULT_WINDOW_DAYS,
    station: StationInfo | None = None,
) -> list[StationClimatology]:
    """Fetch history and reduce to climatologies for both kinds. Network call."""
    history = fetch_daily_history(station_id, years_back=years_back, station=station)
    out: list[StationClimatology] = []
    for kind, (dates, values) in sorted(history.items()):
        if not dates:
            log.warning("climatology_empty_history", station=station_id, kind=kind)
            continue
        climo, n_obs = daily_series_to_doy_climatology(dates, values, window_days=window_days)
        out.append(StationClimatology(
            station_id=station_id.upper(),
            kind=kind,
            climo_f=climo,
            n_obs=n_obs,
            years_back=years_back,
            source="era5_openmeteo",
        ))
    return out


def write_climatology(
    path: Path, climatologies: list[StationClimatology], *, merge_existing: bool = True
) -> None:
    """Atomic write: one row per (station, kind, doy); NaN entries are skipped.

    With `merge_existing` (default), rows already in the file for stations NOT in this
    batch are preserved — so a targeted or partially-failed `fetch-climatology` run can
    never silently drop other stations from the committed file. Refetched stations are
    fully replaced.
    """
    now = datetime.now(UTC)
    rows: list[dict] = []
    for c in climatologies:
        for i in range(366):
            if np.isnan(c.climo_f[i]):
                continue
            rows.append({
                "station_id": c.station_id,
                "kind": c.kind,
                "doy": i + 1,
                "climo_f": float(c.climo_f[i]),
                "n_obs": int(c.n_obs[i]),
                "years_back": c.years_back,
                "source": c.source,
                "computed_at_utc": now,
            })
    if merge_existing and path.exists():
        refreshed = {c.station_id for c in climatologies}
        kept = [r for r in pq.read_table(path).to_pylist() if r["station_id"] not in refreshed]
        rows = kept + rows
    rows.sort(key=lambda r: (r["station_id"], r["kind"], r["doy"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(rows, schema=CLIMATOLOGY_PARQUET_SCHEMA)
    fd, tmp = tempfile.mkstemp(prefix=".climatology-", suffix=".parquet", dir=str(path.parent))
    os.close(fd)
    try:
        pq.write_table(tbl, tmp, compression="zstd")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load_climatology(path: Path) -> dict[tuple[str, str], np.ndarray]:
    """Return {(station_id, kind): climo_f[366]} (NaN where absent); empty if file missing."""
    if not path.exists():
        return {}
    tbl = pq.read_table(path, columns=["station_id", "kind", "doy", "climo_f"])
    out: dict[tuple[str, str], np.ndarray] = {}
    for row in tbl.to_pylist():
        key = (row["station_id"], row["kind"])
        if key not in out:
            out[key] = np.full(366, np.nan)
        out[key][int(row["doy"]) - 1] = float(row["climo_f"])
    return out


def climo_for(
    climatology: dict[tuple[str, str], np.ndarray],
    station_id: str | None,
    kind: str | None,
    target_date: date,
) -> float | None:
    """Look up the climatological value for a (station, kind) on a date; None if absent."""
    if not station_id or not kind:
        return None
    arr = climatology.get((station_id, kind))
    if arr is None:
        return None
    v = arr[doy_of(target_date) - 1]
    return None if np.isnan(v) else float(v)
