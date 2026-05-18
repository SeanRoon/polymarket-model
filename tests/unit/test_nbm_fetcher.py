"""Unit tests for nbm.py fetcher logic — cycle selection, peak-hour mapping, idx parsing.

No network: all tests operate on synthetic data or invoke pure functions.
"""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

import pytest

from polymarket_model.weather.nbm import (
    DEFAULT_PERCENTILES,
    PEAK_HOUR_OFFSET_HIGH,
    PEAK_HOUR_OFFSET_LOW,
    QMD_UPLOAD_LAG_HOURS,
    _aws_qmd_url,
    _enforce_monotonic,
    _parse_idx,
    _peak_hour_target_utc,
    _pick_cycle,
    _select_tmp_percentile_rows,
)
from polymarket_model.weather.stations import get_station


def test_peak_hour_east_coast_high_uses_lst_4pm():
    # KNYC LST = EST = UTC-5. 4pm LST = 21Z.
    station = get_station("KNYC")
    got = _peak_hour_target_utc(station, date(2026, 5, 18), "high")
    assert got == datetime(2026, 5, 18, 21, 0, tzinfo=UTC)


def test_peak_hour_pacific_high_uses_lst_4pm_pst():
    # KLAX LST = PST = UTC-8. 4pm PST = 00Z next day.
    station = get_station("KLAX")
    got = _peak_hour_target_utc(station, date(2026, 5, 18), "high")
    assert got == datetime(2026, 5, 19, 0, 0, tzinfo=UTC)


def test_peak_hour_low_uses_lst_5am():
    # KNYC: 5am EST = 10Z.
    station = get_station("KNYC")
    got = _peak_hour_target_utc(station, date(2026, 5, 18), "low")
    assert got == datetime(2026, 5, 18, 10, 0, tzinfo=UTC)


def test_peak_hour_constants_consistent():
    """High at +16h (4pm LST), low at +5h (5am LST). Document expectation in code."""
    assert PEAK_HOUR_OFFSET_HIGH == 16
    assert PEAK_HOUR_OFFSET_LOW == 5


def test_pick_cycle_uses_freshest_6hourly_cycle():
    # now = May 18 21:00Z. Lag back QMD_UPLOAD_LAG_HOURS (9h) -> 12Z. Round to 6h: 12Z.
    # target = May 19 21:00Z -> lead = (May 19 21 - May 18 12) = 33h.
    now = datetime(2026, 5, 18, 21, 0, tzinfo=UTC)
    target = datetime(2026, 5, 19, 21, 0, tzinfo=UTC)
    cycle, lead = _pick_cycle(now, target)
    assert cycle == datetime(2026, 5, 18, 12, 0, tzinfo=UTC)
    assert lead == 33


def test_pick_cycle_walks_back_when_target_in_past_relative_to_natural_cycle():
    # now = May 18 21:00Z natural cycle = 12Z. Ask for target = May 18 06:00Z (past relative
    # to that cycle). _pick_cycle should raise — predicting the past is not a real use case.
    now = datetime(2026, 5, 18, 21, 0, tzinfo=UTC)
    target = datetime(2026, 5, 18, 6, 0, tzinfo=UTC)
    with pytest.raises(ValueError, match="predates"):
        _pick_cycle(now, target)


def test_pick_cycle_walks_back_when_lead_too_far():
    # Target very far in the future > MAX_LEAD_HOURS. Should still raise eventually.
    now = datetime(2026, 5, 18, 21, 0, tzinfo=UTC)
    target = datetime(2027, 5, 18, 21, 0, tzinfo=UTC)  # ~1 year out
    with pytest.raises(ValueError):
        _pick_cycle(now, target)


def test_pick_cycle_respects_upload_lag():
    """A target that requires a cycle younger than QMD_UPLOAD_LAG_HOURS old should walk back."""
    # At now=12:00Z, the natural cycle = (now - lag).round_to_6h = 00Z today (or earlier).
    # Verify the picked cycle is at least lag hours old.
    now = datetime(2026, 5, 18, 12, 0, tzinfo=UTC)
    target = datetime(2026, 5, 19, 21, 0, tzinfo=UTC)
    cycle, _ = _pick_cycle(now, target)
    assert (now - cycle).total_seconds() / 3600 >= QMD_UPLOAD_LAG_HOURS


