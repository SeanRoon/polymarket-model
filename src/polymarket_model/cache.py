from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import duckdb

from polymarket_model.config import settings


SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS markets (
        condition_id      TEXT PRIMARY KEY,
        slug              TEXT NOT NULL,
        question          TEXT NOT NULL,
        category          TEXT,
        city              TEXT,
        kind              TEXT,                  -- 'high' | 'low'
        target_date_local DATE NOT NULL,
        station_id        TEXT,                  -- e.g. KNYC, KLGA
        resolution_source TEXT,
        end_date_utc      TIMESTAMP,
        first_seen_utc    TIMESTAMP NOT NULL,
        last_seen_utc     TIMESTAMP NOT NULL,
        raw_metadata      JSON
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS market_bins (
        condition_id  TEXT NOT NULL,
        outcome_index INTEGER NOT NULL,
        token_id      TEXT NOT NULL,
        outcome_label TEXT NOT NULL,
        lo_f          DOUBLE,                 -- inclusive lower bound in degrees F
        hi_f          DOUBLE,                 -- exclusive upper bound; +inf for open top
        is_open_low   BOOLEAN DEFAULT FALSE,
        is_open_high  BOOLEAN DEFAULT FALSE,
        PRIMARY KEY (condition_id, outcome_index)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS price_snapshots (
        token_id            TEXT NOT NULL,
        condition_id        TEXT NOT NULL,
        snapshot_ts_utc     TIMESTAMP NOT NULL,
        snapshot_bucket_utc TIMESTAMP NOT NULL,    -- floor to 5 min for idempotency
        midpoint            DOUBLE,
        best_bid            DOUBLE,
        best_ask            DOUBLE,
        bid_size            DOUBLE,
        ask_size            DOUBLE,
        PRIMARY KEY (token_id, snapshot_bucket_utc)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS forecasts (
        station_id      TEXT NOT NULL,
        valid_date_local DATE NOT NULL,
        kind            TEXT NOT NULL,          -- 'high' | 'low'
        run_ts_utc      TIMESTAMP NOT NULL,     -- model init time
        model           TEXT NOT NULL,          -- 'ecmwf_ifs' | 'gfs' etc
        member          INTEGER NOT NULL,       -- 0 = control, 1..N perturbed
        lead_hours      INTEGER NOT NULL,       -- nominal lead from run to valid date midnight
        value_f         DOUBLE NOT NULL,
        fetched_at_utc  TIMESTAMP NOT NULL,
        PRIMARY KEY (station_id, valid_date_local, kind, run_ts_utc, model, member)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS resolutions (
        station_id      TEXT NOT NULL,
        valid_date_local DATE NOT NULL,
        kind            TEXT NOT NULL,          -- 'high' | 'low'
        value_f         DOUBLE NOT NULL,
        source          TEXT NOT NULL,          -- 'nws_cli'
        fetched_at_utc  TIMESTAMP NOT NULL,
        raw_text        TEXT,
        PRIMARY KEY (station_id, valid_date_local, kind)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS signals (
        emitted_ts_utc      TIMESTAMP NOT NULL,
        condition_id        TEXT NOT NULL,
        token_id            TEXT NOT NULL,
        outcome_index       INTEGER NOT NULL,
        model_p             DOUBLE NOT NULL,
        market_mid          DOUBLE NOT NULL,
        edge                DOUBLE NOT NULL,
        kelly_fraction      DOUBLE NOT NULL,
        lead_hours          INTEGER,
        outside_bin_mass    DOUBLE,
        sum_of_mids         DOUBLE,
        model_name          TEXT NOT NULL,
        PRIMARY KEY (emitted_ts_utc, token_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS run_log (
        run_id        TEXT NOT NULL,
        component     TEXT NOT NULL,            -- 'snapshot' | 'scan' | 'forecast' | 'resolution'
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
