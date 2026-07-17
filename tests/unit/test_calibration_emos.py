"""EMOS/NGR recalibration in anomaly space: fit from synthetic biased+overconfident
forecasts (SQL join + CRPS minimization), seasonal-trend invariance via the climatology
anchor, min_days/station guards, moment reconstruction, Gaussian bin-prob apply with
clip+renormalize, Parquet round-trip, live-city exclusion, and the recorder path."""
from __future__ import annotations

import math
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from polymarket_model.calibration.emos import (
    EMOS_PARQUET_SCHEMA,
    EmosCoefficients,
    EmosFit,
    apply_emos_to_event,
    fit_station_emos,
    load_emos,
    moments_from_bin_probs,
    write_emos,
)
from polymarket_model.config import DEFAULT_EMOS_STATIONS
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
        pa.field("model_bias_applied_f", pa.float64()),
    ])


def _norm_cdf(x: float, mu: float, sigma: float) -> float:
    return 0.5 * (1.0 + math.erf((x - mu) / (sigma * math.sqrt(2.0))))


def _gaussian_bins(m: float, sigma: float = 1.0) -> list[tuple[str, float | None, float | None, bool, bool, float]]:
    """Six Kalshi-style bins around forecast mean m with exact N(m, sigma) masses.

    Returns (tag, lo_f, hi_f, is_open_low, is_open_high, p) per bin.
    """
    out: list[tuple[str, float | None, float | None, bool, bool, float]] = [
        ("B0", None, m - 2.0, True, False, _norm_cdf(m - 2.0, m, sigma)),
    ]
    for i, (lo, hi) in enumerate([(m - 2, m - 1), (m - 1, m), (m, m + 1), (m + 1, m + 2)]):
        out.append((f"B{i+1}", lo, hi, False, False,
                    _norm_cdf(hi, m, sigma) - _norm_cdf(lo, m, sigma)))
    out.append(("B5", m + 2.0, None, False, True, 1.0 - _norm_cdf(m + 2.0, m, sigma)))
    return out


def _flat_climo(station_id: str = "KLAX", kind: str = "high", value: float = 70.0):
    return {(station_id, kind): np.full(366, value)}


def _write_biased_overconfident(
    root: Path, *, station_id: str = "KLAX", n_days: int = 45,
    mean_bias: float = 5.0, true_spread: float = 4.0, forecast_spread: float = 1.0,
    seasonal_trend_per_day: float = 0.0,
) -> tuple[Path, Path, dict]:
    """n_days of forecasts that run `mean_bias` °F warm with `forecast_spread` °F spread,
    against actuals that deviate ±`true_spread` °F: EMOS must learn to shift the mean
    down ~mean_bias and widen sigma toward true_spread.

    With `seasonal_trend_per_day` nonzero, the climate baseline drifts linearly across
    the window (a compressed seasonal transition) and the returned climatology dict
    tracks it — the anomaly-space fit must be unaffected by the trend.

    Returns (snapshots_root, resolutions_path, climatology_dict).
    """
    snaps_root = root / "snapshots"
    snaps_root.mkdir(parents=True, exist_ok=True)
    today = datetime.now(UTC).date()
    bucket = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)
    snap_rows: list[dict] = []
    res_rows: list[dict] = []
    climo_arr = np.full(366, np.nan)

    for i in range(n_days):
        day = today - timedelta(days=i + 1)
        baseline = 70.0 - seasonal_trend_per_day * (i + 1)   # older days = earlier season
        weather_anom = float((i % 21) - 10)                  # day-to-day variation for the regression
        true_temp = baseline + weather_anom
        climo_arr[day.timetuple().tm_yday - 1] = baseline
        actual = true_temp + (true_spread if i % 2 == 0 else -true_spread)
        forecast_mean = true_temp + mean_bias
        event = f"KX-{station_id}-{day.isoformat()}"
        for tag, lo, hi, open_low, open_high, p in _gaussian_bins(forecast_mean, forecast_spread):
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
                "model_bias_applied_f": None,
            })
        res_rows.append({
            "station_id": station_id,
            "valid_date_local": day,
            "kind": "high",
            "value_f": actual,
            "source": "nws_cli",
            "fetched_at_utc": datetime.now(UTC),
            "raw_text": "x",
        })

    snaps_path = snaps_root / "test.parquet"
    pq.write_table(pa.Table.from_pylist(snap_rows, schema=_snap_schema()), snaps_path)
    res_path = root / "resolutions.parquet"
    pq.write_table(pa.Table.from_pylist(res_rows, schema=RESOLUTIONS_SCHEMA), res_path)
    return snaps_root, res_path, {(station_id, "high"): climo_arr}


