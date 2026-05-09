from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import duckdb

from polymarket_model.config import settings


SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS markets (
        event_ticker      TEXT PRIMARY KEY,            -- e.g. KXHIGHNY-26MAY09
        series_ticker     TEXT NOT NULL,
        title             TEXT NOT NULL,
        city              TEXT,
        kind              TEXT,                         -- 'high' | 'low'
        target_date_local DATE NOT NULL,
        station_id        TEXT,
        rules_primary     TEXT,
        close_time_utc    TIMESTAMP,
        first_seen_utc    TIMESTAMP NOT NULL,
        last_seen_utc     TIMESTAMP NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS market_bins (
        market_ticker     TEXT PRIMARY KEY,             -- e.g. KXHIGHNY-26MAY09-B65.5
        event_ticker      TEXT NOT NULL,
        bin_index         INTEGER NOT NULL,
        subtitle          TEXT,
        floor_strike      DOUBLE,
        cap_strike        DOUBLE,
        lo_f              DOUBLE,                       -- nullable when open-low
        hi_f              DOUBLE,                       -- nullable when open-high
        is_open_low       BOOLEAN,
        is_open_high      BOOLEAN
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS price_snapshots (
        market_ticker          TEXT NOT NULL,
        event_ticker           TEXT NOT NULL,
        snapshot_ts_utc        TIMESTAMP NOT NULL,
        snapshot_bucket_utc    TIMESTAMP NOT NULL,
        midpoint               DOUBLE,
        yes_bid                DOUBLE,
        yes_ask                DOUBLE,
        last_price             DOUBLE,
        volume                 DOUBLE,
        yes_bid_size           DOUBLE,
        yes_ask_size           DOUBLE,
        model_p                DOUBLE,
        model_lead_hours       INTEGER,
        model_name             TEXT,
        model_n_members        INTEGER,
        model_outside_bin_mass DOUBLE,
        PRIMARY KEY (market_ticker, snapshot_bucket_utc)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecasts (
        station_id       TEXT NOT NULL,
        valid_date_local DATE NOT NULL,
        kind             TEXT NOT NULL,
        run_ts_utc       TIMESTAMP NOT NULL,
        model            TEXT NOT NULL,
        member           INTEGER NOT NULL,
        lead_hours       INTEGER NOT NULL,
        value_f          DOUBLE NOT NULL,
        fetched_at_utc   TIMESTAMP NOT NULL,
        PRIMARY KEY (station_id, valid_date_local, kind, run_ts_utc, model, member)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS resolutions (
        station_id       TEXT NOT NULL,
        valid_date_local DATE NOT NULL,
        kind             TEXT NOT NULL,
        value_f          DOUBLE NOT NULL,
        source           TEXT NOT NULL,
        fetched_at_utc   TIMESTAMP NOT NULL,
        raw_text         TEXT,
        PRIMARY KEY (station_id, valid_date_local, kind)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS signals (
        emitted_ts_utc       TIMESTAMP NOT NULL,
        event_ticker         TEXT NOT NULL,
        market_ticker        TEXT NOT NULL,
        bin_index            INTEGER NOT NULL,
        model_p              DOUBLE NOT NULL,
        market_mid           DOUBLE NOT NULL,
        edge                 DOUBLE NOT NULL,
        kelly_fraction       DOUBLE NOT NULL,
        lead_hours           INTEGER,
        outside_bin_mass     DOUBLE,
        sum_of_mids          DOUBLE,
        model_name           TEXT NOT NULL,
        PRIMARY KEY (emitted_ts_utc, market_ticker)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS run_log (
        run_id        TEXT NOT NULL,
        component     TEXT NOT NULL,
        started_utc   TIMESTAMP NOT NULL,
        ended_utc     TIMESTAMP,
        ok            BOOLEAN,
        rows_written  BIGINT,
        message       TEXT,
        PRIMARY KEY (run_id, component, started_utc)
    );
    """,
]


def ensure_data_dir() -> Path:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    return settings.data_dir


def bootstrap(con: duckdb.DuckDBPyConnection) -> None:
    for stmt in SCHEMA_SQL:
        con.execute(stmt)


@contextmanager
def connect(read_only: bool = False) -> Iterator[duckdb.DuckDBPyConnection]:
    ensure_data_dir()
    con = duckdb.connect(str(settings.cache_db_path), read_only=read_only)
    try:
        if not read_only:
            bootstrap(con)
        yield con
    finally:
        con.close()
