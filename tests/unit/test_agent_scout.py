"""Agent scout: flattening, filtering, digest selection/rendering — all offline."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from polymarket_model.agent.scout import (
    filter_rows,
    flatten_events,
    render_digest,
    select_digest,
)

NOW = datetime(2026, 7, 12, 15, 0, tzinfo=UTC)


def event(category: str = "Economics", n_markets: int = 2, **market_overrides) -> dict:
    markets = []
    for i in range(n_markets):
        m = {
            "ticker": f"KX{category[:3].upper()}-{i}",
            "status": "open",
            "title": f"Market {i}",
            "yes_bid_dollars": "0.40",
            "yes_ask_dollars": "0.45",
            "last_price_dollars": "0.42",
            "volume_24h": 1000 * (i + 1),
            "open_interest": 500,
            "close_time": (NOW + timedelta(days=2)).isoformat(),
        }
        m.update(market_overrides)
        m["ticker"] = f"KX{category[:3].upper()}-{i}"
        markets.append(m)
    return {
        "event_ticker": f"KX{category[:3].upper()}EV",
        "category": category,
        "title": f"{category} event",
        "markets": markets,
    }


class TestFlatten:
    def test_one_row_per_open_market_with_event_context(self):
        rows = flatten_events([event(n_markets=3)])
        assert len(rows) == 3
        assert rows[0].category == "Economics"
        assert rows[0].event_title == "Economics event"

    def test_skips_non_open_markets(self):
        rows = flatten_events([event(n_markets=1, status="closed")])
        assert rows == []

    def test_prices_parse_from_cent_ints_too(self):
        rows = flatten_events([event(
            n_markets=1, yes_bid_dollars=None, yes_ask_dollars=None,
            yes_bid=40, yes_ask=45,
        )])
        assert rows[0].yes_bid == 0.40
        assert rows[0].yes_ask == 0.45


class TestFilter:
    def _rows(self, **overrides):
        return flatten_events([event(n_markets=1, **overrides)])

    def test_keeps_liquid_two_sided_near_close(self):
        kept = filter_rows(self._rows(), now_utc=NOW, max_close_days=10, min_volume_24h=500)
        assert len(kept) == 1

    def test_drops_one_sided_books(self):
        rows = self._rows(yes_bid_dollars="0.00", yes_bid=0)
        assert filter_rows(rows, now_utc=NOW, max_close_days=10, min_volume_24h=0) == []

    def test_drops_low_volume(self):
        assert filter_rows(self._rows(volume_24h=10), now_utc=NOW,
                           max_close_days=10, min_volume_24h=500) == []

    def test_drops_far_or_past_close(self):
        far = self._rows(close_time=(NOW + timedelta(days=30)).isoformat())
        past = self._rows(close_time=(NOW - timedelta(hours=1)).isoformat())
        assert filter_rows(far, now_utc=NOW, max_close_days=10, min_volume_24h=0) == []
        assert filter_rows(past, now_utc=NOW, max_close_days=10, min_volume_24h=0) == []

    def test_category_substring_filter(self):
        rows = self._rows()
        assert filter_rows(rows, now_utc=NOW, max_close_days=10,
                           min_volume_24h=0, category="econ") == rows
        assert filter_rows(rows, now_utc=NOW, max_close_days=10,
                           min_volume_24h=0, category="sports") == []


class TestDigest:
    def test_per_category_cap_prevents_one_vertical_dominating(self):
        rows = flatten_events([event("Sports", n_markets=10), event("Economics", n_markets=2)])
        picked = select_digest(rows, top=100, per_category=3)
        by_cat = {}
        for r in picked:
            by_cat[r.category] = by_cat.get(r.category, 0) + 1
        assert by_cat["Sports"] == 3
        assert by_cat["Economics"] == 2

    def test_render_groups_by_category_and_escapes_pipes(self):
        rows = flatten_events([event("Sports", n_markets=1, title="A | B")])
        md = render_digest(rows, now_utc=NOW)
        assert "## Sports" in md
        assert "A / B" in md
        assert "| ticker |" in md
