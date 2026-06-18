"""Series-ticker -> station mapping must align with the resolutionSource station Kalshi cites."""
from __future__ import annotations

from polymarket_model.markets.discovery import WEATHER_SERIES
from polymarket_model.weather.nws import issuedby_from_station
from polymarket_model.weather.stations import _FALLBACK


def test_known_series_have_station_mapping():
    # Confirm every series has a city + kind + station_id triple.
    for series, (city, kind, station_id) in WEATHER_SERIES.items():
        assert isinstance(city, str) and city, f"empty city for {series}"
        assert kind in ("high", "low"), f"bad kind for {series}: {kind}"
        assert station_id.startswith("K") and len(station_id) == 4, f"bad ICAO for {series}: {station_id}"


def test_nyc_uses_central_park_not_laguardia():
    # Polymarket used KLGA (LaGuardia). Kalshi uses Central Park (KNYC).
    assert WEATHER_SERIES["KXHIGHNY"][2] == "KNYC"
    assert WEATHER_SERIES["KXLOWNY"][2] == "KNYC"


def test_chicago_uses_midway_not_ohare():
    # Polymarket used KORD (O'Hare). Kalshi uses Midway (KMDW).
    assert WEATHER_SERIES["KXHIGHCHI"][2] == "KMDW"
    assert WEATHER_SERIES["KXLOWTCHI"][2] == "KMDW"


def test_every_station_has_fallback_coords():
    # Open-Meteo needs lat/lon for every traded station, and get_station falls back
    # to _FALLBACK when the NWS lookup is down — so a new city can't ship without it.
    for series, (_city, _kind, station_id) in WEATHER_SERIES.items():
        assert station_id in _FALLBACK, f"{series} station {station_id} missing from _FALLBACK"


def test_new_city_stations_use_settlement_airport():
    # Kalshi settles these against a specific airport's CLI — verified against each
    # series' settlement_sources. Guard the non-obvious picks against regressions.
    assert WEATHER_SERIES["KXHIGHTDAL"][2] == "KDFW"   # DFW, not Love Field (KDAL)
    assert WEATHER_SERIES["KXHIGHTHOU"][2] == "KHOU"   # Hobby, not Intercontinental (KIAH)


def test_station_id_matches_cli_issuedby_convention():
    # The resolver derives the CLI office by stripping the leading K; that 3-letter
    # code must be what Kalshi's settlement office uses (checked live at add time).
    for series, (_city, _kind, station_id) in WEATHER_SERIES.items():
        office = issuedby_from_station(station_id)
        assert len(office) == 3 and office == station_id[1:], f"{series}: {station_id} -> {office}"
