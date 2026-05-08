"""Scrape the NWS Climatological Report (CLI) for a station's daily high/low.

The CLI product is the canonical daily-temperature ground truth that Polymarket
weather markets settle against. Each office issues a separate CLI for each
major airport it covers. The web product page is plain text wrapped in a <pre>
tag, with a header line naming the reporting date and a table containing
MAXIMUM and MINIMUM observed temperatures.

Free, no auth. Reports stay live as a stack of 'versions'; version=1 is the
latest. To fetch older history walk version forward (left for Phase 4).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timezone

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger

log = get_logger(__name__)


CLI_URL = "https://forecast.weather.gov/product.php"

_MONTHS = {m: i for i, m in enumerate(
    ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"], start=1
)}

_HEADER_DATE_RE = re.compile(
    r"CLIMATE SUMMARY FOR\s+([A-Z]+)\s+(\d{1,2})\s+(\d{4})",
    re.IGNORECASE,
)
_PRE_RE = re.compile(r"<pre[^>]*>(.*?)</pre>", re.IGNORECASE | re.DOTALL)
# Numeric capture for MAXIMUM/MINIMUM lines under TEMPERATURE (F).
# Examples (variable spacing):
#   MAXIMUM         64    259 PM  93    2000  69     -5       76
#   MAXIMUM        102                       MM      MM       99
_MAX_RE = re.compile(r"^\s*MAXIMUM\s+(-?\d+|MM)\b", re.IGNORECASE | re.MULTILINE)
_MIN_RE = re.compile(r"^\s*MINIMUM\s+(-?\d+|MM)\b", re.IGNORECASE | re.MULTILINE)
_TEMP_BLOCK_RE = re.compile(
    r"TEMPERATURE\s*\(F\)(.*?)(?:PRECIPITATION|WIND|RELATIVE HUMIDITY|\Z)",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class CliObservation:
    station_id: str
    issued_by: str
    report_date_local: date
    max_f: float | None
    min_f: float | None
    raw_text: str
    fetched_at_utc: datetime


_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


def issuedby_from_station(station_id: str) -> str:
    """ICAO `KXXX` -> NWS issuedby `XXX`. Defensive against non-K prefixes."""
    sid = station_id.upper().strip()
    return sid[1:] if sid.startswith("K") and len(sid) == 4 else sid


@retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
def _fetch_cli_text(issuedby: str, version: int = 1) -> str:
    headers = {"User-Agent": settings.http_user_agent, "Accept": "text/html,*/*"}
    params = {
        "site": "NWS",
        "issuedby": issuedby,
        "product": "CLI",
        "format": "TXT",
        "version": str(version),
        "glossary": "0",
    }
    with httpx.Client(timeout=settings.http_timeout_seconds, headers=headers) as c:
        r = c.get(CLI_URL, params=params)
        r.raise_for_status()
        return r.text


def _parse_header_date(body: str) -> date | None:
    m = _HEADER_DATE_RE.search(body)
    if not m:
        return None
    month_name, day, year = m.groups()
    month = _MONTHS.get(month_name.upper())
    if not month:
        return None
    try:
        return date(int(year), month, int(day))
    except ValueError:
        return None


def _parse_temp(body: str, pattern: re.Pattern) -> float | None:
    block_match = _TEMP_BLOCK_RE.search(body)
    if not block_match:
        return None
    block = block_match.group(1)
    m = pattern.search(block)
    if not m:
        return None
    val = m.group(1)
    if val.upper() == "MM":
        return None
    try:
        return float(val)
    except ValueError:
        return None


def fetch_cli_for_station(station_id: str, *, version: int = 1) -> CliObservation | None:
    issuedby = issuedby_from_station(station_id)
    fetched_at = datetime.now(timezone.utc)
    html = _fetch_cli_text(issuedby, version=version)
    pre = _PRE_RE.search(html)
    body = pre.group(1) if pre else html

    report_date = _parse_header_date(body)
    if report_date is None:
        log.warning("nws_cli_header_unparsed", station_id=station_id, issuedby=issuedby, version=version)
        return None
    max_f = _parse_temp(body, _MAX_RE)
    min_f = _parse_temp(body, _MIN_RE)
    return CliObservation(
        station_id=station_id.upper(),
        issued_by=issuedby,
        report_date_local=report_date,
        max_f=max_f,
        min_f=min_f,
        raw_text=body.strip(),
        fetched_at_utc=fetched_at,
    )


def fetch_cli_for_date(
    station_id: str,
    target_date_local: date,
    *,
    max_versions: int = 8,
) -> CliObservation | None:
    """Walk version=1..N looking for the CLI that covers `target_date_local`."""
    for version in range(1, max_versions + 1):
        try:
            obs = fetch_cli_for_station(station_id, version=version)
        except Exception:
            log.exception("cli_fetch_failed", station_id=station_id, version=version)
            return None
        if obs is None:
            return None
        if obs.report_date_local == target_date_local:
            return obs
        if obs.report_date_local < target_date_local:
            # We've stepped past the desired date going backward; not in the live archive.
            log.info(
                "cli_date_not_in_archive",
                station_id=station_id,
                target=target_date_local.isoformat(),
                latest_version_date=obs.report_date_local.isoformat(),
            )
            return None
    log.info(
        "cli_walk_exhausted",
        station_id=station_id,
        target=target_date_local.isoformat(),
        max_versions=max_versions,
    )
    return None
