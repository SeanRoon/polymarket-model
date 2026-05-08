"""NWS CLI parser: feed a known fixture and confirm date/MAX/MIN extraction."""
from __future__ import annotations

from datetime import date

from polymarket_model.weather.nws import (
    _parse_header_date,
    _parse_temp,
    _MAX_RE,
    _MIN_RE,
)


SAMPLE = """
802
CDUS41 KOKX 072042
CLILGA

CLIMATE REPORT
NATIONAL WEATHER SERVICE NEW YORK, NY
442 PM EDT THU MAY 07 2026

...................................

...THE LAGUARDIA NY CLIMATE SUMMARY FOR MAY 7 2026...
VALID TODAY AS OF 0400 PM LOCAL TIME.

CLIMATE NORMAL PERIOD 1991 TO 2020
CLIMATE RECORD PERIOD 1939 TO 2026


WEATHER ITEM   OBSERVED TIME   RECORD YEAR NORMAL DEPARTURE LAST
                VALUE   (LST)  VALUE       VALUE  FROM      YEAR
                                                  NORMAL
...................................................................
TEMPERATURE (F)
 TODAY
  MAXIMUM         64    259 PM  93    2000  69     -5       76
  MINIMUM         51    658 AM  40    1970  53     -2       58
  AVERAGE         58                        61     -3       67

PRECIPITATION (IN)
  TODAY            0.12          1.11 1967   0.11   0.01      T
"""


def test_parse_header_date():
    assert _parse_header_date(SAMPLE) == date(2026, 5, 7)


def test_parse_max_min():
    assert _parse_temp(SAMPLE, _MAX_RE) == 64.0
    assert _parse_temp(SAMPLE, _MIN_RE) == 51.0


SAMPLE_MISSING = """
...THE TEST CLIMATE SUMMARY FOR MAY 7 2026...

TEMPERATURE (F)
 TODAY
  MAXIMUM         MM
  MINIMUM         MM
  AVERAGE         MM

PRECIPITATION (IN)
"""


def test_parse_missing_returns_none():
    assert _parse_temp(SAMPLE_MISSING, _MAX_RE) is None
    assert _parse_temp(SAMPLE_MISSING, _MIN_RE) is None
