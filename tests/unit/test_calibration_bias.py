"""Per-station bias correction: compute from synthetic data, apply shifts samples by exact amount,
round-trip Parquet, min_days filter, recorder integration with `_build_model_outputs`."""
from __future__ import annotations

import math
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from polymarket_model.calibration.bias import (
    BIAS_PARQUET_SCHEMA,
    BiasEstimate,
    apply_bias_to_samples,
    compute_station_biases,
    load_biases,
    write_biases,
)
from polymarket_model.evaluation import RESOLUTIONS_SCHEMA


def _snap_schema() -> pa.Schema:
    return pa.schema([
        pa.field("snapshot_bucket_utc", pa.timestamp("us", tz="UTC")),
        pa.field("snapshot_ts_utc", pa.timestamp("us", tz="UTC")),
        pa.field("series_ticker", pa.string()),
        pa.field("event_ticker", pa.string()),
        pa.field("market_ticker", pa.string()),
        pa.field("city", pa.string()),
        pa.field("kind", pa.string()),
        pa.field("target_date_local", pa.date32()),
        pa.field("station_id", pa.string()),
        pa.field("bin_index", pa.int64()),
        pa.field("subtitle", pa.string()),
        pa.field("lo_f", pa.float64()),
        pa.field("hi_f", pa.float64()),
        pa.field("is_open_low", pa.bool_()),
        pa.field("is_open_high", pa.bool_()),
        pa.field("midpoint", pa.float64()),
        pa.field("model_p", pa.float64()),
    ])


def _six_bins_centered_at(center: float) -> list[dict]:
    """Six bins of 2°F width around `center`, plus open-low and open-high."""
    return [
        {"lo": -math.inf, "hi": center - 3, "open_low": True, "open_high": False, "p": 0.05},
        {"lo": center - 3, "hi": center - 1, "open_low": False, "open_high": False, "p": 0.20},
        {"lo": center - 1, "hi": center + 1, "open_low": False, "open_high": False, "p": 0.50},
        {"lo": center + 1, "hi": center + 3, "open_low": False, "open_high": False, "p": 0.20},
        {"lo": center + 3, "hi": center + 5, "open_low": False, "open_high": False, "p": 0.04},
        {"lo": center + 5, "hi": math.inf, "open_low": False, "open_high": True, "p": 0.01},
    ]


def _write_snapshots(
    root: Path,
    *,
    station_id: str,
    kind: str,
    days: list[date],
    predicted_center: float,
) -> Path:
    snapshots_root = root / "snapshots"
    snapshots_root.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    bucket = datetime(2026, 5, 23, 12, 0, tzinfo=UTC)
    for d in days:
        bins = _six_bins_centered_at(predicted_center)
        event_ticker = f"KX-{station_id}-{d.isoformat()}"
        for i, b in enumerate(bins):
            rows.append({
                "snapshot_bucket_utc": bucket,
                "snapshot_ts_utc": bucket,
                "series_ticker": f"KX{station_id}",
                "event_ticker": event_ticker,
                "market_ticker": f"{event_ticker}-B{i}",
                "city": station_id,
                "kind": kind,
                "target_date_local": d,
                "station_id": station_id,
                "bin_index": i,
                "subtitle": f"bin-{i}",
                "lo_f": None if b["open_low"] else b["lo"],
                "hi_f": None if b["open_high"] else b["hi"],
                "is_open_low": b["open_low"],
                "is_open_high": b["open_high"],
                "midpoint": 0.5,
                "model_p": b["p"],
            })
    out = snapshots_root / "test.parquet"
    pq.write_table(pa.Table.from_pylist(rows, schema=_snap_schema()), out)
    return snapshots_root


def _write_resolutions(root: Path, rows: list[dict]) -> Path:
    path = root / "resolutions.parquet"
    pq.write_table(pa.Table.from_pylist(rows, schema=RESOLUTIONS_SCHEMA), path)
    return path


# ---- compute_station_biases -------------------------------------------------

