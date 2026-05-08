"""Snapshot recorder: persist live midpoints + best bid/ask for every active weather market.

This is the highest-leverage component in the project: without an accumulating
snapshot history, no future modeling work can be backtested. Run it on a 15-min
cron (Windows Task Scheduler) to build a database of price history over time.

Idempotent on (token_id, snapshot_bucket_utc) where the bucket is floor(now, 5 min):
two runs in the same 5-min window won't create duplicate rows.
"""
from __future__ import annotations

import json
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime

import duckdb

from polymarket_model.cache import connect
from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import ClobClient
from polymarket_model.markets.discovery import Bin, WeatherEvent, discover_weather_events
from polymarket_model.markets.prices import floor_to_bucket

log = get_logger(__name__)


PRICE_FETCH_CONCURRENCY = 10


@dataclass
class SnapshotResult:
    started_utc: datetime
    ended_utc: datetime
    events_seen: int
    bins_seen: int
    rows_inserted: int
    errors: int


def _upsert_event(con: duckdb.DuckDBPyConnection, event: WeatherEvent, now: datetime) -> None:
    raw_meta = json.dumps({
        "tags": [t.get("slug") for t in (event.raw.get("tags") or []) if isinstance(t, dict)],
        "title": event.title,
        "endDate": event.raw.get("endDate"),
    })
    condition_id = event.condition_ids[0] if event.condition_ids else event.event_id
    con.execute(
        """
        INSERT INTO markets (
            condition_id, slug, question, category, city, kind, target_date_local,
            station_id, resolution_source, end_date_utc, first_seen_utc, last_seen_utc, raw_metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (condition_id) DO UPDATE SET
            slug = EXCLUDED.slug,
            question = EXCLUDED.question,
            station_id = EXCLUDED.station_id,
            resolution_source = EXCLUDED.resolution_source,
            end_date_utc = EXCLUDED.end_date_utc,
            last_seen_utc = EXCLUDED.last_seen_utc,
            raw_metadata = EXCLUDED.raw_metadata
        """,
        [
            condition_id,
            event.slug,
            event.title,
            "weather",
            event.city,
            event.kind,
            event.target_date_local,
            event.station_id,
            event.resolution_source,
            event.end_date_utc,
            now,
            now,
            raw_meta,
        ],
    )


def _upsert_bins(con: duckdb.DuckDBPyConnection, event: WeatherEvent) -> None:
    condition_id = event.condition_ids[0] if event.condition_ids else event.event_id
    for b in event.bins:
        # Each bin has its own conditionId on Polymarket; we keep the event-level condition_id as
        # the FK on `markets` and key bins by (event_condition_id, outcome_index).
        con.execute(
            """
            INSERT INTO market_bins (
                condition_id, outcome_index, token_id, outcome_label,
                lo_f, hi_f, is_open_low, is_open_high
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (condition_id, outcome_index) DO UPDATE SET
                token_id = EXCLUDED.token_id,
                outcome_label = EXCLUDED.outcome_label,
                lo_f = EXCLUDED.lo_f,
                hi_f = EXCLUDED.hi_f,
                is_open_low = EXCLUDED.is_open_low,
                is_open_high = EXCLUDED.is_open_high
            """,
            [
                condition_id,
                b.outcome_index,
                b.yes_token_id,
                b.label,
                None if b.is_open_low else b.lo_f,
                None if b.is_open_high else b.hi_f,
                b.is_open_low,
                b.is_open_high,
            ],
        )


def _insert_price_snapshot(
    con: duckdb.DuckDBPyConnection,
    *,
    token_id: str,
    condition_id: str,
    snapshot_ts_utc: datetime,
    bucket_utc: datetime,
    midpoint: float | None,
    best_bid: float | None,
    best_ask: float | None,
    bid_size: float | None,
    ask_size: float | None,
) -> int:
    res = con.execute(
        """
        INSERT INTO price_snapshots (
            token_id, condition_id, snapshot_ts_utc, snapshot_bucket_utc,
            midpoint, best_bid, best_ask, bid_size, ask_size
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (token_id, snapshot_bucket_utc) DO NOTHING
        """,
        [
            token_id,
            condition_id,
            snapshot_ts_utc,
            bucket_utc,
            midpoint,
            best_bid,
            best_ask,
            bid_size,
            ask_size,
        ],
    )
    # DuckDB doesn't return rowcount on ON CONFLICT DO NOTHING; assume one row attempted.
    _ = res
    return 1


