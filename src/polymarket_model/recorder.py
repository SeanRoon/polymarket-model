"""Snapshot recorder: persist live midpoints + bid/ask for every active Kalshi weather market.

This is the highest-leverage component in the project: without an accumulating
snapshot history, no future modeling work can be backtested. The GitHub Actions
workflow at .github/workflows/snapshot.yml runs this every 15 minutes and
commits a Parquet file back to the repo.

Idempotent on (market_ticker, snapshot_bucket_utc) where the bucket is floor(now, 5 min):
two runs in the same 5-min window won't create duplicate rows.
"""
from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

from polymarket_model.cache import connect
from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import KalshiClient
from polymarket_model.markets.discovery import WeatherEvent, discover_weather_events
from polymarket_model.markets.prices import EventPrices, fetch_event_prices, floor_to_bucket

log = get_logger(__name__)


PRICE_FETCH_CONCURRENCY = 8


@dataclass
class SnapshotResult:
    started_utc: datetime
    ended_utc: datetime
    events_seen: int
    bins_seen: int
    rows_inserted: int
    errors: int
    parquet_path: Path | None = None


def _upsert_event(con: duckdb.DuckDBPyConnection, event: WeatherEvent, now: datetime) -> None:
    con.execute(
        """
        INSERT INTO markets (
            event_ticker, series_ticker, title, city, kind, target_date_local,
            station_id, rules_primary, close_time_utc, first_seen_utc, last_seen_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (event_ticker) DO UPDATE SET
            series_ticker = EXCLUDED.series_ticker,
            title = EXCLUDED.title,
            city = EXCLUDED.city,
            kind = EXCLUDED.kind,
            target_date_local = EXCLUDED.target_date_local,
            station_id = EXCLUDED.station_id,
            rules_primary = EXCLUDED.rules_primary,
            close_time_utc = EXCLUDED.close_time_utc,
            last_seen_utc = EXCLUDED.last_seen_utc
        """,
        [
            event.event_ticker,
            event.series_ticker,
            event.title,
            event.city,
            event.kind,
            event.target_date_local,
            event.station_id,
            event.rules_primary,
            event.close_time_utc,
            now,
            now,
        ],
    )


def _upsert_bins(con: duckdb.DuckDBPyConnection, event: WeatherEvent) -> None:
    for b in event.bins:
        con.execute(
            """
            INSERT INTO market_bins (
                market_ticker, event_ticker, bin_index, subtitle,
                floor_strike, cap_strike, lo_f, hi_f, is_open_low, is_open_high
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (market_ticker) DO UPDATE SET
                event_ticker = EXCLUDED.event_ticker,
                bin_index = EXCLUDED.bin_index,
                subtitle = EXCLUDED.subtitle,
                floor_strike = EXCLUDED.floor_strike,
                cap_strike = EXCLUDED.cap_strike,
                lo_f = EXCLUDED.lo_f,
                hi_f = EXCLUDED.hi_f,
                is_open_low = EXCLUDED.is_open_low,
                is_open_high = EXCLUDED.is_open_high
            """,
            [
                b.market_ticker,
                b.event_ticker,
                b.bin_index,
                b.subtitle,
                b.floor_strike,
                b.cap_strike,
                None if b.is_open_low else b.lo_f,
                None if b.is_open_high else b.hi_f,
                b.is_open_low,
                b.is_open_high,
            ],
        )


def _insert_price_snapshot(
    con: duckdb.DuckDBPyConnection,
    *,
    market_ticker: str,
    event_ticker: str,
    snapshot_ts_utc: datetime,
    bucket_utc: datetime,
    midpoint: float | None,
    yes_bid: float | None,
    yes_ask: float | None,
    last_price: float | None,
    volume: float | None,
    yes_bid_size: float | None,
    yes_ask_size: float | None,
) -> None:
    con.execute(
        """
        INSERT INTO price_snapshots (
            market_ticker, event_ticker, snapshot_ts_utc, snapshot_bucket_utc,
            midpoint, yes_bid, yes_ask, last_price, volume, yes_bid_size, yes_ask_size
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (market_ticker, snapshot_bucket_utc) DO NOTHING
        """,
        [
            market_ticker,
            event_ticker,
            snapshot_ts_utc,
            bucket_utc,
            midpoint,
            yes_bid,
            yes_ask,
            last_price,
            volume,
            yes_bid_size,
            yes_ask_size,
        ],
    )


def _parquet_path_for_bucket(parquet_dir: Path, bucket: datetime) -> Path:
    return parquet_dir / f"{bucket.strftime('%Y-%m-%d')}" / f"{bucket.strftime('%H%M')}.parquet"