def test_aws_qmd_url_format():
    cycle = datetime(2026, 5, 17, 12, 0, tzinfo=UTC)
    url = _aws_qmd_url(cycle, fxx=36, region="co")
    assert url == (
        "https://noaa-nbm-grib2-pds.s3.amazonaws.com/"
        "blend.20260517/12/qmd/blend.t12z.qmd.f036.co.grib2"
    )


def test_parse_idx_extracts_offsets_and_computes_end_bytes():
    idx_text = (
        "1:0:d=2026051712:ABC:foo:0 hour fcst\n"
        "2:1000:d=2026051712:DEF:bar:0 hour fcst\n"
        "3:2500:d=2026051712:GHI:baz:0 hour fcst\n"
    )
    rows = _parse_idx(idx_text)
    assert len(rows) == 3
    assert rows[0]["start_byte"] == 0
    assert rows[0]["end_byte"] == 999
    assert rows[1]["start_byte"] == 1000
    assert rows[1]["end_byte"] == 2499
    assert rows[2]["start_byte"] == 2500
    assert rows[2]["end_byte"] is None  # last row has unbounded tail


def test_select_tmp_percentile_rows_picks_requested_levels():
    # Real wgrib2-style .idx line shape (trailing fields ARE NOT colon-terminated).
    lines = [
        "1:0:d=2026051712:OTHER:2 m above ground:36 hour fcst:0% level",
        "2:100:d=2026051712:TMP:2 m above ground:36 hour fcst:10% level",
        "3:200:d=2026051712:TMP:2 m above ground:36 hour fcst:25% level",
        "4:300:d=2026051712:TMP:2 m above ground:36 hour fcst:50% level",
        "5:400:d=2026051712:TMP:2 m above ground:36 hour fcst:75% level",
        "6:500:d=2026051712:TMP:2 m above ground:36 hour fcst:90% level",
        "7:600:d=2026051712:TMP:2 m above ground:36 hour fcst:95% level",
    ]
    rows = _parse_idx("\n".join(lines) + "\n")
    selected = _select_tmp_percentile_rows(rows, (10, 25, 50, 75, 90))
    assert [r["msg"] for r in selected] == [2, 3, 4, 5, 6]
    # Ordering reflects the requested percentiles, not idx-file order.
    selected_reverse = _select_tmp_percentile_rows(rows, (90, 75, 50, 25, 10))
    assert [r["msg"] for r in selected_reverse] == [6, 5, 4, 3, 2]


def test_select_tmp_percentile_rows_raises_on_missing_percentile():
    lines = [
        "1:0:d=2026051712:TMP:2 m above ground:36 hour fcst:10% level",
        "2:100:d=2026051712:TMP:2 m above ground:36 hour fcst:50% level",
    ]
    rows = _parse_idx("\n".join(lines) + "\n")
    with pytest.raises(RuntimeError, match="missing TMP percentile"):
        _select_tmp_percentile_rows(rows, (10, 25, 50))


def test_enforce_monotonic_keeps_sorted_inputs_unchanged():
    q = {10: 60.0, 25: 65.0, 50: 70.0, 75: 75.0, 90: 80.0}
    assert _enforce_monotonic(q) == q


def test_enforce_monotonic_repairs_inversions():
    # Adversarial: q25 < q10 (could in principle happen from independent nearest-grid lookups).
    q = {10: 60.0, 25: 58.0, 50: 70.0, 75: 75.0, 90: 80.0}
    fixed = _enforce_monotonic(q)
    assert fixed[10] == 60.0
    assert fixed[25] == 60.0  # bumped up to running max
    assert fixed[50] == 70.0


def test_default_percentiles_are_10_25_50_75_90():
    assert DEFAULT_PERCENTILES == (10, 25, 50, 75, 90)
