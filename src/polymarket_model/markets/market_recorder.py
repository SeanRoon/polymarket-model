"""Price-only snapshot feed for weather markets we don't (yet) model.

The main `recorder.py` snapshots the daily high/low temperature markets in
`discovery.WEATHER_SERIES` together with a model probability (`model_p`) derived
from the ECMWF ensemble. That model only speaks daily-extreme temperature, so the
rest of Kalshi's weather vertical — monthly rain, hurricanes, tornadoes, air
quality, drought, hourly / monthly temperature, long-range climate — has no
`model_p` and is skipped there.

This module records those "other" markets as a **price-only** feed: one bulk
`list_all_open_events` call (the same call the agent scan uses), flattened to one
row per market, filtered to a category (default "Climate and Weather") with the
already-modeled temperature series excluded, keeping only markets that carry a
live price signal. No forecast, no model, no order-book depth — just the touch
prices, sizes, volume, and strike metadata, so a model can be fitted against this
history later. Output lands under `data/market_snapshots/` to stay separate from
the modeled `data/snapshots/` tree.

The bulk endpoint serves prices as fixed-point `*_dollars` strings and counts as
`*_fp`; the two `_price`/`_num` helpers below read either encoding (mirroring the
agent scout, kept local so `markets` doesn't import from `agent`).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import KalshiClient
from polymarket_model.markets.discovery import WEATHER_SERIES
from polymarket_model.markets.prices import floor_to_bucket

log = get_logger(__name__)

DEFAULT_MARKET_SNAPSHOT_DIR = settings.data_dir / "market_snapshots"
DEFAULT_CATEGORY = "Climate and Weather"

MARKET_SNAPSHOT_SCHEMA = pa.schema([
    pa.field("snapshot_bucket_utc", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("snapshot_ts_utc", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("series_ticker", pa.string(), nullable=False),
    pa.field("event_ticker", pa.string(), nullable=False),
    pa.field("market_ticker", pa.string(), nullable=False),
    pa.field("category", pa.string(), nullable=True),
    pa.field("event_title", pa.string(), nullable=True),
    pa.field("market_title", pa.string(), nullable=True),
    pa.field("strike_type", pa.string(), nullable=True),
    pa.field("floor_strike", pa.float64(), nullable=True),
    pa.field("cap_strike", pa.float64(), nullable=True),
    pa.field("yes_bid", pa.float64(), nullable=True),
    pa.field("yes_ask", pa.float64(), nullable=True),
    pa.field("midpoint", pa.float64(), nullable=True),
    pa.field("last_price", pa.float64(), nullable=True),
    pa.field("previous_price", pa.float64(), nullable=True),
    pa.field("yes_bid_size", pa.float64(), nullable=True),
    pa.field("yes_ask_size", pa.float64(), nullable=True),
    pa.field("volume", pa.float64(), nullable=True),
    pa.field("volume_24h", pa.float64(), nullable=True),
    pa.field("open_interest", pa.float64(), nullable=True),
    pa.field("liquidity_dollars", pa.float64(), nullable=True),
    pa.field("close_time_utc", pa.timestamp("us", tz="UTC"), nullable=True),
])


@dataclass
class MarketSnapshotResult:
    started_utc: datetime
    ended_utc: datetime
    events_seen: int
    markets_in_scope: int
    rows_written: int
    parquet_path: Path | None = None


def _price(market: dict[str, Any], field: str) -> float | None:
    """Decimal-dollar price from either `{field}_dollars` (string) or `field` (cents int)."""
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


def _num(market: dict[str, Any], field: str) -> float | None:
    """Numeric field served as either `field` or fixed-point `{field}_fp`; None if absent."""
    for key in (field, f"{field}_fp"):
        v = market.get(key)
        if v is None or v == "":
            continue
        try:
            return float(v)
        except (TypeError, ValueError):
            continue
    return None


def _to_float(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _close_ts(market: dict[str, Any]) -> datetime | None:
    raw = market.get("close_time") or market.get("expiration_time")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _midpoint(yes_bid: float | None, yes_ask: float | None) -> float | None:
    if yes_bid is None or yes_ask is None:
        return None
    return (yes_bid + yes_ask) / 2.0


def _series_of(event: dict[str, Any], market: dict[str, Any]) -> str:
    series = event.get("series_ticker")
    if series:
        return str(series)
    # Fall back to the ticker prefix (event_ticker up to the first '-').
    et = str(event.get("event_ticker") or market.get("event_ticker") or "")
    return et.split("-")[0]


def build_market_rows(
    events: list[dict[str, Any]],
    *,
    bucket: datetime,
    started: datetime,
    category: str | None,
    exclude_series: frozenset[str],
) -> list[dict]:
    """Flatten events -> one row per in-scope, price-bearing market.

    In scope = open status, matching `category` (case-insensitive substring; None = any),
    series not in `exclude_series`. Price-bearing = at least one of yes_bid / yes_ask /
    last_price present, so we don't record thousands of never-quoted tail bins.
    """
    rows: list[dict] = []
    for ev in events:
        ev_category = str(ev.get("category") or "")
        if category and category.lower() not in ev_category.lower():
            continue
        event_title = str(ev.get("title") or ev.get("event_ticker") or "")
        for m in ev.get("markets") or []:
            if m.get("status") not in (None, "open", "active"):
                continue
            series = _series_of(ev, m)
            if series in exclude_series:
                continue
            yes_bid = _price(m, "yes_bid")
            yes_ask = _price(m, "yes_ask")
            last_price = _price(m, "last_price")
            if yes_bid is None and yes_ask is None and last_price is None:
                continue  # no live price signal — skip
            rows.append({
                "snapshot_bucket_utc": bucket,
                "snapshot_ts_utc": started,
                "series_ticker": series,
                "event_ticker": str(ev.get("event_ticker") or m.get("event_ticker") or ""),
                "market_ticker": str(m.get("ticker") or ""),
                "category": ev_category or None,
                "event_title": event_title or None,
                "market_title": str(m.get("yes_sub_title") or m.get("subtitle") or m.get("title") or "") or None,
                "strike_type": str(m.get("strike_type") or "") or None,
                "floor_strike": _to_float(m.get("floor_strike")),
                "cap_strike": _to_float(m.get("cap_strike")),
                "yes_bid": yes_bid,
                "yes_ask": yes_ask,
                "midpoint": _midpoint(yes_bid, yes_ask),
                "last_price": last_price,
                "previous_price": _price(m, "previous_price"),
                "yes_bid_size": _num(m, "yes_bid_size"),
                "yes_ask_size": _num(m, "yes_ask_size"),
                "volume": _num(m, "volume"),
                "volume_24h": _num(m, "volume_24h"),
                "open_interest": _num(m, "open_interest"),
                "liquidity_dollars": _num(m, "liquidity"),
                "close_time_utc": _close_ts(m),
            })
    return rows


def _parquet_path_for_bucket(parquet_dir: Path, bucket: datetime) -> Path:
    return parquet_dir / f"{bucket.strftime('%Y-%m-%d')}" / f"{bucket.strftime('%H%M')}.parquet"


def collect_market_snapshot_once(
    *,
    parquet_dir: Path | None = None,
    now: datetime | None = None,
    category: str | None = DEFAULT_CATEGORY,
    exclude_series: frozenset[str] | None = None,
    client: KalshiClient | None = None,
) -> MarketSnapshotResult:
    """Fetch the venue once and write a price-only snapshot of the in-scope markets.

    category: substring-matched against each event's category (case-insensitive).
        Defaults to "Climate and Weather"; pass None to capture every category.
    exclude_series: series to skip (defaults to the modeled temperature set in
        WEATHER_SERIES, which `recorder.py` already snapshots with a model_p).
    """
    started = now or datetime.now(UTC)
    bucket = floor_to_bucket(started, minutes=5)
    parquet_dir = parquet_dir or DEFAULT_MARKET_SNAPSHOT_DIR
    exclude_series = exclude_series if exclude_series is not None else frozenset(WEATHER_SERIES)
    client = client or KalshiClient()
    run_id = uuid.uuid4().hex

    events = client.list_all_open_events()
    rows = build_market_rows(
        events, bucket=bucket, started=started,
        category=category, exclude_series=exclude_series,
    )
    log.info(
        "market_snapshot", run_id=run_id, events=len(events),
        rows=len(rows), category=category,
    )

    parquet_path: Path | None = None
    if rows:
        parquet_path = _parquet_path_for_bucket(parquet_dir, bucket)
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        tbl = pa.Table.from_pylist(rows, schema=MARKET_SNAPSHOT_SCHEMA)
        pq.write_table(tbl, parquet_path, compression="zstd")
    else:
        log.warning("market_snapshot_empty", bucket=str(bucket))

    return MarketSnapshotResult(
        started_utc=started,
        ended_utc=datetime.now(UTC),
        events_seen=len(events),
        markets_in_scope=len(rows),
        rows_written=len(rows),
        parquet_path=parquet_path,
    )
