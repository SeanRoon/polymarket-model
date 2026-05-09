"""LST-aware daily-window cutoff — Kalshi settles on Local Standard Time (no DST shift)."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

import numpy as np

from polymarket_model.weather.openmeteo import lst_day_window_utc, standard_offset


def test_standard_offset_is_winter_offset():
    # NY: standard offset = UTC-5 even in summer.
    assert standard_offset("America/New_York") == timedelta(hours=-5)
    # Chicago: UTC-6.
    assert standard_offset("America/Chicago") == timedelta(hours=-6)
    # Phoenix: UTC-7 year-round (Arizona doesn't observe DST, but our function still finds Jan offset).
    assert standard_offset("America/Phoenix") == timedelta(hours=-7)


def test_lst_window_for_dst_date_uses_winter_offset():
    # May 9, 2026 falls during EDT (DST). Kalshi still settles on EST window.
    start, end = lst_day_window_utc(date(2026, 5, 9), "America/New_York")
    # EST midnight on May 9 = 05:00 UTC on May 9.
    assert start == datetime(2026, 5, 9, 5, 0, tzinfo=UTC)
    assert end == datetime(2026, 5, 10, 5, 0, tzinfo=UTC)


def test_lst_window_for_winter_date():
    # February: DST off, so LST and local clock agree. Same UTC bounds either way.
    start, end = lst_day_window_utc(date(2026, 2, 15), "America/New_York")
    assert start == datetime(2026, 2, 15, 5, 0, tzinfo=UTC)
    assert end == datetime(2026, 2, 16, 5, 0, tzinfo=UTC)


def test_lst_max_over_synthetic_hours_includes_correct_window():
    """Synthetic 48h hourly UTC series; verify the LST window picks the right slice for May 9."""
    # 48 hours starting 2026-05-08 00:00 UTC. Set the May 9 LST window's noon-EST hour
    # (UTC = May 9 17:00 = index 41) to a peak; everything else cooler.
    times_utc = [datetime(2026, 5, 8, 0, tzinfo=UTC) + timedelta(hours=h) for h in range(48)]
    values = np.full(48, 60.0)
    values[41] = 95.0  # peak during May 9 LST day
    values[4] = 100.0  # peak during May 8 LST day; should NOT be picked for May 9

    start, end = lst_day_window_utc(date(2026, 5, 9), "America/New_York")
    mask = np.array([start <= t < end for t in times_utc])
    assert values[mask].max() == 95.0  # NOT 100, because hour 4 is in May 8's LST window
