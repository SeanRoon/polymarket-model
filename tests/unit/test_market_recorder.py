"""Price-only market feed: field decoding (_dollars/_fp), category + modeled-series
filtering, price-bearing filter, midpoint, and the Parquet schema round-trip. Offline —
the venue fetch is production network code; these drive synthetic event dicts."""
from __future__ import annotations

from datetime import UTC, datetime

import pyarrow.parquet as pq
import pytest

from polymarket_model.markets.market_recorder import (
    MARKET_SNAPSHOT_SCHEMA,
    build_market_rows,
    collect_market_snapshot_once,
)

BUCKET = datetime(2026, 7, 17, 23, 40, tzinfo=UTC)


def _market(ticker, **over):
    m = {
        "ticker": ticker,
        "status": "open",
        "yes_sub_title": "Above 1 inch",
        "strike_type": "greater",
        "floor_strike": 1,
        "cap_strike": None,
        "yes_bid_dollars": "0.40",
        "yes_ask_dollars": "0.45",
        "last_price_dollars": "0.42",
        "yes_bid_size_fp": "12",
        "yes_ask_size_fp": "8",
        "volume_fp": "100",
        "volume_24h_fp": "30",
        "open_interest_fp": "50",
        "liquidity_fp": "5",
        "close_time": "2026-08-01T03:59:59Z",
    }
    m.update(over)
    return m


def _event(series, category="Climate and Weather", markets=None):
    return {
        "series_ticker": series,
        "event_ticker": f"{series}-26JUL",
        "category": category,
        "title": f"{series} title",
        "markets": markets if markets is not None else [_market(f"{series}-26JUL-1")],
    }


def test_flatten_decodes_prices_and_computes_midpoint():
    rows = build_market_rows(
        [_event("KXRAINNYCM")], bucket=BUCKET, started=BUCKET,
        category="Climate and Weather", exclude_series=frozenset(),
    )
    assert len(rows) == 1
    r = rows[0]
    assert r["series_ticker"] == "KXRAINNYCM"
    assert r["yes_bid"] == 0.40 and r["yes_ask"] == 0.45
    assert r["midpoint"] == pytest.approx(0.425)
    assert r["last_price"] == 0.42
    assert r["yes_bid_size"] == 12 and r["yes_ask_size"] == 8
    assert r["volume"] == 100 and r["volume_24h"] == 30 and r["open_interest"] == 50
    assert r["floor_strike"] == 1.0 and r["cap_strike"] is None
    assert r["market_title"] == "Above 1 inch"
    assert r["close_time_utc"] == datetime(2026, 8, 1, 3, 59, 59, tzinfo=UTC)


def test_cents_int_fallback_when_no_dollars_key():
    m = _market("KXAQICITY-1")
    for k in ("yes_bid_dollars", "yes_ask_dollars", "last_price_dollars"):
        del m[k]
    m["yes_bid"] = 41  # integer cents
    m["yes_ask"] = 47
    rows = build_market_rows(
        [_event("KXAQICITY", markets=[m])], bucket=BUCKET, started=BUCKET,
        category=None, exclude_series=frozenset(),
    )
    assert rows[0]["yes_bid"] == 0.41 and rows[0]["yes_ask"] == 0.47


def test_excludes_modeled_series():
    # KXHIGHNY is a modeled temperature series — must be dropped when excluded.
    evs = [_event("KXHIGHNY"), _event("KXRAINNYCM")]
    rows = build_market_rows(
        evs, bucket=BUCKET, started=BUCKET,
        category="Climate and Weather", exclude_series=frozenset({"KXHIGHNY"}),
    )
    assert {r["series_ticker"] for r in rows} == {"KXRAINNYCM"}


def test_category_filter_substring_case_insensitive():
    evs = [_event("KXRAINNYCM", category="Climate and Weather"),
           _event("KXNBAGAME", category="Sports")]
    rows = build_market_rows(
        evs, bucket=BUCKET, started=BUCKET,
        category="climate", exclude_series=frozenset(),
    )
    assert {r["series_ticker"] for r in rows} == {"KXRAINNYCM"}
    # None category keeps everything.
    rows_all = build_market_rows(
        evs, bucket=BUCKET, started=BUCKET, category=None, exclude_series=frozenset(),
    )
    assert len(rows_all) == 2


def test_skips_markets_with_no_price_signal_and_non_open():
    quoted = _market("KXRAINNYCM-26JUL-1")
    empty = _market("KXRAINNYCM-26JUL-2", yes_bid_dollars="", yes_ask_dollars="",
                    last_price_dollars="")
    for k in ("yes_bid", "yes_ask", "last_price"):
        empty.pop(k, None)
    settled = _market("KXRAINNYCM-26JUL-3", status="settled")
    rows = build_market_rows(
        [_event("KXRAINNYCM", markets=[quoted, empty, settled])],
        bucket=BUCKET, started=BUCKET, category=None, exclude_series=frozenset(),
    )
    assert [r["market_ticker"] for r in rows] == ["KXRAINNYCM-26JUL-1"]


def test_series_falls_back_to_ticker_prefix_when_missing():
    ev = _event("KXTORNADO")
    del ev["series_ticker"]
    rows = build_market_rows(
        [ev], bucket=BUCKET, started=BUCKET, category=None, exclude_series=frozenset(),
    )
    assert rows[0]["series_ticker"] == "KXTORNADO"


class _FakeClient:
    def __init__(self, events):
        self._events = events

    def list_all_open_events(self):
        return self._events


def test_collect_once_writes_parquet_matching_schema(tmp_path):
    client = _FakeClient([_event("KXRAINNYCM"), _event("KXHURRICANE")])
    result = collect_market_snapshot_once(
        parquet_dir=tmp_path, now=BUCKET, category="Climate and Weather",
        exclude_series=frozenset(), client=client,
    )
    assert result.rows_written == 2
    assert result.parquet_path is not None and result.parquet_path.exists()
    tbl = pq.read_table(result.parquet_path)
    assert tbl.schema.equals(MARKET_SNAPSHOT_SCHEMA)
    assert tbl.num_rows == 2


def test_collect_once_no_rows_writes_nothing(tmp_path):
    client = _FakeClient([_event("KXNBAGAME", category="Sports")])
    result = collect_market_snapshot_once(
        parquet_dir=tmp_path, now=BUCKET, category="Climate and Weather",
        exclude_series=frozenset(), client=client,
    )
    assert result.rows_written == 0
    assert result.parquet_path is None
