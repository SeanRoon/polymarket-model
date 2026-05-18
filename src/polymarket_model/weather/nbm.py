"""NBM probabilistic temperature forecasts via QMD GRIB2 on AWS S3.

NBM (NWS National Blend of Models) publishes the QMD product family at
00/06/12/18 UTC. QMD contains instantaneous 2m TMP at 21 percentile levels
(0%, 5%, ..., 95%, 100%) — **not** a period Tmax/Tmin product. NBM emits its
deterministic 12h MaxT/MinT only in the CORE family. We approximate the daily
Tmax/Tmin distribution by picking the forecast hour valid at each city's
climatological peak hour (Tmax ~4pm LST, Tmin ~5am LST) and using the TMP
percentiles at that instant.

This is a known approximation: temperature plateau makes peak-hour TMP a close
proxy for the true daily Tmax (~0.5-1F bias), and Phase 3 EMOS will add a
learned correction. Code is structured so swapping the proxy strategy is local
to `_peak_hour_target_utc`.
"""
from __future__ import annotations

import contextlib
import re
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta, timezone
from pathlib import Path

import eccodes  # type: ignore[import-untyped]
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger
from polymarket_model.weather.openmeteo import standard_offset
from polymarket_model.weather.stations import StationInfo, get_station

log = get_logger(__name__)


NBM_S3_BASE = "https://noaa-nbm-grib2-pds.s3.amazonaws.com"
# QMD upload completes 6-8h after the cycle time. 9h gives a safety margin.
QMD_UPLOAD_LAG_HOURS = 9
DEFAULT_PERCENTILES: tuple[int, ...] = (10, 25, 50, 75, 90)
# Climatological peak-Tmax is ~3-4pm local LST; pre-dawn Tmin is ~5am LST.
PEAK_HOUR_OFFSET_HIGH = 16
PEAK_HOUR_OFFSET_LOW = 5
# NBM forecast horizon: hourly through f036, 3-hourly through f192, 6-hourly to f264.
MAX_LEAD_HOURS = 264


@dataclass(frozen=True)
class NBMQuantileForecast:
    """Five-quantile forecast for a station's daily Tmax or Tmin.

    `quantiles` keys are integer percentile labels (10, 25, 50, 75, 90); values
    are temperatures in Fahrenheit. By construction `quantiles` is monotonic
    non-decreasing.
    """
    station_id: str
    target_date_local: date
    kind: str                     # 'high' | 'low'
    unit: str                     # 'F'
    model: str                    # 'nbm_qmd'
    cycle_time_utc: datetime
    valid_time_utc: datetime
    lead_hours: int
    quantiles: dict[int, float]
    percentile_levels: tuple[int, ...] = field(default=DEFAULT_PERCENTILES)


def _aws_qmd_url(cycle: datetime, fxx: int, region: str = "co") -> str:
    return (
        f"{NBM_S3_BASE}/blend.{cycle:%Y%m%d}/{cycle:%H}/qmd/"
        f"blend.t{cycle:%H}z.qmd.f{fxx:03d}.{region}.grib2"
    )


def _peak_hour_target_utc(station: StationInfo, target_date_local: date, kind: str) -> datetime:
    """Climatological peak-Tmax (4pm LST) or Tmin (5am LST) hour in UTC.

    Uses the station's *standard* offset (LST) to match Kalshi's settlement
    convention — see `weather/openmeteo.lst_day_window_utc` for the same logic
    applied to ensemble-window math.
    """
    offset = standard_offset(station.timezone)
    fixed_tz = timezone(offset)
    midnight_local = datetime.combine(target_date_local, time(0, 0), tzinfo=fixed_tz)
    delta = PEAK_HOUR_OFFSET_HIGH if kind == "high" else PEAK_HOUR_OFFSET_LOW
    return (midnight_local + timedelta(hours=delta)).astimezone(UTC)


