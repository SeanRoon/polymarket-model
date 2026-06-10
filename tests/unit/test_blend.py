"""blend_bin_probs: convex per-bin combination of ECMWF and NBM probabilities."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from polymarket_model.model import blend_bin_probs


def _out(probs: dict[str, float]) -> SimpleNamespace:
    """Minimal stand-in for EventModelOutput — blend only reads bin_probs[*].bin.market_ticker / .p."""
    bps = [SimpleNamespace(bin=SimpleNamespace(market_ticker=t), p=p) for t, p in probs.items()]
    return SimpleNamespace(bin_probs=bps)


def test_convex_combination():
    out = blend_bin_probs(_out({"A": 0.2, "B": 0.8}), _out({"A": 0.4, "B": 0.6}), 0.5)
    assert out["A"] == pytest.approx(0.3)
    assert out["B"] == pytest.approx(0.7)


def test_weight_zero_is_pure_ecmwf():
    out = blend_bin_probs(_out({"A": 0.2}), _out({"A": 0.9}), 0.0)
    assert out["A"] == pytest.approx(0.2)


def test_weight_one_is_pure_nbm():
    out = blend_bin_probs(_out({"A": 0.2}), _out({"A": 0.9}), 1.0)
    assert out["A"] == pytest.approx(0.9)


def test_weight_is_clamped_to_unit_interval():
    assert blend_bin_probs(_out({"A": 0.2}), _out({"A": 0.9}), 5.0)["A"] == pytest.approx(0.9)
    assert blend_bin_probs(_out({"A": 0.2}), _out({"A": 0.9}), -1.0)["A"] == pytest.approx(0.2)


def test_falls_back_when_a_source_is_missing():
    e = _out({"A": 0.2})
    assert blend_bin_probs(e, None, 0.7)["A"] == pytest.approx(0.2)
    assert blend_bin_probs(None, e, 0.7)["A"] == pytest.approx(0.2)
    assert blend_bin_probs(None, None, 0.5) == {}


def test_bin_present_in_only_one_source_uses_that_source():
    out = blend_bin_probs(_out({"A": 0.2, "B": 0.8}), _out({"A": 0.4}), 0.5)
    assert out["A"] == pytest.approx(0.3)  # blended
    assert out["B"] == pytest.approx(0.8)  # NBM lacks B -> ECMWF value
