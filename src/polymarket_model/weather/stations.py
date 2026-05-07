from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger

log = get_logger(__name__)


@dataclass(frozen=True)
class StationInfo:
    station_id: str
    name: str
    latitude: float
    longitude: float
    timezone: str        # IANA name, e.g. 'America/New_York'
    elevation_m: float | None = None


# Hardcoded fallback metadata for the most common Polymarket-resolution stations.
# Used only if the NWS lookup fails (network, etc).
_FALLBACK: dict[str, StationInfo] = {
    "KLGA": StationInfo("KLGA", "New York LaGuardia", 40.7769, -73.8740, "America/New_York", 6),
    "KJFK": StationInfo("KJFK", "New York JFK",       40.6413, -73.7781, "America/New_York", 4),
    "KNYC": StationInfo("KNYC", "New York Central Park", 40.7794, -73.9692, "America/New_York", 47),
    "KEWR": StationInfo("KEWR", "Newark Liberty",     40.6925, -74.1687, "America/New_York", 5),
    "KLAX": StationInfo("KLAX", "Los Angeles Intl",   33.9425, -118.4081, "America/Los_Angeles", 38),
    "KMIA": StationInfo("KMIA", "Miami Intl",         25.7959, -80.2870, "America/New_York", 3),
    "KORD": StationInfo("KORD", "Chicago O'Hare",     41.9786, -87.9047, "America/Chicago", 200),
    "KMDW": StationInfo("KMDW", "Chicago Midway",     41.7868, -87.7522, "America/Chicago", 188),
    "KATL": StationInfo("KATL", "Atlanta",            33.6407, -84.4277, "America/New_York", 313),
    "KDAL": StationInfo("KDAL", "Dallas Love",        32.8471, -96.8517, "America/Chicago", 149),
    "KDFW": StationInfo("KDFW", "Dallas-Fort Worth",  32.8998, -97.0403, "America/Chicago", 185),
    "KSEA": StationInfo("KSEA", "Seattle-Tacoma",     47.4502, -122.3088, "America/Los_Angeles", 132),
    "KBOS": StationInfo("KBOS", "Boston Logan",       42.3656, -71.0096, "America/New_York", 6),
    "KAUS": StationInfo("KAUS", "Austin-Bergstrom",   30.1975, -97.6664, "America/Chicago", 165),
    "KIAH": StationInfo("KIAH", "Houston Intercontinental", 29.9844, -95.3414, "America/Chicago", 30),
    "KHOU": StationInfo("KHOU", "Houston Hobby",      29.6454, -95.2789, "America/Chicago", 14),
    "KPHX": StationInfo("KPHX", "Phoenix Sky Harbor", 33.4373, -112.0078, "America/Phoenix", 337),
    "KDEN": StationInfo("KDEN", "Denver Intl",        39.8561, -104.6737, "America/Denver", 1655),
    "KMSP": StationInfo("KMSP", "Minneapolis-St Paul",44.8848, -93.2223, "America/Chicago", 256),
    "KPHL": StationInfo("KPHL", "Philadelphia",       39.8729, -75.2437, "America/New_York", 11),
    "KSFO": StationInfo("KSFO", "San Francisco",      37.6213, -122.3790, "America/Los_Angeles", 4),
    "KSAN": StationInfo("KSAN", "San Diego",          32.7338, -117.1933, "America/Los_Angeles", 5),
    "KLAS": StationInfo("KLAS", "Las Vegas",          36.0840, -115.1537, "America/Los_Angeles", 665),
    "KDCA": StationInfo("KDCA", "Washington Reagan",  38.8521, -77.0377, "America/New_York", 5),
    "KIAD": StationInfo("KIAD", "Washington Dulles",  38.9445, -77.4558, "America/New_York", 95),
}


_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


@retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
def _fetch_nws_station(station_id: str) -> dict | None:
    headers = {"User-Agent": settings.http_user_agent, "Accept": "application/geo+json"}
    url = f"{settings.nws_base_url.rstrip('/')}/stations/{station_id}"
    with httpx.Client(timeout=settings.http_timeout_seconds, headers=headers) as c:
        r = c.get(url)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()


@lru_cache(maxsize=256)
def get_station(station_id: str) -> StationInfo:
    """Lookup station metadata. Uses NWS API; falls back to hardcoded table on failure."""
    sid = station_id.upper().strip()
    try:
        data = _fetch_nws_station(sid)
        if data:
            geom = data.get("geometry") or {}
            coords = geom.get("coordinates") or [None, None]
            props = data.get("properties") or {}
            tz = props.get("timeZone") or _FALLBACK.get(sid, StationInfo(sid, "", 0, 0, "UTC")).timezone
            elev_m = None
            elev = props.get("elevation") or {}
            if isinstance(elev, dict) and "value" in elev:
                elev_m = elev["value"]
            return StationInfo(
                station_id=sid,
                name=props.get("name") or "",
                latitude=float(coords[1]) if coords[1] is not None else _FALLBACK[sid].latitude,
                longitude=float(coords[0]) if coords[0] is not None else _FALLBACK[sid].longitude,
                timezone=tz,
                elevation_m=elev_m,
            )
    except Exception:
        log.warning("nws_station_lookup_failed", station_id=sid)
    if sid in _FALLBACK:
        return _FALLBACK[sid]
    raise KeyError(f"Unknown station: {sid}")
