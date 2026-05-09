"""simulate_pnl replays signal logic + a fee deduction. Verify the four routing paths."""
from __future__ import annotations

import pytest

from polymarket_model.evaluation import EvaluationConfig, simulate_pnl


def cfg(min_edge=0.05, kelly=0.25, fee=0.02) -> EvaluationConfig:
    return EvaluationConfig(min_edge=min_edge, kelly_multiplier=kelly, fee=fee)


def test_below_min_edge_is_no_trade():
    pnl, direction, kelly = simulate_pnl(model_p=0.52, market_mid=0.50, realized=1, cfg=cfg())
    assert pnl == 0.0
    assert direction is None
    assert kelly == 0.0


def test_buy_yes_winning_trade():
    # model_p=0.70, market=0.50, fee=0.02 -> entry 0.52. Realized=1 -> payoff=1.
    # full Kelly = (0.70 - 0.52) / (1 - 0.52) = 0.375. Quarter Kelly = 0.09375.
    # PnL per dollar = 1 - 0.52 = 0.48. Scaled = 0.48 * 0.09375 = 0.045.
    pnl, direction, kelly = simulate_pnl(model_p=0.70, market_mid=0.50, realized=1, cfg=cfg())
    assert direction == "BUY_YES"
    assert kelly == pytest.approx(0.25 * (0.70 - 0.52) / (1 - 0.52))
    assert pnl == pytest.approx((1 - 0.52) * kelly)
    assert pnl > 0


def test_buy_yes_losing_trade():
    # Same setup but realized=0 -> payoff=0; PnL per dollar = -0.52.
    pnl, direction, kelly = simulate_pnl(model_p=0.70, market_mid=0.50, realized=0, cfg=cfg())
    assert direction == "BUY_YES"
    assert pnl == pytest.approx(-0.52 * kelly)
    assert pnl < 0


def test_buy_no_winning_trade():
    # model_p=0.20, market=0.50 -> edge=-0.30 -> BUY_NO.
    # entry = (1 - 0.50) + 0.02 = 0.52. realized=0 (NO won) -> payoff=1.
    # full Kelly = ((1 - 0.20) - 0.52) / (1 - 0.52) = 0.5833...
    pnl, direction, kelly = simulate_pnl(model_p=0.20, market_mid=0.50, realized=0, cfg=cfg())
    assert direction == "BUY_NO"
    assert kelly == pytest.approx(0.25 * ((1 - 0.20) - 0.52) / (1 - 0.52))
    assert pnl == pytest.approx((1 - 0.52) * kelly)
    assert pnl > 0


def test_buy_no_losing_trade():
    # Same setup but realized=1 -> NO loses -> payoff=0.
    pnl, direction, kelly = simulate_pnl(model_p=0.20, market_mid=0.50, realized=1, cfg=cfg())
    assert direction == "BUY_NO"
    assert pnl == pytest.approx(-0.52 * kelly)
    assert pnl < 0


def test_entry_at_or_above_one_skips_trade():
    # If market_mid is so high that fee pushes entry >=1, we can't take the trade.
    pnl, direction, kelly = simulate_pnl(model_p=0.999, market_mid=0.99, realized=1, cfg=cfg(min_edge=0.001, fee=0.02))
    assert direction is None
    assert pnl == 0.0
    assert kelly == 0.0
