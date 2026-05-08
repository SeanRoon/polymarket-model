"""Bin label parsing: every label shape Polymarket has been observed to use."""
from __future__ import annotations

import math

import pytest

from polymarket_model.markets.discovery import _detect_unit, _parse_bin_label


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("55°F or below", (-math.inf, 56.0, True, False)),
        ("56-57°F", (56.0, 58.0, False, False)),
        ("60-61°F", (60.0, 62.0, False, False)),
        ("74°F or higher", (74.0, math.inf, False, True)),
        ("12°C or higher", (12.0, math.inf, False, True)),
        ("2°C or below", (-math.inf, 3.0, True, False)),
        ("6°C", (6.0, 7.0, False, False)),
        ("Will the highest temperature be between 64-65 on May 8?", (64.0, 66.0, False, False)),
    ],
)
def test_parse_bin_label(label, expected):
    assert _parse_bin_label(label) == expected


def test_parse_bin_label_returns_none_for_garbage():
    assert _parse_bin_label("hot") is None
    assert _parse_bin_label("") is None
    assert _parse_bin_label(None) is None


@pytest.mark.parametrize(
    ("label", "unit"),
    [
        ("55°F or below", "F"),
        ("56-57°F", "F"),
        ("12°C or higher", "C"),
        ("6°C", "C"),
        ("65", "F"),  # default when no unit present
    ],
)
def test_detect_unit(label, unit):
    assert _detect_unit(label) == unit
