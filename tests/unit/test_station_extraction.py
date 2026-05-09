"""Series-ticker -> station mapping must align with the resolutionSource station Kalshi cites."""
from __future__ import annotations

from polymarket_model.markets.discovery import WEATHER_SERIES


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
