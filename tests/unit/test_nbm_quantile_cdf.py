"""Unit tests for the NBM quantile-CDF integration in `model.evaluate_event_nbm`.

Synthetic forecasts only — no network. Verifies that linear CDF interpolation between
quantiles, plus edge-slope tail extrapolation, produces sensible bin probabilities for
the Kalshi 6-bin partition layout.
"""
from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from polymarket_model.markets.discovery import Bin, WeatherEvent
from polymarket_model.model import _cdf_eval, _quantile_cdf_anchors, evaluate_event_nbm
from polymarket_model.weather.nbm import NBMQuantileForecast


def _make_event(boundaries: list[float]) -> WeatherEvent:
    """Build a 6-bin Kalshi-style event from 5 boundary temperatures.

    Boundaries [b1..b5] produce bins:
        (-inf, b1), [b1, b2), [b2, b3), [b3, b4), [b4, b5), [b5, +inf)
    """
    assert len(boundaries) == 5
    bins: list[Bin] = []
    bins.append(Bin(
        market_ticker="T-1", event_ticker="E", bin_index=0, subtitle=f"below {boundaries[0]}",
        floor_strike=None, cap_strike=boundaries[0] - 0.5, lo_f=float("-inf"), hi_f=boundaries[0],
        is_open_low=True, is_open_high=False,
    ))
    for i in range(4):
        lo, hi = boundaries[i], boundaries[i + 1]
        bins.append(Bin(
            market_ticker=f"B-{i}", event_ticker="E", bin_index=i + 1, subtitle=f"[{lo},{hi})",
            floor_strike=lo - 0.5, cap_strike=hi - 0.5, lo_f=lo, hi_f=hi,
            is_open_low=False, is_open_high=False,
        ))
    bins.append(Bin(
        market_ticker="T-2", event_ticker="E", bin_index=5, subtitle=f"at or above {boundaries[-1]}",
        floor_strike=boundaries[-1] - 0.5, cap_strike=None, lo_f=boundaries[-1], hi_f=float("inf"),
        is_open_low=False, is_open_high=True,
    ))
    return WeatherEvent(
        event_ticker="E", series_ticker="S", title="t", city="X", kind="high",
        target_date_local=date(2026, 5, 18), station_id="KNYC",
        rules_primary=None, close_time_utc=datetime(2026, 5, 18, 0, 0, tzinfo=UTC),
        bins=bins,
    )


def _make_forecast(quantiles: dict[int, float]) -> NBMQuantileForecast:
    return NBMQuantileForecast(
        station_id="KNYC",
        target_date_local=date(2026, 5, 18),
        kind="high",
        unit="F",
        model="nbm_qmd",
        cycle_time_utc=datetime(2026, 5, 17, 12, tzinfo=UTC),
        valid_time_utc=datetime(2026, 5, 18, 21, tzinfo=UTC),
        lead_hours=33,
        quantiles=quantiles,
        percentile_levels=tuple(sorted(quantiles.keys())),
    )


def test_cdf_anchors_monotonic_and_bounded():
    full_x, full_y = _quantile_cdf_anchors({10: 60.0, 25: 65.0, 50: 70.0, 75: 75.0, 90: 80.0})
    assert full_y[0] == pytest.approx(0.0)
    assert full_y[-1] == pytest.approx(1.0)
    assert all(full_y[i] <= full_y[i + 1] for i in range(len(full_y) - 1))
    assert all(full_x[i] <= full_x[i + 1] for i in range(len(full_x) - 1))


def test_cdf_eval_hits_quantile_anchors_exactly():
    quantiles = {10: 60.0, 25: 65.0, 50: 70.0, 75: 75.0, 90: 80.0}
    fx, fy = _quantile_cdf_anchors(quantiles)
    for pct, val in quantiles.items():
        assert _cdf_eval(fx, fy, val) == pytest.approx(pct / 100.0, abs=1e-9)


