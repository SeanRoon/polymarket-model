"""Live midpoints for a Kalshi weather event.

We don't need a separate orderbook call for normal scans — `list_event_markets`
already returns yes_bid_dollars / yes_ask_dollars. The orderbook endpoint is
available if we want depth later.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import KalshiClient
from polymarket_model.markets.discovery import Bin, WeatherEvent

log = get_logger(__name__)


@dataclass
class BinPrice:
    bin: Bin
    midpoint: float | None
    yes_bid: float | None
    yes_ask: float | None
    last_price: float | None
    volume: float | None
    yes_bid_size: float | None
    yes_ask_size: float | None
    snapshot_ts_utc: datetime


@dataclass
class EventPrices:
    event: WeatherEvent
    prices: list[BinPrice]
    sum_of_mids: float
    has_complete_mids: bool

    @property
    def passes_qc(self) -> bool:
        return (
            self.has_complete_mids
            and settings.sum_of_mids_low <= self.sum_of_mids <= settings.sum_of_mids_high
        )


def _to_float(s: str | float | int | None) -> float | None:
    if s is None or s == "":
        return None
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def floor_to_bucket(ts: datetime, minutes: int = 5) -> datetime:
    seconds = minutes * 60
    epoch = ts.timestamp()
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=UTC)


def _midpoint(bid: float | None, ask: float | None) -> float | None:
    if bid is None or ask is None:
        return None
    if ask < bid:
        return None
    return (bid + ask) / 2.0


def fetch_event_prices(event: WeatherEvent, client: KalshiClient | None = None) -> EventPrices:
    """Re-fetch every bin's market record so we get fresh bid/ask/last/volume."""
    client = client or KalshiClient()
    now = datetime.now(UTC)
    raw_markets = client.list_event_markets(event.event_ticker)
    by_ticker = {m.get("ticker"): m for m in raw_markets}

    prices: list[BinPrice] = []
    for b in event.bins:
        m = by_ticker.get(b.market_ticker) or {}
        bid = _to_float(m.get("yes_bid_dollars"))
        ask = _to_float(m.get("yes_ask_dollars"))
        last = _to_float(m.get("last_price_dollars"))
        vol = _to_float(m.get("volume_fp"))
        bid_size = _to_float(m.get("yes_bid_size_fp"))
        ask_size = _to_float(m.get("yes_ask_size_fp"))
        prices.append(BinPrice(
            bin=b,
            midpoint=_midpoint(bid, ask),
            yes_bid=bid,
            yes_ask=ask,
            last_price=last,
            volume=vol,
            yes_bid_size=bid_size,
            yes_ask_size=ask_size,
            snapshot_ts_utc=now,
        ))

    mids = [p.midpoint for p in prices if p.midpoint is not None]
    has_complete = len(mids) == len(prices)
    sum_of_mids = sum(mids) if mids else 0.0
    return EventPrices(event=event, prices=prices, sum_of_mids=sum_of_mids, has_complete_mids=has_complete)


def is_event_within_signal_window(event: WeatherEvent, *, now: datetime | None = None) -> bool:
    now = now or datetime.now(UTC)
    delta = event.close_time_utc - now
    return timedelta(0) <= delta <= timedelta(days=settings.max_lead_days_for_signal)
