"""Agent paper-ledger: guards, pricing, settlement, bankroll — all offline."""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from polymarket_model.agent.ledger import (
    MAX_COST_PER_TRADE,
    MAX_OPEN_POSITIONS,
    STARTING_BANKROLL,
    TradeRejectedError,
    apply_result,
    build_trade,
    cash_balance,
    kalshi_fee,
    load_trades,
    render_performance,
    write_trades,
)

NOW = datetime(2026, 7, 12, 15, 0, tzinfo=UTC)


def market(**overrides) -> dict:
    m = {
        "ticker": "KXTEST-26JUL13-B50",
        "event_ticker": "KXTEST-26JUL13",
        "category": "Economics",
        "title": "Test market",
        "status": "open",
        "yes_bid_dollars": "0.40",
        "yes_ask_dollars": "0.45",
        "volume_24h": 5000,
        "close_time": "2026-07-13T15:00:00Z",
    }
    m.update(overrides)
    return m


def open_trade(**overrides) -> dict:
    t = build_trade(
        market=market(),
        side="yes",
        count=10,
        thesis="test thesis",
        strategy_version="v1",
        existing=[],
        now_utc=NOW,
    )
    t.update(overrides)
    return t


class TestFee:
    def test_matches_kalshi_formula_rounded_up_to_cent(self):
        # 0.07 * 10 * 0.45 * 0.55 = 0.17325 -> ceil to 0.18
        assert kalshi_fee(10, 0.45) == 0.18

    def test_zero_outside_open_interval(self):
        assert kalshi_fee(10, 0.0) == 0.0
        assert kalshi_fee(10, 1.0) == 0.0


class TestBuildTrade:
    def test_yes_fills_at_ask_no_fills_at_one_minus_bid(self):
        yes = build_trade(market=market(), side="yes", count=1, thesis="t",
                          strategy_version="v1", existing=[], now_utc=NOW)
        no = build_trade(market=market(), side="no", count=1, thesis="t",
                         strategy_version="v1", existing=[], now_utc=NOW)
        assert yes["entry_price"] == pytest.approx(0.45)
        assert no["entry_price"] == pytest.approx(0.60)

    def test_cents_fallback_when_dollar_fields_missing(self):
        m = market(yes_bid_dollars=None, yes_ask_dollars=None, yes_bid=40, yes_ask=45)
        t = build_trade(market=m, side="yes", count=1, thesis="t",
                        strategy_version="v1", existing=[], now_utc=NOW)
        assert t["entry_price"] == pytest.approx(0.45)

    def test_cost_is_count_price_plus_fee(self):
        t = build_trade(market=market(), side="yes", count=10, thesis="t",
                        strategy_version="v1", existing=[], now_utc=NOW)
        assert t["cost"] == pytest.approx(10 * 0.45 + 0.18)

    def test_rejects_one_sided_book(self):
        with pytest.raises(TradeRejectedError, match="YES ask"):
            build_trade(market=market(yes_ask_dollars=None, yes_ask=None), side="yes",
                        count=1, thesis="t", strategy_version="v1", existing=[], now_utc=NOW)
        with pytest.raises(TradeRejectedError, match="YES bid"):
            build_trade(market=market(yes_bid_dollars="0.00", yes_bid=0), side="no",
                        count=1, thesis="t", strategy_version="v1", existing=[], now_utc=NOW)

    def test_rejects_cost_over_cap(self):
        with pytest.raises(TradeRejectedError, match="per-trade cap"):
            build_trade(market=market(), side="yes", count=120, thesis="t",
                        strategy_version="v1", existing=[], now_utc=NOW)
        assert MAX_COST_PER_TRADE < 120 * 0.45

    def test_rejects_duplicate_open_position_same_side_only(self):
        existing = [open_trade()]
        with pytest.raises(TradeRejectedError, match="already holding"):
            build_trade(market=market(), side="yes", count=1, thesis="t",
                        strategy_version="v1", existing=existing, now_utc=NOW)
        # opposite side is allowed
        build_trade(market=market(), side="no", count=1, thesis="t",
                    strategy_version="v1", existing=existing, now_utc=NOW)

    def test_rejects_when_position_cap_reached(self):
        existing = [
            open_trade(market_ticker=f"KXTEST-{i}") for i in range(MAX_OPEN_POSITIONS)
        ]
        with pytest.raises(TradeRejectedError, match="open-position cap"):
            build_trade(market=market(), side="yes", count=1, thesis="t",
                        strategy_version="v1", existing=existing, now_utc=NOW)

    def test_rejects_when_cash_exhausted(self):
        # 22 open trades at ~$45.18 each burn > $990 of the $1000 bankroll.
        existing = [
            open_trade(market_ticker=f"KXBIG-{i}", count=100,
                       cost=45.18) for i in range(22)
        ]
        assert cash_balance(existing) < 45.0
        with pytest.raises(TradeRejectedError, match="free cash"):
            build_trade(market=market(), side="yes", count=100, thesis="t",
                        strategy_version="v1", existing=existing, now_utc=NOW)

    def test_rejects_missing_thesis_or_version_or_closed_market(self):
        with pytest.raises(TradeRejectedError, match="thesis"):
            build_trade(market=market(), side="yes", count=1, thesis="  ",
                        strategy_version="v1", existing=[], now_utc=NOW)
        with pytest.raises(TradeRejectedError, match="strategy_version"):
            build_trade(market=market(), side="yes", count=1, thesis="t",
                        strategy_version="", existing=[], now_utc=NOW)
        with pytest.raises(TradeRejectedError, match="not open"):
            build_trade(market=market(status="closed"), side="yes", count=1, thesis="t",
                        strategy_version="v1", existing=[], now_utc=NOW)


