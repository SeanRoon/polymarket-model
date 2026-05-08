"""Model.evaluate_event must integrate the predictive distribution over bin intervals correctly.

We hand-construct a sample distribution where the answer is computable, then check that
prob_in_bin and evaluate_event match within the expected Laplace-smoothing tolerance.
"""
from __future__ import annotations

import math
from datetime import UTC, date, datetime

import numpy as np

from polymarket_model.markets.discovery import Bin, WeatherEvent
from polymarket_model.model import (
    PredictiveDistribution,
    assert_bins_cover_support,
    evaluate_event,
)


def _bin(idx, lo, hi, label, open_low=False, open_high=False):
    return Bin(
        outcome_index=idx,
        yes_token_id=f"yes_{idx}",
        no_token_id=f"no_{idx}",
        label=label,
        lo_f=lo,
        hi_f=hi,
        is_open_low=open_low,
        is_open_high=open_high,
    )


def _event(bins):
    return WeatherEvent(
        event_id="test",
        slug="test-event",
        title="test",
        end_date_utc=datetime(2026, 5, 8, 12, tzinfo=UTC),
        target_date_local=date(2026, 5, 8),
        kind="high",
        city="Test",
        station_id="KTEST",
        resolution_source=None,
        unit="F",
        condition_ids=["c0"],
        bins=bins,
    )


def test_prob_in_bin_uniform_samples():
    # 100 evenly spaced samples in [0, 100): bin [25, 50) should contain ~25%.
    samples = np.arange(0, 100, 1, dtype=float)
    dist = PredictiveDistribution(samples=samples, unit="F", model="test")
    assert dist.prob_in_bin(25, 50) == 0.25
    assert dist.prob_in_bin(-math.inf, 25) == 0.25
    assert dist.prob_in_bin(75, math.inf) == 0.25
    assert dist.prob_in_bin(0, 100) == 1.0


def test_evaluate_event_with_full_coverage():
    bins = [
        _bin(0, -math.inf, 50.0, "<50", open_low=True),
        _bin(1, 50.0, 60.0, "50-59"),
        _bin(2, 60.0, 70.0, "60-69"),
        _bin(3, 70.0, math.inf, ">=70", open_high=True),
    ]
    ok, _ = assert_bins_cover_support(bins)
    assert ok
    samples = np.array([45, 55, 55, 65, 75, 75, 85, 95, 95, 95], dtype=float)  # n=10
    dist = PredictiveDistribution(samples=samples, unit="F", model="test")
    out = evaluate_event(_event(bins), dist, laplace_alpha=0.0)
    # With alpha=0, probabilities are raw counts/N.
    assert [round(b.p, 3) for b in out.bin_probs] == [0.1, 0.2, 0.1, 0.6]
    assert math.isclose(out.sum_of_bin_probs, 1.0)
    assert out.outside_bin_mass == 0.0


def test_evaluate_event_outside_mass_when_bins_have_gap():
    # Deliberately leave a gap [60, 70).
    bins = [
        _bin(0, -math.inf, 50.0, "<50", open_low=True),
        _bin(1, 50.0, 60.0, "50-59"),
        _bin(2, 70.0, math.inf, ">=70", open_high=True),
    ]
    samples = np.array([45, 55, 65, 75, 85], dtype=float)  # 65 falls in the gap
    dist = PredictiveDistribution(samples=samples, unit="F", model="test")
    out = evaluate_event(_event(bins), dist, laplace_alpha=0.0)
    assert math.isclose(out.outside_bin_mass, 0.2)


def test_laplace_smoothing_avoids_zeros():
    # Empty bin would have raw p=0; smoothing must give something > 0.
    bins = [
        _bin(0, -math.inf, 0.0, "<0", open_low=True),
        _bin(1, 0.0, 100.0, "0-99"),
        _bin(2, 100.0, math.inf, ">=100", open_high=True),
    ]
    samples = np.array([50.0] * 51)  # all in middle bin
    dist = PredictiveDistribution(samples=samples, unit="F", model="test")
    out = evaluate_event(_event(bins), dist, laplace_alpha=0.5)
    probs = [b.p for b in out.bin_probs]
    assert all(p > 0 for p in probs)
    assert all(p < 1 for p in probs)
    assert math.isclose(sum(probs), 1.0, abs_tol=1e-9)


def test_assert_bins_cover_support_detects_missing_open_bins():
    closed_only = [_bin(0, 50.0, 60.0, "50-59"), _bin(1, 60.0, 70.0, "60-69")]
    ok, reason = assert_bins_cover_support(closed_only)
    assert not ok
    assert "open-low" in reason or "open-high" in reason
