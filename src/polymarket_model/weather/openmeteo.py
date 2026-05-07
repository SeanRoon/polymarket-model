from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import httpx
import numpy as np
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger
from polymarket_model.weather.stations import StationInfo, get_station

log = get_logger(__name__)


# Open-Meteo ensemble model identifiers (free; no key)
DEFAULT_MODEL = "ecmwf_ifs025"
SUPPORTED_MODELS = ("ecmwf_ifs025", "gfs025", "gfs_seamless", "icon_seamless")

_MEMBER_KEY_RE = re.compile(r"^temperature_2m(?:_member(\d+))?$")


@dataclass(frozen=True)
class EnsembleDailyExtreme:
    """Per-member daily max (or min) for a single (station, target_date_local, kind)."""
    station_id: str
    target_date_local: date
    kind: str                 # 'high' | 'low'
    unit: str                 # 'F' | 'C'
    model: str
    fetched_at_utc: datetime
    lead_hours: int
    values: np.ndarray        # shape (n_members,)
    member_ids: np.ndarray    # shape (n_members,) ints, 0 = control

    @property
    def n_members(self) -> int:
        return int(self.values.shape[0])


_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


@retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
def _get_ensemble(params: dict) -> dict:
    headers = {"User-Agent": settings.http_user_agent, "Accept": "application/json"}
    with httpx.Client(timeout=settings.http_timeout_seconds, headers=headers) as c:
        r = c.get(f"{settings.open_meteo_base_url.rstrip('/')}/ensemble", params=params)
        r.raise_for_status()
        return r.json()


def _required_forecast_days(target_date_local: date, station_tz: str, *, now_utc: datetime | None = None) -> int:
    now_utc = now_utc or datetime.now(UTC)
    tz = ZoneInfo(station_tz)
    today_local = now_utc.astimezone(tz).date()
    days = (target_date_local - today_local).days + 1
    return max(1, min(16, days))


def fetch_daily_extreme(
    station_id: str,
    target_date_local: date,
    kind: str,
    *,
    unit: str = "F",
    model: str = DEFAULT_MODEL,
    station: StationInfo | None = None,
) -> EnsembleDailyExtreme:
    """Fetch ECMWF (or other) ensemble members and compute per-member daily high/low for a station/date."""
    if kind not in ("high", "low"):
        raise ValueError(f"kind must be 'high' or 'low', got {kind!r}")
    if unit not in ("F", "C"):
        raise ValueError(f"unit must be 'F' or 'C', got {unit!r}")

    station = station or get_station(station_id)
    forecast_days = _required_forecast_days(target_date_local, station.timezone)
    temperature_unit = "fahrenheit" if unit == "F" else "celsius"

    params = {
        "latitude": station.latitude,
        "longitude": station.longitude,
        "hourly": "temperature_2m",
        "models": model,
        "temperature_unit": temperature_unit,
        "timezone": station.timezone,
        "forecast_days": forecast_days,
        "wind_speed_unit": "kmh",
    }
    fetched_at = datetime.now(UTC)
    data = _get_ensemble(params)

    hourly = data.get("hourly") or {}
    times = hourly.get("time") or []
    if not times:
        raise RuntimeError(f"open-meteo returned empty hourly time series for {station_id}")

    tz = ZoneInfo(station.timezone)
    parsed_times = [datetime.fromisoformat(t).replace(tzinfo=tz) for t in times]
    target_start = datetime.combine(target_date_local, time(0, 0), tzinfo=tz)
    target_end = target_start + timedelta(days=1)
    mask = np.array([target_start <= t < target_end for t in parsed_times])
    if not mask.any():
        raise RuntimeError(
            f"target date {target_date_local} not within forecast window for {station_id}"
        )

    member_ids: list[int] = []
    member_arrays: list[np.ndarray] = []
    for key, vals in hourly.items():
        m = _MEMBER_KEY_RE.match(key)
        if not m:
            continue
        member_id = int(m.group(1)) if m.group(1) else 0  # bare 'temperature_2m' is the control
        arr = np.asarray(vals, dtype=float)
        if arr.shape[0] != mask.shape[0]:
            log.warning("openmeteo_member_length_mismatch", key=key, len=arr.shape[0])
            continue
        member_ids.append(member_id)
        member_arrays.append(arr)

    if not member_arrays:
        raise RuntimeError(f"no ensemble members returned for {station_id} {model}")

    members = np.stack(member_arrays, axis=0)            # shape (M, T)
    target_slice = members[:, mask]                      # shape (M, hours_in_target_day)

    if np.isnan(target_slice).any():
        # Drop members with any NaN in the target window — typically tail-end leads near the
        # forecast horizon. Better to discard than to bias the distribution.
        valid = ~np.isnan(target_slice).any(axis=1)
        target_slice = target_slice[valid]
        member_ids = [mid for mid, ok in zip(member_ids, valid, strict=True) if ok]
        if target_slice.shape[0] == 0:
            raise RuntimeError(f"all ensemble members contain NaN for {station_id} {target_date_local}")

    op = np.max if kind == "high" else np.min
    daily_values = op(target_slice, axis=1)              # shape (M,)

    # Lead hours from model init proxy (now) to the centre of the local day in UTC.
    target_centre_utc = (target_start + timedelta(hours=12)).astimezone(UTC)
    lead_hours = max(0, int((target_centre_utc - fetched_at).total_seconds() // 3600))

    return EnsembleDailyExtreme(
        station_id=station.station_id,
        target_date_local=target_date_local,
        kind=kind,
        unit=unit,
        model=model,
        fetched_at_utc=fetched_at,
        lead_hours=lead_hours,
        values=daily_values,
        member_ids=np.asarray(member_ids, dtype=int),
    )