def _fake_bin_probs(m: float, sigma: float = 1.0) -> list[SimpleNamespace]:
    return [
        SimpleNamespace(
            bin=SimpleNamespace(
                market_ticker=tag, lo_f=lo, hi_f=hi,
                is_open_low=open_low, is_open_high=open_high,
            ),
            p=p,
        )
        for tag, lo, hi, open_low, open_high, p in _gaussian_bins(m, sigma)
    ]


# ---- fit_station_emos ---------------------------------------------------------

def test_fit_recovers_mean_bias_and_widens_spread(tmp_path):
    snaps, res, climo = _write_biased_overconfident(tmp_path, station_id="KLAX")
    fits = fit_station_emos(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KLAX"}), climatology=climo, days_back=90, min_days=30,
    )
    assert len(fits) == 1
    f = fits[0]
    assert (f.station_id, f.kind) == ("KLAX", "high")
    assert f.n_days == 45
    # The fit must beat the raw ensemble in-sample (guaranteed by the emit guard,
    # but assert the margin is real for this blatant miscalibration).
    assert f.crps_fit < f.crps_raw * 0.8

    co = f.coefficients
    # Mean correction, anomaly space: forecasts run +5°F warm, so a raw-mean anomaly of
    # +5 must map back to ~0 (i.e. mu = climo + a + b*5 ≈ climo).
    assert co.a + co.b * 5.0 == pytest.approx(0.0, abs=1.0)
    # Spread correction: reconstructed forecast std is ~1.4°F but actuals deviate ±4°F;
    # the fitted sigma must widen to the true error scale.
    recon_std = moments_from_bin_probs(_fake_bin_probs(75.0))[1]
    sigma = math.sqrt(co.c + co.d * recon_std**2)
    assert 3.0 <= sigma <= 5.5


def test_fit_is_invariant_to_a_seasonal_trend(tmp_path):
    """A strong linear climate drift across the window (compressed 'seasonal transition')
    must not contaminate the anomaly-space coefficients: same recovery as the flat case."""
    snaps, res, climo = _write_biased_overconfident(
        tmp_path, station_id="KLAX", seasonal_trend_per_day=0.5,   # 22.5°F drift over 45d
    )
    fits = fit_station_emos(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KLAX"}), climatology=climo, days_back=90, min_days=30,
    )
    assert len(fits) == 1
    co = fits[0].coefficients
    assert co.a + co.b * 5.0 == pytest.approx(0.0, abs=1.0)
    recon_std = moments_from_bin_probs(_fake_bin_probs(75.0))[1]
    sigma = math.sqrt(co.c + co.d * recon_std**2)
    assert 3.0 <= sigma <= 5.5


def test_fit_skips_cells_without_climatology(tmp_path):
    snaps, res, _ = _write_biased_overconfident(tmp_path, station_id="KLAX")
    fits = fit_station_emos(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KLAX"}), climatology={}, days_back=90, min_days=30,
    )
    assert fits == []


def test_fit_skips_below_min_days(tmp_path):
    snaps, res, climo = _write_biased_overconfident(tmp_path, station_id="KLAX")
    fits = fit_station_emos(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KLAX"}), climatology=climo, days_back=90, min_days=100,
    )
    assert fits == []


def test_fit_only_configured_stations(tmp_path):
    snaps, res, climo = _write_biased_overconfident(tmp_path, station_id="KLAX")
    fits = fit_station_emos(
        snapshots_root=snaps, resolutions_parquet=res,
        stations=frozenset({"KMIA"}), climatology=climo, days_back=90, min_days=30,
    )
    assert fits == []


def test_fit_returns_empty_when_resolutions_missing(tmp_path):
    snaps = tmp_path / "snapshots"
    snaps.mkdir()
    assert fit_station_emos(
        snapshots_root=snaps, resolutions_parquet=tmp_path / "nope.parquet",
        stations=frozenset({"KLAX"}), climatology=_flat_climo(),
    ) == []


# ---- moments_from_bin_probs ---------------------------------------------------

def test_moments_known_two_bin_case():
    # Open-low (<70, center 67) at p=0.25 and open-high (>=70, center 73) at p=0.75.
    bps = [
        SimpleNamespace(bin=SimpleNamespace(market_ticker="LO", lo_f=None, hi_f=70.0,
                                            is_open_low=True, is_open_high=False), p=0.25),
        SimpleNamespace(bin=SimpleNamespace(market_ticker="HI", lo_f=70.0, hi_f=None,
                                            is_open_low=False, is_open_high=True), p=0.75),
    ]
    mean, std = moments_from_bin_probs(bps)
    assert mean == pytest.approx(0.25 * 67 + 0.75 * 73)
    var = 0.25 * 67**2 + 0.75 * 73**2 - mean**2
    assert std == pytest.approx(math.sqrt(var))


