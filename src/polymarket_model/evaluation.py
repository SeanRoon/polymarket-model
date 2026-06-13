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
import os
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import duckdb
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from polymarket_model.config import settings

DEFAULT_RESOLUTIONS_PARQUET = settings.data_dir / "resolutions.parquet"


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


RESOLUTIONS_SCHEMA = pa.schema([
    pa.field("station_id", pa.string(), nullable=False),
    pa.field("valid_date_local", pa.date32(), nullable=False),
    pa.field("kind", pa.string(), nullable=False),
    pa.field("value_f", pa.float64(), nullable=False),
    pa.field("source", pa.string(), nullable=False),
    pa.field("fetched_at_utc", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("raw_text", pa.string(), nullable=True),
])


def load_resolutions_parquet(path: Path) -> list[dict]:
    """Read the canonical resolutions Parquet into a list of row dicts. Empty if absent."""
    if not path.exists():
        return []
    tbl = pq.read_table(path)
    return tbl.to_pylist()


def write_resolutions_parquet(path: Path, rows: list[dict]) -> None:
    """Atomically write resolutions to Parquet (temp file + rename). Dedupes on the primary key."""
    deduped: dict[tuple[str, date, str], dict] = {}
    for r in rows:
        key = (r["station_id"], r["valid_date_local"], r["kind"])
        deduped[key] = r
    ordered = sorted(
        deduped.values(),
        key=lambda r: (r["station_id"], r["valid_date_local"], r["kind"]),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(ordered, schema=RESOLUTIONS_SCHEMA)
    fd, tmp = tempfile.mkstemp(prefix=".resolutions-", suffix=".parquet", dir=str(path.parent))
    os.close(fd)
    try:
        pq.write_table(tbl, tmp, compression="zstd")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def discover_unresolved_from_snapshots(
    *,
    snapshots_root: Path,
    earliest_date: date,
    latest_date: date,
    stations: set[str] | None = None,
    already_resolved: set[tuple[str, date, str]] | None = None,
) -> list[tuple[str, date, str]]:
    """Distinct (station_id, target_date_local, kind) tuples from snapshot Parquets in the window."""
    glob = str((snapshots_root / "**/*.parquet").as_posix())
    sql = f"""
        SELECT DISTINCT station_id, target_date_local, kind
        FROM read_parquet('{glob}', union_by_name=True, filename=True)
        WHERE station_id IS NOT NULL
          AND target_date_local BETWEEN ? AND ?
          AND NOT contains(filename, '_archive_polymarket')
        ORDER BY station_id, target_date_local, kind
    """
    con = duckdb.connect(":memory:")
    try:
        try:
            rows = con.execute(sql, [earliest_date, latest_date]).fetchall()
        except duckdb.IOException:
            return []
    finally:
        con.close()
    already = already_resolved or set()
    out: list[tuple[str, date, str]] = []
    for sid, target_date, kind in rows:
        if stations and sid.upper() not in stations:
            continue
        if (sid, target_date, kind) in already:
            continue
        out.append((sid, target_date, kind))
    return out


def _any_snapshot_has_column(snapshots_root: Path, column: str) -> bool:
    """Return True if at least one recent Parquet under `snapshots_root` carries `column`.

    Walks newest-first and stops on the first hit — typically O(1) once the column is in
    regular rotation. Used to decide whether to bind a column in the SQL or substitute a NULL
    literal, since DuckDB's union_by_name only adds a column when some input file has it.
    """
    if not snapshots_root.exists():
        return False
    # Sort by name (YYYY-MM-DD/HHMM.parquet) — newest last; reverse to check freshest first.
    candidates = sorted(snapshots_root.rglob("*.parquet"), reverse=True)
    for path in candidates[:50]:  # cap the scan in case the dir has thousands of files
        try:
            schema = pq.read_schema(path)
        except Exception:
            continue
        if column in schema.names:
            return True
    return False


def score_resolutions(
    *,
    snapshots_root: Path | str | None = None,
    resolutions_parquet: Path | str | None = None,
    cfg: EvaluationConfig | None = None,
) -> pd.DataFrame:
    """Join all snapshot Parquets with the resolutions Parquet and compute per-row metrics.

    Returns one row per (market_ticker, snapshot_bucket_utc) for which model_p and a
    matching resolution both exist. Empty DataFrame if either side is missing.
    """
    snapshots_root = Path(snapshots_root) if snapshots_root else (settings.data_dir / "snapshots")
    resolutions_path = Path(resolutions_parquet) if resolutions_parquet else DEFAULT_RESOLUTIONS_PARQUET
    cfg = cfg or EvaluationConfig(
        min_edge=settings.min_edge,
        kelly_multiplier=settings.kelly_fraction,
        fee=settings.fee_assumption,
    )

    glob = str((snapshots_root / "**/*.parquet").as_posix())
    # NBM columns only exist on snapshots written after 2026-05-18 (b902735). DuckDB's
    # union_by_name=True only adds a column when at least one input has it; if zero files
    # carry nbm_p the column reference would be unbound. Check the most recent Parquet
    # and substitute NULL literals if NBM hasn't landed yet.
    has_nbm_in_snapshots = _any_snapshot_has_column(snapshots_root, "nbm_p")
    if has_nbm_in_snapshots:
        nbm_select = (
            "TRY_CAST(s.nbm_p AS DOUBLE) AS nbm_p, "
            "TRY_CAST(s.nbm_lead_hours AS INTEGER) AS nbm_lead_hours, "
            "CAST(s.nbm_model_name AS VARCHAR) AS nbm_model_name,"
        )
    else:
        nbm_select = (
            "CAST(NULL AS DOUBLE) AS nbm_p, "
            "CAST(NULL AS INTEGER) AS nbm_lead_hours, "
            "CAST(NULL AS VARCHAR) AS nbm_model_name,"
        )
    # blended_p lands later than nbm_p (Phase 3 ECMWF/NBM blend). Same union_by_name guard.
    if _any_snapshot_has_column(snapshots_root, "blended_p"):
        blend_select = (
            "TRY_CAST(s.blended_p AS DOUBLE) AS blended_p, "
            "TRY_CAST(s.blend_weight_nbm AS DOUBLE) AS blend_weight_nbm,"
        )
    else:
        blend_select = (
            "CAST(NULL AS DOUBLE) AS blended_p, "
            "CAST(NULL AS DOUBLE) AS blend_weight_nbm,"
        )
    sql = f"""
        WITH s AS (
            SELECT *
            FROM read_parquet('{glob}', union_by_name=True, filename=True)
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
            {nbm_select}
            {blend_select}
            r.value_f AS realized_value_f
        FROM s
        JOIN r
          ON r.station_id = s.station_id
         AND r.valid_date_local = s.target_date_local
         AND r.kind = s.kind
    """
    con = duckdb.connect(":memory:")
    try:
        if resolutions_path.exists():
            con.execute(
                "CREATE TEMP VIEW resolutions AS "
                f"SELECT * FROM read_parquet('{resolutions_path.as_posix()}')"
            )
        else:
            con.execute(
                "CREATE TEMP VIEW resolutions AS "
                "SELECT NULL AS station_id, NULL::DATE AS valid_date_local, "
                "NULL AS kind, NULL::DOUBLE AS value_f WHERE FALSE"
            )
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

    # NBM-side metrics: NaN whenever nbm_p is null (older snapshots, NBM fetch failures).
    # pandas mean/sum default to skipna=True, so aggregate() handles the partial coverage naturally.
    has_nbm = df["nbm_p"].notna()
    df["brier_nbm"] = float("nan")
    df["log_loss_nbm"] = float("nan")
    if has_nbm.any():
        df.loc[has_nbm, "brier_nbm"] = df.loc[has_nbm].apply(
            lambda r: brier(r["nbm_p"], r["realized_yes"]), axis=1
        )
        df.loc[has_nbm, "log_loss_nbm"] = df.loc[has_nbm].apply(
            lambda r: log_loss(r["nbm_p"], r["realized_yes"], clip=cfg.log_clip), axis=1
        )

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

    # NBM simulated PnL — same Kelly-sizing rules, same fee, but using nbm_p as the
    # signal. Rows without an NBM forecast get NaN/None and are excluded from aggregate
    # sums automatically.
    nbm_pnl = df["nbm_p"].notna()
    pnl_nbm_col = pd.Series(float("nan"), index=df.index)
    direction_nbm_col = pd.Series([None] * len(df), index=df.index, dtype=object)
    kelly_nbm_col = pd.Series(float("nan"), index=df.index)
    if nbm_pnl.any():
        nbm_records = df.loc[nbm_pnl].apply(
            lambda r: simulate_pnl(
                model_p=float(r["nbm_p"]),
                market_mid=float(r["market_mid"]),
                realized=int(r["realized_yes"]),
                cfg=cfg,
            ),
            axis=1,
            result_type="expand",
        )
        nbm_records.columns = ["pnl_nbm", "direction_nbm", "kelly_nbm_sized"]
        pnl_nbm_col.loc[nbm_pnl] = nbm_records["pnl_nbm"]
        direction_nbm_col.loc[nbm_pnl] = nbm_records["direction_nbm"]
        kelly_nbm_col.loc[nbm_pnl] = nbm_records["kelly_nbm_sized"]
    df["pnl_nbm"] = pnl_nbm_col
    df["direction_nbm"] = direction_nbm_col
    df["kelly_nbm_sized"] = kelly_nbm_col

    # Blend-side metrics (ECMWF/NBM convex blend). blended_p is NaN on snapshots written
    # before the blend landed; for cells with weight 0 it equals model_p exactly, so the
    # blend column reproduces the ECMWF metrics there and diverges only on weighted cells.
    has_blend = df["blended_p"].notna()
    df["brier_blend"] = float("nan")
    df["log_loss_blend"] = float("nan")
    if has_blend.any():
        df.loc[has_blend, "brier_blend"] = df.loc[has_blend].apply(
            lambda r: brier(r["blended_p"], r["realized_yes"]), axis=1
        )
        df.loc[has_blend, "log_loss_blend"] = df.loc[has_blend].apply(
            lambda r: log_loss(r["blended_p"], r["realized_yes"], clip=cfg.log_clip), axis=1
        )

    pnl_blend_col = pd.Series(float("nan"), index=df.index)
    direction_blend_col = pd.Series([None] * len(df), index=df.index, dtype=object)
    kelly_blend_col = pd.Series(float("nan"), index=df.index)
    if has_blend.any():
        blend_records = df.loc[has_blend].apply(
            lambda r: simulate_pnl(
                model_p=float(r["blended_p"]),
                market_mid=float(r["market_mid"]),
                realized=int(r["realized_yes"]),
                cfg=cfg,
            ),
            axis=1,
            result_type="expand",
        )
        blend_records.columns = ["pnl_blend", "direction_blend", "kelly_blend_sized"]
        pnl_blend_col.loc[has_blend] = blend_records["pnl_blend"]
        direction_blend_col.loc[has_blend] = blend_records["direction_blend"]
        kelly_blend_col.loc[has_blend] = blend_records["kelly_blend_sized"]
    df["pnl_blend"] = pnl_blend_col
    df["direction_blend"] = direction_blend_col
    df["kelly_blend_sized"] = kelly_blend_col

    df["lead_bucket"] = df["model_lead_hours"].apply(lead_bucket)
    return df


def aggregate(df: pd.DataFrame, by: list[str] | None = None) -> pd.DataFrame:
    """Group by the given dimensions and compute mean / sum metrics.

    by=None or [] returns a single-row 'overall' summary.

    NBM columns are populated only on the subset of rows where nbm_p exists; pandas
    mean/sum skip NaN by default, so the NBM averages reflect that smaller denominator
    automatically. `n_nbm` reports how many rows backed the NBM aggregates.

    `brier_blend_mean` is averaged over only the `n_blend` rows where blended_p exists,
    so comparing it against `brier_model_mean` / `brier_nbm_mean` (full-sample denominators)
    is apples-to-oranges. The `brier_*_on_blend` columns give the like-for-like comparison:
    the ECMWF and NBM Brier restricted to exactly those blend rows.
    """
    if df.empty:
        return df
    has_nbm = "nbm_p" in df.columns
    has_blend = "blended_p" in df.columns
    if has_blend:
        # Non-mutating: add per-row ECMWF/NBM Brier masked to the blend rows, so the
        # grouped/overall means below land on the same denominator as brier_blend_mean.
        df = df.copy()
        blend_rows = df["blended_p"].notna()
        df["brier_model_on_blend"] = df["brier_model"].where(blend_rows)
        df["brier_nbm_on_blend"] = (
            df["brier_nbm"].where(blend_rows) if has_nbm else float("nan")
        )
    if not by:
        out: dict = {
            "n": len(df),
            "n_nbm": int(df["nbm_p"].notna().sum()) if has_nbm else 0,
            "n_blend": int(df["blended_p"].notna().sum()) if has_blend else 0,
            "brier_model_mean": df["brier_model"].mean(),
            "brier_nbm_mean": df["brier_nbm"].mean() if has_nbm else float("nan"),
            "brier_blend_mean": df["brier_blend"].mean() if has_blend else float("nan"),
            "brier_model_on_blend": df["brier_model_on_blend"].mean() if has_blend else float("nan"),
            "brier_nbm_on_blend": df["brier_nbm_on_blend"].mean() if has_blend else float("nan"),
            "brier_market_mean": df["brier_market"].mean(),
            "log_loss_model_mean": df["log_loss_model"].mean(),
            "log_loss_nbm_mean": df["log_loss_nbm"].mean() if has_nbm else float("nan"),
            "log_loss_blend_mean": df["log_loss_blend"].mean() if has_blend else float("nan"),
            "log_loss_market_mean": df["log_loss_market"].mean(),
            "pnl_sum": df["pnl"].sum(),
            "pnl_nbm_sum": df["pnl_nbm"].sum() if has_nbm else 0.0,
            "pnl_blend_sum": df["pnl_blend"].sum() if has_blend else 0.0,
            "kelly_sum": df["kelly_sized"].sum(),
            "kelly_nbm_sum": df["kelly_nbm_sized"].sum() if has_nbm else 0.0,
            "kelly_blend_sum": df["kelly_blend_sized"].sum() if has_blend else 0.0,
            "trades_emitted": int(df["direction"].notna().sum()),
            "trades_nbm_emitted": int(df["direction_nbm"].notna().sum()) if has_nbm else 0,
            "trades_blend_emitted": int(df["direction_blend"].notna().sum()) if has_blend else 0,
        }
        return pd.DataFrame([out])

    agg_kwargs = {
        "n": ("brier_model", "size"),
        "brier_model_mean": ("brier_model", "mean"),
        "brier_market_mean": ("brier_market", "mean"),
        "log_loss_model_mean": ("log_loss_model", "mean"),
        "log_loss_market_mean": ("log_loss_market", "mean"),
        "pnl_sum": ("pnl", "sum"),
        "kelly_sum": ("kelly_sized", "sum"),
        "trades_emitted": ("direction", lambda s: int(s.notna().sum())),
    }
    if has_nbm:
        agg_kwargs.update({
            "n_nbm": ("nbm_p", lambda s: int(s.notna().sum())),
            "brier_nbm_mean": ("brier_nbm", "mean"),
            "log_loss_nbm_mean": ("log_loss_nbm", "mean"),
            "pnl_nbm_sum": ("pnl_nbm", "sum"),
            "kelly_nbm_sum": ("kelly_nbm_sized", "sum"),
            "trades_nbm_emitted": ("direction_nbm", lambda s: int(s.notna().sum())),
        })
    if has_blend:
        agg_kwargs.update({
            "n_blend": ("blended_p", lambda s: int(s.notna().sum())),
            "brier_blend_mean": ("brier_blend", "mean"),
            "brier_model_on_blend": ("brier_model_on_blend", "mean"),
            "brier_nbm_on_blend": ("brier_nbm_on_blend", "mean"),
            "log_loss_blend_mean": ("log_loss_blend", "mean"),
            "pnl_blend_sum": ("pnl_blend", "sum"),
            "kelly_blend_sum": ("kelly_blend_sized", "sum"),
            "trades_blend_emitted": ("direction_blend", lambda s: int(s.notna().sum())),
        })
    grouped = df.groupby(by, dropna=False).agg(**agg_kwargs).reset_index()
    # Reorder so NBM and blend columns sit next to their ECMWF counterparts in the table.
    if has_nbm or has_blend:
        def _triplet(model_col: str, nbm_col: str, blend_col: str, market_col: str | None = None) -> list[str]:
            cols = [model_col]
            if has_nbm:
                cols.append(nbm_col)
            if has_blend:
                cols.append(blend_col)
            if market_col is not None:
                cols.append(market_col)
            return cols

        # Brier group: model / nbm / blend (full-sample), then the like-for-like
        # blend-row-restricted ECMWF & NBM Brier, then market.
        brier_group = _triplet("brier_model_mean", "brier_nbm_mean", "brier_blend_mean")
        if has_blend:
            brier_group.append("brier_model_on_blend")
            if has_nbm:
                brier_group.append("brier_nbm_on_blend")
        brier_group.append("brier_market_mean")

        col_order = [
            *by,
            "n",
            *(["n_nbm"] if has_nbm else []),
            *(["n_blend"] if has_blend else []),
            *brier_group,
            *_triplet("log_loss_model_mean", "log_loss_nbm_mean", "log_loss_blend_mean", "log_loss_market_mean"),
            *_triplet("pnl_sum", "pnl_nbm_sum", "pnl_blend_sum"),
            *_triplet("kelly_sum", "kelly_nbm_sum", "kelly_blend_sum"),
            *_triplet("trades_emitted", "trades_nbm_emitted", "trades_blend_emitted"),
        ]
        grouped = grouped[col_order]
    return grouped
