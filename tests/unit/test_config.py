"""signal_excluded_cells must parse env strings and pair iterables into normalized tuples."""
from __future__ import annotations

import pytest

from polymarket_model.config import DEFAULT_SIGNAL_EXCLUDED_CELLS, Settings


def test_default_excludes_chicago_high():
    s = Settings()
    assert ("KMDW", "high") in s.signal_excluded_cells
    assert s.signal_excluded_cells == DEFAULT_SIGNAL_EXCLUDED_CELLS


def test_parses_env_style_string():
    s = Settings(signal_excluded_cells="KMDW:high, KORD:LOW")
    assert s.signal_excluded_cells == frozenset({("KMDW", "high"), ("KORD", "low")})


def test_parses_pair_iterable():
    s = Settings(signal_excluded_cells=[("KMDW", "High"), ["KNYC", "low"]])
    assert s.signal_excluded_cells == frozenset({("KMDW", "high"), ("KNYC", "low")})


def test_empty_string_clears_default():
    assert Settings(signal_excluded_cells="").signal_excluded_cells == frozenset()


def test_malformed_string_raises():
    with pytest.raises(ValueError):
        Settings(signal_excluded_cells="KMDW")  # missing ':kind'


def test_blend_weights_default_only_on_proven_cells():
    s = Settings()
    assert s.nbm_blend_weight_for("KMDW", "high") == 0.5
    assert s.nbm_blend_weight_for("KNYC", "high") == 0.5
    # Unlisted cells fall back to the default (pure ECMWF).
    assert s.nbm_blend_weight_for("KMDW", "low") == 0.0
    assert s.nbm_blend_weight_for("KAUS", "high") == 0.0


def test_blend_weights_env_string_and_case_insensitive():
    s = Settings(nbm_blend_weights="KMDW:high:0.7, KNYC:HIGH:0.6")
    assert s.nbm_blend_weight_for("KMDW", "high") == 0.7
    assert s.nbm_blend_weight_for("KNYC", "high") == 0.6
    # kind lookup is case-insensitive.
    assert s.nbm_blend_weight_for("KMDW", "HIGH") == 0.7


def test_blend_weight_default_override():
    s = Settings(nbm_blend_weights="", nbm_blend_default_weight=0.25)
    assert s.nbm_blend_weight_for("KAUS", "high") == 0.25


def test_blend_weight_none_inputs_use_default():
    s = Settings()
    assert s.nbm_blend_weight_for(None, "high") == 0.0
    assert s.nbm_blend_weight_for("KMDW", None) == 0.0


def test_blend_weights_malformed_raises():
    with pytest.raises(ValueError):
        Settings(nbm_blend_weights="KMDW:high")  # missing ':weight'
