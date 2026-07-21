"""Flag families fire (and stay quiet) on synthetic scored DataFrames."""
from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from polymarket_model.diagnostics import (
    DiagnosticsConfig,
    Flag,
    render_markdown,
    run_diagnostics,
)

REF = date(2026, 5, 27)


def _rows(
    *,
    n: int,
    city: str,
    kind: str,
    station: str,
    brier_model: float,
    brier_market: float,
    pnl: float,
    model_p: float = 0.2,
    realized_yes: int = 0,
    nbm_p: float | None = None,
    brier_nbm: float | None = None,
    emos_p: float | None = None,
    brier_emos: float | None = None,
    lead_bucket: str = "0-6h",
    target_date: date = REF,
) -> list[dict]:
    """n identical scored rows with the columns run_diagnostics reads."""
    nan = float("nan")
    return [
        {
            "city": city,
            "kind": kind,
            "station_id": station,
            "lead_bucket": lead_bucket,
            "target_date_local": target_date,
            "brier_model": brier_model,
            "brier_market": brier_market,
            "pnl": pnl / n,  # so the per-cell sum equals `pnl`
            "model_p": model_p,
            "realized_yes": realized_yes,
            "nbm_p": nbm_p if nbm_p is not None else nan,
            "brier_nbm": brier_nbm if brier_nbm is not None else nan,
            "emos_p": emos_p if emos_p is not None else nan,
            "brier_emos": brier_emos if brier_emos is not None else nan,
        }
        for _ in range(n)
    ]


def test_empty_frame_returns_no_flags():
    assert run_diagnostics(pd.DataFrame(), reference_date=REF) == []