def _pick_cycle(now: datetime, target_valid_utc: datetime) -> tuple[datetime, int]:
    """Choose the freshest 00/06/12/18Z cycle whose QMD upload is complete and that
    can forecast the requested target valid time.

    Walks back in 6h steps if the natural pick gives a non-positive or out-of-horizon lead.
    """
    now_hour = now.astimezone(UTC).replace(minute=0, second=0, microsecond=0)
    candidate = now_hour - timedelta(hours=QMD_UPLOAD_LAG_HOURS)
    candidate_hour = (candidate.hour // 6) * 6
    cycle = candidate.replace(hour=candidate_hour)
    for _ in range(8):  # at most 48h of walk-back
        lead = (target_valid_utc - cycle).total_seconds() / 3600
        if lead < 1:
            # Target already in the past for this cycle — but stale snapshots want a forward forecast.
            # Forecasts of past hours aren't useful, but the closest forward cycle is the next one
            # (which doesn't yet exist), so we surface a clear error.
            raise ValueError(
                f"NBM target {target_valid_utc.isoformat()} predates the freshest "
                f"available cycle {cycle.isoformat()}; nothing to fetch."
            )
        if lead > MAX_LEAD_HOURS:
            cycle -= timedelta(hours=6)
            continue
        return cycle, round(lead)
    raise ValueError(f"Could not find a usable NBM cycle for valid time {target_valid_utc}")


_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


@retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
def _http_get_text(url: str) -> str:
    with httpx.Client(timeout=settings.http_timeout_seconds, headers={"User-Agent": settings.http_user_agent}) as c:
        r = c.get(url)
        r.raise_for_status()
        return r.text


@retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
def _http_get_range(url: str, start: int, end: int) -> bytes:
    headers = {"User-Agent": settings.http_user_agent, "Range": f"bytes={start}-{end}"}
    with httpx.Client(timeout=settings.http_timeout_seconds, headers=headers) as c:
        r = c.get(url)
        r.raise_for_status()
        return r.content


# wgrib2 .idx line: <msg>:<offset>:<reftime>:<var>:<level>:<fcsttime>:<aux1>:<aux2>:
_IDX_LINE_RE = re.compile(r"^(?P<msg>\d+):(?P<offset>\d+):(?P<rest>.+)$")


def _parse_idx(text: str) -> list[dict]:
    rows: list[dict] = []
    raw = [ln for ln in text.splitlines() if ln.strip()]
    for line in raw:
        m = _IDX_LINE_RE.match(line)
        if not m:
            continue
        rows.append({
            "msg": int(m.group("msg")),
            "offset": int(m.group("offset")),
            "line": line,
        })
    for i, row in enumerate(rows):
        row["start_byte"] = row["offset"]
        row["end_byte"] = rows[i + 1]["offset"] - 1 if i + 1 < len(rows) else None
    return rows


def _select_tmp_percentile_rows(
    idx_rows: list[dict],
    percentiles: tuple[int, ...],
) -> list[dict]:
    """Find the .idx rows for TMP 2m at exactly the requested percentile levels."""
    selected: dict[int, dict] = {}
    for row in idx_rows:
        if ":TMP:2 m above ground:" not in row["line"]:
            continue
        for pct in percentiles:
            if pct in selected:
                continue
            if re.search(rf":{pct}% level(?::|$)", row["line"]):
                selected[pct] = row
                break
    missing = [p for p in percentiles if p not in selected]
    if missing:
        raise RuntimeError(f"NBM QMD .idx missing TMP percentile rows: {missing}")
    return [selected[p] for p in percentiles]


def _fetch_percentile_messages_concatenated(
    grib_url: str,
    msg_rows: list[dict],
    *,
    max_workers: int = 5,
) -> bytes:
    """Fetch only the specific percentile messages in parallel; return concatenated GRIB2 bytes.

    GRIB2 supports message concatenation in a single file/stream, so the result of joining
    these byte blobs is a valid multi-message file that eccodes can iterate. Per-file
    bandwidth is ~5MB/message vs ~80MB for the full TMP percentile block.
    """
    def fetch_one(row: dict) -> bytes:
        start = row["start_byte"]
        end = row["end_byte"]
        # Last GRIB2 message in the file: pad the end to a generous upper bound (S3 returns
        # only the available bytes for an over-range request).
        if end is None:
            end = start + 10_000_000
        return _http_get_range(grib_url, start, end)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        blobs = list(pool.map(fetch_one, msg_rows))
    return b"".join(blobs)


def _decode_tmp_percentiles_multi(
    blob: bytes,
    points: list[tuple[str, float, float]],
    percentiles: tuple[int, ...],
) -> dict[str, dict[int, float]]:
    """Iterate the GRIB2 blob once and extract {pct: temp_F} at the nearest grid cell for many points.

    Why eccodes instead of cfgrib/xarray: NBM QMD percentile messages share all the
    standard time/level/grid metadata and differ only in `percentileValue`. cfgrib
    won't auto-promote percentileValue to a dimension, so a multi-message blob
    collapses to a single record. Direct eccodes iteration sidesteps this cleanly
    and lets us use the built-in `codes_grib_find_nearest` for the lat/lon lookup
    (which handles NBM's Lambert Conformal grid correctly without manual KDTree work).
    """
    with tempfile.NamedTemporaryFile(suffix=".grib2", delete=False) as f:
        f.write(blob)
        path = Path(f.name)

    wanted = set(percentiles)
    out: dict[str, dict[int, float]] = {key: {} for key, _, _ in points}
    try:
        with open(path, "rb") as fh:
            while True:
                gid = eccodes.codes_grib_new_from_file(fh)
                if gid is None:
                    break
                try:
                    pct = int(eccodes.codes_get(gid, "percentileValue"))
                    if pct in wanted:
                        for key, lat, lon in points:
                            if pct in out[key]:
                                continue
                            nearest = eccodes.codes_grib_find_nearest(gid, lat, lon, npoints=1)[0]
                            kelvin = float(nearest.value)
                            out[key][pct] = (kelvin - 273.15) * 9 / 5 + 32
                finally:
                    eccodes.codes_release(gid)
        for key, by_pct in out.items():
            missing = wanted - by_pct.keys()
            if missing:
                raise RuntimeError(f"NBM QMD blob missing percentile {sorted(missing)} for point {key!r}")
        return out
    finally:
        with contextlib.suppress(OSError):
            path.unlink()


def _enforce_monotonic(quantiles: dict[int, float]) -> dict[int, float]:
    """NBM percentile messages are constructed to be monotonic, but nearest-neighbor
    selection across separate grid messages could theoretically introduce tiny inversions.
    Defensive non-decreasing pass."""
    fixed: dict[int, float] = {}
    running = -float("inf")
    for pct in sorted(quantiles.keys()):
        val = max(quantiles[pct], running)
        fixed[pct] = val
        running = val
    return fixed


def _plan_fetch(
    station_id: str,
    target_date_local: date,
    kind: str,
    now: datetime,
) -> tuple[StationInfo, datetime, datetime, int]:
    if kind not in ("high", "low"):
        raise ValueError(f"kind must be 'high' or 'low', got {kind!r}")
    station = get_station(station_id)
    target_valid_utc = _peak_hour_target_utc(station, target_date_local, kind)
    cycle, lead_hours = _pick_cycle(now, target_valid_utc)
    return station, target_valid_utc, cycle, lead_hours


def fetch_nbm_quantiles(
    station_id: str,
    target_date_local: date,
    kind: str,
    *,
    percentiles: tuple[int, ...] = DEFAULT_PERCENTILES,
    now: datetime | None = None,
) -> NBMQuantileForecast:
    """Fetch a 5-quantile NBM forecast for the LST day's Tmax (kind='high') or Tmin (kind='low').

    Single-shot convenience wrapper. For multiple stations sharing the same NBM cycle,
    prefer `fetch_nbm_quantiles_many` — it dedupes the GRIB2 download (~80MB per cycle)
    across all stations in the same (cycle, fxx) group.
    """
    station, target_valid_utc, cycle, lead_hours = _plan_fetch(
        station_id, target_date_local, kind, now or datetime.now(UTC)
    )
    grib_url = _aws_qmd_url(cycle, lead_hours, region="co")
    idx_rows = _parse_idx(_http_get_text(grib_url + ".idx"))
    msg_rows = _select_tmp_percentile_rows(idx_rows, percentiles)
    blob = _fetch_percentile_messages_concatenated(grib_url, msg_rows)
    decoded = _decode_tmp_percentiles_multi(
        blob,
        [(station_id, station.latitude, station.longitude)],
        percentiles,
    )
    quantiles = _enforce_monotonic(decoded[station_id])
    return NBMQuantileForecast(
        station_id=station_id,
        target_date_local=target_date_local,
        kind=kind,
        unit="F",
        model="nbm_qmd",
        cycle_time_utc=cycle,
        valid_time_utc=target_valid_utc,
        lead_hours=lead_hours,
        quantiles=quantiles,
        percentile_levels=tuple(sorted(quantiles.keys())),
    )


# (station_id, target_date_local, kind)
NBMRequestKey = tuple[str, date, str]


def _process_cycle_lead_group(
    cycle: datetime,
    lead: int,
    keys_in_group: list[NBMRequestKey],
    plans: dict[NBMRequestKey, tuple[StationInfo, datetime, datetime, int]],
    percentiles: tuple[int, ...],
) -> dict[NBMRequestKey, NBMQuantileForecast | Exception]:
    """Download + decode one (cycle, fxx) GRIB2 file for all stations sharing it."""
    grib_url = _aws_qmd_url(cycle, lead, region="co")
    try:
        idx_rows = _parse_idx(_http_get_text(grib_url + ".idx"))
        msg_rows = _select_tmp_percentile_rows(idx_rows, percentiles)
        blob = _fetch_percentile_messages_concatenated(grib_url, msg_rows)
        points = [
            (key[0], plans[key][0].latitude, plans[key][0].longitude)
            for key in keys_in_group
        ]
        decoded = _decode_tmp_percentiles_multi(blob, points, percentiles)
    except Exception as ex:
        return {key: ex for key in keys_in_group}

    out: dict[NBMRequestKey, NBMQuantileForecast | Exception] = {}
    for key in keys_in_group:
        _, target_valid_utc, _, _ = plans[key]
        try:
            quantiles = _enforce_monotonic(decoded[key[0]])
            out[key] = NBMQuantileForecast(
                station_id=key[0],
                target_date_local=key[1],
                kind=key[2],
                unit="F",
                model="nbm_qmd",
                cycle_time_utc=cycle,
                valid_time_utc=target_valid_utc,
                lead_hours=lead,
                quantiles=quantiles,
                percentile_levels=tuple(sorted(quantiles.keys())),
            )
        except Exception as ex:
            out[key] = ex
    return out


def fetch_nbm_quantiles_many(
    requests: list[NBMRequestKey],
    *,
    percentiles: tuple[int, ...] = DEFAULT_PERCENTILES,
    now: datetime | None = None,
    max_workers: int = 4,
) -> dict[NBMRequestKey, NBMQuantileForecast | Exception]:
    """Batched fetch: dedupe + parallelize GRIB2 downloads across (cycle, fxx) groups.

    Each unique NBM (cycle, fxx) file is downloaded once (~25MB of selected percentile
    messages) and decoded for every (station, date, kind) request that maps to it. Per-group
    download and decode runs in a worker thread; per-file the 5 percentile-message byte
    ranges fetch concurrently. Failures are captured per-key as Exception values so callers
    can still record partial success.
    """
    when = now or datetime.now(UTC)
    plans: dict[NBMRequestKey, tuple[StationInfo, datetime, datetime, int] | Exception] = {}
    for key in requests:
        try:
            plans[key] = _plan_fetch(key[0], key[1], key[2], when)
        except Exception as ex:
            plans[key] = ex

    grouped: dict[tuple[datetime, int], list[NBMRequestKey]] = {}
    for key, plan in plans.items():
        if isinstance(plan, Exception):
            continue
        _, _, cycle, lead = plan
        grouped.setdefault((cycle, lead), []).append(key)

    results: dict[NBMRequestKey, NBMQuantileForecast | Exception] = {
        key: plan for key, plan in plans.items() if isinstance(plan, Exception)
    }
    if not grouped:
        return results

    # Plans dict has only valid (non-exception) entries for keys we hand to the group worker.
    valid_plans = {k: v for k, v in plans.items() if not isinstance(v, Exception)}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_process_cycle_lead_group, cyc, lead, keys, valid_plans, percentiles): (cyc, lead)
            for (cyc, lead), keys in grouped.items()
        }
        for fut in as_completed(futures):
            results.update(fut.result())
    return results
