"""Brier and log-loss correctness + boundary clipping."""
from __future__ import annotations

import math

import pandas as pd
import pytest

from polymarket_model.evaluation import aggregate, brier, lead_bucket, log_loss


def test_brier_constant_50_50_baseline():
    # A model that says 0.5 on every bin and the realized vector is 50/50:
    # mean Brier should be 0.25.
    n = 100
    total = sum(brier(0.5, 1) for _ in range(n // 2)) + sum(brier(0.5, 0) for _ in range(n // 2))
    assert math.isclose(total / n, 0.25)


def test_brier_perfect_zero():
    assert brier(1.0, 1) == 0.0
    assert brier(0.0, 0) == 0.0


def test_brier_worst_case():
    assert brier(1.0, 0) == 1.0
    assert brier(0.0, 1) == 1.0


def test_log_loss_clips_at_zero_and_one():
    # Without clipping, log_loss(0, 1) = -log(0) = inf. With clip=1e-6, ~13.8.
    v = log_loss(0.0, 1)
    assert math.isfinite(v)
    assert v == pytest.approx(-math.log(1e-6), rel=1e-6)
    v2 = log_loss(1.0, 0)
    assert math.isfinite(v2)


def test_log_loss_perfect_is_near_zero():
    assert log_loss(1.0, 1, clip=1e-9) == pytest.approx(0.0, abs=1e-8)
    assert log_loss(0.0, 0, clip=1e-9) == pytest.approx(0.0, abs=1e-8)


@pytest.mark.parametrize(
    ("hours", "label"),
    [
        (0, "0-6h"),
        (5.5, "0-6h"),
        (6, "6-24h"),
        (23, "6-24h"),
        (24, "24-72h"),
        (71, "24-72h"),
        (72, "3-7d"),
        (167, "3-7d"),
        (168, ">7d"),
        (None, "unknown"),
    ],
)
def test_lead_bucket(hours, label):
    assert lead_bucket(hours) == label


def _synthetic_score_df(n_total: int, n_with_nbm: int, n_with_blend: int = 0) -> pd.DataFrame:
    """Build a minimal score_resolutions-shaped DataFrame for aggregate() tests.

    Blend rows (the first `n_with_blend`, a subset of the NBM rows) get a deliberately
    *worse* ECMWF Brier (0.32) than the non-blend rows (0.20) so that the full-sample
    `brier_model_mean` and the blend-row-restricted `brier_model_on_blend` differ — that
    gap is exactly the reporting artifact the on_blend columns exist to expose.
    """
    nan = float("nan")
    rows = []
    for i in range(n_total):
        has_nbm = i < n_with_nbm
        has_blend = i < n_with_blend
        rows.append({
            "city": "Miami",
            "kind": "high",
            "lead_bucket": "0-6h",
            "brier_model": 0.32 if has_blend else 0.20,
            "brier_market": 0.05,
            "log_loss_model": 0.50,
            "log_loss_market": 0.15,
            "pnl": 0.10,
            "kelly_sized": 1.0,
            "direction": "BUY_YES",
            "nbm_p": 0.60 if has_nbm else nan,
            "brier_nbm": 0.08 if has_nbm else nan,
            "log_loss_nbm": 0.25 if has_nbm else nan,
            "pnl_nbm": 0.20 if has_nbm else nan,
            "direction_nbm": "BUY_YES" if has_nbm else None,
            "kelly_nbm_sized": 1.0 if has_nbm else nan,
        })
        if n_with_blend:
            rows[-1].update({
                "blended_p": 0.55 if has_blend else nan,
                "brier_blend": 0.18 if has_blend else nan,
                "log_loss_blend": 0.40 if has_blend else nan,
                "pnl_blend": 0.15 if has_blend else nan,
                "direction_blend": "BUY_YES" if has_blend else None,
                "kelly_blend_sized": 1.0 if has_blend else nan,
            })
    return pd.DataFrame(rows)


def test_aggregate_overall_separates_nbm_denominator():
    df = _synthetic_score_df(n_total=10, n_with_nbm=3)
    out = aggregate(df, by=None)
    row = out.iloc[0]
    assert row["n"] == 10
    assert row["n_nbm"] == 3
    # ECMWF mean over all 10, NBM mean over the 3 with nbm_p; both should equal their constant inputs.
    assert row["brier_model_mean"] == pytest.approx(0.20)
    assert row["brier_nbm_mean"] == pytest.approx(0.08)
    assert row["brier_market_mean"] == pytest.approx(0.05)
    # PnL sums independently per source.
    assert row["pnl_sum"] == pytest.approx(0.10 * 10)
    assert row["pnl_nbm_sum"] == pytest.approx(0.20 * 3)
    assert row["trades_emitted"] == 10
    assert row["trades_nbm_emitted"] == 3


def test_aggregate_grouped_column_order_puts_nbm_next_to_ecmwf():
    df = _synthetic_score_df(n_total=10, n_with_nbm=4)
    out = aggregate(df, by=["city", "kind", "lead_bucket"])
    cols = list(out.columns)
    # NBM columns should immediately follow their ECMWF counterparts in the rendered table.
    assert cols.index("brier_nbm_mean") == cols.index("brier_model_mean") + 1
    assert cols.index("log_loss_nbm_mean") == cols.index("log_loss_model_mean") + 1
    assert cols.index("pnl_nbm_sum") == cols.index("pnl_sum") + 1
    assert cols.index("n_nbm") == cols.index("n") + 1


def test_aggregate_blend_on_blend_columns_use_blend_denominator():
    # 10 rows, 6 with NBM, 4 of those with a blend. Blend rows have brier_model=0.32,
    # the other 6 have 0.20 -> full-sample model mean is a mix, on_blend mean is 0.32.
    df = _synthetic_score_df(n_total=10, n_with_nbm=6, n_with_blend=4)
    out = aggregate(df, by=None)
    row = out.iloc[0]
    assert row["n"] == 10
    assert row["n_blend"] == 4
    # Full-sample ECMWF Brier mixes blend (0.32) and non-blend (0.20) rows.
    assert row["brier_model_mean"] == pytest.approx((0.32 * 4 + 0.20 * 6) / 10)
    # Like-for-like: ECMWF/NBM Brier restricted to exactly the 4 blend rows.
    assert row["brier_model_on_blend"] == pytest.approx(0.32)
    assert row["brier_nbm_on_blend"] == pytest.approx(0.08)
    assert row["brier_blend_mean"] == pytest.approx(0.18)


def test_aggregate_grouped_on_blend_columns_sit_after_blend():
    df = _synthetic_score_df(n_total=10, n_with_nbm=6, n_with_blend=4)
    out = aggregate(df, by=["city", "kind", "lead_bucket"])
    cols = list(out.columns)
    # on_blend Brier columns immediately follow brier_blend_mean, before market.
    assert cols.index("brier_model_on_blend") == cols.index("brier_blend_mean") + 1
    assert cols.index("brier_nbm_on_blend") == cols.index("brier_model_on_blend") + 1
    assert cols.index("brier_market_mean") == cols.index("brier_nbm_on_blend") + 1
    row = out.iloc[0]
    assert row["brier_model_on_blend"] == pytest.approx(0.32)
    assert row["brier_blend_mean"] == pytest.approx(0.18)


def test_aggregate_handles_zero_nbm_rows_gracefully():
    """When no rows have NBM, NBM means are NaN, sums are 0 — matches the pre-cron state."""
    df = _synthetic_score_df(n_total=10, n_with_nbm=0)
    out = aggregate(df, by=None)
    row = out.iloc[0]
    assert row["n"] == 10
    assert row["n_nbm"] == 0
    assert math.isnan(row["brier_nbm_mean"])
    assert row["pnl_nbm_sum"] == 0.0
    assert row["trades_nbm_emitted"] == 0
