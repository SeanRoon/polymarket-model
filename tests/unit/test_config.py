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
