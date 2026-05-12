"""Paper-trading replay: one trade per (market, direction), take-side pricing, settlement join."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from polymarket_model.evaluation import RESOLUTIONS_SCHEMA
from polymarket_model.paper import (
    KALSHI_FEE_RATE,
    PaperTradingConfig,
    derive_paper_trades,
    kalshi_fee_per_dollar,
)


def _cfg(min_edge: float = 0.05, kelly: float = 0.25, lead_days: int = 7) -> PaperTradingConfig:
    return PaperTradingConfig(min_edge=min_edge, kelly_multiplier=kelly, max_lead_hours=lead_days * 24)


def _snapshot_schema() -> pa.Schema:
    # Minimal subset of the recorder's denormalized snapshot schema for tests.
    return pa.schema([
        pa.field("snapshot_bucket_utc", pa.timestamp("us", tz="UTC")),
        pa.field("snapshot_ts_utc", pa.timestamp("us", tz="UTC")),
        pa.field("series_ticker", pa.string()),
        pa.field("event_ticker", pa.string()),
        pa.field("market_ticker", pa.string()),
        pa.field("city", pa.string()),
        pa.field("kind", pa.string()),
        pa.field("target_date_local", pa.date32()),
        pa.field("station_id", pa.string()),
        pa.field("subtitle", pa.string()),
        pa.field("lo_f", pa.float64()),
        pa.field("hi_f", pa.float64()),
        pa.field("is_open_low", pa.bool_()),
        pa.field("is_open_high", pa.bool_()),
        pa.field("midpoint", pa.float64()),
        pa.field("yes_bid", pa.float64()),
        pa.field("yes_ask", pa.float64()),
        pa.field("model_p", pa.float64()),
        pa.field("model_lead_hours", pa.int32()),
    ])


def _row(
    *,
    market_ticker: str,
    bucket: datetime,
    midpoint: float,
    model_p: float,
    yes_bid: float | None,
    yes_ask: float | None,
    target_date: date = date(2026, 5, 10),
    station_id: str = "KORD",
    city: str = "Chicago",
    kind: str = "high",
    lo_f: float | None = 60.0,
    hi_f: float | None = 65.0,
    is_open_low: bool = False,
    is_open_high: bool = False,
    lead_hours: int = 12,
) -> dict:
    return {
        "snapshot_bucket_utc": bucket,
        "snapshot_ts_utc": bucket,
        "series_ticker": "KXHIGHCHI",
        "event_ticker": "KXHIGHCHI-26MAY10",
        "market_ticker": market_ticker,
        "city": city,
        "kind": kind,
        "target_date_local": target_date,
        "station_id": station_id,
        "subtitle": "60-65",
        "lo_f": lo_f,
        "hi_f": hi_f,
        "is_open_low": is_open_low,
        "is_open_high": is_open_high,
        "midpoint": midpoint,
        "yes_bid": yes_bid,
        "yes_ask": yes_ask,
        "model_p": model_p,
        "model_lead_hours": lead_hours,
    }


def _write_snapshots(tmp_path: Path, rows: list[dict]) -> Path:
    snapshots_root = tmp_path / "snapshots"
    snapshots_root.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(rows, schema=_snapshot_schema())
    pq.write_table(tbl, snapshots_root / "2026-05-10" / "1200.parquet" if False else snapshots_root / "test.parquet")
    return snapshots_root


def _write_resolutions(tmp_path: Path, rows: list[dict]) -> Path:
    path = tmp_path / "resolutions.parquet"
    tbl = pa.Table.from_pylist(rows, schema=RESOLUTIONS_SCHEMA)
    pq.write_table(tbl, path)
    return path


def test_fee_formula_matches_kalshi_spec():
    # f(P) = 0.07 * P * (1-P), max at P=0.5 -> 0.0175
    assert kalshi_fee_per_dollar(0.5) == pytest.approx(KALSHI_FEE_RATE * 0.25)
    assert kalshi_fee_per_dollar(0.1) == pytest.approx(KALSHI_FEE_RATE * 0.1 * 0.9)
    assert kalshi_fee_per_dollar(0.9) == pytest.approx(KALSHI_FEE_RATE * 0.9 * 0.1)
    # Boundary values: at 0 or 1 the trade is degenerate; fee is zero.
    assert kalshi_fee_per_dollar(0.0) == 0.0
    assert kalshi_fee_per_dollar(1.0) == 0.0


def test_first_crossing_opens_exactly_one_trade(tmp_path):
    # Three buckets for the same market: signal already qualifies in all three,
    # but we must record only ONE paper trade (the earliest).
    base = datetime(2026, 5, 10, 12, 0, tzinfo=UTC)
    rows = [
        _row(market_ticker="MKT-A", bucket=base + timedelta(minutes=0),
             midpoint=0.30, model_p=0.55, yes_bid=0.29, yes_ask=0.32),
        _row(market_ticker="MKT-A", bucket=base + timedelta(minutes=5),
             midpoint=0.32, model_p=0.55, yes_bid=0.31, yes_ask=0.34),
        _row(market_ticker="MKT-A", bucket=base + timedelta(minutes=10),
             midpoint=0.31, model_p=0.55, yes_bid=0.30, yes_ask=0.33),
    ]
    snapshots_root = _write_snapshots(tmp_path, rows)
    resolutions = _write_resolutions(tmp_path, [])
    trades = derive_paper_trades(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions,
        cfg=_cfg(min_edge=0.05),
    )
    assert len(trades) == 1
    t = trades[0]
    assert t["market_ticker"] == "MKT-A"
    assert t["direction"] == "BUY_YES"
    # Earliest bucket's ask was 0.32; entry_price uses yes_ask, not midpoint.
    assert t["entry_price"] == pytest.approx(0.32)
    assert t["opened_at_utc"] == base
    assert t["status"] == "OPEN"


def test_buy_no_uses_one_minus_yes_bid(tmp_path):
    # Negative edge: model thinks YES is less likely than market.
    base = datetime(2026, 5, 10, 12, 0, tzinfo=UTC)
    rows = [_row(
        market_ticker="MKT-B", bucket=base,
        midpoint=0.70, model_p=0.40, yes_bid=0.69, yes_ask=0.72,
    )]
    snapshots_root = _write_snapshots(tmp_path, rows)
    resolutions = _write_resolutions(tmp_path, [])
    trades = derive_paper_trades(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions,
        cfg=_cfg(min_edge=0.05),
    )
    assert len(trades) == 1
    t = trades[0]
    assert t["direction"] == "BUY_NO"
    # BUY_NO take-side cost = 1 - yes_bid (i.e., what we'd pay to buy NO).
    assert t["entry_price"] == pytest.approx(1.0 - 0.69)


def test_settlement_joins_resolution_and_computes_pnl(tmp_path):
    # BUY_YES, bin lo_f=60 hi_f=65 -> realized=1 iff value in [60, 65).
    base = datetime(2026, 5, 10, 12, 0, tzinfo=UTC)
    rows = [_row(
        market_ticker="MKT-C", bucket=base,
        midpoint=0.30, model_p=0.60, yes_bid=0.29, yes_ask=0.31,
        target_date=date(2026, 5, 10), station_id="KORD", kind="high",
        lo_f=60.0, hi_f=65.0,
    )]
    snapshots_root = _write_snapshots(tmp_path, rows)
    resolutions = _write_resolutions(tmp_path, [{
        "station_id": "KORD",
        "valid_date_local": date(2026, 5, 10),
        "kind": "high",
        "value_f": 62.0,
        "source": "nws_cli",
        "fetched_at_utc": datetime(2026, 5, 11, 13, 0, tzinfo=UTC),
        "raw_text": "fake",
    }])
    trades = derive_paper_trades(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions,
        cfg=_cfg(min_edge=0.05),
    )
    assert len(trades) == 1
    t = trades[0]
    assert t["status"] == "SETTLED"
    assert t["realized_yes"] == 1
    assert t["payoff"] == 1.0
    # pnl = payoff - (entry_price + fee). entry=0.31, fee=0.07*0.31*0.69, total~=0.3250.
    expected_pnl = 1.0 - (0.31 + KALSHI_FEE_RATE * 0.31 * 0.69)
    assert t["pnl_per_dollar"] == pytest.approx(expected_pnl)


def test_empty_book_is_skipped(tmp_path):
    # yes_ask is None at the BUY_YES-qualifying bucket; we wait for the next one.
    base = datetime(2026, 5, 10, 12, 0, tzinfo=UTC)
    rows = [
        _row(market_ticker="MKT-D", bucket=base,
             midpoint=0.30, model_p=0.60, yes_bid=None, yes_ask=None),
        _row(market_ticker="MKT-D", bucket=base + timedelta(minutes=5),
             midpoint=0.30, model_p=0.60, yes_bid=0.29, yes_ask=0.31),
    ]
    snapshots_root = _write_snapshots(tmp_path, rows)
    resolutions = _write_resolutions(tmp_path, [])
    trades = derive_paper_trades(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions,
        cfg=_cfg(min_edge=0.05),
    )
    assert len(trades) == 1
    assert trades[0]["opened_at_utc"] == base + timedelta(minutes=5)


def test_existing_trade_is_not_reopened(tmp_path):
    base = datetime(2026, 5, 10, 12, 0, tzinfo=UTC)
    rows = [_row(
        market_ticker="MKT-E", bucket=base,
        midpoint=0.30, model_p=0.55, yes_bid=0.29, yes_ask=0.32,
    )]
    snapshots_root = _write_snapshots(tmp_path, rows)
    resolutions = _write_resolutions(tmp_path, [])
    existing = [{
        "trade_id": "preexisting",
        "opened_at_utc": base - timedelta(hours=1),  # earlier than the snapshot
        "event_ticker": "KXHIGHCHI-26MAY10",
        "market_ticker": "MKT-E",
        "series_ticker": "KXHIGHCHI",
        "city": "Chicago",
        "kind": "high",
        "target_date_local": date(2026, 5, 10),
        "station_id": "KORD",
        "subtitle": "60-65",
        "lo_f": 60.0,
        "hi_f": 65.0,
        "is_open_low": False,
        "is_open_high": False,
        "direction": "BUY_YES",
        "entry_price": 0.40,
        "entry_fee": 0.01,
        "entry_cost": 0.41,
        "model_p_at_open": 0.55,
        "market_mid_at_open": 0.40,
        "edge_at_open": 0.15,
        "model_lead_hours_at_open": 24,
        "kelly_full": 0.25,
        "kelly_sized": 0.0625,
        "status": "OPEN",
        "settled_at_utc": None,
        "realized_value_f": None,
        "realized_yes": None,
        "payoff": None,
        "pnl_per_dollar": None,
    }]
    trades = derive_paper_trades(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions,
        cfg=_cfg(min_edge=0.05),
        existing=existing,
    )
    assert len(trades) == 1
    # Same trade_id => row not regenerated from the snapshot.
    assert trades[0]["trade_id"] == "preexisting"
    assert trades[0]["entry_price"] == pytest.approx(0.40)


def test_lead_window_excludes_far_signals(tmp_path):
    base = datetime(2026, 5, 10, 12, 0, tzinfo=UTC)
    rows = [_row(
        market_ticker="MKT-F", bucket=base,
        midpoint=0.30, model_p=0.55, yes_bid=0.29, yes_ask=0.32,
        lead_hours=24 * 14,  # 14 days out
    )]
    snapshots_root = _write_snapshots(tmp_path, rows)
    resolutions = _write_resolutions(tmp_path, [])
    trades = derive_paper_trades(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions,
        cfg=_cfg(min_edge=0.05, lead_days=7),  # cap at 7d
    )
    assert trades == []
