"""Paper-trading replay over the accumulating snapshot Parquets.

The model-validation loop in `evaluation.py` computes a counterfactual replay
that opens a fresh "trade" at every snapshot bucket — useful for calibration
metrics but not what a real trader does. This module records *one* hypothetical
fill per market at the first bucket where the model emits a tradeable signal,
using take-side prices (yes_ask for BUY_YES, 1-yes_bid for BUY_NO) and Kalshi's
actual fee formula, then settles against `data/resolutions.parquet`.

Idempotent: re-running picks up newly-signaled markets, refreshes settlement
status on previously-open trades, and leaves already-recorded trades alone.

The output (`data/paper_trades.parquet`) is the dataset we'll compare against
once we eventually go live — same schema, same sizing rules.
"""
from __future__ import annotations

import os
import tempfile
import uuid
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

from polymarket_model.config import settings
from polymarket_model.evaluation import realized_yes

DEFAULT_PAPER_TRADES_PARQUET = settings.data_dir / "paper_trades.parquet"

# Kalshi documents trading fees as round_up(0.07 * C * P * (1 - P)) cents per
# side, where C is contracts and P is the per-$1 price. For per-dollar
# bookkeeping we drop C and the cent rounding (we're sizing in fractional
# dollars anyway).
KALSHI_FEE_RATE = 0.07


