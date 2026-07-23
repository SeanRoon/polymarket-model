"""NWS CLI parser: feed a known fixture and confirm date/MAX/MIN extraction."""
from __future__ import annotations

from datetime import date

from polymarket_model.weather.nws import (
    _MAX_RE,
    _MIN_RE,
    _PRELIMINARY_RE,
    _parse_header_date,
    _parse_temp,
    fetch_cli_for_date,
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


# A mid-morning PRELIMINARY CLI: MAXIMUM so far is only the overnight max (78), the
# afternoon high hasn't happened. Real KEWX/KBOU shape that poisoned the live trio.
SAMPLE_PRELIMINARY = """
836
CDUS44 KEWX 211238
CLIAUS

CLIMATE REPORT
NATIONAL WEATHER SERVICE AUSTIN/SAN ANTONIO
738 AM CDT TUE JUL 21 2026

...THE AUSTIN BERGSTROM CLIMATE SUMMARY FOR JULY 21 2026...
VALID AS OF 0700 AM LOCAL TIME.

TEMPERATURE (F)
 TODAY
  MAXIMUM         78     12 AM
  MINIMUM         74    600 AM

PRECIPITATION (IN)
"""


def test_preliminary_regex_flags_am_not_pm():
    # AM cutoff => preliminary; the final report's PM cutoff (or no marker) => not.
    assert _PRELIMINARY_RE.search(SAMPLE_PRELIMINARY)
    assert not _PRELIMINARY_RE.search(SAMPLE)  # SAMPLE is "VALID TODAY AS OF 0400 PM"
    assert not _PRELIMINARY_RE.search(SAMPLE_MISSING)  # no VALID marker at all


def _obs_stub(monkeypatch, body: str) -> None:
    """Patch the network fetch so fetch_cli_for_station parses `body` at version 1."""
    from polymarket_model.weather import nws

    monkeypatch.setattr(nws, "_fetch_cli_text", lambda issuedby, version=1: f"<pre>{body}</pre>")


def test_fetch_for_date_skips_preliminary(monkeypatch):
    # Only a same-day preliminary exists for the target -> no final -> None (unresolved),
    # never the poisoned overnight max.
    _obs_stub(monkeypatch, SAMPLE_PRELIMINARY)
    assert fetch_cli_for_date("KAUS", date(2026, 7, 21)) is None


def test_fetch_for_date_accepts_final(monkeypatch):
    # A PM/complete report for the target is accepted with the real afternoon high.
    _obs_stub(monkeypatch, SAMPLE)  # LaGuardia MAY 7, "VALID TODAY AS OF 0400 PM", MAX 64
    obs = fetch_cli_for_date("KLGA", date(2026, 5, 7))
    assert obs is not None
    assert obs.is_preliminary is False
    assert obs.max_f == 64.0
