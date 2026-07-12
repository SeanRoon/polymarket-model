"""Whole-venue market scan for the self-directed paper agent.

Flattens `/events?status=open&with_nested_markets=true` into one row per market,
filters to books an agent could plausibly paper-trade (two-sided, some volume,
closing soon enough to score), and renders a compact markdown digest grouped by
category. The digest is the agent's entire view of the venue — keep it small
enough to read in one sitting, rich enough to reason about.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import KalshiClient

log = get_logger(__name__)


@dataclass(frozen=True)
class MarketRow:
    market_ticker: str
    event_ticker: str
    category: str
    event_title: str
    market_title: str
    yes_bid: float | None
    yes_ask: float | None
    last_price: float | None
    volume_24h: float
    open_interest: float
    close_time_utc: datetime | None

    @property
    def midpoint(self) -> float | None:
        if self.yes_bid is None or self.yes_ask is None or self.yes_ask < self.yes_bid:
            return None
        return (self.yes_bid + self.yes_ask) / 2.0

    @property
    def spread(self) -> float | None:
        if self.yes_bid is None or self.yes_ask is None:
            return None
        return self.yes_ask - self.yes_bid

    @property
    def two_sided(self) -> bool:
        return (
            self.yes_bid is not None
            and self.yes_ask is not None
            and self.yes_bid > 0.0
            and self.yes_ask < 1.0
        )


def price_dollars(market: dict[str, Any], field: str) -> float | None:
    """Price field as decimal dollars, from either the *_dollars string or cent int."""
    dollars = market.get(f"{field}_dollars")
    if dollars is not None and dollars != "":
        try:
            return float(dollars)
        except (TypeError, ValueError):
            pass
    cents = market.get(field)
    if cents is None or cents == "":
        return None
    try:
        return float(cents) / 100.0
    except (TypeError, ValueError):
        return None


def num_field(market: dict[str, Any], field: str) -> float:
    """Numeric field that Kalshi serves as either `field` or fixed-point `field_fp`."""
    for key in (field, f"{field}_fp"):
        v = market.get(key)
        if v is None or v == "":
            continue
        try:
            return float(v)
        except (TypeError, ValueError):
            continue
    return 0.0


def _parse_close(market: dict[str, Any]) -> datetime | None:
    raw = market.get("close_time") or market.get("expiration_time")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def flatten_events(events: list[dict[str, Any]]) -> list[MarketRow]:
    """One MarketRow per nested market, carrying the event's category/title."""
    rows: list[MarketRow] = []
    for ev in events:
        category = str(ev.get("category") or "Uncategorized")
        event_title = str(ev.get("title") or ev.get("event_ticker") or "")
        for m in ev.get("markets") or []:
            if m.get("status") not in (None, "open", "active"):
                continue
            title = str(m.get("title") or m.get("subtitle") or m.get("yes_sub_title") or "")
            rows.append(
                MarketRow(
                    market_ticker=str(m.get("ticker") or ""),
                    event_ticker=str(ev.get("event_ticker") or m.get("event_ticker") or ""),
                    category=category,
                    event_title=event_title,
                    market_title=title,
                    yes_bid=price_dollars(m, "yes_bid"),
                    yes_ask=price_dollars(m, "yes_ask"),
                    last_price=price_dollars(m, "last_price"),
                    volume_24h=num_field(m, "volume_24h"),
                    open_interest=num_field(m, "open_interest"),
                    close_time_utc=_parse_close(m),
                )
            )
    return rows


def filter_rows(
    rows: list[MarketRow],
    *,
    now_utc: datetime,
    max_close_days: float,
    min_volume_24h: float,
    category: str | None = None,
) -> list[MarketRow]:
    horizon = now_utc + timedelta(days=max_close_days)
    out = []
    for r in rows:
        if not r.market_ticker or not r.two_sided:
            continue
        if r.volume_24h < min_volume_24h:
            continue
        if r.close_time_utc is None or r.close_time_utc > horizon or r.close_time_utc <= now_utc:
            continue
        if category and category.lower() not in r.category.lower():
            continue
        out.append(r)
    return out


def select_digest(
    rows: list[MarketRow], *, top: int, per_category: int
) -> list[MarketRow]:
    """Most-active markets, capped per category so one vertical can't drown the rest."""
    by_cat: dict[str, list[MarketRow]] = {}
    for r in sorted(rows, key=lambda r: r.volume_24h, reverse=True):
        bucket = by_cat.setdefault(r.category, [])
        if len(bucket) < per_category:
            bucket.append(r)
    merged = [r for bucket in by_cat.values() for r in bucket]
    merged.sort(key=lambda r: (r.category, -r.volume_24h))
    return merged[:top]


def _fmt_price(p: float | None) -> str:
    return f"{p:.2f}" if p is not None else "-"


def render_digest(rows: list[MarketRow], *, now_utc: datetime) -> str:
    lines = [
        f"# Kalshi open-market digest ({len(rows)} markets)",
        "",
        f"_Generated {now_utc.strftime('%Y-%m-%d %H:%M UTC')}. Prices are decimal "
        "dollars for the YES side; NO costs (1 - yes_bid). closes_h = hours to close._",
        "",
    ]
    current_cat: str | None = None
    for r in rows:
        if r.category != current_cat:
            current_cat = r.category
            lines += [
                f"## {current_cat}",
                "",
                "| ticker | market | bid | ask | last | vol24h | OI | closes_h |",
                "|:-------|:-------|----:|----:|-----:|-------:|---:|---------:|",
            ]
        closes_h = (
            (r.close_time_utc - now_utc).total_seconds() / 3600.0
            if r.close_time_utc
            else float("nan")
        )
        title = f"{r.event_title} — {r.market_title}" if r.market_title else r.event_title
        title = title.replace("|", "/")[:90]
        lines.append(
            f"| {r.market_ticker} | {title} | {_fmt_price(r.yes_bid)} | {_fmt_price(r.yes_ask)} "
            f"| {_fmt_price(r.last_price)} | {int(r.volume_24h)} | {int(r.open_interest)} "
            f"| {closes_h:.0f} |"
        )
    lines.append("")
    return "\n".join(lines)


def scan_digest(
    *,
    client: KalshiClient | None = None,
    top: int = 120,
    per_category: int = 15,
    max_close_days: float = 10.0,
    min_volume_24h: float = 500.0,
    category: str | None = None,
    now_utc: datetime | None = None,
) -> str:
    """Fetch the whole venue and render the filtered digest (network)."""
    client = client or KalshiClient()
    now_utc = now_utc or datetime.now(UTC)
    events = client.list_all_open_events()
    rows = flatten_events(events)
    log.info("agent_scan", events=len(events), markets=len(rows))
    kept = filter_rows(
        rows,
        now_utc=now_utc,
        max_close_days=max_close_days,
        min_volume_24h=min_volume_24h,
        category=category,
    )
    return render_digest(
        select_digest(kept, top=top, per_category=per_category), now_utc=now_utc
    )


def event_detail(event_ticker: str, *, client: KalshiClient | None = None) -> str:
    """Every market in one event, unfiltered — the agent's drill-down view."""
    client = client or KalshiClient()
    now_utc = datetime.now(UTC)
    markets = client.list_event_markets(event_ticker)
    rows = flatten_events([{"event_ticker": event_ticker, "category": "Event detail",
                            "title": event_ticker, "markets": markets}])
    return render_digest(sorted(rows, key=lambda r: -r.volume_24h), now_utc=now_utc)