def _build_snapshot_table(
    *,
    bucket: datetime,
    started: datetime,
    priced_events: list[EventPrices],
) -> pa.Table:
    rows: list[dict] = []
    for ep in priced_events:
        e = ep.event
        for p in ep.prices:
            if p.midpoint is None:
                continue
            rows.append({
                "snapshot_bucket_utc": bucket,
                "snapshot_ts_utc": started,
                "series_ticker": e.series_ticker,
                "event_ticker": e.event_ticker,
                "market_ticker": p.bin.market_ticker,
                "city": e.city,
                "kind": e.kind,
                "target_date_local": e.target_date_local,
                "close_time_utc": e.close_time_utc.replace(tzinfo=None),
                "station_id": e.station_id,
                "bin_index": p.bin.bin_index,
                "subtitle": p.bin.subtitle,
                "floor_strike": p.bin.floor_strike,
                "cap_strike": p.bin.cap_strike,
                "lo_f": None if p.bin.is_open_low else p.bin.lo_f,
                "hi_f": None if p.bin.is_open_high else p.bin.hi_f,
                "is_open_low": p.bin.is_open_low,
                "is_open_high": p.bin.is_open_high,
                "midpoint": p.midpoint,
                "yes_bid": p.yes_bid,
                "yes_ask": p.yes_ask,
                "last_price": p.last_price,
                "volume": p.volume,
                "yes_bid_size": p.yes_bid_size,
                "yes_ask_size": p.yes_ask_size,
            })
    return pa.Table.from_pylist(rows)


def snapshot_once(
    *,
    now: datetime | None = None,
    max_workers: int = PRICE_FETCH_CONCURRENCY,
    parquet_dir: Path | None = None,
    write_duckdb: bool = True,
) -> SnapshotResult:
    """Single shot: discover, fetch prices in parallel, persist to Parquet and/or DuckDB.

    parquet_dir: if provided, write a self-contained Parquet at
        {parquet_dir}/YYYY-MM-DD/HHMM.parquet. Each row is fully denormalized.
    write_duckdb: if True (default), also write to data/cache.duckdb. The GHA runner
        sets this False because the runner is ephemeral.
    """
    started = now or datetime.now(UTC)
    bucket = floor_to_bucket(started, minutes=5)
    run_id = uuid.uuid4().hex
    client = KalshiClient()
    events = discover_weather_events(client)

    errors = 0

    # Fetch each event's prices in parallel; Kalshi returns all bins in one /markets call,
    # so concurrency is per-event, not per-bin.
    priced_events: list[EventPrices] = []
    if events:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(fetch_event_prices, e, client): e for e in events}
            for fut in as_completed(futures):
                e = futures[fut]
                try:
                    priced_events.append(fut.result())
                except Exception:
                    errors += 1
                    log.exception("event_price_fetch_failed", event_ticker=e.event_ticker)

    rows_written = 0
    bins_with_mid = 0

    parquet_path: Path | None = None
    if parquet_dir is not None:
        try:
            tbl = _build_snapshot_table(bucket=bucket, started=started, priced_events=priced_events)
            parquet_path = _parquet_path_for_bucket(parquet_dir, bucket)
            parquet_path.parent.mkdir(parents=True, exist_ok=True)
            pq.write_table(tbl, parquet_path, compression="zstd")
            rows_written = tbl.num_rows
            bins_with_mid = tbl.num_rows
        except Exception:
            errors += 1
            log.exception("parquet_write_failed", path=str(parquet_path))

    if write_duckdb:
        with connect() as con:
            try:
                for ep in priced_events:
                    try:
                        _upsert_event(con, ep.event, started)
                        _upsert_bins(con, ep.event)
                        for p in ep.prices:
                            if p.midpoint is None:
                                continue
                            _insert_price_snapshot(
                                con,
                                market_ticker=p.bin.market_ticker,
                                event_ticker=ep.event.event_ticker,
                                snapshot_ts_utc=started,
                                bucket_utc=bucket,
                                midpoint=p.midpoint,
                                yes_bid=p.yes_bid,
                                yes_ask=p.yes_ask,
                                last_price=p.last_price,
                                volume=p.volume,
                                yes_bid_size=p.yes_bid_size,
                                yes_ask_size=p.yes_ask_size,
                            )
                            if parquet_dir is None:  # only count once
                                rows_written += 1
                                bins_with_mid += 1
                    except Exception:
                        errors += 1
                        log.exception("event_record_failed", event_ticker=ep.event.event_ticker)
                ended = datetime.now(UTC)
                con.execute(
                    """
                    INSERT INTO run_log (run_id, component, started_utc, ended_utc, ok, rows_written, message)
                    VALUES (?, 'snapshot', ?, ?, ?, ?, ?)
                    """,
                    [run_id, started, ended, errors == 0, rows_written,
                     f"events={len(events)} bins_with_mid={bins_with_mid} errors={errors}"],
                )
            except Exception:
                log.exception("snapshot_failed_unrecoverable")
                errors += 1
                ended = datetime.now(UTC)
    else:
        ended = datetime.now(UTC)

    return SnapshotResult(
        started_utc=started,
        ended_utc=ended,
        events_seen=len(events),
        bins_seen=bins_with_mid,
        rows_inserted=rows_written,
        errors=errors,
        parquet_path=parquet_path,
    )
