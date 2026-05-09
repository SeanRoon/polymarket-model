"""Score model predictions against NWS resolutions.

Joins the snapshot Parquets (which carry per-bucket model_p + market midpoint)
against the resolutions table (NWS CLI ground truth), and computes Brier, log
loss, and a simulated PnL replay using the same Kelly-sizing rules as live
signals.

The function is designed to run from any working directory: it reads via
DuckDB's native Parquet glob and falls back to an empty result when nothing
has resolved yet.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import duckdb
import pandas as pd

from polymarket_model.config import settings


# Lead-time buckets in hours for "by lead" aggregations.
LEAD_BUCKETS = [
    ("0-6h",   0,    6),
    ("6-24h",  6,    24),
    ("24-72h", 24,   72),
    ("3-7d",   72,   168),
    (">7d",    168,  10_000),
]


@dataclass(frozen=True)
class EvaluationConfig:
    min_edge: float
    kelly_multiplier: float
    fee: float
    log_clip: float = 1e-6


def realized_yes(value_f: float, lo_f: float | None, hi_f: float | None) -> int:
    """Return 1 if `value_f` falls in the bin's [lo_f, hi_f) interval, else 0.

    None bounds mean open ends: lo_f=None -> open-low (-inf); hi_f=None -> open-high (+inf).
    Matches the convention in markets.discovery.Bin.
    """
    if lo_f is not None and value_f < lo_f:
        return 0
    if hi_f is not None and value_f >= hi_f:
        return 0
    return 1


def brier(p: float, y: int) -> float:
    return (float(p) - int(y)) ** 2


def log_loss(p: float, y: int, *, clip: float = 1e-6) -> float:
    p_ = min(max(float(p), clip), 1.0 - clip)
    return -math.log(p_) if y == 1 else -math.log(1.0 - p_)


def simulate_pnl(
    *,
    model_p: float,
    market_mid: float,
    realized: int,
    cfg: EvaluationConfig,
) -> tuple[float, str | None, float]:
    """Replay the live signal logic for a single bucket and return (pnl, direction, kelly_sized).

    direction is None (and pnl=0) when |edge| < min_edge or fee makes the trade -EV.
    PnL is in dollars per dollar of bankroll allocated, scaled by kelly_sized.
    Fee is deducted from the entry price symmetrically (round-trip cost approximation).
    """
    edge = float(model_p) - float(market_mid)
    if abs(edge) < cfg.min_edge:
        return 0.0, None, 0.0
    if edge > 0:
        direction = "BUY_YES"
        entry = float(market_mid) + cfg.fee
        if entry >= 1.0:
            return 0.0, None, 0.0
        kelly_full = max(0.0, (float(model_p) - entry) / (1.0 - entry))
        kelly_sized = kelly_full * cfg.kelly_multiplier
        payoff = 1.0 if realized == 1 else 0.0
        pnl_per_dollar = payoff - entry
    else:
        direction = "BUY_NO"
        entry = (1.0 - float(market_mid)) + cfg.fee
        if entry >= 1.0:
            return 0.0, None, 0.0
        kelly_full = max(0.0, ((1.0 - float(model_p)) - entry) / (1.0 - entry))
        kelly_sized = kelly_full * cfg.kelly_multiplier
        payoff = 1.0 if realized == 0 else 0.0
        pnl_per_dollar = payoff - entry
    return pnl_per_dollar * kelly_sized, direction, kelly_sized


def lead_bucket(hours: float | int | None) -> str:
    if hours is None or (isinstance(hours, float) and math.isnan(hours)):
        return "unknown"
    h = float(hours)
    for label, lo, hi in LEAD_BUCKETS:
        if lo <= h < hi:
            return label
    return "unknown"


def score_resolutions(
    *,
    snapshots_root: Path | str | None = None,
    cfg: EvaluationConfig | None = None,
) -> pd.DataFrame:
    """Join all snapshot Parquets with the resolutions table and compute per-row metrics.

    Returns one row per (market_ticker, snapshot_bucket_utc) for which model_p and a
    matching resolution both exist. Empty DataFrame if either side is missing.
    """
    snapshots_root = Path(snapshots_root) if snapshots_root else (settings.data_dir / "snapshots")
    cfg = cfg or EvaluationConfig(
        min_edge=settings.min_edge,
        kelly_multiplier=settings.kelly_fraction,
        fee=settings.fee_assumption,
    )

    glob = str((snapshots_root / "**/*.parquet").as_posix())
    sql = f"""
        WITH s AS (
            SELECT *
            FROM read_parquet('{glob}', union_by_name=True)
            WHERE model_p IS NOT NULL
              AND midpoint IS NOT NULL
              AND target_date_local <= CURRENT_DATE
              AND NOT contains(filename, '_archive_polymarket')
        ),
        r AS (
            SELECT station_id, valid_date_local, kind, value_f
            FROM resolutions
        )
        SELECT
            s.snapshot_bucket_utc,
            s.snapshot_ts_utc,
            s.event_ticker,
            s.market_ticker,
            s.series_ticker,
            s.city,
            s.kind,
            s.target_date_local,
            s.station_id,
            s.subtitle,
            s.lo_f,
            s.hi_f,
            s.is_open_low,
            s.is_open_high,
            s.midpoint AS market_mid,
            s.model_p,
            s.model_lead_hours,
            s.model_name,
            s.model_outside_bin_mass,
            r.value_f AS realized_value_f
        FROM s
        JOIN r
          ON r.station_id = s.station_id
         AND r.valid_date_local = s.target_date_local
         AND r.kind = s.kind
    """
    con = duckdb.connect(":memory:")
    try:
        try:
            con.execute(f"ATTACH '{settings.cache_db_path.as_posix()}' AS cache_db (READ_ONLY);")
            con.execute("CREATE TEMP VIEW resolutions AS SELECT * FROM cache_db.resolutions;")
        except duckdb.Error:
            con.execute("CREATE TEMP VIEW resolutions AS SELECT NULL AS station_id, NULL::DATE AS valid_date_local, NULL AS kind, NULL::DOUBLE AS value_f WHERE FALSE;")
        df = con.execute(sql).df()
    finally:
        con.close()

    if df.empty:
        return df

    df["realized_yes"] = df.apply(
        lambda row: realized_yes(
            float(row["realized_value_f"]),
            None if row["is_open_low"] else float(row["lo_f"]),
            None if row["is_open_high"] else float(row["hi_f"]),
        ),
        axis=1,
    )
    df["brier_model"] = df.apply(lambda r: brier(r["model_p"], r["realized_yes"]), axis=1)
    df["brier_market"] = df.apply(lambda r: brier(r["market_mid"], r["realized_yes"]), axis=1)
    df["log_loss_model"] = df.apply(lambda r: log_loss(r["model_p"], r["realized_yes"], clip=cfg.log_clip), axis=1)
    df["log_loss_market"] = df.apply(lambda r: log_loss(r["market_mid"], r["realized_yes"], clip=cfg.log_clip), axis=1)

    pnl_records = df.apply(
        lambda r: simulate_pnl(
            model_p=float(r["model_p"]),
            market_mid=float(r["market_mid"]),
            realized=int(r["realized_yes"]),
            cfg=cfg,
        ),
        axis=1,
        result_type="expand",
    )
    pnl_records.columns = ["pnl", "direction", "kelly_sized"]
    df = pd.concat([df, pnl_records], axis=1)

    df["lead_bucket"] = df["model_lead_hours"].apply(lead_bucket)
    return df


def aggregate(df: pd.DataFrame, by: list[str] | None = None) -> pd.DataFrame:
    """Group by the given dimensions and compute mean / sum metrics.

    by=None or [] returns a single-row 'overall' summary.
    """
    if df.empty:
        return df
    if not by:
        out = {
            "n": len(df),
            "brier_model_mean": df["brier_model"].mean(),
            "brier_market_mean": df["brier_market"].mean(),
            "log_loss_model_mean": df["log_loss_model"].mean(),
            "log_loss_market_mean": df["log_loss_market"].mean(),
            "pnl_sum": df["pnl"].sum(),
            "kelly_sum": df["kelly_sized"].sum(),
            "trades_emitted": int(df["direction"].notna().sum()),
        }
        return pd.DataFrame([out])
    return df.groupby(by, dropna=False).agg(
        n=("brier_model", "size"),
        brier_model_mean=("brier_model", "mean"),
        brier_market_mean=("brier_market", "mean"),
        log_loss_model_mean=("log_loss_model", "mean"),
        log_loss_market_mean=("log_loss_market", "mean"),
        pnl_sum=("pnl", "sum"),
        kelly_sum=("kelly_sized", "sum"),
        trades_emitted=("direction", lambda s: int(s.notna().sum())),
    ).reset_index()
