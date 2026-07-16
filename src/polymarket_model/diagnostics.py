"""Deterministic model-health diagnostics.

Reads the scored per-row DataFrame from `evaluation.score_resolutions` and emits a
list of `Flag`s: discrete, thresholded findings about where the model is weak or
where an opportunity exists. The rendered `diagnostics.md` is what the scheduled
`model-watch` agent reads — the agent reasons over these conclusions and the git
history rather than re-deriving statistics from the snapshot Parquets.

Pure functions over a DataFrame: no network, no disk. Unit-tested offline. The
arithmetic lives here so the agent's output stays auditable and cheap; anything
that requires judgment (is a flag noise? what changed in git? what to try next?)
is left to the agent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta

import pandas as pd

from polymarket_model.config import settings

# Lower sorts first: criticals at the top of the table, info at the bottom.
SEVERITY_ORDER = {"critical": 0, "warn": 1, "good": 2, "info": 3}


@dataclass(frozen=True)
class Flag:
    """One thresholded finding. `code` is stable/machine-readable; the rest is prose."""

    code: str
    severity: str  # critical | warn | good | info
    dimension: str  # e.g. "Miami (KMIA)" or "Denver / high / 24-72h"
    detail: str
    suggestion: str


@dataclass(frozen=True)
class DiagnosticsConfig:
    # A (city,kind) or station cell needs at least this many scored rows to be trusted.
    min_sample: int = 100
    # Brier gap (model minus market) above which an *included* station is flagged to exclude.
    worse_than_market_margin: float = 0.02
    # Brier gap (ECMWF minus NBM) above which NBM is flagged as the better base model for a cell.
    nbm_margin: float = 0.02
    # Brier gap (vs the raw model, same rows) beyond which the EMOS pilot is flagged as
    # materially better (info) or materially worse (warn) than what it replaces.
    emos_margin: float = 0.02
    # Brier increase (recent window minus prior window) above which a regression is flagged.
    wow_regression_margin: float = 0.02
    # abs(mean(model_p) minus realized rate) above which aggregate miscalibration is flagged.
    calibration_gap: float = 0.04
    # Length in days of the recent/prior windows for the week-over-week comparison.
    window_days: int = 7
    excluded_stations: frozenset[str] = field(
        default_factory=lambda: frozenset(s.upper() for s in settings.signal_excluded_stations)
    )


def _exclusion_flags(df: pd.DataFrame, cfg: DiagnosticsConfig) -> list[Flag]:
    """Per-station review of the signal-exclusion list (config.signal_excluded_stations).

    For excluded stations: are they ready to re-enable (model Brier <= market)?
    For included stations: should they be excluded (model worse than market AND losing)?
    """
    flags: list[Flag] = []
    g = (
        df.groupby(["station_id", "city"], dropna=False)
        .agg(
            n=("brier_model", "size"),
            brier_model=("brier_model", "mean"),
            brier_market=("brier_market", "mean"),
            pnl=("pnl", "sum"),
        )
        .reset_index()
    )
    for _, r in g.iterrows():
        if r["n"] < cfg.min_sample:
            continue
        station = str(r["station_id"]).upper()
        gap = r["brier_model"] - r["brier_market"]
        dim = f"{r['city']} ({station})"
        if station in cfg.excluded_stations:
            if r["brier_model"] <= r["brier_market"]:
                flags.append(Flag(
                    code="reenable_candidate",
                    severity="good",
                    dimension=dim,
                    detail=(
                        f"Excluded station now matches/beats market: model Brier "
                        f"{r['brier_model']:.3f} <= market {r['brier_market']:.3f} over n={int(r['n'])}."
                    ),
                    suggestion=f"Consider removing {station} from signal_excluded_stations.",
                ))
            else:
                flags.append(Flag(
                    code="exclusion_holds",
                    severity="info",
                    dimension=dim,
                    detail=(
                        f"Still miscalibrated: model Brier {r['brier_model']:.3f} vs market "
                        f"{r['brier_market']:.3f} (gap +{gap:.3f}) over n={int(r['n'])}."
                    ),
                    suggestion=f"Keep {station} excluded; revisit after Phase 3 calibration.",
                ))
        elif gap > cfg.worse_than_market_margin and r["pnl"] < 0:
            flags.append(Flag(
                code="exclude_candidate",
                severity="critical",
                dimension=dim,
                detail=(
                    f"Model worse than market and losing: Brier {r['brier_model']:.3f} vs "
                    f"{r['brier_market']:.3f} (gap +{gap:.3f}), PnL {r['pnl']:+.2f} over n={int(r['n'])}."
                ),
                suggestion=f"Consider adding {station} to signal_excluded_stations until calibration improves.",
            ))
    return flags


def _regression_flags(
    df: pd.DataFrame, cfg: DiagnosticsConfig, reference_date: date
) -> list[Flag]:
    """Week-over-week Brier regression per (city, kind): recent window vs the prior window."""
    if "target_date_local" not in df.columns:
        return []
    d = df.copy()
    d["_td"] = pd.to_datetime(d["target_date_local"]).dt.date
    recent_lo = reference_date - timedelta(days=cfg.window_days - 1)
    prior_hi = recent_lo - timedelta(days=1)
    prior_lo = prior_hi - timedelta(days=cfg.window_days - 1)
    recent = d[(d["_td"] >= recent_lo) & (d["_td"] <= reference_date)]
    prior = d[(d["_td"] >= prior_lo) & (d["_td"] <= prior_hi)]
    if recent.empty or prior.empty:
        return []

    def _by_ck(frame: pd.DataFrame) -> pd.DataFrame:
        return (
            frame.groupby(["city", "kind"], dropna=False)
            .agg(n=("brier_model", "size"), brier=("brier_model", "mean"))
            .reset_index()
        )

    merged = _by_ck(recent).merge(
        _by_ck(prior), on=["city", "kind"], suffixes=("_recent", "_prior")
    )
    flags: list[Flag] = []
    for _, r in merged.iterrows():
        if r["n_recent"] < cfg.min_sample or r["n_prior"] < cfg.min_sample:
            continue
        delta = r["brier_recent"] - r["brier_prior"]
        if delta > cfg.wow_regression_margin:
            flags.append(Flag(
                code="regression_wow",
                severity="warn",
                dimension=f"{r['city']} / {r['kind']}",
                detail=(
                    f"Brier worsened {r['brier_prior']:.3f} -> {r['brier_recent']:.3f} (+{delta:.3f}) "
                    f"over the last {cfg.window_days}d vs the prior {cfg.window_days}d."
                ),
                suggestion="Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions.",
            ))
    return flags


def _nbm_flags(df: pd.DataFrame, cfg: DiagnosticsConfig) -> list[Flag]:
    """Cells (city, kind, lead_bucket) where NBM has materially lower Brier than ECMWF."""
    if "nbm_p" not in df.columns:
        return []
    has = df[df["nbm_p"].notna()]
    if has.empty:
        return []
    g = (
        has.groupby(["city", "kind", "lead_bucket"], dropna=False)
        .agg(
            n=("brier_nbm", "size"),
            brier_model=("brier_model", "mean"),
            brier_nbm=("brier_nbm", "mean"),
        )
        .reset_index()
    )
    flags: list[Flag] = []
    for _, r in g.iterrows():
        if r["n"] < cfg.min_sample:
            continue
        gap = r["brier_model"] - r["brier_nbm"]
        if gap > cfg.nbm_margin:
            flags.append(Flag(
                code="nbm_beats_ecmwf",
                severity="info",
                dimension=f"{r['city']} / {r['kind']} / {r['lead_bucket']}",
                detail=(
                    f"NBM lower Brier {r['brier_nbm']:.3f} vs ECMWF {r['brier_model']:.3f} "
                    f"(gap {gap:.3f}) over n={int(r['n'])}."
                ),
                suggestion="Consider weighting toward NBM for this cell, or an ECMWF/NBM blend.",
            ))
    return flags


def _emos_flags(df: pd.DataFrame, cfg: DiagnosticsConfig) -> list[Flag]:
    """Track the EMOS pilot per (city, kind): its Brier vs the raw model and the market.

    All three means are restricted to exactly the rows where emos_p exists, so the
    comparison is like-for-like out-of-sample. The market comparison is the pilot's
    graduation bar (same bar KSAT/high met before re-enabling); the model comparison
    says whether EMOS at least improves on what it replaces.
    """
    if "emos_p" not in df.columns:
        return []
    has = df[df["emos_p"].notna()]
    if has.empty:
        return []
    g = (
        has.groupby(["city", "kind"], dropna=False)
        .agg(
            n=("brier_emos", "size"),
            brier_emos=("brier_emos", "mean"),
            brier_model=("brier_model", "mean"),
            brier_market=("brier_market", "mean"),
        )
        .reset_index()
    )
    flags: list[Flag] = []
    for _, r in g.iterrows():
        if r["n"] < cfg.min_sample:
            continue
        dim = f"{r['city']} / {r['kind']}"
        vs = (
            f"EMOS Brier {r['brier_emos']:.3f} vs model {r['brier_model']:.3f} "
            f"vs market {r['brier_market']:.3f} over n={int(r['n'])} (same rows)."
        )
        if r["brier_emos"] <= r["brier_market"]:
            flags.append(Flag(
                code="emos_beats_market",
                severity="good",
                dimension=dim,
                detail=f"EMOS pilot at/above market out-of-sample: {vs}",
                suggestion=(
                    "If this holds for ~30 days of settlements, candidate to promote emos_p "
                    "for this cell (human decision; live cities stay out per operator mandate)."
                ),
            ))
        elif r["brier_emos"] < r["brier_model"] - cfg.emos_margin:
            flags.append(Flag(
                code="emos_improves_model",
                severity="info",
                dimension=dim,
                detail=f"EMOS beats the raw model but not yet the market: {vs}",
                suggestion="Keep accruing; no action until the market gap closes.",
            ))
        elif r["brier_emos"] > r["brier_model"] + cfg.emos_margin:
            flags.append(Flag(
                code="emos_underperforms",
                severity="warn",
                dimension=dim,
                detail=f"EMOS worse than the raw model it replaces: {vs}",
                suggestion=(
                    "Inspect coefficient stability across daily refits (data/station_emos.parquet "
                    "history) and consider dropping this cell from emos_stations."
                ),
            ))
    return flags


def _calibration_flags(df: pd.DataFrame, cfg: DiagnosticsConfig) -> list[Flag]:
    """Coarse aggregate calibration per (city, kind): mean(model_p) vs realized YES rate.

    Across all bins of an event the model_p sum ~1 and exactly one bin realizes, so a
    persistent gap signals systematic over/under-confidence (or leaked outside-bin mass).
    This is a cheap screen; a proper reliability curve is Phase 3 work.
    """
    g = (
        df.groupby(["city", "kind"], dropna=False)
        .agg(
            n=("model_p", "size"),
            mean_p=("model_p", "mean"),
            realized=("realized_yes", "mean"),
        )
        .reset_index()
    )
    flags: list[Flag] = []
    for _, r in g.iterrows():
        if r["n"] < cfg.min_sample:
            continue
        gap = r["mean_p"] - r["realized"]
        if abs(gap) > cfg.calibration_gap:
            direction = "over" if gap > 0 else "under"
            flags.append(Flag(
                code="calibration_bias",
                severity="warn",
                dimension=f"{r['city']} / {r['kind']}",
                detail=(
                    f"Aggregate model probability {direction}-predicts YES: mean(model_p) "
                    f"{r['mean_p']:.3f} vs realized rate {r['realized']:.3f} (gap {gap:+.3f}) over n={int(r['n'])}."
                ),
                suggestion="Coarse screen — build a reliability curve and consider isotonic recalibration (Phase 3).",
            ))
    return flags


def run_diagnostics(
    df: pd.DataFrame,
    cfg: DiagnosticsConfig | None = None,
    *,
    reference_date: date | None = None,
) -> list[Flag]:
    """Run every flag family over the scored DataFrame, sorted critical-first.

    `df` is the output of `evaluation.score_resolutions` (optionally pre-filtered by
    date). Returns [] for an empty frame.
    """
    cfg = cfg or DiagnosticsConfig()
    if df.empty:
        return []
    reference_date = reference_date or datetime.now(UTC).date()
    flags = [
        *_exclusion_flags(df, cfg),
        *_regression_flags(df, cfg, reference_date),
        *_nbm_flags(df, cfg),
        *_emos_flags(df, cfg),
        *_calibration_flags(df, cfg),
    ]
    flags.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 9), f.code, f.dimension))
    return flags


def render_markdown(
    flags: list[Flag], *, generated_at: datetime | None = None
) -> str:
    """Render flags as the committed `diagnostics.md` the model-watch agent reads."""
    generated_at = generated_at or datetime.now(UTC)
    lines = [
        "# Model diagnostics",
        "",
        f"_Generated {generated_at:%Y-%m-%d %H:%M UTC}. Deterministic flags from "
        "`polymarket diagnose`; see `model-watch.md` for the agent's interpretation._",
        "",
    ]
    if not flags:
        lines += ["No flags — model health within thresholds across all monitored cells.", ""]
        return "\n".join(lines)

    counts: dict[str, int] = {}
    for f in flags:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    summary = ", ".join(
        f"{counts[s]} {s}" for s in ("critical", "warn", "good", "info") if s in counts
    )
    lines += [
        f"**{len(flags)} flag(s):** {summary}",
        "",
        "| severity | code | dimension | detail | suggestion |",
        "|:---------|:-----|:----------|:-------|:-----------|",
    ]
    for f in flags:
        detail = f.detail.replace("|", "\\|")
        sugg = f.suggestion.replace("|", "\\|")
        lines.append(f"| {f.severity} | {f.code} | {f.dimension} | {detail} | {sugg} |")
    lines.append("")
    return "\n".join(lines)
