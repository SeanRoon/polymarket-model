"""Per-(station, kind) EMOS / NGR recalibration of the ensemble predictive distribution.

Bias correction (`bias.py`) shifts the ensemble mean; isotonic (`isotonic.py`) remaps
bin probabilities after the fact. Neither fixes the *spread*: the ECMWF 0.25° ensemble
is systematically over-confident at the marine and lake stations (KLAX/KMIA/KNYC/KMDW),
where the grid cell averages over water and the member spread understates the true
forecast error. EMOS (Ensemble Model Output Statistics, a.k.a. Non-homogeneous Gaussian
Regression) fits a full Gaussian predictive distribution

    T_actual ~ N( a + b * ens_mean,  sqrt(c + d * ens_var) )

per (station, kind) by minimizing the mean CRPS over the paired snapshot + resolution
history. Because ``a``/``b`` absorb the mean error, EMOS *subsumes* the rolling bias
correction rather than stacking on it: the fit reconstructs the RAW (pre-biascorr)
ensemble mean by adding ``model_bias_applied_f`` back to the recorded distribution's
expectation, and the recorder applies the coefficients to the same raw-mean feature.

Train/apply feature symmetry: snapshots don't store ensemble mean/std directly, so the
fit reconstructs both from the recorded per-bin ``model_p`` using bin centers (open bins
proxied at ±3°F, the same convention as `bias.py`). The recorder reconstructs the
moments from the live bin probabilities with the *identical* formula
(`moments_from_bin_probs`), so the features EMOS sees at apply time match the ones it
was fitted on by construction.

Like the blend and the isotonic pilot, EMOS output is a recorded-only ``emos_p`` column:
it does NOT drive live signals. Scope is `settings.emos_stations`, which deliberately
contains no station with a live trading cell (operator mandate 2026-07-16) — the pilot
accrues out-of-sample evidence on excluded stations only.

Cells with fewer than ``min_days`` paired records, or whose reconstructed means don't
vary, get no fit so a thin sample can't produce wild coefficients.
"""
from __future__ import annotations

import math
import os
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import NamedTuple, Protocol

import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.optimize import minimize  # type: ignore[import-untyped]
from scipy.special import erf  # type: ignore[import-untyped]

from polymarket_model.config import settings
from polymarket_model.model import _clip_and_renormalize

DEFAULT_EMOS_PARQUET = settings.data_dir / "station_emos.parquet"

# Open bins have no finite center; proxy at threshold ± this many °F. MUST match the
# bin_center_f CASE in the fit SQL and `bias.py` — train/apply symmetry depends on it.
_OPEN_BIN_OFFSET_F = 3.0

# Predictive sigma is floored here (°F) so a distribution that collapsed into one bin
# can't produce a near-degenerate Gaussian; applied identically in fit and apply.
_SIGMA_FLOOR_F = 0.5

# Same clip bounds as the NBM path in `model.evaluate_event_nbm`: keeps a zero-density
# bin from blowing up downstream log-loss / Kelly sizing.
_P_FLOOR = 0.005
_P_CEIL = 0.995

EMOS_PARQUET_SCHEMA = pa.schema([
    pa.field("station_id", pa.string(), nullable=False),
    pa.field("kind", pa.string(), nullable=False),
    pa.field("a", pa.float64(), nullable=False),
    pa.field("b", pa.float64(), nullable=False),
    pa.field("c", pa.float64(), nullable=False),
    pa.field("d", pa.float64(), nullable=False),
    pa.field("n_days", pa.int32(), nullable=False),
    pa.field("days_back", pa.int32(), nullable=False),
    pa.field("crps_raw", pa.float64(), nullable=False),
    pa.field("crps_fit", pa.float64(), nullable=False),
    pa.field("computed_at_utc", pa.timestamp("us", tz="UTC"), nullable=False),
])


class EmosCoefficients(NamedTuple):
    """Fitted NGR coefficients: mu = a + b*mean, sigma = sqrt(c + d*var)."""
    a: float
    b: float
    c: float
    d: float


@dataclass(frozen=True)
class EmosFit:
    """A fitted EMOS model for one (station, kind) cell.

    `crps_raw` / `crps_fit` are IN-SAMPLE mean CRPS of the uncorrected
    (a=0, b=1, c=0, d=1) and fitted Gaussians — a sanity signal only; the honest
    evaluation is the forward-recorded `emos_p` column resolving over following weeks.
    """
    station_id: str
    kind: str
    coefficients: EmosCoefficients
    n_days: int
    days_back: int
    crps_raw: float
    crps_fit: float