def test_excluded_station_ready_to_reenable():
    # KMIA is excluded by default; here its model Brier beats the market -> "good" flag.
    df = pd.DataFrame(_rows(
        n=200, city="Miami", kind="high", station="KMIA",
        brier_model=0.04, brier_market=0.05, pnl=2.0,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    codes = {f.code for f in flags}
    assert "reenable_candidate" in codes
    f = next(f for f in flags if f.code == "reenable_candidate")
    assert f.severity == "good"
    assert "KMIA" in f.suggestion


def test_excluded_station_still_bad_holds():
    df = pd.DataFrame(_rows(
        n=200, city="Miami", kind="high", station="KMIA",
        brier_model=0.23, brier_market=0.03, pnl=-7.0,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    assert any(f.code == "exclusion_holds" for f in flags)
    # An excluded station must never be told to exclude again.
    assert not any(f.code == "exclude_candidate" for f in flags)


def test_included_station_worse_than_market_flags_exclude():
    # KAUS is not excluded; model worse than market AND losing -> critical exclude_candidate.
    df = pd.DataFrame(_rows(
        n=200, city="Austin", kind="high", station="KAUS",
        brier_model=0.20, brier_market=0.04, pnl=-3.0,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    f = next(f for f in flags if f.code == "exclude_candidate")
    assert f.severity == "critical"
    assert "KAUS" in f.suggestion


def test_worse_than_market_but_profitable_does_not_exclude():
    # Higher Brier than market but still positive PnL -> not an exclude candidate.
    df = pd.DataFrame(_rows(
        n=200, city="Austin", kind="high", station="KAUS",
        brier_model=0.20, brier_market=0.04, pnl=+5.0,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    assert not any(f.code == "exclude_candidate" for f in flags)


def test_fully_cell_excluded_station_emits_no_exclude_candidate():
    # KMDW is not in signal_excluded_stations, but both its cells are cell-excluded. The
    # station rollup must drop those rows and stay silent rather than fire a phantom
    # exclude_candidate critical (the issue-#6 diagnose-rollup artifact).
    df = pd.DataFrame(
        _rows(n=200, city="Chicago", kind="high", station="KMDW",
              brier_model=0.20, brier_market=0.04, pnl=-9.0)
        + _rows(n=200, city="Chicago", kind="low", station="KMDW",
                brier_model=0.18, brier_market=0.05, pnl=-4.0)
    )
    cfg = DiagnosticsConfig(excluded_cells=frozenset({("KMDW", "high"), ("KMDW", "low")}))
    flags = run_diagnostics(df, cfg, reference_date=REF)
    assert not any(f.code == "exclude_candidate" and "KMDW" in f.dimension for f in flags)


def test_partial_cell_exclusion_judges_station_on_live_cell():
    # KSAT/low is cell-excluded and losing; KSAT/high is live and healthy (Brier <= market,
    # positive PnL). Dropping the dark /low row means the station reads as its live /high cell,
    # so no exclude_candidate fires despite the /low drag.
    df = pd.DataFrame(
        _rows(n=200, city="San Antonio", kind="high", station="KSAT",
              brier_model=0.03, brier_market=0.05, pnl=+8.0)
        + _rows(n=200, city="San Antonio", kind="low", station="KSAT",
                brier_model=0.22, brier_market=0.04, pnl=-6.0)
    )
    cfg = DiagnosticsConfig(excluded_cells=frozenset({("KSAT", "low")}))
    flags = run_diagnostics(df, cfg, reference_date=REF)
    assert not any(f.code == "exclude_candidate" for f in flags)


def test_below_min_sample_is_ignored():
    df = pd.DataFrame(_rows(
        n=10, city="New York City", kind="high", station="KNYC",
        brier_model=0.20, brier_market=0.04, pnl=-3.0,
    ))
    flags = run_diagnostics(df, DiagnosticsConfig(min_sample=100), reference_date=REF)
    assert not any(f.code == "exclude_candidate" for f in flags)


def test_week_over_week_regression():
    prior = _rows(
        n=150, city="Chicago", kind="low", station="KMDW",
        brier_model=0.10, brier_market=0.10, pnl=0.0,
        target_date=REF - timedelta(days=10),
    )
    recent = _rows(
        n=150, city="Chicago", kind="low", station="KMDW",
        brier_model=0.16, brier_market=0.10, pnl=0.0,
        target_date=REF - timedelta(days=2),
    )
    df = pd.DataFrame(prior + recent)
    flags = run_diagnostics(df, reference_date=REF)
    f = next(f for f in flags if f.code == "regression_wow")
    assert f.severity == "warn"
    assert f.dimension == "Chicago / low"


def test_nbm_beats_ecmwf():
    df = pd.DataFrame(_rows(
        n=200, city="Denver", kind="high", station="KDEN",
        brier_model=0.14, brier_market=0.14, pnl=0.0,
        nbm_p=0.5, brier_nbm=0.10,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    f = next(f for f in flags if f.code == "nbm_beats_ecmwf")
    assert f.dimension == "Denver / high / 0-6h"


def test_calibration_bias_overprediction():
    # mean(model_p)=0.40 but realized rate=0.10 -> over-predicts YES.
    df = pd.DataFrame(_rows(
        n=200, city="Los Angeles", kind="high", station="KLAX",
        brier_model=0.10, brier_market=0.10, pnl=0.0,
        model_p=0.40, realized_yes=0,
    ) + _rows(
        n=20, city="Los Angeles", kind="high", station="KLAX",
        brier_model=0.10, brier_market=0.10, pnl=0.0,
        model_p=0.40, realized_yes=1,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    assert any(f.code == "calibration_bias" for f in flags)


def test_flags_sorted_critical_first():
    df = pd.DataFrame(
        _rows(n=200, city="Austin", kind="high", station="KAUS",
              brier_model=0.20, brier_market=0.04, pnl=-3.0)
        + _rows(n=200, city="Denver", kind="high", station="KDEN",
                brier_model=0.14, brier_market=0.14, pnl=0.0,
                nbm_p=0.5, brier_nbm=0.10)
    )
    flags = run_diagnostics(df, reference_date=REF)
    severities = [f.severity for f in flags]
    # critical must precede info in the sorted output.
    assert severities.index("critical") < severities.index("info")


def test_render_markdown_empty_and_nonempty():
    assert "within thresholds" in render_markdown([])
    md = render_markdown([
        Flag("exclude_candidate", "critical", "NYC (KNYC)", "detail | with pipe", "do x"),
    ])
    assert "| critical | exclude_candidate |" in md
    # Pipe in the detail must be escaped so the table doesn't break.
    assert "detail \\| with pipe" in md


def test_emos_beats_market_fires_good_flag():
    df = pd.DataFrame(_rows(
        n=200, city="Los Angeles", kind="high", station="KLAX",
        brier_model=0.25, brier_market=0.06, pnl=0.0,
        emos_p=0.5, brier_emos=0.05,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    f = next(f for f in flags if f.code == "emos_beats_market")
    assert f.severity == "good"
    assert f.dimension == "Los Angeles / high"


def test_emos_improves_model_but_not_market_is_info():
    df = pd.DataFrame(_rows(
        n=200, city="Los Angeles", kind="high", station="KLAX",
        brier_model=0.25, brier_market=0.06, pnl=0.0,
        emos_p=0.5, brier_emos=0.12,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    codes = {f.code for f in flags}
    assert "emos_improves_model" in codes
    assert "emos_beats_market" not in codes


def test_emos_underperforming_model_is_warn():
    df = pd.DataFrame(_rows(
        n=200, city="Los Angeles", kind="high", station="KLAX",
        brier_model=0.10, brier_market=0.06, pnl=0.0,
        emos_p=0.5, brier_emos=0.20,
    ))
    flags = run_diagnostics(df, reference_date=REF)
    f = next(f for f in flags if f.code == "emos_underperforms")
    assert f.severity == "warn"


def test_emos_flags_quiet_without_emos_rows_or_below_min_sample():
    # No emos_p at all -> no EMOS flags.
    df = pd.DataFrame(_rows(
        n=200, city="Los Angeles", kind="high", station="KLAX",
        brier_model=0.25, brier_market=0.06, pnl=0.0,
    ))
    assert not any(f.code.startswith("emos_") for f in run_diagnostics(df, reference_date=REF))
    # EMOS rows present but under min_sample -> still quiet.
    df_small = pd.DataFrame(_rows(
        n=50, city="Los Angeles", kind="high", station="KLAX",
        brier_model=0.25, brier_market=0.06, pnl=0.0,
        emos_p=0.5, brier_emos=0.05,
    ))
    assert not any(f.code.startswith("emos_") for f in run_diagnostics(df_small, reference_date=REF))
