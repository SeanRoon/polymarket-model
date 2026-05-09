"""Inserting the same (market_ticker, snapshot_bucket_utc) twice must not duplicate."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import duckdb
import pytest

from polymarket_model.cache import SCHEMA_SQL


@pytest.fixture
def con():
    c = duckdb.connect(":memory:")
    for stmt in SCHEMA_SQL:
        c.execute(stmt)
    yield c
    c.close()


def _insert(con, market_ticker, ts, bucket, mid):
    con.execute(
        """
        INSERT INTO price_snapshots (market_ticker, event_ticker, snapshot_ts_utc, snapshot_bucket_utc,
                                     midpoint, yes_bid, yes_ask, last_price, volume, yes_bid_size, yes_ask_size)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (market_ticker, snapshot_bucket_utc) DO NOTHING
        """,
        [market_ticker, "EVT", ts, bucket, mid, mid - 0.01, mid + 0.01, mid, 100.0, 50.0, 50.0],
    )


def test_idempotent_insert_in_same_bucket(con):
    bucket = datetime(2026, 5, 7, 19, 55, tzinfo=UTC)
    for i in range(5):
        ts = bucket + timedelta(seconds=i * 30)
        _insert(con, "KXTEST-1", ts, bucket, 0.50 + i * 0.01)
    rows = con.execute(
        "SELECT COUNT(*), MAX(midpoint) FROM price_snapshots WHERE market_ticker='KXTEST-1'"
    ).fetchone()
    # Five attempts, all in the same 5-min bucket -> one persisted row, with the FIRST midpoint.
    assert rows[0] == 1
    assert rows[1] == pytest.approx(0.50)


def test_distinct_buckets_each_persist(con):
    for minutes_offset in (0, 5, 10):
        bucket = datetime(2026, 5, 7, 19, minutes_offset, tzinfo=UTC)
        _insert(con, "KXTEST-2", bucket, bucket, 0.50)
    rows = con.execute(
        "SELECT COUNT(*) FROM price_snapshots WHERE market_ticker='KXTEST-2'"
    ).fetchone()
    assert rows[0] == 3
