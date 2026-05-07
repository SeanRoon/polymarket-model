from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import ClobClient
from polymarket_model.markets.discovery import Bin, WeatherEvent

log = get_logger(__name__)


@dataclass
class BinPrice:
    bin: Bin
    midpoint: float | None
    best_bid: float | None
    best_ask: float | None
    bid_size: float | None
    ask_size: float | None
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


def floor_to_bucket(ts: datetime, minutes: int = 5) -> datetime:
    seconds = minutes * 60
    epoch = ts.timestamp()
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=UTC)


def fetch_event_prices(event: WeatherEvent, clob: ClobClient | None = None, *, with_book: bool = True) -> EventPrices:
    clob = clob or ClobClient()
    now = datetime.now(UTC)
    prices: list[BinPrice] = []
    for b in event.bins:
        mid = clob.get_midpoint(b.yes_token_id)
        bb = ba = bs = as_ = None
        if with_book:
            book = clob.get_book(b.yes_token_id)
            bb, ba, bs, as_ = ClobClient.best_bid_ask(book)
        prices.append(BinPrice(
            bin=b,
            midpoint=mid,
            best_bid=bb,
            best_ask=ba,
            bid_size=bs,
            ask_size=as_,
            snapshot_ts_utc=now,
        ))
    mids = [p.midpoint for p in prices if p.midpoint is not None]
    has_complete = len(mids) == len(prices)
    sum_of_mids = sum(mids) if mids else 0.0
    return EventPrices(event=event, prices=prices, sum_of_mids=sum_of_mids, has_complete_mids=has_complete)


def is_event_within_signal_window(event: WeatherEvent, *, now: datetime | None = None) -> bool:
    """Per plan: only signal within 1..max_lead_days_for_signal days of resolution."""
    now = now or datetime.now(UTC)
    delta = event.end_date_utc - now
    return timedelta(0) <= delta <= timedelta(days=settings.max_lead_days_for_signal)