def test_compute_station_biases_matches_expected_mean_error(tmp_path):
    """Predicted center 70, actual values 77 every day → bias ≈ 70 - 77 = -7."""
    today = datetime.now(UTC).date()
    days = [today - timedelta(days=i) for i in range(5)]
    snaps = _write_snapshots(tmp_path, station_id="KMIA", kind="high", days=days, predicted_center=70.0)
    res = _write_resolutions(tmp_path, [
        {
            "station_id": "KMIA",
            "valid_date_local": d,
            "kind": "high",
            "value_f": 77.0,
            "source": "nws_cli",
            "fetched_at_utc": datetime.now(UTC),
            "raw_text": "x",
        }
        for d in days
    ])
    biases = compute_station_biases(
        snapshots_root=snaps,
        resolutions_parquet=res,
        window_days=7,
        min_days=3,
    )
    assert len(biases) == 1
    b = biases[0]
    assert b.station_id == "KMIA"
    assert b.kind == "high"
    # Prob-weighted center of the synthetic bins ≈ 69.94, not exactly 70, so the
    # computed bias is -7.06 rather than -7.0. Tolerance leaves room for that drift
    # without masking real bugs.
    assert b.bias_f == pytest.approx(-7.0, abs=0.1)
    assert b.n_days_used == 5


def test_min_days_filter_excludes_thin_stations(tmp_path):
    """Only 2 paired days → omitted from output when min_days=3."""
    today = datetime.now(UTC).date()
    days = [today - timedelta(days=i) for i in range(2)]
    snaps = _write_snapshots(tmp_path, station_id="KMIA", kind="high", days=days, predicted_center=70.0)
    res = _write_resolutions(tmp_path, [
        {
            "station_id": "KMIA",
            "valid_date_local": d,
            "kind": "high",
            "value_f": 75.0,
            "source": "nws_cli",
            "fetched_at_utc": datetime.now(UTC),
            "raw_text": "x",
        }
        for d in days
    ])
    biases = compute_station_biases(
        snapshots_root=snaps,
        resolutions_parquet=res,
        window_days=7,
        min_days=3,
    )
    assert biases == []


def test_window_days_filter_drops_old_pairs(tmp_path):
    """Days older than window_days are excluded from the mean."""
    today = datetime.now(UTC).date()
    # 4 recent days within window; 4 ancient days outside.
    recent = [today - timedelta(days=i) for i in range(4)]
    ancient = [today - timedelta(days=30 + i) for i in range(4)]
    snaps = _write_snapshots(
        tmp_path, station_id="KMIA", kind="high", days=recent + ancient, predicted_center=70.0,
    )
    res = _write_resolutions(tmp_path, [
        # Recent days: actual=77 → error=-7
        *[
            {
                "station_id": "KMIA", "valid_date_local": d, "kind": "high", "value_f": 77.0,
                "source": "nws_cli", "fetched_at_utc": datetime.now(UTC), "raw_text": "x",
            }
            for d in recent
        ],
        # Ancient days: actual=100 → error=-30 — must NOT influence the mean.
        *[
            {
                "station_id": "KMIA", "valid_date_local": d, "kind": "high", "value_f": 100.0,
                "source": "nws_cli", "fetched_at_utc": datetime.now(UTC), "raw_text": "x",
            }
            for d in ancient
        ],
    ])
    biases = compute_station_biases(
        snapshots_root=snaps, resolutions_parquet=res, window_days=7, min_days=3,
    )
    assert len(biases) == 1
    assert biases[0].bias_f == pytest.approx(-7.0, abs=0.1)


def test_compute_returns_empty_when_resolutions_missing(tmp_path):
    snaps = tmp_path / "snapshots"
    snaps.mkdir()
    missing = tmp_path / "nonexistent_resolutions.parquet"
    assert compute_station_biases(
        snapshots_root=snaps, resolutions_parquet=missing,
    ) == []


# ---- apply_bias_to_samples --------------------------------------------------

def test_apply_bias_subtracts_exact_amount():
    samples = np.array([70.0, 75.0, 80.0])
    out = apply_bias_to_samples(samples, -7.0)
    np.testing.assert_array_almost_equal(out, [77.0, 82.0, 87.0])


def test_apply_bias_zero_is_identity():
    samples = np.array([70.0, 75.0, 80.0])
    out = apply_bias_to_samples(samples, 0.0)
    np.testing.assert_array_almost_equal(out, samples)


