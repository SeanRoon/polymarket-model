"""Per-(station, kind) isotonic recalibration of bin probabilities.

Bias correction (`bias.py`) fixes systematic *temperature* errors by shifting
ensemble samples. It cannot fix *probability* miscalibration — a station where the
model's bin probabilities are too sharp (over-confident) even though the mean
forecast is roughly right. The marine stations are the canonical case: KLAX and
KMIA sit far from the market's Brier (gaps ~+0.17 / +0.14 in `diagnostics.md`)
despite small temperature bias, because the ECMWF 0.25° grid cell averages over
water and the empirical CDF is then too confident about the result.

This module fits a monotonic map ``p_raw -> p_calibrated`` per (station, kind)
from the joined snapshot + resolution history (Pool-Adjacent-Violators via
scikit-learn's :class:`~sklearn.isotonic.IsotonicRegression`) and lets the
recorder write a ``calibrated_p`` column alongside ``model_p`` / ``nbm_p`` /
``blended_p``. As with the ECMWF/NBM blend, calibration is recorded but does
**not** drive live signals yet: the pilot accrues out-of-sample calibrated
predictions so the per-station calibrated Brier can justify re-enabling KLAX/KMIA
before any trade depends on it. The fit is in-sample; honest evaluation comes from
the forward-recorded column resolving over the following weeks.

Stations with fewer than ``min_samples`` paired (p, outcome) records, or whose
predictions don't vary enough to fit a map, get no calibration so a thin or
degenerate sample can't produce a wild mapping.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.isotonic import IsotonicRegression  # type: ignore[import-untyped]

from polymarket_model.config import settings

DEFAULT_CALIBRATION_PARQUET = settings.data_dir / "station_calibration.parquet"

# Calibrated probabilities are clipped to this interval so an isotonic step that
# lands at exactly 0 or 1 can't blow up downstream log-loss / Kelly sizing. Matches
# the spirit of the NBM clip floor/ceiling in `model.evaluate_event_nbm`.
_P_FLOOR = 1e-3
_P_CEIL = 1.0 - 1e-3

# One row per isotonic knot (breakpoint). The map is the piecewise-linear
# interpolation through (knot_x, knot_y); apply via np.interp, so we never have to
# pickle a fitted sklearn object.
CALIBRATION_PARQUET_SCHEMA = pa.schema([
    pa.field("station_id", pa.string(), nullable=False),
    pa.field("kind", pa.string(), nullable=False),
    pa.field("knot_index", pa.int32(), nullable=False),
    pa.field("knot_x", pa.float64(), nullable=False),
    pa.field("knot_y", pa.float64(), nullable=False),
    pa.field("n_samples", pa.int32(), nullable=False),
    pa.field("brier_before", pa.float64(), nullable=False),
    pa.field("brier_after", pa.float64(), nullable=False),
    pa.field("days_back", pa.int32(), nullable=False),
    pa.field("computed_at_utc", pa.timestamp("us", tz="UTC"), nullable=False),
])


@dataclass(frozen=True)
class CalibrationFit:
    """A fitted isotonic map for one (station, kind) cell.

    `x_thresholds` / `y_thresholds` are the sklearn isotonic knots; the calibrated
    probability for a raw `p` is ``np.interp(p, x_thresholds, y_thresholds)`` clipped
    to [_P_FLOOR, _P_CEIL]. `brier_before` / `brier_after` are *in-sample* and only a
    sanity signal — real evaluation is the forward-recorded `calibrated_p` column.
    """
    station_id: str
    kind: str
    x_thresholds: tuple[float, ...]
    y_thresholds: tuple[float, ...]
    n_samples: int
    brier_before: float
    brier_after: float
    days_back: int


def _paired_outcomes(
    *,
    snapshots_root: Path,
    resolutions_parquet: Path,
    stations: frozenset[str],
    days_back: int,
) -> dict[tuple[str, str], tuple[np.ndarray, np.ndarray]]:
    """Return {(station_id, kind): (model_p[], realized_yes[])} for the given stations.

    One (p, outcome) pair per bin per resolved day: we keep only the LATEST snapshot
    bucket per market_ticker (mirroring `bias.py`), which gives independent samples and
    avoids over-weighting markets that happened to be snapshotted more often. The trade-
    off is that the fit pools across lead times and leans toward the shortest-lead
    forecast for each market — acceptable for the marine-station overconfidence the pilot
    targets, which is roughly lead-invariant.
    """
    if not resolutions_parquet.exists() or not stations:
        return {}
    snaps_glob = str((snapshots_root / "**/*.parquet").as_posix())
    res_path = str(resolutions_parquet.as_posix())
    station_list = ", ".join(f"'{s}'" for s in sorted(stations))

    sql = f"""
        WITH snaps AS (
            SELECT station_id, kind, market_ticker, target_date_local, model_p,
                   lo_f, hi_f, is_open_low, is_open_high
            FROM read_parquet('{snaps_glob}', union_by_name=True, filename=True)
            WHERE model_p IS NOT NULL
              AND target_date_local <= CURRENT_DATE
              AND target_date_local >= (CURRENT_DATE - INTERVAL '{days_back} days')
              AND station_id IN ({station_list})
              AND NOT contains(filename, '_archive_polymarket')
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY market_ticker ORDER BY snapshot_bucket_utc DESC
            ) = 1
        ),
        res AS (
            SELECT station_id, valid_date_local AS target_date_local, kind, value_f
            FROM read_parquet('{res_path}')
        )
        SELECT s.station_id, s.kind, s.model_p,
               CASE WHEN (s.is_open_low OR r.value_f >= s.lo_f)
                     AND (s.is_open_high OR r.value_f < s.hi_f)
                    THEN 1 ELSE 0 END AS realized_yes
        FROM snaps s
        JOIN res r USING (station_id, target_date_local, kind)
    """
    con = duckdb.connect(":memory:")
    try:
        rows = con.execute(sql).fetchall()
    finally:
        con.close()

    buckets: dict[tuple[str, str], list[tuple[float, int]]] = {}
    for station_id, kind, model_p, realized_yes in rows:
        buckets.setdefault((station_id, kind), []).append((float(model_p), int(realized_yes)))
    out: dict[tuple[str, str], tuple[np.ndarray, np.ndarray]] = {}
    for key, pairs in buckets.items():
        ps = np.array([p for p, _ in pairs], dtype=float)
        ys = np.array([y for _, y in pairs], dtype=float)
        out[key] = (ps, ys)
    return out


def fit_station_calibrations(
    *,
    snapshots_root: Path,
    resolutions_parquet: Path,
    stations: frozenset[str],
    days_back: int = 60,
    min_samples: int = 100,
) -> list[CalibrationFit]:
    """Fit an isotonic p->p map per (station, kind) for the configured stations.

    A cell is skipped (no calibration emitted) when it has fewer than `min_samples`
    paired records or when its raw predictions don't vary (a degenerate isotonic fit).
    """
    paired = _paired_outcomes(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions_parquet,
        stations=stations,
        days_back=days_back,
    )
    fits: list[CalibrationFit] = []
    for (station_id, kind), (ps, ys) in sorted(paired.items()):
        if ps.shape[0] < min_samples:
            continue
        if np.unique(ps).shape[0] < 2:
            # All predictions identical — isotonic has nothing to learn.
            continue
        iso = IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds="clip")
        iso.fit(ps, ys)
        cal = np.clip(iso.predict(ps), _P_FLOOR, _P_CEIL)
        brier_before = float(np.mean((ps - ys) ** 2))
        brier_after = float(np.mean((cal - ys) ** 2))
        xt = np.asarray(iso.X_thresholds_, dtype=float)
        yt = np.clip(np.asarray(iso.y_thresholds_, dtype=float), _P_FLOOR, _P_CEIL)
        fits.append(
            CalibrationFit(
                station_id=station_id,
                kind=kind,
                x_thresholds=tuple(xt.tolist()),
                y_thresholds=tuple(yt.tolist()),
                n_samples=int(ps.shape[0]),
                brier_before=brier_before,
                brier_after=brier_after,
                days_back=days_back,
            )
        )
    return fits


def write_calibrations(path: Path, fits: list[CalibrationFit]) -> None:
    """Atomic write: temp file in same directory, then os.replace. One row per knot."""
    now = datetime.now(UTC)
    rows: list[dict] = []
    for f in fits:
        for i, (x, y) in enumerate(zip(f.x_thresholds, f.y_thresholds, strict=True)):
            rows.append({
                "station_id": f.station_id,
                "kind": f.kind,
                "knot_index": i,
                "knot_x": float(x),
                "knot_y": float(y),
                "n_samples": f.n_samples,
                "brier_before": f.brier_before,
                "brier_after": f.brier_after,
                "days_back": f.days_back,
                "computed_at_utc": now,
            })
    path.parent.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(rows, schema=CALIBRATION_PARQUET_SCHEMA)
    fd, tmp = tempfile.mkstemp(prefix=".calibration-", suffix=".parquet", dir=str(path.parent))
    os.close(fd)
    try:
        pq.write_table(tbl, tmp, compression="zstd")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load_calibrations(path: Path) -> dict[tuple[str, str], tuple[np.ndarray, np.ndarray]]:
    """Return {(station_id, kind): (x_thresholds, y_thresholds)}; empty if file missing."""
    if not path.exists():
        return {}
    tbl = pq.read_table(path)
    knots: dict[tuple[str, str], list[tuple[int, float, float]]] = {}
    for row in tbl.to_pylist():
        key = (row["station_id"], row["kind"])
        knots.setdefault(key, []).append((int(row["knot_index"]), float(row["knot_x"]), float(row["knot_y"])))
    out: dict[tuple[str, str], tuple[np.ndarray, np.ndarray]] = {}
    for key, items in knots.items():
        items.sort(key=lambda t: t[0])
        xs = np.array([x for _, x, _ in items], dtype=float)
        ys = np.array([y for _, _, y in items], dtype=float)
        out[key] = (xs, ys)
    return out


def apply_calibration(p: float, x_thresholds: np.ndarray, y_thresholds: np.ndarray) -> float:
    """Map a raw probability through the isotonic knots (np.interp clamps at the ends)."""
    cal = float(np.interp(p, x_thresholds, y_thresholds))
    return min(max(cal, _P_FLOOR), _P_CEIL)


def calibrate_bin_probs(
    bin_to_p: dict[str, float],
    x_thresholds: np.ndarray,
    y_thresholds: np.ndarray,
) -> dict[str, float]:
    """Calibrate every bin prob for an event, then renormalize to the original total.

    Isotonic maps each bin independently, so the calibrated values no longer sum to the
    event's original probability mass. We rescale them back to ``sum(bin_to_p)`` (the
    ECMWF union mass) so the calibrated distribution keeps the same outside-bin mass and
    stays comparable to model_p — mirroring the clip-renormalize invariant on the NBM path.
    Returns ``{}`` for an empty input; falls back to the calibrated values unscaled if they
    sum to zero (degenerate, shouldn't happen with the floor clip).
    """
    if not bin_to_p:
        return {}
    calibrated = {t: apply_calibration(p, x_thresholds, y_thresholds) for t, p in bin_to_p.items()}
    target = float(sum(bin_to_p.values()))
    total = float(sum(calibrated.values()))
    if total <= 0.0 or target <= 0.0:
        return calibrated
    scale = target / total
    return {t: p * scale for t, p in calibrated.items()}