@dataclass
class _BinPrice:
    bin: Bin
    condition_id: str
    midpoint: float | None
    best_bid: float | None
    best_ask: float | None
    bid_size: float | None
    ask_size: float | None
    error: str | None = None


def _fetch_bin_price(clob: ClobClient, condition_id: str, bin_: Bin) -> _BinPrice:
    try:
        mid = clob.get_midpoint(bin_.yes_token_id)
        book = clob.get_book(bin_.yes_token_id)
        bb, ba, bs, as_ = ClobClient.best_bid_ask(book)
        return _BinPrice(bin=bin_, condition_id=condition_id, midpoint=mid, best_bid=bb, best_ask=ba, bid_size=bs, ask_size=as_)
    except Exception as exc:
        return _BinPrice(bin=bin_, condition_id=condition_id, midpoint=None, best_bid=None, best_ask=None, bid_size=None, ask_size=None, error=str(exc))


def snapshot_once(
    *,
    now: datetime | None = None,
    max_workers: int = PRICE_FETCH_CONCURRENCY,
) -> SnapshotResult:
    """Single shot: discover, fetch prices in parallel, persist to DuckDB."""
    started = now or datetime.now(UTC)
    bucket = floor_to_bucket(started, minutes=5)
    run_id = uuid.uuid4().hex
    clob = ClobClient()
    events = discover_weather_events()

    rows_inserted = 0
    bins_seen = 0
    errors = 0

    # Build the (condition_id, bin) work list across all events first so the thread pool is fully saturated.
    work: list[tuple[str, Bin]] = []
    for event in events:
        condition_id = event.condition_ids[0] if event.condition_ids else event.event_id
        for b in event.bins:
            work.append((condition_id, b))

    results: list[_BinPrice] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(_fetch_bin_price, clob, cid, b) for cid, b in work]
        for fut in as_completed(futures):
            results.append(fut.result())

    by_token = {r.bin.yes_token_id: r for r in results}

    with connect() as con:
        try:
            for event in events:
                try:
                    _upsert_event(con, event, started)
                    _upsert_bins(con, event)
                    condition_id = event.condition_ids[0] if event.condition_ids else event.event_id
                    for b in event.bins:
                        r = by_token.get(b.yes_token_id)
                        if r is None or r.error:
                            errors += 1
                            if r is not None:
                                log.warning("price_fetch_failed", token_id=b.yes_token_id, slug=event.slug, error=r.error)
                            continue
                        _insert_price_snapshot(
                            con,
                            token_id=b.yes_token_id,
                            condition_id=condition_id,
                            snapshot_ts_utc=started,
                            bucket_utc=bucket,
                            midpoint=r.midpoint,
                            best_bid=r.best_bid,
                            best_ask=r.best_ask,
                            bid_size=r.bid_size,
                            ask_size=r.ask_size,
                        )
                        rows_inserted += 1
                        bins_seen += 1
                except Exception:
                    errors += 1
                    log.exception("event_record_failed", slug=event.slug)
            ended = datetime.now(UTC)
            con.execute(
                """
                INSERT INTO run_log (run_id, component, started_utc, ended_utc, ok, rows_written, message)
                VALUES (?, 'snapshot', ?, ?, ?, ?, ?)
                """,
                [run_id, started, ended, errors == 0, rows_inserted, f"events={len(events)} bins={bins_seen} errors={errors}"],
            )
        except Exception:
            log.exception("snapshot_failed_unrecoverable")
            errors += 1
            ended = datetime.now(UTC)

    return SnapshotResult(
        started_utc=started,
        ended_utc=ended,
        events_seen=len(events),
        bins_seen=bins_seen,
        rows_inserted=rows_inserted,
        errors=errors,
    )
