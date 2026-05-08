from __future__ import annotations

import pytest

from polymarket_model.markets.discovery import _extract_station_id


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("https://www.wunderground.com/history/daily/us/ny/new-york-city/KLGA", "KLGA"),
        ("Resolves against NOAA station KMIA on the resolution date.", "KMIA"),
        ("Resolves against KEWR https://example.com/some/path", "KEWR"),
        # NWS CLI URL with only the 3-letter issuedby has no K-prefixed ICAO; we don't try to map it.
        ("https://forecast.weather.gov/product.php?site=NWS&issuedby=LAX&product=CLI", None),
        ("https://example.com/no-station-here", None),
        (None, None),
        ("", None),
    ],
)
def test_extract_station_id(source, expected):
    assert _extract_station_id(source) == expected
