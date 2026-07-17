"""Discover Kalshi weather events and parse their bin structure.

Each daily-temperature event (e.g. KXHIGHNY-26MAY09) contains a small set of
mutually-exclusive binary markets. Two ticker shapes:
  - "T<X>": threshold market. floor_strike or cap_strike is set; the other is None.
  - "B<X.5>": between market. Both floor_strike and cap_strike set, inclusive.

Daily NWS CLI temperatures are integers, so:
  - Closed bin (B): floor=A, cap=B  ->  [A, B+1)
  - Open-high (T): floor=X, cap=None  ->  [X+1, +inf)   (rule says "greater than X")
  - Open-low  (T): floor=None, cap=X  ->  (-inf, X)     (rule says "less than X")
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from typing import Any

from dateutil import parser as dtparser

from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import KalshiClient

log = get_logger(__name__)


# Hard-coded weather series we scan + their resolution stations. The station_id
# lines up with the NWS office cited in rules_primary; weather/stations.py owns
# the lat/lon/timezone for each.
WEATHER_SERIES: dict[str, tuple[str, str, str]] = {
    # series_ticker: (city, kind, station_id)
    # station_id is the airport whose NWS CLI Kalshi settles against — verified
    # against each series' settlement_sources (issuedby office == station minus 'K').
    # Note the non-obvious picks: Dallas settles at DFW (not Love Field), Houston at
    # Hobby (not Intercontinental).
    "KXHIGHNY":   ("New York City", "high", "KNYC"),
    # NYC and Miami low re-tickered by Kalshi to the standard KXLOWT* form (2026-07);
    # the old KXLOWNY / KXLOWMIA stopped resolving and silently dropped from collection.
    "KXLOWTNYC":  ("New York City", "low",  "KNYC"),
    "KXHIGHCHI":  ("Chicago",       "high", "KMDW"),
    "KXLOWTCHI":  ("Chicago",       "low",  "KMDW"),
    "KXHIGHMIA":  ("Miami",         "high", "KMIA"),
    "KXLOWTMIA":  ("Miami",         "low",  "KMIA"),
    "KXHIGHLAX":  ("Los Angeles",   "high", "KLAX"),
    "KXLOWTLAX":  ("Los Angeles",   "low",  "KLAX"),
    "KXHIGHAUS":  ("Austin",        "high", "KAUS"),
    "KXLOWTAUS":  ("Austin",        "low",  "KAUS"),
    "KXHIGHDEN":  ("Denver",        "high", "KDEN"),
    "KXLOWTDEN":  ("Denver",        "low",  "KDEN"),
    # Cities added 2026-06-18 (data collection only; models pending ~30d of pairs).
    "KXHIGHTATL": ("Atlanta",       "high", "KATL"),
    "KXLOWTATL":  ("Atlanta",       "low",  "KATL"),
    "KXHIGHTBOS": ("Boston",        "high", "KBOS"),
    "KXLOWTBOS":  ("Boston",        "low",  "KBOS"),
    "KXHIGHTDAL": ("Dallas",        "high", "KDFW"),
    "KXLOWTDAL":  ("Dallas",        "low",  "KDFW"),
    "KXHIGHTDC":  ("Washington DC", "high", "KDCA"),
    "KXLOWTDC":   ("Washington DC", "low",  "KDCA"),
    "KXHIGHTHOU": ("Houston",       "high", "KHOU"),
    "KXLOWTHOU":  ("Houston",       "low",  "KHOU"),
    "KXHIGHTLV":  ("Las Vegas",     "high", "KLAS"),
    "KXLOWTLV":   ("Las Vegas",     "low",  "KLAS"),
    "KXHIGHTMIN": ("Minneapolis",   "high", "KMSP"),
    "KXLOWTMIN":  ("Minneapolis",   "low",  "KMSP"),
    "KXHIGHTNOLA":("New Orleans",   "high", "KMSY"),
    "KXLOWTNOLA": ("New Orleans",   "low",  "KMSY"),
    "KXHIGHTOKC": ("Oklahoma City", "high", "KOKC"),
    "KXLOWTOKC":  ("Oklahoma City", "low",  "KOKC"),
    "KXHIGHTPHX": ("Phoenix",       "high", "KPHX"),
    "KXLOWTPHX":  ("Phoenix",       "low",  "KPHX"),
    "KXHIGHTSATX":("San Antonio",   "high", "KSAT"),
    "KXLOWTSATX": ("San Antonio",   "low",  "KSAT"),
    "KXHIGHTSEA": ("Seattle",       "high", "KSEA"),
    "KXLOWTSEA":  ("Seattle",       "low",  "KSEA"),
    "KXHIGHTSFO": ("San Francisco", "high", "KSFO"),
    "KXLOWTSFO":  ("San Francisco", "low",  "KSFO"),
    # Philadelphia added 2026-07-17 (data collection only; excluded from live signals
    # until ~30d of paired model_p/resolution data accrues, same as the 06-18 cohort).
    "KXHIGHPHIL": ("Philadelphia",  "high", "KPHL"),
    "KXLOWTPHIL": ("Philadelphia",  "low",  "KPHL"),
}


@dataclass(frozen=True)
class Bin:
    bin_index: int
    market_ticker: str            # e.g. KXHIGHNY-26MAY09-B65.5
    event_ticker: str             # e.g. KXHIGHNY-26MAY09
    subtitle: str                 # human-readable, e.g. "65° to 66°"
    floor_strike: float | None
    cap_strike: float | None
    lo_f: float                   # inclusive lower bound of [lo, hi); -inf for open-low
    hi_f: float                   # exclusive upper bound; +inf for open-high
    is_open_low: bool
    is_open_high: bool


@dataclass(frozen=True)
class WeatherEvent:
    event_ticker: str             # e.g. KXHIGHNY-26MAY09
    series_ticker: str
    title: str
    city: str
    kind: str                     # 'high' | 'low'
    station_id: str               # e.g. KNYC
    target_date_local: date
    close_time_utc: datetime
    rules_primary: str | None
    bins: list[Bin]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


# Match the "May 9, 2026" date inside an event title or rules_primary.
_DATE_IN_TITLE = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"(\d{1,2}),?\s+(\d{4})",
    re.IGNORECASE,
)
_MONTHS = {m.lower(): i for i, m in enumerate(
    ["January","February","March","April","May","June","July","August","September","October","November","December"], start=1
)}

# Match a 3-letter month abbreviation in the event ticker, e.g. KXHIGHNY-26MAY09.
_TICKER_DATE = re.compile(r"-(\d{2})([A-Z]{3})(\d{2})$")
_MONTH_ABBR = {m.upper(): i for i, m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], start=1
)}


def _parse_target_date(event: dict[str, Any]) -> date | None:
    title = event.get("title") or ""
    m = _DATE_IN_TITLE.search(title)
    if m:
        try:
            return date(int(m.group(3)), _MONTHS[m.group(1).lower()], int(m.group(2)))
        except (KeyError, ValueError):
            pass
    ticker = event.get("event_ticker") or ""
    m2 = _TICKER_DATE.search(ticker)
    if m2:
        try:
            yy, mon, dd = m2.groups()
            year = 2000 + int(yy)
            month = _MONTH_ABBR[mon.upper()]
            return date(year, month, int(dd))
        except (KeyError, ValueError):
            pass
    return None


def _interval_for_market(market: dict[str, Any]) -> tuple[float, float, bool, bool] | None:
    """Translate Kalshi (floor_strike, cap_strike) into our half-open [lo, hi) convention."""
    floor = market.get("floor_strike")
    cap = market.get("cap_strike")

    if floor is None and cap is None:
        return None

    if floor is None and cap is not None:
        # Open-low; rule says "less than cap" (strict).
        return (-math.inf, float(cap), True, False)

    if cap is None and floor is not None:
        # Open-high; rule says "greater than floor" (strict).
        # Integer +1 because daily NWS CLI values are integers.
        return (float(floor) + 1.0, math.inf, False, True)

    # Closed bin: inclusive both sides; map to [floor, cap+1).
    return (float(floor), float(cap) + 1.0, False, False)


def parse_event(event: dict[str, Any], markets: list[dict[str, Any]]) -> WeatherEvent | None:
    series = event.get("series_ticker")
    if series not in WEATHER_SERIES:
        return None
    city, kind, station_id = WEATHER_SERIES[series]
    target_date = _parse_target_date(event)
    if target_date is None:
        log.warning("event_target_date_unparsed", event_ticker=event.get("event_ticker"))
        return None

    bins: list[Bin] = []
    rules_primary: str | None = None
    close_time_utc: datetime | None = None
    for i, m in enumerate(markets):
        if m.get("status") != "active":
            continue
        interval = _interval_for_market(m)
        if interval is None:
            log.warning("market_interval_unparsed", ticker=m.get("ticker"))
            continue
        lo, hi, open_lo, open_hi = interval
        bins.append(Bin(
            bin_index=i,
            market_ticker=m.get("ticker") or "",
            event_ticker=m.get("event_ticker") or event.get("event_ticker") or "",
            subtitle=m.get("yes_sub_title") or m.get("subtitle") or "",
            floor_strike=None if m.get("floor_strike") is None else float(m["floor_strike"]),
            cap_strike=None if m.get("cap_strike") is None else float(m["cap_strike"]),
            lo_f=lo,
            hi_f=hi,
            is_open_low=open_lo,
            is_open_high=open_hi,
        ))
        rules_primary = rules_primary or m.get("rules_primary")
        ct = m.get("close_time")
        if ct:
            try:
                ct_dt = dtparser.isoparse(ct)
                if close_time_utc is None or ct_dt > close_time_utc:
                    close_time_utc = ct_dt
            except Exception:
                pass

    if not bins:
        return None

    if close_time_utc is None:
        close_time_utc = datetime.now(UTC)
    if close_time_utc.tzinfo is None:
        close_time_utc = close_time_utc.replace(tzinfo=UTC)

    # Sort bins by lo_f so the table reads bottom-up.
    bins.sort(key=lambda b: (b.lo_f, b.hi_f))
    bins = [Bin(
        bin_index=i,
        market_ticker=b.market_ticker,
        event_ticker=b.event_ticker,
        subtitle=b.subtitle,
        floor_strike=b.floor_strike,
        cap_strike=b.cap_strike,
        lo_f=b.lo_f,
        hi_f=b.hi_f,
        is_open_low=b.is_open_low,
        is_open_high=b.is_open_high,
    ) for i, b in enumerate(bins)]

    return WeatherEvent(
        event_ticker=event.get("event_ticker") or "",
        series_ticker=series,
        title=event.get("title") or "",
        city=city,
        kind=kind,
        station_id=station_id,
        target_date_local=target_date,
        close_time_utc=close_time_utc,
        rules_primary=rules_primary,
        bins=bins,
        raw=event,
    )


def discover_weather_events(client: KalshiClient | None = None) -> list[WeatherEvent]:
    """Walk the hard-coded weather series list, fetch open events + their markets, parse."""
    client = client or KalshiClient()
    events: list[WeatherEvent] = []
    for series in WEATHER_SERIES:
        try:
            metadata = client.get_series(series)
        except Exception:
            log.exception("series_check_failed", series=series)
            continue
        if metadata is None:
            log.info("series_not_found", series=series)
            continue
        try:
            open_events = client.list_open_events(series)
        except Exception:
            log.exception("events_list_failed", series=series)
            continue
        for ev in open_events:
            ticker = ev.get("event_ticker")
            if not ticker:
                continue
            try:
                markets = client.list_event_markets(ticker)
            except Exception:
                log.exception("markets_list_failed", event_ticker=ticker)
                continue
            we = parse_event(ev, markets)
            if we is not None:
                events.append(we)
    events.sort(key=lambda e: (e.target_date_local, e.series_ticker))
    return events