def test_cdf_tails_extrapolate_to_zero_and_one():
    # With q10=60 and q25=65 (slope=0.03 per °F), tail anchor for F=0 is at
    # 60 - 0.10 / 0.03 = 60 - 3.33 = 56.67. Below that, F(x) == 0.
    fx, fy = _quantile_cdf_anchors({10: 60.0, 25: 65.0, 50: 70.0, 75: 75.0, 90: 80.0})
    assert _cdf_eval(fx, fy, 50.0) == 0.0
    assert _cdf_eval(fx, fy, 100.0) == 1.0


def test_bin_probs_sum_equals_union_after_clip_renormalize():
    """Bin probs sum to `union` (=1 - outside_bin_mass) exactly; clip drift is rebalanced
    onto unpinned bins so the total is invariant. This is the property edge math relies on.
    """
    event = _make_event([65.0, 70.0, 75.0, 80.0, 85.0])
    forecast = _make_forecast({10: 60.0, 25: 65.0, 50: 70.0, 75: 75.0, 90: 80.0})
    out = evaluate_event_nbm(event, forecast)
    assert len(out.bin_probs) == 6
    # Bins partition R, so union == 1.0 and outside_bin_mass == 0.
    assert out.outside_bin_mass == pytest.approx(0.0, abs=1e-9)
    assert out.sum_of_bin_probs == pytest.approx(1.0, abs=1e-9)


def test_clipping_drift_is_absorbed_by_unpinned_bins():
    """Narrow forecast where 4/6 bins floor out: previously sum drifted to ~1.02; now the
    two unpinned bins absorb the excess so the total still equals union exactly."""
    event = _make_event([65.0, 70.0, 75.0, 80.0, 85.0])
    forecast = _make_forecast({10: 65.0, 25: 65.5, 50: 66.0, 75: 67.0, 90: 68.0})
    out = evaluate_event_nbm(event, forecast)
    probs = [bp.p for bp in out.bin_probs]
    assert sum(probs) == pytest.approx(1.0 - out.outside_bin_mass, abs=1e-9)
    # Pinned bins (those whose raw prob was below floor) stay exactly at floor.
    pinned = [p for p in probs if p <= 0.005 + 1e-9]
    assert len(pinned) >= 1
    for p in pinned:
        assert p == pytest.approx(0.005, abs=1e-9)


def test_narrow_forecast_concentrates_mass_on_one_bin():
    """LA-style ultra-narrow forecast (P10..P90 spans 4F) — most mass on one or two bins."""
    event = _make_event([65.0, 70.0, 75.0, 80.0, 85.0])
    forecast = _make_forecast({10: 65.0, 25: 65.5, 50: 66.0, 75: 67.0, 90: 68.0})
    out = evaluate_event_nbm(event, forecast)
    probs = {bp.bin.subtitle: bp.p for bp in out.bin_probs}
    # 'below 65' bin should hold most mass (open-low covers everything < 65)
    # and the [65,70) bin should hold the rest. Bins above 70 should be at the floor.
    assert probs["below 65.0"] > 0.05
    assert probs["[65.0,70.0)"] > 0.50  # the bulk of the (66-67F) forecast
    assert probs["[70.0,75.0)"] == pytest.approx(0.005, abs=1e-6)
    assert probs["[75.0,80.0)"] == pytest.approx(0.005, abs=1e-6)


def test_wide_forecast_spreads_mass_across_bins():
    """Chicago-style spring forecast: P10..P90 spans 14F — mass spread across bins."""
    event = _make_event([72.0, 76.0, 80.0, 84.0, 88.0])
    forecast = _make_forecast({10: 73.0, 25: 76.0, 50: 80.0, 75: 84.0, 90: 87.0})
    out = evaluate_event_nbm(event, forecast)
    probs = sorted([bp.p for bp in out.bin_probs], reverse=True)
    # Top three bins should each be > 10% — mass is spread, not concentrated.
    assert probs[0] > 0.15
    assert probs[1] > 0.15
    assert probs[2] > 0.15


def test_evaluate_event_nbm_model_name_carries_through():
    event = _make_event([65.0, 70.0, 75.0, 80.0, 85.0])
    forecast = _make_forecast({10: 60.0, 25: 65.0, 50: 70.0, 75: 75.0, 90: 80.0})
    out = evaluate_event_nbm(event, forecast)
    assert out.distribution.model == "nbm_qmd"
