from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from typing import Any

from dateutil import parser as dtparser

from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import GammaClient, parse_json_field

log = get_logger(__name__)


WEATHER_TAG_ID = 84
DAILY_TEMPERATURE_TAG_ID = 103040


@dataclass(frozen=True)
class Bin:
    outcome_index: int
    yes_token_id: str
    no_token_id: str
    label: str
    lo_f: float       # inclusive lower bound in event.unit (-inf for open low)
    hi_f: float       # exclusive upper bound in event.unit (+inf for open high)
    is_open_low: bool
    is_open_high: bool


@dataclass(frozen=True)
class WeatherEvent:
    event_id: str
    slug: str
    title: str
    end_date_utc: datetime
    target_date_local: date
    kind: str                 # 'high' | 'low'
    city: str
    station_id: str | None
    resolution_source: str | None
    unit: str                 # 'F' | 'C'
    condition_ids: list[str]
    bins: list[Bin]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


_KIND_PATTERNS = {
    "high": re.compile(r"\bhighest\b", re.IGNORECASE),
    "low": re.compile(r"\blowest\b", re.IGNORECASE),
}

_SLUG_DATE_RE = re.compile(
    r"-on-(?P<month>[a-z]+)-(?P<day>\d{1,2})-(?P<year>\d{4})$",
    re.IGNORECASE,
)
_MONTHS = {m.lower(): i for i, m in enumerate(
    ["January","February","March","April","May","June","July","August","September","October","November","December"], start=1
)}

# Match four-letter ICAO codes (K + 3 uppercase letters). NWS US airports are KXXX.
_STATION_RE = re.compile(r"\b(K[A-Z]{3})\b")


def _parse_kind(title: str) -> str | None:
    for kind, pat in _KIND_PATTERNS.items():
        if pat.search(title):
            return kind
    return None


def _parse_target_date_from_slug(slug: str) -> date | None:
    m = _SLUG_DATE_RE.search(slug)
    if not m:
        return None
    month = _MONTHS.get(m.group("month").lower())
    if not month:
        return None
    try:
        return date(int(m.group("year")), month, int(m.group("day")))
    except ValueError:
        return None


