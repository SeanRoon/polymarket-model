"""realized_yes maps a NWS observed value into the bin's [lo, hi) outcome correctly."""
from __future__ import annotations

import pytest

from polymarket_model.evaluation import realized_yes


@pytest.mark.parametrize(
    ("value", "lo", "hi", "expected"),
    [
        # Closed bin [60, 62): {60, 61}.
        (60.0, 60.0, 62.0, 1),
        (61.0, 60.0, 62.0, 1),
        (62.0, 60.0, 62.0, 0),  # hi is exclusive
        (59.0, 60.0, 62.0, 0),
        # Open-low (-inf, 56): integers <=55.
        (50.0, None, 56.0, 1),
        (55.0, None, 56.0, 1),
        (56.0, None, 56.0, 0),  # boundary excluded
        # Open-high [70, +inf): integers >=70.
        (70.0, 70.0, None, 1),
        (200.0, 70.0, None, 1),
        (69.0, 70.0, None, 0),
        # Both open == always YES (not realistic for our markets, but should not crash)
        (50.0, None, None, 1),
    ],
)
def test_realized_yes_boundary(value, lo, hi, expected):
    assert realized_yes(value, lo, hi) == expected