class TestSettlement:
    def test_win_pays_dollar_per_contract(self):
        t = open_trade()
        assert apply_result(t, market(status="settled", result="yes"), NOW)
        assert t["status"] == "SETTLED"
        assert t["payoff"] == pytest.approx(10.0)
        assert t["pnl"] == pytest.approx(round(10.0 - t["cost"], 2))

    def test_loss_pays_zero(self):
        t = open_trade()
        assert apply_result(t, market(status="settled", result="no"), NOW)
        assert t["payoff"] == 0.0
        assert t["pnl"] == pytest.approx(-t["cost"])

    def test_unresolved_market_leaves_trade_open(self):
        t = open_trade()
        assert not apply_result(t, market(status="open", result=""), NOW)
        assert t["status"] == "OPEN"

    def test_void_refunds_cost(self):
        t = open_trade()
        assert apply_result(t, market(status="settled", result="void"), NOW)
        assert t["status"] == "VOID"
        assert t["pnl"] == 0.0
        assert cash_balance([t]) == pytest.approx(STARTING_BANKROLL)


class TestBankroll:
    def test_cash_flows_through_open_settle_void(self):
        t1 = open_trade(market_ticker="A")  # cost deducted
        t2 = open_trade(market_ticker="B")
        apply_result(t2, market(ticker="B", status="settled", result="yes"), NOW)
        expected = STARTING_BANKROLL - t1["cost"] - t2["cost"] + 10.0
        assert cash_balance([t1, t2]) == pytest.approx(expected)


class TestPersistenceAndReport:
    def test_roundtrip_and_report_renders(self, tmp_path):
        path = tmp_path / "agent_trades.parquet"
        t1 = open_trade(market_ticker="A")
        t2 = open_trade(market_ticker="B", strategy_version="v2")
        apply_result(t2, market(ticker="B", status="settled", result="yes"), NOW)
        write_trades([t1, t2], path)
        back = load_trades(path)
        assert {t["market_ticker"] for t in back} == {"A", "B"}
        md = render_performance(back, now_utc=NOW)
        assert "By strategy version" in md
        assert "v1" in md and "v2" in md
        assert "Open positions" in md
