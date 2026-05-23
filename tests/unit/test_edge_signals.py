"""signals_for_event must respect min_edge, route BUY_YES vs BUY_NO correctly, and size Kelly safely."""
from __future__ import annotations

import math
from datetime import UTC, date, datetime

import numpy as np
import pytest

from polymarket_model.markets.discovery import Bin, WeatherEvent
from polymarket_model.markets.prices import BinPrice, EventPrices
from polymarket_model.model import PredictiveDistribution, evaluate_event
from polymarket_model.edge.signals import signals_for_event


def _make_event_with_prices(bin_specs, market_mids):
    bins = [
        Bin(
            bin_index=i,
            market_ticker=f"KXTEST-{i}",
            event_ticker="KXTEST",
            subtitle=label,
            floor_strike=None if open_lo else lo,
            cap_strike=None if open_hi else hi - 1,
            lo_f=lo,
            hi_f=hi,
            is_open_low=open_lo,
            is_open_high=open_hi,
        )
        for i, (label, lo, hi, open_lo, open_hi) in enumerate(bin_specs)
    ]
    event = WeatherEvent(
        event_ticker="KXTEST-26MAY09",
        series_ticker="KXTEST",
        title="t",
        city="Test",
        kind="high",
        station_id="KTEST",
        target_date_local=date(2026, 5, 9),
        close_time_utc=datetime(2026, 5, 10, 4, tzinfo=UTC),
        rules_primary=None,
        bins=bins,
    )
    now = datetime(2026, 5, 9, 0, tzinfo=UTC)
    prices = [
        BinPrice(
            bin=b, midpoint=mid, yes_bid=mid - 0.01, yes_ask=mid + 0.01,
            last_price=mid, volume=100.0, yes_bid_size=50.0, yes_ask_size=50.0,
            snapshot_ts_utc=now,
        )
        for b, mid in zip(bins, market_mids)
    ]
    ep = EventPrices(event=event, prices=prices, sum_of_mids=sum(market_mids), has_complete_mids=True)
    return event, ep


def test_signal_emits_buy_yes_when_model_above_market():
    bin_specs = [
        ("<50", -math.inf, 50.0, True, False),
        ("50-59", 50.0, 60.0, False, False),
        (">=60", 60.0, math.inf, False, True),
    ]
    market_mids = [0.10, 0.30, 0.60]
    event, prices = _make_event_with_prices(bin_specs, market_mids)
    samples = np.concatenate([np.full(10, 40.0), np.full(50, 55.0), np.full(40, 70.0)]).astype(float)
    dist = PredictiveDistribution(samples=samples, model="test")
    out = evaluate_event(event, dist, laplace_alpha=0.0)
    sigs = signals_for_event(out, prices, min_edge=0.10, kelly_multiplier=0.25,
                             now=datetime(2026, 5, 9, 0, tzinfo=UTC))
    by_label = {s.bin.subtitle: s for s in sigs}
    assert "50-59" in by_label
    s = by_label["50-59"]
    assert s.direction == "BUY_YES"
    assert s.entry_price == pytest.approx(0.30)
    assert s.model_p_yes == pytest.approx(0.50)
    assert s.kelly_sized == pytest.approx(0.25 * (0.50 - 0.30) / (1 - 0.30))


def test_signal_emits_buy_no_when_market_above_model():
    bin_specs = [
        ("<50", -math.inf, 50.0, True, False),
        ("50-59", 50.0, 60.0, False, False),
        (">=60", 60.0, math.inf, False, True),
    ]
    market_mids = [0.10, 0.70, 0.20]
    event, prices = _make_event_with_prices(bin_specs, market_mids)
    samples = np.concatenate([np.full(20, 40.0), np.full(30, 55.0), np.full(50, 70.0)]).astype(float)
    dist = PredictiveDistribution(samples=samples, model="test")
    out = evaluate_event(event, dist, laplace_alpha=0.0)
    sigs = signals_for_event(out, prices, min_edge=0.10, kelly_multiplier=0.25,
                             now=datetime(2026, 5, 9, 0, tzinfo=UTC))
    by_label = {s.bin.subtitle: s for s in sigs}
    s = by_label["50-59"]
    assert s.direction == "BUY_NO"
    assert s.entry_price == pytest.approx(0.30)  # 1 - market YES
    expected = 0.25 * (0.70 - 0.30) / 0.70
    assert s.kelly_sized == pytest.approx(expected)


def test_min_edge_filters_below_threshold():
    bin_specs = [("a", -math.inf, 50.0, True, False), ("b", 50.0, math.inf, False, True)]
    market_mids = [0.50, 0.51]
    event, prices = _make_event_with_prices(bin_specs, market_mids)
    samples = np.array([45.0] * 50 + [55.0] * 50, dtype=float)
    dist = PredictiveDistribution(samples=samples, model="test")
    out = evaluate_event(event, dist, laplace_alpha=0.0)
    sigs = signals_for_event(out, prices, min_edge=0.05,
                             now=datetime(2026, 5, 9, 0, tzinfo=UTC))
    assert sigs == []


def test_excluded_station_emits_no_signals_even_with_strong_edge():
    """Stations in the exclude set are dropped entirely; passing an empty exclude set re-enables them."""
    bin_specs = [
        ("<50", -math.inf, 50.0, True, False),
        ("50-59", 50.0, 60.0, False, False),
        (">=60", 60.0, math.inf, False, True),
    ]
    market_mids = [0.10, 0.30, 0.60]
    event, prices = _make_event_with_prices(bin_specs, market_mids)
    # event.station_id is "KTEST" — override the exclude set to include it.
    samples = np.concatenate([np.full(10, 40.0), np.full(50, 55.0), np.full(40, 70.0)]).astype(float)
    dist = PredictiveDistribution(samples=samples, model="test")
    out = evaluate_event(event, dist, laplace_alpha=0.0)
    now = datetime(2026, 5, 9, 0, tzinfo=UTC)

    sigs_excluded = signals_for_event(
        out, prices, min_edge=0.10, kelly_multiplier=0.25, now=now,
        excluded_stations={"KTEST"},
    )
    assert sigs_excluded == []

    sigs_enabled = signals_for_event(
        out, prices, min_edge=0.10, kelly_multiplier=0.25, now=now,
        excluded_stations=set(),
    )
    assert len(sigs_enabled) >= 1