class _BinLike(Protocol):
    # Read-only properties so any Bin-shaped object (frozen dataclass, SimpleNamespace)
    # satisfies the protocol covariantly, including lo_f/hi_f declared as plain float.
    @property
    def market_ticker(self) -> str: ...
    @property
    def lo_f(self) -> float | None: ...
    @property
    def hi_f(self) -> float | None: ...
    @property
    def is_open_low(self) -> bool: ...
    @property
    def is_open_high(self) -> bool: ...


class _BinProbLike(Protocol):
    @property
    def bin(self) -> _BinLike: ...
    @property
    def p(self) -> float: ...


def _norm_cdf(z: np.ndarray | float) -> np.ndarray | float:
    return 0.5 * (1.0 + erf(np.asarray(z) / math.sqrt(2.0)))


def _norm_pdf(z: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def _crps_gaussian(y: np.ndarray, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """Closed-form CRPS of N(mu, sigma) against observations y (Gneiting et al. 2005)."""
    z = (y - mu) / sigma
    return sigma * (z * (2.0 * _norm_cdf(z) - 1.0) + 2.0 * _norm_pdf(z) - 1.0 / math.sqrt(math.pi))


def _bin_center(lo_f: float | None, hi_f: float | None, is_open_low: bool, is_open_high: bool) -> float:
    if is_open_low:
        assert hi_f is not None
        return hi_f - _OPEN_BIN_OFFSET_F
    if is_open_high:
        assert lo_f is not None
        return lo_f + _OPEN_BIN_OFFSET_F
    assert lo_f is not None and hi_f is not None
    return (lo_f + hi_f) / 2.0


def moments_from_bin_probs(bin_probs: Iterable[_BinProbLike]) -> tuple[float, float] | None:
    """(mean, std) of the recorded per-bin distribution, via the bin-center convention.

    This is the Python mirror of the fit SQL's moment reconstruction — the two MUST
    stay in lockstep or the apply-time features drift from the fitted ones. Returns
    None when total mass is degenerate (missing/empty bin probs).
    """
    ps: list[float] = []
    cs: list[float] = []
    for bp in bin_probs:
        b = bp.bin
        ps.append(float(bp.p))
        cs.append(_bin_center(b.lo_f, b.hi_f, b.is_open_low, b.is_open_high))
    mass = sum(ps)
    if mass <= 0.5:  # a real event's bin probs sum to ~1 minus outside-bin mass
        return None
    mean = sum(p * c for p, c in zip(ps, cs, strict=True)) / mass
    m2 = sum(p * c * c for p, c in zip(ps, cs, strict=True)) / mass
    var = max(m2 - mean * mean, 0.0)
    return mean, math.sqrt(max(var, _SIGMA_FLOOR_F * _SIGMA_FLOOR_F))


def _paired_moments(
    *,
    snapshots_root: Path,
    resolutions_parquet: Path,
    stations: frozenset[str],
    days_back: int,
) -> dict[tuple[str, str], tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """{(station, kind): (raw_mean[], var[], actual[])} from the snapshot+resolution join.

    One sample per resolved event: the LATEST snapshot bucket per event (mirroring
    `bias.py`), moments reconstructed from model_p over bin centers, and the recorded
    bias added back so `raw_mean` is the PRE-biascorr ensemble expectation.
    """
    if not resolutions_parquet.exists() or not stations:
        return {}
    snaps_glob = str((snapshots_root / "**/*.parquet").as_posix())
    res_path = str(resolutions_parquet.as_posix())
    station_list = ", ".join(f"'{s}'" for s in sorted(stations))

    sql = f"""
        WITH snaps AS (
            SELECT station_id, kind, event_ticker, target_date_local, model_p,
                   COALESCE(model_bias_applied_f, 0.0) AS bias_f,
                   snapshot_bucket_utc,
                   CASE WHEN is_open_low THEN hi_f - {_OPEN_BIN_OFFSET_F}
                        WHEN is_open_high THEN lo_f + {_OPEN_BIN_OFFSET_F}
                        ELSE (lo_f + hi_f) / 2.0
                   END AS bin_center_f
            FROM read_parquet('{snaps_glob}', union_by_name=True, filename=True)
            WHERE model_p IS NOT NULL
              AND station_id IN ({station_list})
              AND target_date_local <= CURRENT_DATE
              AND target_date_local >= (CURRENT_DATE - INTERVAL '{days_back} days')
              AND NOT contains(filename, '_archive_polymarket')
        ),
        latest AS (
            SELECT * FROM (
                SELECT *, MAX(snapshot_bucket_utc) OVER (PARTITION BY event_ticker) AS max_bucket
                FROM snaps
            ) WHERE snapshot_bucket_utc = max_bucket
        ),
        moments AS (
            SELECT station_id, kind, event_ticker, target_date_local,
                   SUM(model_p * bin_center_f) / SUM(model_p) AS mean_f,
                   SUM(model_p * bin_center_f * bin_center_f) / SUM(model_p) AS m2_f,
                   MAX(bias_f) AS bias_f
            FROM latest
            GROUP BY station_id, kind, event_ticker, target_date_local
            HAVING SUM(model_p) > 0.5
        ),
        res AS (
            SELECT station_id, valid_date_local AS target_date_local, kind, value_f
            FROM read_parquet('{res_path}')
        )
        SELECT m.station_id, m.kind,
               m.mean_f + m.bias_f AS raw_mean_f,
               m.m2_f - m.mean_f * m.mean_f AS var_f,
               r.value_f AS actual_f
        FROM moments m
        JOIN res r USING (station_id, target_date_local, kind)
    """
    con = duckdb.connect(":memory:")
    try:
        rows = con.execute(sql).fetchall()
    finally:
        con.close()

    buckets: dict[tuple[str, str], list[tuple[float, float, float]]] = {}
    for station_id, kind, raw_mean, var, actual in rows:
        var = max(float(var), _SIGMA_FLOOR_F * _SIGMA_FLOOR_F)
        buckets.setdefault((station_id, kind), []).append((float(raw_mean), var, float(actual)))
    out: dict[tuple[str, str], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for key, triples in buckets.items():
        arr = np.array(triples, dtype=float)
        out[key] = (arr[:, 0], arr[:, 1], arr[:, 2])
    return out


def _sigma_from(c: float, d: float, var: np.ndarray) -> np.ndarray:
    return np.sqrt(np.maximum(c + d * var, _SIGMA_FLOOR_F * _SIGMA_FLOOR_F))


def _fit_one(
    raw_mean: np.ndarray, var: np.ndarray, actual: np.ndarray
) -> tuple[EmosCoefficients, float, float]:
    """CRPS-minimizing NGR fit for one cell. Returns (coefficients, crps_raw, crps_fit).

    c and d are kept non-negative by optimizing their square roots. Nelder-Mead over
    4 params on <200 points is fast and doesn't need gradients of the CRPS.
    """
    crps_raw = float(np.mean(_crps_gaussian(actual, raw_mean, _sigma_from(0.0, 1.0, var))))

    # Initialize (a, b) from OLS of actual on raw_mean; split the residual variance
    # between the constant and the spread-scaling terms.
    b0, a0 = np.polyfit(raw_mean, actual, 1)
    resid_var = float(np.var(actual - (a0 + b0 * raw_mean)))
    mean_var = float(np.mean(var))
    c0 = max(resid_var / 2.0, 0.01)
    d0 = max(resid_var / 2.0 / mean_var, 0.01) if mean_var > 0 else 1.0

    def objective(params: np.ndarray) -> float:
        a, b, sc, sd = params
        sigma = _sigma_from(sc * sc, sd * sd, var)
        return float(np.mean(_crps_gaussian(actual, a + b * raw_mean, sigma)))

    x0 = np.array([a0, b0, math.sqrt(c0), math.sqrt(d0)])
    res = minimize(objective, x0, method="Nelder-Mead",
                   options={"maxiter": 4000, "xatol": 1e-4, "fatol": 1e-7})
    a, b, sc, sd = (float(v) for v in res.x)
    coeffs = EmosCoefficients(a=a, b=b, c=sc * sc, d=sd * sd)
    crps_fit = float(objective(res.x))
    return coeffs, crps_raw, crps_fit


def fit_station_emos(
    *,
    snapshots_root: Path,
    resolutions_parquet: Path,
    stations: frozenset[str],
    days_back: int = 60,
    min_days: int = 30,
) -> list[EmosFit]:
    """Fit an EMOS Gaussian per (station, kind) for the configured stations.

    A cell is skipped when it has fewer than `min_days` paired events, when its
    reconstructed means don't vary (degenerate regression), or when the optimizer
    fails to beat the raw ensemble's in-sample CRPS (fit not trustworthy).
    """
    paired = _paired_moments(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions_parquet,
        stations=stations,
        days_back=days_back,
    )
    fits: list[EmosFit] = []
    for (station_id, kind), (raw_mean, var, actual) in sorted(paired.items()):
        n = raw_mean.shape[0]
        if n < min_days:
            continue
        if float(np.std(raw_mean)) < 1e-6:
            continue
        coeffs, crps_raw, crps_fit = _fit_one(raw_mean, var, actual)
        if not math.isfinite(crps_fit) or crps_fit > crps_raw:
            continue
        fits.append(
            EmosFit(
                station_id=station_id,
                kind=kind,
                coefficients=coeffs,
                n_days=n,
                days_back=days_back,
                crps_raw=crps_raw,
                crps_fit=crps_fit,
            )
        )
    return fits


def write_emos(path: Path, fits: list[EmosFit]) -> None:
    """Atomic write: temp file in same directory, then os.replace. One row per cell."""
    now = datetime.now(UTC)
    rows = [
        {
            "station_id": f.station_id,
            "kind": f.kind,
            "a": f.coefficients.a,
            "b": f.coefficients.b,
            "c": f.coefficients.c,
            "d": f.coefficients.d,
            "n_days": f.n_days,
            "days_back": f.days_back,
            "crps_raw": f.crps_raw,
            "crps_fit": f.crps_fit,
            "computed_at_utc": now,
        }
        for f in fits
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(rows, schema=EMOS_PARQUET_SCHEMA)
    fd, tmp = tempfile.mkstemp(prefix=".emos-", suffix=".parquet", dir=str(path.parent))
    os.close(fd)
    try:
        pq.write_table(tbl, tmp, compression="zstd")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load_emos(path: Path) -> dict[tuple[str, str], EmosCoefficients]:
    """Return {(station_id, kind): coefficients}; empty if file missing."""
    if not path.exists():
        return {}
    tbl = pq.read_table(path)
    out: dict[tuple[str, str], EmosCoefficients] = {}
    for row in tbl.to_pylist():
        out[(row["station_id"], row["kind"])] = EmosCoefficients(
            a=float(row["a"]), b=float(row["b"]), c=float(row["c"]), d=float(row["d"])
        )
    return out


def apply_emos_to_event(
    bin_probs: Iterable[_BinProbLike],
    coeffs: EmosCoefficients,
    bias_applied_f: float | None,
) -> tuple[dict[str, float], float, float] | None:
    """EMOS-calibrated per-bin probabilities for one event, keyed by market_ticker.

    Reconstructs the distribution moments from the recorded bin probs (identical
    formula to the fit SQL), un-does the bias shift to recover the raw ensemble mean,
    and evaluates the fitted Gaussian's mass over each bin. Clip + renormalize follows
    the NBM path so no bin is exactly 0 or 1. Returns (bin_to_p, mu, sigma), or None
    when the moments are degenerate.
    """
    bps = list(bin_probs)
    moments = moments_from_bin_probs(bps)
    if moments is None:
        return None
    mean_corrected, std = moments
    raw_mean = mean_corrected + (bias_applied_f or 0.0)
    mu = coeffs.a + coeffs.b * raw_mean
    sigma = float(_sigma_from(coeffs.c, coeffs.d, np.array([std * std]))[0])

    tickers: list[str] = []
    raw_probs: list[float] = []
    for bp in bps:
        b = bp.bin
        lo = -math.inf if b.is_open_low else float(b.lo_f)  # type: ignore[arg-type]
        hi = math.inf if b.is_open_high else float(b.hi_f)  # type: ignore[arg-type]
        p_hi = 1.0 if math.isinf(hi) else float(_norm_cdf((hi - mu) / sigma))
        p_lo = 0.0 if math.isinf(lo) and lo < 0 else float(_norm_cdf((lo - mu) / sigma))
        tickers.append(b.market_ticker)
        raw_probs.append(max(0.0, p_hi - p_lo))

    target = float(sum(raw_probs))
    if target <= 0.0:
        return None
    clipped = _clip_and_renormalize(raw_probs, target=target, floor=_P_FLOOR, ceiling=_P_CEIL)
    return dict(zip(tickers, clipped, strict=True)), mu, sigma