def _parse_city(slug: str, title: str) -> str:
    # Slug pattern: highest-temperature-in-{city-slug}-on-...
    m = re.search(r"temperature-in-(.+?)-on-", slug)
    if m:
        city = m.group(1).replace("-", " ")
        return city.title()
    # Fallback: parse from title "Highest temperature in {City} on May 8?"
    m2 = re.search(r"temperature in (.+?) on ", title or "", re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return slug


def _extract_station_id(resolution_source: str | None) -> str | None:
    if not resolution_source:
        return None
    m = _STATION_RE.search(resolution_source)
    return m.group(1) if m else None


def _detect_unit(label: str) -> str:
    """Return 'F' or 'C' based on label content. Defaults to 'F'."""
    s = label.upper()
    if "°C" in s or "º C" in s or re.search(r"\d\s*C\b", s):
        return "C"
    return "F"


def _normalize_label(label: str) -> str:
    """Strip degree signs and unit letters so a numeric parser can work cleanly."""
    s = label
    for ch in ("°", "º", "Â°"):
        s = s.replace(ch, " ")
    s = s.lower()
    # Replace standalone unit letters surrounded by digits/spaces with a space.
    s = re.sub(r"(?<=\d)\s*[fc]\b", " ", s)
    s = re.sub(r"\b[fc](?=\s|$)", " ", s)
    return s


def _parse_bin_label(label: str | None) -> tuple[float, float, bool, bool] | None:
    """Parse a Polymarket bin label into half-open interval [lo, hi).
    Returns (lo, hi, is_open_low, is_open_high) or None if unparseable.

    Polymarket reports daily highs as integers in either °F (US) or °C (intl).
    Conventions (in whatever unit the label uses):
      "55°F or below"   -> [-inf, 56)
      "56-57°F"         -> [56, 58)
      "74°F or higher"  -> [74, +inf)
      "62°F"            -> [62, 63)  (single-integer bin)
    """
    if not label:
        return None
    s = _normalize_label(label)

    # Open-low: "X or below" / "below X"
    m = re.search(r"(-?\d+)\s*or\s*below", s)
    if m:
        x = int(m.group(1))
        return (-math.inf, float(x + 1), True, False)
    m = re.search(r"below\s*(-?\d+)", s)
    if m:
        x = int(m.group(1))
        return (-math.inf, float(x), True, False)

    # Open-high: "X or higher / above / more / greater"
    m = re.search(r"(-?\d+)\s*or\s*(higher|above|more|greater)", s)
    if m:
        x = int(m.group(1))
        return (float(x), math.inf, False, True)
    m = re.search(r"above\s*(-?\d+)", s)
    if m:
        x = int(m.group(1))
        return (float(x + 1), math.inf, False, True)

    # Range: "A-B" / "A to B" / "between A and B"
    m = re.search(r"(-?\d+)\s*(?:-|–|to|and)\s*(-?\d+)", s)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a > b:
            a, b = b, a
        return (float(a), float(b + 1), False, False)

    # Single integer fallback (e.g. "6")
    m = re.search(r"-?\d+", s)
    if m and re.fullmatch(r"\s*-?\d+\s*", s):
        x = int(m.group(0))
        return (float(x), float(x + 1), False, False)

    return None


def parse_event(event: dict[str, Any]) -> WeatherEvent | None:
    slug = event.get("slug") or ""
    title = event.get("title") or ""
    kind = _parse_kind(title) or _parse_kind(slug)
    if kind is None:
        return None

    target_date = _parse_target_date_from_slug(slug)
    end_date_raw = event.get("endDate")
    end_date_utc = dtparser.isoparse(end_date_raw) if end_date_raw else datetime.now(UTC)
    if end_date_utc.tzinfo is None:
        end_date_utc = end_date_utc.replace(tzinfo=UTC)

    if target_date is None:
        # Fall back to UTC end-date date — close enough for slug-less cases.
        target_date = end_date_utc.date()

    city = _parse_city(slug, title)

    # resolutionSource sometimes lives at event level, sometimes per-market — check event then bins.
    resolution_source = event.get("resolutionSource")
    station_id = _extract_station_id(resolution_source)

    bins: list[Bin] = []
    condition_ids: list[str] = []
    units_seen: list[str] = []
    for idx, m in enumerate(event.get("markets") or []):
        token_ids = parse_json_field(m.get("clobTokenIds")) or []
        if not isinstance(token_ids, list) or len(token_ids) < 2:
            continue
        outcomes = parse_json_field(m.get("outcomes")) or ["Yes", "No"]
        if isinstance(outcomes, list) and len(outcomes) >= 2 and outcomes[0].lower() == "no":
            yes_token, no_token = token_ids[1], token_ids[0]
        else:
            yes_token, no_token = token_ids[0], token_ids[1]

        label = m.get("groupItemTitle") or m.get("question") or ""
        parsed = _parse_bin_label(label)
        if parsed is None:
            log.warning("bin_label_unparseable", event_slug=slug, label=label, market_id=m.get("id"))
            continue
        lo, hi, open_lo, open_hi = parsed
        units_seen.append(_detect_unit(label))
        bins.append(Bin(
            outcome_index=idx,
            yes_token_id=str(yes_token),
            no_token_id=str(no_token),
            label=label,
            lo_f=lo,
            hi_f=hi,
            is_open_low=open_lo,
            is_open_high=open_hi,
        ))
        if m.get("conditionId"):
            condition_ids.append(str(m["conditionId"]))

        if not resolution_source and m.get("resolutionSource"):
            resolution_source = m.get("resolutionSource")
            station_id = _extract_station_id(resolution_source) or station_id

    if not bins:
        return None

    # Pick the dominant unit; if mixed (shouldn't happen) prefer F.
    unit = "C" if units_seen and units_seen.count("C") > units_seen.count("F") else "F"

    return WeatherEvent(
        event_id=str(event.get("id") or ""),
        slug=slug,
        title=title,
        end_date_utc=end_date_utc,
        target_date_local=target_date,
        kind=kind,
        city=city,
        station_id=station_id,
        resolution_source=resolution_source,
        unit=unit,
        condition_ids=condition_ids,
        bins=bins,
        raw=event,
    )


def discover_weather_events(
    gamma: GammaClient | None = None,
    tag_ids: tuple[int, ...] = (WEATHER_TAG_ID,),
    limit: int = 500,
    units: tuple[str, ...] | None = ("F",),
) -> list[WeatherEvent]:
    """Fetch active weather events and parse them into WeatherEvent objects.

    Args:
      units: filter by unit. Default ('F',) limits to US cities. Pass None for all units.
    """
    gamma = gamma or GammaClient()
    seen: dict[str, dict[str, Any]] = {}
    for tag_id in tag_ids:
        for ev in gamma.list_active_events_by_tag(tag_id, limit=limit):
            eid = str(ev.get("id"))
            if eid and eid not in seen:
                seen[eid] = ev

    parsed: list[WeatherEvent] = []
    for ev in seen.values():
        try:
            we = parse_event(ev)
        except Exception:
            log.exception("event_parse_failed", slug=ev.get("slug"))
            continue
        if we is None:
            continue
        if units is not None and we.unit not in units:
            continue
        parsed.append(we)
    parsed.sort(key=lambda w: w.end_date_utc)
    return parsed