PAPER_TRADES_SCHEMA = pa.schema([
    pa.field("trade_id", pa.string(), nullable=False),
    pa.field("opened_at_utc", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("event_ticker", pa.string(), nullable=False),
    pa.field("market_ticker", pa.string(), nullable=False),
    pa.field("series_ticker", pa.string(), nullable=False),
    pa.field("city", pa.string(), nullable=False),
    pa.field("kind", pa.string(), nullable=False),
    pa.field("target_date_local", pa.date32(), nullable=False),
    pa.field("station_id", pa.string(), nullable=False),
    pa.field("subtitle", pa.string(), nullable=True),
    pa.field("lo_f", pa.float64(), nullable=True),
    pa.field("hi_f", pa.float64(), nullable=True),
    pa.field("is_open_low", pa.bool_(), nullable=True),
    pa.field("is_open_high", pa.bool_(), nullable=True),
    pa.field("direction", pa.string(), nullable=False),
    pa.field("entry_price", pa.float64(), nullable=False),
    pa.field("entry_fee", pa.float64(), nullable=False),
    pa.field("entry_cost", pa.float64(), nullable=False),
    pa.field("model_p_at_open", pa.float64(), nullable=False),
    pa.field("market_mid_at_open", pa.float64(), nullable=False),
    pa.field("edge_at_open", pa.float64(), nullable=False),
    pa.field("model_lead_hours_at_open", pa.int32(), nullable=True),
    pa.field("kelly_full", pa.float64(), nullable=False),
    pa.field("kelly_sized", pa.float64(), nullable=False),
    pa.field("status", pa.string(), nullable=False),
    pa.field("settled_at_utc", pa.timestamp("us", tz="UTC"), nullable=True),
    pa.field("realized_value_f", pa.float64(), nullable=True),
    pa.field("realized_yes", pa.int32(), nullable=True),
    pa.field("payoff", pa.float64(), nullable=True),
    pa.field("pnl_per_dollar", pa.float64(), nullable=True),
])


@dataclass(frozen=True)
class PaperTradingConfig:
    min_edge: float
    kelly_multiplier: float
    max_lead_hours: int  # skip signals further out than this (model unreliable past ~7d)
    excluded_stations: frozenset[str] = frozenset()
    excluded_cells: frozenset[tuple[str, str]] = frozenset()


def default_config() -> PaperTradingConfig:
    return PaperTradingConfig(
        min_edge=settings.min_edge,
        kelly_multiplier=settings.kelly_fraction,
        max_lead_hours=settings.max_lead_days_for_signal * 24,
        excluded_stations=settings.signal_excluded_stations,
        excluded_cells=settings.signal_excluded_cells,
    )


def kalshi_fee_per_dollar(price: float, fee_rate: float = KALSHI_FEE_RATE) -> float:
    """Per-dollar Kalshi trading fee at the given decimal price. One side."""
    if price <= 0.0 or price >= 1.0:
        return 0.0
    return fee_rate * price * (1.0 - price)


def _settled_pnl(*, direction: str, entry_cost: float, realized: int) -> tuple[float, float]:
    """Return (payoff, pnl_per_dollar) for a fully-settled paper trade.

    payoff is the gross terminal value of one contract ($1 if our side won, else 0).
    pnl_per_dollar is (payoff - entry_cost), so positive when the post-fee entry
    paid off and negative otherwise.
    """
    side_won = (direction == "BUY_YES" and realized == 1) or (direction == "BUY_NO" and realized == 0)
    payoff = 1.0 if side_won else 0.0
    return payoff, payoff - entry_cost


def load_paper_trades(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return pq.read_table(path).to_pylist()


def write_paper_trades(path: Path, rows: list[dict]) -> None:
    deduped: dict[tuple[str, str], dict] = {}
    for r in rows:
        key = (r["market_ticker"], r["direction"])
        deduped[key] = r
    ordered = sorted(
        deduped.values(),
        key=lambda r: (r["opened_at_utc"], r["market_ticker"], r["direction"]),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(ordered, schema=PAPER_TRADES_SCHEMA)
    fd, tmp = tempfile.mkstemp(prefix=".paper-", suffix=".parquet", dir=str(path.parent))
    os.close(fd)
    try:
        pq.write_table(tbl, tmp, compression="zstd")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _first_crossings(
    *,
    snapshots_root: Path,
    cfg: PaperTradingConfig,
) -> list[dict]:
    """For each market, find the earliest snapshot bucket where the model emits
    a tradeable signal AND the book is non-empty in the direction we'd take.
    """
    glob = str((snapshots_root / "**/*.parquet").as_posix())
    sql = f"""
        WITH s AS (
            SELECT *,
                CASE
                    WHEN model_p - midpoint >= ? THEN 'BUY_YES'
                    WHEN midpoint - model_p >= ? THEN 'BUY_NO'
                    ELSE NULL
                END AS direction
            FROM read_parquet('{glob}', union_by_name=True, filename=True)
            WHERE model_p IS NOT NULL
              AND midpoint IS NOT NULL
              AND NOT contains(filename, '_archive_polymarket')
              AND (model_lead_hours IS NULL OR model_lead_hours <= ?)
              AND station_id NOT IN (SELECT UNNEST(?))
              AND (station_id || '|' || kind) NOT IN (SELECT UNNEST(?))
        ),
        tradeable AS (
            SELECT *
            FROM s
            WHERE direction IS NOT NULL
              AND ((direction = 'BUY_YES' AND yes_ask IS NOT NULL AND yes_ask < 1.0)
                OR (direction = 'BUY_NO' AND yes_bid IS NOT NULL AND yes_bid > 0.0))
        ),
        ranked AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY market_ticker
                    ORDER BY snapshot_bucket_utc
                ) AS rn
            FROM tradeable
        )
        SELECT
            snapshot_bucket_utc, snapshot_ts_utc, event_ticker, market_ticker,
            series_ticker, city, kind, target_date_local, station_id, subtitle,
            lo_f, hi_f, is_open_low, is_open_high, midpoint, yes_bid, yes_ask,
            model_p, model_lead_hours, direction
        FROM ranked
        WHERE rn = 1
    """
    con = duckdb.connect(":memory:")
    try:
        rows = con.execute(
            sql,
            [
                cfg.min_edge,
                cfg.min_edge,
                cfg.max_lead_hours,
                sorted(cfg.excluded_stations),
                sorted(f"{s}|{k}" for s, k in cfg.excluded_cells),
            ],
        ).fetchall()
        cols = [d[0] for d in con.description]
    finally:
        con.close()
    return [dict(zip(cols, r, strict=True)) for r in rows]


def _resolution_index(resolutions_parquet: Path) -> dict[tuple[str, date, str], float]:
    if not resolutions_parquet.exists():
        return {}
    tbl = pq.read_table(resolutions_parquet)
    idx: dict[tuple[str, date, str], float] = {}
    for r in tbl.to_pylist():
        idx[(r["station_id"], r["valid_date_local"], r["kind"])] = float(r["value_f"])
    return idx


def _build_trade(row: dict, cfg: PaperTradingConfig, now_utc: datetime) -> dict | None:
    """Convert a first-crossing snapshot row into a fully-priced paper trade."""
    direction = row["direction"]
    model_p = float(row["model_p"])
    market_mid = float(row["midpoint"])
    if direction == "BUY_YES":
        entry_price = float(row["yes_ask"])
        kelly_full = max(0.0, (model_p - entry_price) / (1.0 - entry_price)) if entry_price < 1.0 else 0.0
    else:
        entry_price = 1.0 - float(row["yes_bid"])
        p_true_no = 1.0 - model_p
        kelly_full = max(0.0, (p_true_no - entry_price) / (1.0 - entry_price)) if entry_price < 1.0 else 0.0
    if entry_price <= 0.0 or entry_price >= 1.0 or kelly_full <= 0.0:
        return None
    fee = kalshi_fee_per_dollar(entry_price)
    entry_cost = entry_price + fee
    if entry_cost >= 1.0:
        return None
    return {
        "trade_id": uuid.uuid4().hex,
        "opened_at_utc": row["snapshot_ts_utc"],
        "event_ticker": row["event_ticker"],
        "market_ticker": row["market_ticker"],
        "series_ticker": row["series_ticker"],
        "city": row["city"],
        "kind": row["kind"],
        "target_date_local": row["target_date_local"],
        "station_id": row["station_id"],
        "subtitle": row.get("subtitle"),
        "lo_f": row.get("lo_f"),
        "hi_f": row.get("hi_f"),
        "is_open_low": row.get("is_open_low"),
        "is_open_high": row.get("is_open_high"),
        "direction": direction,
        "entry_price": entry_price,
        "entry_fee": fee,
        "entry_cost": entry_cost,
        "model_p_at_open": model_p,
        "market_mid_at_open": market_mid,
        "edge_at_open": model_p - market_mid,
        "model_lead_hours_at_open": int(row["model_lead_hours"]) if row.get("model_lead_hours") is not None else None,
        "kelly_full": kelly_full,
        "kelly_sized": kelly_full * cfg.kelly_multiplier,
        "status": "OPEN",
        "settled_at_utc": None,
        "realized_value_f": None,
        "realized_yes": None,
        "payoff": None,
        "pnl_per_dollar": None,
    }


def _apply_settlement(
    trade: dict,
    resolutions: dict[tuple[str, date, str], float],
    now_utc: datetime,
) -> dict:
    """Mutate a trade dict in place to SETTLED if a matching resolution exists."""
    if trade.get("status") == "SETTLED":
        return trade
    key = (trade["station_id"], trade["target_date_local"], trade["kind"])
    value = resolutions.get(key)
    if value is None:
        return trade
    lo = None if trade["is_open_low"] else trade["lo_f"]
    hi = None if trade["is_open_high"] else trade["hi_f"]
    realized = realized_yes(value, lo, hi)
    payoff, pnl = _settled_pnl(
        direction=trade["direction"],
        entry_cost=trade["entry_cost"],
        realized=realized,
    )
    trade.update({
        "status": "SETTLED",
        "settled_at_utc": now_utc,
        "realized_value_f": float(value),
        "realized_yes": realized,
        "payoff": payoff,
        "pnl_per_dollar": pnl,
    })
    return trade


def derive_paper_trades(
    *,
    snapshots_root: Path,
    resolutions_parquet: Path,
    cfg: PaperTradingConfig | None = None,
    existing: list[dict] | None = None,
    now_utc: datetime | None = None,
) -> list[dict]:
    """Replay snapshots → list of paper trades. See module docstring for semantics."""
    cfg = cfg or default_config()
    now_utc = now_utc or datetime.now().astimezone()
    existing = existing or []
    resolutions = _resolution_index(resolutions_parquet)

    # Index existing trades by their natural key so we don't reopen them.
    by_key: dict[tuple[str, str], dict] = {
        (t["market_ticker"], t["direction"]): t for t in existing
    }

    # Refresh settlement status on already-open trades.
    for t in by_key.values():
        _apply_settlement(t, resolutions, now_utc)

    # Open any newly-signaled markets.
    for row in _first_crossings(snapshots_root=snapshots_root, cfg=cfg):
        key = (row["market_ticker"], row["direction"])
        if key in by_key:
            continue
        trade = _build_trade(row, cfg, now_utc)
        if trade is None:
            continue
        _apply_settlement(trade, resolutions, now_utc)
        by_key[key] = trade

    return list(by_key.values())


def summarize(trades: list[dict]) -> dict:
    """Aggregate stats over a list of paper trades. PnL is per-dollar-deployed."""
    settled = [t for t in trades if t.get("status") == "SETTLED"]
    open_ = [t for t in trades if t.get("status") == "OPEN"]
    n_settled = len(settled)
    wins = sum(1 for t in settled if (t.get("pnl_per_dollar") or 0.0) > 0)
    pnl_per_dollar_sum = sum(t["pnl_per_dollar"] for t in settled) if settled else 0.0
    kelly_sized_sum_settled = sum(t["kelly_sized"] for t in settled) if settled else 0.0
    weighted_pnl = sum(t["pnl_per_dollar"] * t["kelly_sized"] for t in settled) if settled else 0.0
    return {
        "n_total": len(trades),
        "n_open": len(open_),
        "n_settled": n_settled,
        "n_wins": wins,
        "win_rate": (wins / n_settled) if n_settled else None,
        "pnl_per_dollar_sum": pnl_per_dollar_sum,
        "kelly_sized_sum_settled": kelly_sized_sum_settled,
        "weighted_pnl": weighted_pnl,
        "weighted_roi": (weighted_pnl / kelly_sized_sum_settled) if kelly_sized_sum_settled else None,
    }
