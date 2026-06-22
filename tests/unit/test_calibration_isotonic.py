"""Isotonic recalibration: fit from synthetic overconfident data (SQL join + PAV),
min_samples filter, monotonic apply with clamping, per-event renormalization, Parquet
round-trip, and the empty/missing-file paths."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from polymarket_model.calibration.isotonic import (
    CALIBRATION_PARQUET_SCHEMA,
    CalibrationFit,
    apply_calibration,
    calibrate_bin_probs,
    fit_station_calibrations,
    load_calibrations,
    write_calibrations,
)
from polymarket_model.evaluation import RESOLUTIONS_SCHEMA


def _snap_schema() -> pa.Schema:
    return pa.schema([
        pa.field("snapshot_bucket_utc", pa.timestamp("us", tz="UTC")),
        pa.field("event_ticker", pa.string()),
        pa.field("market_ticker", pa.string()),
        pa.field("kind", pa.string()),
        pa.field("target_date_local", pa.date32()),
        pa.field("station_id", pa.string()),
        pa.field("lo_f", pa.float64()),
        pa.field("hi_f", pa.float64()),
        pa.field("is_open_low", pa.bool_()),
        pa.field("is_open_high", pa.bool_()),
        pa.field("model_p", pa.float64()),
    ])


def _write_overconfident(root: Path, *, station_id: str = "KLAX") -> tuple[Path, Path]:
    """Two-bin (open-low <70 / open-high >=70) events where the model is over-confident.

    30 days at p(high)=0.9 but only 0.6 actually clear 70; 30 days at p(high)=0.1 but 0.4
    clear it. Pooled across the two bins per event, the empirical frequency at p=0.9 is 0.6
    and at p=0.1 is 0.4 — so a correct isotonic map shrinks both extremes toward the middle.
    """
    snaps_root = root / "snapshots"
    snaps_root.mkdir(parents=True, exist_ok=True)
    today = datetime.now(UTC).date()
    bucket = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)
    snap_rows: list[dict] = []
    res_rows: list[dict] = []

    def add_day(day, p_high: float, high_wins: bool) -> None:
        value_f = 75.0 if high_wins else 65.0  # threshold is 70
        event = f"KX-{station_id}-{day.isoformat()}"
        for tag, lo, hi, open_low, open_high, p in (
            ("LO", None, 70.0, True, False, 1.0 - p_high),
            ("HI", 70.0, None, False, True, p_high),
        ):
            snap_rows.append({
                "snapshot_bucket_utc": bucket,
                "event_ticker": event,
                "market_ticker": f"{event}-{tag}",
                "kind": "high",
                "target_date_local": day,
                "station_id": station_id,
                "lo_f": lo,
                "hi_f": hi,
                "is_open_low": open_low,
                "is_open_high": open_high,
                "model_p": p,
            })
        res_rows.append({
            "station_id": station_id,
            "valid_date_local": day,
            "kind": "high",
            "value_f": value_f,
            "source": "nws_cli",
            "fetched_at_utc": datetime.now(UTC),
            "raw_text": "x",
        })

    # Group 1: p_high=0.9, 18/30 high wins -> empirical 0.6
    for i in range(30):
        add_day(today - timedelta(days=i + 1), 0.9, high_wins=(i < 18))
    # Group 2: p_high=0.1, 12/30 high wins -> empirical 0.4
    for i in range(30):
        add_day(today - timedelta(days=i + 31), 0.1, high_wins=(i < 12))

    snaps_path = snaps_root / "test.parquet"
    pq.write_table(pa.Table.from_pylist(snap_rows, schema=_snap_schema()), snaps_path)
    res_path = root / "resolutions.parquet"
    pq.write_table(pa.Table.from_pylist(res_rows, schema=RESOLUTIONS_SCHEMA), res_path)
    return snaps_root, res_path


# ---- fit_station_calibrations -----------------------------------------------

def test_fit_reduces_in_sample_brier_and_is_monotonic(tmp_path):
    snaps, res = _write_overconfident(tmp_path, station_id="KLAX")
    fits = fit_station_calibrations(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KLAX"}), days_back=90, min_samples=100,
    )
    assert len(fits) == 1
    f = fits[0]
    assert (f.station_id, f.kind) == ("KLAX", "high")
    assert f.n_samples == 120
    # Calibration must not hurt in-sample Brier, and here should clearly help.
    assert f.brier_after <= f.brier_before
    # The map shrinks the extremes: p=0.9 -> ~0.6, p=0.1 -> ~0.4.
    xt = np.array(f.x_thresholds)
    yt = np.array(f.y_thresholds)
    assert apply_calibration(0.9, xt, yt) == pytest.approx(0.6, abs=0.08)
    assert apply_calibration(0.1, xt, yt) == pytest.approx(0.4, abs=0.08)
    # Monotonic non-decreasing knots.
    assert np.all(np.diff(yt) >= -1e-9)


def test_fit_skips_station_below_min_samples(tmp_path):
    snaps, res = _write_overconfident(tmp_path, station_id="KLAX")
    fits = fit_station_calibrations(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KLAX"}), days_back=90, min_samples=1000,
    )
    assert fits == []


def test_fit_only_configured_stations(tmp_path):
    snaps, res = _write_overconfident(tmp_path, station_id="KLAX")
    fits = fit_station_calibrations(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KMIA"}), days_back=90, min_samples=100,
    )
    assert fits == []


def test_fit_returns_empty_when_resolutions_missing(tmp_path):
    snaps = tmp_path / "snapshots"
    snaps.mkdir()
    assert fit_station_calibrations(
        snapshots_root=snaps, resolutions_parquet=tmp_path / "nope.parquet",
        stations=frozenset({"KLAX"}),
    ) == []


# ---- apply_calibration ------------------------------------------------------

def test_apply_calibration_interpolates_and_clamps():
    x = np.array([0.2, 0.8])
    y = np.array([0.3, 0.7])
    # Midpoint interpolates linearly.
    assert apply_calibration(0.5, x, y) == pytest.approx(0.5)
    # Below/above the knot range clamps to the end knots (np.interp behavior).
    assert apply_calibration(0.0, x, y) == pytest.approx(0.3)
    assert apply_calibration(1.0, x, y) == pytest.approx(0.7)


def test_apply_calibration_floor_ceiling():
    x = np.array([0.0, 1.0])
    y = np.array([0.0, 1.0])
    assert apply_calibration(0.0, x, y) >= 1e-3
    assert apply_calibration(1.0, x, y) <= 1.0 - 1e-3


# ---- calibrate_bin_probs ----------------------------------------------------

def test_calibrate_bin_probs_renormalizes_to_original_sum():
    # Identity-ish map but renormalization must preserve the input total (0.95 union mass).
    x = np.array([0.0, 1.0])
    y = np.array([0.0, 1.0])
    bins = {"A": 0.5, "B": 0.3, "C": 0.15}  # sums to 0.95
    out = calibrate_bin_probs(bins, x, y)
    assert sum(out.values()) == pytest.approx(0.95, abs=1e-9)
    assert set(out) == {"A", "B", "C"}


def test_calibrate_bin_probs_empty_input():
    x = np.array([0.0, 1.0])
    y = np.array([0.0, 1.0])
    assert calibrate_bin_probs({}, x, y) == {}


# ---- write / load round trip ------------------------------------------------

def test_write_load_round_trip(tmp_path):
    path = tmp_path / "cal.parquet"
    fit = CalibrationFit(
        station_id="KLAX", kind="high",
        x_thresholds=(0.1, 0.5, 0.9), y_thresholds=(0.2, 0.5, 0.7),
        n_samples=120, brier_before=0.25, brier_after=0.21, days_back=60,
    )
    write_calibrations(path, [fit])
    loaded = load_calibrations(path)
    assert ("KLAX", "high") in loaded
    xs, ys = loaded[("KLAX", "high")]
    np.testing.assert_array_almost_equal(xs, [0.1, 0.5, 0.9])
    np.testing.assert_array_almost_equal(ys, [0.2, 0.5, 0.7])


def test_load_returns_empty_dict_when_missing(tmp_path):
    assert load_calibrations(tmp_path / "nope.parquet") == {}


def test_written_parquet_matches_schema(tmp_path):
    path = tmp_path / "cal.parquet"
    write_calibrations(path, [CalibrationFit("KLAX", "high", (0.1, 0.9), (0.2, 0.7), 120, 0.25, 0.21, 60)])
    tbl = pq.read_table(path)
    for field in CALIBRATION_PARQUET_SCHEMA:
        assert field.name in tbl.column_names


# ---- recorder integration ---------------------------------------------------

def _fake_bin(ticker: str, idx: int, *, open_low=False, open_high=False, lo=None, hi=None):
    return SimpleNamespace(
        market_ticker=ticker, bin_index=idx, subtitle=f"b{idx}",
        floor_strike=lo, cap_strike=hi, lo_f=lo, hi_f=hi,
        is_open_low=open_low, is_open_high=open_high,
    )


def _fake_event_prices(station_id: str, model_p: dict[str, float]):
    """Minimal EventPrices/EventModelOutput stand-ins for _build_snapshot_table."""
    tickers = list(model_p)
    bins = [
        _fake_bin(tickers[0], 0, open_low=True, hi=70.0),
        _fake_bin(tickers[1], 1, open_high=True, lo=70.0),
    ]
    event = SimpleNamespace(
        event_ticker=f"E-{station_id}", series_ticker="S", city=station_id, kind="high",
        target_date_local=date(2026, 6, 1), station_id=station_id,
        close_time_utc=datetime(2026, 6, 1, 22, tzinfo=UTC),
    )
    prices = [
        SimpleNamespace(
            bin=b, midpoint=0.5, yes_bid=0.49, yes_ask=0.51, last_price=0.5,
            volume=1.0, yes_bid_size=1.0, yes_ask_size=1.0,
        )
        for b in bins
    ]
    bin_probs = [SimpleNamespace(bin=b, p=model_p[b.market_ticker]) for b in bins]
    mo = SimpleNamespace(
        bin_probs=bin_probs, outside_bin_mass=0.0,
        distribution=SimpleNamespace(model="empirical_ecmwf_ifs025", n=51),
    )
    ep = SimpleNamespace(event=event, prices=prices)
    return ep, mo


def test_build_snapshot_table_records_calibrated_p_only_for_configured_cells():
    from polymarket_model.recorder import _build_snapshot_table

    ep_klax, mo_klax = _fake_event_prices("KLAX", {"KLAX-LO": 0.1, "KLAX-HI": 0.85})
    ep_kaus, mo_kaus = _fake_event_prices("KAUS", {"KAUS-LO": 0.3, "KAUS-HI": 0.65})

    # Isotonic map that pulls extremes toward the middle (shrink), only for KLAX/high.
    cal = {("KLAX", "high"): (np.array([0.1, 0.85]), np.array([0.3, 0.7]))}

    tbl = _build_snapshot_table(
        bucket=datetime(2026, 6, 1, 12, tzinfo=UTC),
        started=datetime(2026, 6, 1, 12, tzinfo=UTC),
        priced_events=[ep_klax, ep_kaus],
        model_outputs={"E-KLAX": mo_klax, "E-KAUS": mo_kaus},
        forecasts={("KLAX", date(2026, 6, 1), "high"): SimpleNamespace(lead_hours=10),
                   ("KAUS", date(2026, 6, 1), "high"): SimpleNamespace(lead_hours=10)},
        nbm_outputs={}, nbm_forecasts={},
        calibrations=cal,
    )
    df = tbl.to_pandas()
    klax = df[df["station_id"] == "KLAX"]
    kaus = df[df["station_id"] == "KAUS"]

    # KLAX rows: calibration applied, calibrated_p populated and renormalized to model sum.
    assert klax["calibration_applied"].all()
    assert klax["calibrated_p"].notna().all()
    assert klax["calibrated_p"].sum() == pytest.approx(klax["model_p"].sum(), abs=1e-9)
    # KAUS rows: no calibration — NULL calibrated_p, flag False.
    assert not kaus["calibration_applied"].any()
    assert kaus["calibrated_p"].isna().all()
