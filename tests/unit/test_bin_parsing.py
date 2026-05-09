"""Bin interval parsing for Kalshi market shapes.

Kalshi market records come with floor_strike + cap_strike (numeric or None).
The interval -> [lo_f, hi_f) translation is in markets.discovery._interval_for_market.
"""
from __future__ import annotations

import math

import pytest

from polymarket_model.markets.discovery import _interval_for_market


def make(*, ticker: str, floor: float | None, cap: float | None) -> dict:
    return {"ticker": ticker, "floor_strike": floor, "cap_strike": cap}


@pytest.mark.parametrize(
    ("market", "expected"),
    [
        # Closed bins: B-prefix, both strikes set, inclusive both sides.
        # "61° to 62°" -> [61, 63).
        (make(ticker="KXHIGHNY-26MAY09-B61.5", floor=61, cap=62), (61.0, 63.0, False, False)),
        (make(ticker="KXHIGHNY-26MAY09-B65.5", floor=65, cap=66), (65.0, 67.0, False, False)),
        # Open-high T bin: "69° or above", floor=68, cap=None -> (68, +inf) integer ≥ 69 -> [69, +inf).
        (make(ticker="KXHIGHNY-26MAY09-T68", floor=68, cap=None), (69.0, math.inf, False, True)),
        # Open-low T bin: "60° or below", cap=61, floor=None -> ≤60 -> (-inf, 61).
        (make(ticker="KXHIGHNY-26MAY09-T61", floor=None, cap=61), (-math.inf, 61.0, True, False)),
        # Open-high single-digit / negative-strike defenses
        (make(ticker="KXLOWNY-26FEB11-T-5", floor=-5, cap=None), (-4.0, math.inf, False, True)),
    ],
)
def test_interval_for_market(market, expected):
    assert _interval_for_market(market) == expected


def test_interval_for_market_returns_none_when_both_strikes_missing():
    assert _interval_for_market({"ticker": "X", "floor_strike": None, "cap_strike": None}) is None
