"""Brier and log-loss correctness + boundary clipping."""
from __future__ import annotations

import math

import pytest

from polymarket_model.evaluation import brier, lead_bucket, log_loss


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