def test_apply_bias_accepts_lists_and_returns_float64():
    out = apply_bias_to_samples([70, 75, 80], 5)
    assert out.dtype == np.float64
    np.testing.assert_array_almost_equal(out, [65.0, 70.0, 75.0])


# ---- write/load round trip --------------------------------------------------

def test_write_load_round_trip(tmp_path):
    path = tmp_path / "biases.parquet"
    biases = [
        BiasEstimate("KMIA", "high", -7.36, 13, 7),
        BiasEstimate("KLAX", "high", 3.46, 15, 7),
    ]
    write_biases(path, biases)
    loaded = load_biases(path)
    assert loaded[("KMIA", "high")] == pytest.approx(-7.36)
    assert loaded[("KLAX", "high")] == pytest.approx(3.46)


def test_load_returns_empty_dict_when_file_missing(tmp_path):
    assert load_biases(tmp_path / "nope.parquet") == {}


def test_written_parquet_matches_schema(tmp_path):
    path = tmp_path / "biases.parquet"
    write_biases(path, [BiasEstimate("KMIA", "high", -7.0, 5, 7)])
    tbl = pq.read_table(path)
    # All declared fields must be present (order may differ).
    for field in BIAS_PARQUET_SCHEMA:
        assert field.name in tbl.column_names


# ---- recorder integration ---------------------------------------------------

def test_build_model_outputs_applies_bias_when_present():
    """A bias of -7 should shift ensemble samples up by 7 before the CDF is built,
    which in turn changes the bin probabilities. Also: model_name gets +biascorr."""
    from polymarket_model.markets.discovery import Bin, WeatherEvent
    from polymarket_model.recorder import _build_model_outputs
    from polymarket_model.weather.openmeteo import EnsembleDailyExtreme

    bins = [
        Bin(bin_index=0, market_ticker="MKT-0", event_ticker="E", subtitle="<70",
            floor_strike=None, cap_strike=70.0, lo_f=-math.inf, hi_f=70.0,
            is_open_low=True, is_open_high=False),
        Bin(bin_index=1, market_ticker="MKT-1", event_ticker="E", subtitle=">=70",
            floor_strike=70.0, cap_strike=None, lo_f=70.0, hi_f=math.inf,
            is_open_low=False, is_open_high=True),
    ]
    event = WeatherEvent(
        event_ticker="E", series_ticker="S", title="t", city="Miami", kind="high",
        target_date_local=date(2026, 5, 23), station_id="KMIA",
        rules_primary=None, close_time_utc=datetime(2026, 5, 23, 22, tzinfo=UTC),
        bins=bins,
    )
    # All samples at 65 → uncorrected: 100% in <70 bin. With bias=-7, shifted to 72 → 100% in >=70.
    ex = EnsembleDailyExtreme(
        station_id="KMIA", target_date_local=date(2026, 5, 23), kind="high",
        unit="F", model="ecmwf_ifs025",
        fetched_at_utc=datetime(2026, 5, 23, 6, tzinfo=UTC),
        lead_hours=12,
        values=np.full(51, 65.0),
        member_ids=np.arange(51),
    )

    # No bias: most mass on <70.
    outputs, bias_applied = _build_model_outputs([event], {("KMIA", date(2026, 5, 23), "high"): ex})
    mo = outputs["E"]
    low_p = next(bp.p for bp in mo.bin_probs if bp.bin.is_open_low)
    assert low_p > 0.9
    assert bias_applied["E"] is None
    assert "+biascorr" not in mo.distribution.model

    # With bias=-7 (model runs 7F too cool), samples shift to 72 → mass moves to >=70.
    outputs2, bias_applied2 = _build_model_outputs(
        [event],
        {("KMIA", date(2026, 5, 23), "high"): ex},
        biases={("KMIA", "high"): -7.0},
    )
    mo2 = outputs2["E"]
    high_p = next(bp.p for bp in mo2.bin_probs if bp.bin.is_open_high)
    assert high_p > 0.9
    assert bias_applied2["E"] == pytest.approx(-7.0)
    assert "+biascorr" in mo2.distribution.model
