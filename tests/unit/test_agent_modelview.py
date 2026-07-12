"""Agent model-view: edge listing, exclusion labeling, track record — offline."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from polymarket_model.agent.modelview import render_model_view

NOW = datetime(2026, 7, 12, 22, 0, tzinfo=UTC)


def snap_row(**overrides) -> dict:
    r = {
        "snapshot_ts_utc": NOW - timedelta(minutes=10),
        "market_ticker": "KXHIGHAUS-26JUL13-B91.5",
        "city": "Austin",
        "kind": "high",
        "station_id": "KAUS",
        "subtitle": "91-92",
        "midpoint": 0.30,
        "yes_bid": 0.28,
        "yes_ask": 0.32,
        "model_p": 0.45,
        "nbm_p": 0.42,
        "model_lead_hours": 20,
    }
    r.update(overrides)
    return r


class TestEdges:
    def test_lists_edge_above_threshold_sorted_by_magnitude(self):
        rows = [
            snap_row(market_ticker="A", model_p=0.45, midpoint=0.30),  # +0.15
            snap_row(market_ticker="B", model_p=0.36, midpoint=0.30),  # +0.06
            snap_row(market_ticker="C", model_p=0.32, midpoint=0.30),  # +0.02 dropped
        ]
        md = render_model_view(rows, {}, now_utc=NOW, min_edge=0.05)
        assert "| A |" in md and "| B |" in md and "| C |" not in md
        assert md.index("| A |") < md.index("| B |")

    def test_respects_lead_window_and_missing_model_p(self):
        rows = [
            snap_row(market_ticker="FAR", model_lead_hours=24 * 10),
            snap_row(market_ticker="NOMODEL", model_p=None),
            # Day-of bin: outcome partly observed, market knows better — excluded.
            snap_row(market_ticker="TODAYBIN", model_lead_hours=0),
        ]
        md = render_model_view(rows, {}, now_utc=NOW, min_edge=0.05)
        assert "FAR" not in md and "NOMODEL" not in md and "TODAYBIN" not in md
        md0 = render_model_view(rows, {}, now_utc=NOW, min_edge=0.05, min_lead_hours=0)
        assert "TODAYBIN" in md0

    def test_stale_snapshot_warns(self):
        rows = [snap_row(snapshot_ts_utc=NOW - timedelta(hours=3))]
        md = render_model_view(rows, {}, now_utc=NOW)
        assert "WARNING" in md and "stale" in md


class TestProductionStatus:
    def test_labels_live_and_excluded_cells(self):
        rows = [
            snap_row(),  # KAUS/high is live in production
            snap_row(market_ticker="KXHIGHCHI", city="Chicago", kind="high",
                     station_id="KMDW"),  # cell-excluded
            snap_row(market_ticker="KXHIGHLAX", city="Los Angeles", kind="high",
                     station_id="KLAX"),  # station-excluded
        ]
        md = render_model_view(rows, {}, now_utc=NOW, min_edge=0.05)
        assert "LIVE" in md
        assert "excluded (cell)" in md
        assert "excluded (station)" in md


class TestTrackRecord:
    def test_renders_per_cell_roi_and_win_rate(self):
        track = {
            ("Austin", "high"): {"n": 100, "wins": 89, "pnl_weighted": 2.7, "kelly_sum": 10.0},
            ("Chicago", "low"): {"n": 50, "wins": 20, "pnl_weighted": -1.0, "kelly_sum": 10.0},
        }
        md = render_model_view([snap_row()], track, now_utc=NOW)
        assert "| Austin | high | 100 | 89% | +27.0% |" in md
        assert "| Chicago | low | 50 | 40% | -10.0% |" in md
        # best ROI listed first
        assert md.index("| Austin | high") < md.index("| Chicago | low")