def test_moments_degenerate_mass_returns_none():
    bps = [SimpleNamespace(bin=SimpleNamespace(market_ticker="LO", lo_f=None, hi_f=70.0,
                                               is_open_low=True, is_open_high=False), p=0.1)]
    assert moments_from_bin_probs(bps) is None


# ---- apply_emos_to_event ------------------------------------------------------

def test_apply_identity_coeffs_reproduce_gaussian_masses():
    bps = _fake_bin_probs(75.0, sigma=1.0)
    identity = EmosCoefficients(a=0.0, b=1.0, c=0.0, d=1.0)
    result = apply_emos_to_event(bps, identity, bias_applied_f=None, climo_f=70.0)
    assert result is not None
    bin_to_p, mu, sigma = result
    recon_mean, recon_std = moments_from_bin_probs(bps)
    # Identity coefficients make mu = climo + (raw - climo) = raw, whatever the climo.
    assert mu == pytest.approx(recon_mean)
    assert sigma == pytest.approx(recon_std)
    # Bins partition the real line, so the calibrated probs must keep total mass ~1.
    assert sum(bin_to_p.values()) == pytest.approx(1.0, abs=1e-6)
    assert set(bin_to_p) == {f"B{i}" for i in range(6)}
    # All within the clip bounds.
    for p in bin_to_p.values():
        assert 0.005 <= p <= 0.995


def test_apply_identity_mu_is_climo_invariant():
    bps = _fake_bin_probs(75.0)
    identity = EmosCoefficients(a=0.0, b=1.0, c=0.0, d=1.0)
    _, mu_a, _ = apply_emos_to_event(bps, identity, bias_applied_f=None, climo_f=60.0)
    _, mu_b, _ = apply_emos_to_event(bps, identity, bias_applied_f=None, climo_f=80.0)
    assert mu_a == pytest.approx(mu_b)


def test_apply_shrinkage_pulls_toward_climatology():
    # b=0.5 halves the forecast anomaly: raw mean ~75 with climo 65 -> mu ~70.
    bps = _fake_bin_probs(75.0)
    recon_mean, _ = moments_from_bin_probs(bps)
    coeffs = EmosCoefficients(a=0.0, b=0.5, c=0.0, d=1.0)
    _, mu, _ = apply_emos_to_event(bps, coeffs, bias_applied_f=None, climo_f=65.0)
    assert mu == pytest.approx(65.0 + 0.5 * (recon_mean - 65.0))


def test_apply_adds_bias_back_to_mean():
    bps = _fake_bin_probs(75.0)
    identity = EmosCoefficients(a=0.0, b=1.0, c=0.0, d=1.0)
    _, mu_none, _ = apply_emos_to_event(bps, identity, bias_applied_f=None, climo_f=70.0)
    _, mu_bias, _ = apply_emos_to_event(bps, identity, bias_applied_f=2.0, climo_f=70.0)
    # Recorded distribution was shifted down by the 2°F bias correction; EMOS features
    # are on the raw scale, so mu must move up by exactly that bias.
    assert mu_bias - mu_none == pytest.approx(2.0)


def test_apply_far_off_mean_respects_floor():
    bps = _fake_bin_probs(75.0)
    # Huge negative shift: nearly all Gaussian mass lands in the open-low bin.
    coeffs = EmosCoefficients(a=-20.0, b=1.0, c=0.0, d=1.0)
    result = apply_emos_to_event(bps, coeffs, bias_applied_f=None, climo_f=70.0)
    assert result is not None
    bin_to_p, _, _ = result
    for p in bin_to_p.values():
        assert 0.005 <= p <= 0.995


def test_apply_without_climatology_returns_none():
    bps = _fake_bin_probs(75.0)
    assert apply_emos_to_event(bps, EmosCoefficients(0, 1, 0, 1), None, climo_f=None) is None


def test_apply_degenerate_moments_returns_none():
    bps = [SimpleNamespace(bin=SimpleNamespace(market_ticker="LO", lo_f=None, hi_f=70.0,
                                               is_open_low=True, is_open_high=False), p=0.1)]
    assert apply_emos_to_event(bps, EmosCoefficients(0, 1, 0, 1), None, climo_f=70.0) is None


# ---- write / load round trip --------------------------------------------------

