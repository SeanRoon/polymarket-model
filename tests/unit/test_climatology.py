"""Day-of-year climatology: smoothing, circular wrap, leap-day handling, Parquet
round-trip, and the lookup helper. Offline — the transform is tested on synthetic
series; the ERA5 fetch itself is production-only network code."""
from __future__ import annotations

import math
from datetime import date, timedelta

import numpy as np
import pytest

from polymarket_model.weather.climatology import (
    StationClimatology,
    climo_for,
    daily_series_to_doy_climatology,
    doy_of,
    load_climatology,
    write_climatology,
)


def _make_series(years: list[int], value_fn) -> tuple[list[date], list[float]]:
    dates: list[date] = []
    values: list[float] = []
    for y in years:
        d = date(y, 1, 1)
        while d.year == y:
            dates.append(d)
            values.append(value_fn(d))
            d += timedelta(days=1)
    return dates, values


def test_doy_of_leap_and_nonleap():
    assert doy_of(date(2023, 1, 1)) == 1
    assert doy_of(date(2023, 12, 31)) == 365
    assert doy_of(date(2024, 2, 29)) == 60
    assert doy_of(date(2024, 12, 31)) == 366


def test_constant_series_gives_constant_climatology():
    dates, values = _make_series([2020, 2021, 2022], lambda d: 70.0)
    climo, n_obs = daily_series_to_doy_climatology(dates, values, window_days=7)
    assert np.nanmax(np.abs(climo - 70.0)) < 1e-9
    # Every doy has observations (leap day covered by its window).
    assert (n_obs > 0).all()


def test_sinusoid_recovered_and_smoothing_attenuates_noise():
    # True seasonal cycle: 70 + 20*sin(2π(doy-100)/365). The ±7d window average of a
    # slow sinusoid is very close to the sinusoid itself.
    def truth(d: date) -> float:
        return 70.0 + 20.0 * math.sin(2.0 * math.pi * (doy_of(d) - 100) / 365.0)

    dates, values = _make_series([2018, 2019, 2020, 2021, 2022], truth)
    climo, _ = daily_series_to_doy_climatology(dates, values, window_days=7)
    for check_doy in (1, 100, 191, 300, 365):
        d = date(2019, 1, 1) + timedelta(days=check_doy - 1)
        assert climo[check_doy - 1] == pytest.approx(truth(d), abs=0.5)


def test_circular_wrap_at_year_boundary():
    # Series where December is 30°F and the rest of the year 70°F: the Jan 1 window
    # (±7d) reaches back into late December, so climo[0] must sit between the two.
    def step(d: date) -> float:
        return 30.0 if d.month == 12 else 70.0

    dates, values = _make_series([2020, 2021, 2022], step)
    climo, _ = daily_series_to_doy_climatology(dates, values, window_days=7)
    assert 30.0 < climo[0] < 70.0        # Jan 1 borrows December days across the wrap
    assert climo[181] == pytest.approx(70.0)  # mid-year unaffected
    assert climo[350] == pytest.approx(30.0)  # mid-December solidly winter


def test_write_load_round_trip_and_lookup(tmp_path):
    climo = np.full(366, np.nan)
    climo[:365] = np.linspace(40.0, 90.0, 365)
    sc = StationClimatology(
        station_id="KLAX", kind="high", climo_f=climo,
        n_obs=np.full(366, 300, dtype=int), years_back=20, source="era5_openmeteo",
    )
    path = tmp_path / "climo.parquet"
    write_climatology(path, [sc])
    loaded = load_climatology(path)
    assert ("KLAX", "high") in loaded
    # Lookup on a mid-year date matches the stored curve.
    d = date(2023, 7, 15)
    assert climo_for(loaded, "KLAX", "high", d) == pytest.approx(climo[doy_of(d) - 1])
    # doy 366 was NaN (skipped at write): lookup on a leap Dec 31 returns None.
    assert climo_for(loaded, "KLAX", "high", date(2024, 12, 31)) is None
    # Unknown station/kind -> None.
    assert climo_for(loaded, "KMIA", "high", d) is None
    assert climo_for(loaded, "KLAX", "low", d) is None
    assert climo_for(loaded, None, "high", d) is None


def test_load_returns_empty_when_missing(tmp_path):
    assert load_climatology(tmp_path / "nope.parquet") == {}


def test_write_merges_with_existing_stations(tmp_path):
    """A targeted refresh must preserve stations not in the batch and replace refetched ones."""
    def _sc(station: str, value: float) -> StationClimatology:
        return StationClimatology(
            station_id=station, kind="high", climo_f=np.full(366, value),
            n_obs=np.full(366, 300, dtype=int), years_back=20, source="era5_openmeteo",
        )

    path = tmp_path / "climo.parquet"
    write_climatology(path, [_sc("KLAX", 70.0), _sc("KMIA", 85.0)])
    # Refetch only KLAX with a new value: KMIA must survive, KLAX must update.
    write_climatology(path, [_sc("KLAX", 71.0)])
    loaded = load_climatology(path)
    d = date(2023, 7, 15)
    assert climo_for(loaded, "KLAX", "high", d) == pytest.approx(71.0)
    assert climo_for(loaded, "KMIA", "high", d) == pytest.approx(85.0)
