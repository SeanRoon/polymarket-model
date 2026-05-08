"""Daily-high cutoff: the local-day max must include all hours from 00:00 to 23:00 in the
station's timezone, regardless of how UTC hours straddle local midnight.

We don't call the real Open-Meteo here — we rebuild the same masking logic against synthetic
hourly data and confirm it picks the right window across a DST/timezone boundary.
"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import numpy as np


def _local_day_max(times_local_iso: list[str], values: np.ndarray, target_date_local: date, tz_name: str) -> float:
    tz = ZoneInfo(tz_name)
    parsed = [datetime.fromisoformat(t).replace(tzinfo=tz) for t in times_local_iso]
    start = datetime.combine(target_date_local, time(0, 0), tzinfo=tz)
    end = start + timedelta(days=1)
    mask = np.array([start <= t < end for t in parsed])
    return float(values[mask].max())


def test_local_day_max_in_eastern_time():
    # 48 hours of synthetic hourly temps for May 8 (PDT-side and EDT-side) in NY local time.
    base_date = date(2026, 5, 8)
    tz_name = "America/New_York"
    times = []
    values = []
    for h in range(48):
        t = datetime(2026, 5, 7, 0, 0) + timedelta(hours=h)
        times.append(t.isoformat(timespec="minutes"))
        values.append(50.0 + h)  # monotonic — peak at h=47 = May 9 00:00
    times_arr = np.asarray(values, dtype=float)
    # Max for May 8 must come from local hours 00..23 of May 8, indices 24..47 → values 74..97 → peak 97.
    assert _local_day_max(times, times_arr, base_date, tz_name) == 97.0


def test_local_day_max_excludes_neighbouring_day():
    # Peak at h=23 belongs to May 7; max for May 8 must NOT see it.
    tz_name = "America/Los_Angeles"
    times = []
    values = []
    for h in range(48):
        t = datetime(2026, 5, 7, 0, 0) + timedelta(hours=h)
        times.append(t.isoformat(timespec="minutes"))
        # spike at hour 23 of May 7
        values.append(100.0 if h == 23 else 60.0)
    arr = np.asarray(values, dtype=float)
    assert _local_day_max(times, arr, date(2026, 5, 8), tz_name) == 60.0
    assert _local_day_max(times, arr, date(2026, 5, 7), tz_name) == 100.0