def test_write_load_round_trip(tmp_path):
    path = tmp_path / "emos.parquet"
    fit = EmosFit(
        station_id="KLAX", kind="high",
        coefficients=EmosCoefficients(a=-4.8, b=0.98, c=2.5, d=1.7),
        n_days=45, days_back=60, crps_raw=3.1, crps_fit=2.2,
    )
    write_emos(path, [fit])
    loaded = load_emos(path)
    assert loaded[("KLAX", "high")] == pytest.approx(EmosCoefficients(-4.8, 0.98, 2.5, 1.7))


def test_load_returns_empty_dict_when_missing(tmp_path):
    assert load_emos(tmp_path / "nope.parquet") == {}


def test_load_skips_rows_from_a_different_feature_space(tmp_path):
    """A stale parquet written before the anomaly-space change (no feature_space column)
    must be ignored rather than misapplied to anomaly features."""
    path = tmp_path / "old-emos.parquet"
    old_schema = pa.schema([
        pa.field("station_id", pa.string()),
        pa.field("kind", pa.string()),
        pa.field("a", pa.float64()),
        pa.field("b", pa.float64()),
        pa.field("c", pa.float64()),
        pa.field("d", pa.float64()),
    ])
    pq.write_table(pa.Table.from_pylist(
        [{"station_id": "KLAX", "kind": "high", "a": 35.4, "b": 0.485, "c": 1.26, "d": 0.176}],
        schema=old_schema,
    ), path)
    assert load_emos(path) == {}


def test_written_parquet_matches_schema(tmp_path):
    path = tmp_path / "emos.parquet"
    write_emos(path, [EmosFit("KLAX", "high", EmosCoefficients(0, 1, 0, 1), 45, 60, 3.0, 2.0)])
    tbl = pq.read_table(path)
    for field in EMOS_PARQUET_SCHEMA:
        assert field.name in tbl.column_names


# ---- configuration guard ------------------------------------------------------

def test_default_emos_stations_have_no_live_cities():
    """Operator mandate 2026-07-16: EMOS must not touch stations with live trading cells
    (Austin/high, Denver/high, San Antonio/high)."""
    assert DEFAULT_EMOS_STATIONS.isdisjoint({"KAUS", "KDEN", "KSAT"})


# ---- recorder integration -----------------------------------------------------

def _fake_bin(ticker: str, idx: int, *, open_low=False, open_high=False, lo=None, hi=None):
    return SimpleNamespace(
        market_ticker=ticker, bin_index=idx, subtitle=f"b{idx}",
        floor_strike=lo, cap_strike=hi, lo_f=lo, hi_f=hi,
        is_open_low=open_low, is_open_high=open_high,
    )


def _fake_event_prices(station_id: str, model_p: dict[str, float]):
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


def test_build_snapshot_table_records_emos_p_only_for_configured_cells():
    from polymarket_model.recorder import _build_snapshot_table

    ep_klax, mo_klax = _fake_event_prices("KLAX", {"KLAX-LO": 0.25, "KLAX-HI": 0.75})
    ep_kaus, mo_kaus = _fake_event_prices("KAUS", {"KAUS-LO": 0.3, "KAUS-HI": 0.7})

    emos = {("KLAX", "high"): EmosCoefficients(a=0.0, b=1.0, c=4.0, d=1.0)}

    tbl = _build_snapshot_table(
        bucket=datetime(2026, 6, 1, 12, tzinfo=UTC),
        started=datetime(2026, 6, 1, 12, tzinfo=UTC),
        priced_events=[ep_klax, ep_kaus],
        model_outputs={"E-KLAX": mo_klax, "E-KAUS": mo_kaus},
        forecasts={("KLAX", date(2026, 6, 1), "high"): SimpleNamespace(lead_hours=10),
                   ("KAUS", date(2026, 6, 1), "high"): SimpleNamespace(lead_hours=10)},
        nbm_outputs={}, nbm_forecasts={},
        emos=emos,
        climatology=_flat_climo("KLAX", "high", 70.0),
    )
    df = tbl.to_pandas()
    klax = df[df["station_id"] == "KLAX"]
    kaus = df[df["station_id"] == "KAUS"]

    # KLAX rows: EMOS applied — emos_p populated, distribution params recorded.
    assert klax["emos_applied"].all()
    assert klax["emos_p"].notna().all()
    assert klax["emos_mu_f"].notna().all()
    assert klax["emos_sigma_f"].notna().all()
    assert klax["emos_p"].sum() == pytest.approx(1.0, abs=1e-6)
    assert np.isfinite(klax["emos_p"]).all()
    # KAUS (live city, never configured): NULL emos_p, flag False.
    assert not kaus["emos_applied"].any()
    assert kaus["emos_p"].isna().all()
