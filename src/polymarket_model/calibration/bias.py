"""Per-station bias correction for ensemble weather forecasts.

The Open-Meteo ECMWF 0.25° ensemble has stable systematic errors at some stations
(e.g., -7°F on Miami highs across two weeks of paired data). Calibration alone
can't fix this — a 7°F mean error swamps any 1-2°F bin width.

This module computes the rolling-window mean of (model_expected_temp - actual)
per (station_id, kind) from the joined snapshot + resolution history, and the
recorder subtracts that bias from each ensemble sample before the predictive
distribution is built. Downstream code is unchanged: bin probabilities, edge
math, paper trading all see the corrected probabilities.

Stations with fewer than `min_days` paired records get no correction (bias=0)
so a station that was recently re-enabled doesn't get clobbered by a noisy
near-empty average.
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

from polymarket_model.config import settings

DEFAULT_BIAS_PARQUET = settings.data_dir / "station_biases.parquet"

BIAS_PARQUET_SCHEMA = pa.schema([
    pa.field("station_id", pa.string(), nullable=False),
    pa.field("kind", pa.string(), nullable=False),
    pa.field("bias_f", pa.float64(), nullable=False),
    pa.field("n_days_used", pa.int32(), nullable=False),
    pa.field("window_days", pa.int32(), nullable=False),
    pa.field("computed_at_utc", pa.timestamp("us", tz="UTC"), nullable=False),
])


@dataclass(frozen=True)
class BiasEstimate:
    station_id: str
    kind: str
    bias_f: float
    n_days_used: int
    window_days: int


def compute_station_biases(
    *,
    snapshots_root: Path,
    resolutions_parquet: Path,
    window_days: int = 7,
    min_days: int = 3,
) -> list[BiasEstimate]:
    """Compute per-(station, kind) bias from the snapshot+resolution join.

    For each resolved event, take the LATEST snapshot bucket and compute the
    model's probability-weighted expected temperature using bin centers (open
    bins use floor +/- 3°F as a proxy). Bias = mean(expected - actual) over
    the last `window_days` days. Stations with fewer than `min_days` paired
    records are omitted.
    """
    if not resolutions_parquet.exists():
        return []
    snaps_glob = str((snapshots_root / "**/*.parquet").as_posix())
    res_path = str(resolutions_parquet.as_posix())

    sql = f"""
        WITH snaps AS (
            SELECT *,
                   CASE WHEN is_open_low THEN hi_f - 3.0
                        WHEN is_open_high THEN lo_f + 3.0
                        ELSE (lo_f + hi_f) / 2.0
                   END AS bin_center_f
            FROM read_parquet('{snaps_glob}', union_by_name=True, filename=True)
            WHERE model_p IS NOT NULL
              AND NOT contains(filename, '_archive_polymarket')
        ),
        latest AS (
            SELECT * FROM snaps
            WHERE snapshot_bucket_utc = (
                SELECT MAX(snapshot_bucket_utc) FROM snaps s2
                WHERE s2.event_ticker = snaps.event_ticker
            )
        ),
        expected_per_event AS (
            SELECT station_id, kind, event_ticker, target_date_local,
                   SUM(model_p * bin_center_f) AS expected_temp_f
            FROM latest
            GROUP BY station_id, kind, event_ticker, target_date_local
        ),
        res AS (
            SELECT station_id,
                   valid_date_local AS target_date_local,
                   kind,
                   value_f
            FROM read_parquet('{res_path}')
        ),
        joined AS (
            SELECT e.station_id, e.kind, e.target_date_local,
                   e.expected_temp_f - r.value_f AS error_f
            FROM expected_per_event e
            JOIN res r USING (station_id, target_date_local, kind)
            WHERE e.target_date_local >= (CURRENT_DATE - INTERVAL '{window_days} days')
        )
        SELECT station_id, kind,
               AVG(error_f) AS bias_f,
               CAST(COUNT(*) AS INTEGER) AS n_days_used
        FROM joined
        GROUP BY station_id, kind
        HAVING COUNT(*) >= {min_days}
        ORDER BY station_id, kind
    """
    con = duckdb.connect(":memory:")
    try:
        rows = con.execute(sql).fetchall()
    finally:
        con.close()
    return [
        BiasEstimate(
            station_id=r[0], kind=r[1], bias_f=float(r[2]),
            n_days_used=int(r[3]), window_days=window_days,
        )
        for r in rows
    ]


def write_biases(path: Path, biases: list[BiasEstimate]) -> None:
    """Atomic write: temp file in same directory, then os.replace."""
    now = datetime.now(UTC)
    rows = [
        {
            "station_id": b.station_id,
            "kind": b.kind,
            "bias_f": b.bias_f,
            "n_days_used": b.n_days_used,
            "window_days": b.window_days,
            "computed_at_utc": now,
        }
        for b in biases
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(rows, schema=BIAS_PARQUET_SCHEMA)
    fd, tmp = tempfile.mkstemp(prefix=".biases-", suffix=".parquet", dir=str(path.parent))
    os.close(fd)
    try:
        pq.write_table(tbl, tmp, compression="zstd")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load_biases(path: Path) -> dict[tuple[str, str], float]:
    """Return {(station_id, kind): bias_f}; empty dict if file missing."""
    if not path.exists():
        return {}
    tbl = pq.read_table(path)
    out: dict[tuple[str, str], float] = {}
    for row in tbl.to_pylist():
        out[(row["station_id"], row["kind"])] = float(row["bias_f"])
    return out


def apply_bias_to_samples(samples: np.ndarray, bias_f: float) -> np.ndarray:
    """Return samples - bias_f. Positive bias means model runs too hot, so we
    shift samples down so the corrected forecast lines up with reality."""
    return np.asarray(samples, dtype=float) - float(bias_f)


def distribution_for(ex, *, station_id, kind, biases):
    """Build the predictive distribution for an event's ensemble forecast, applying
    the per-(station, kind) bias correction when one exists.

    Single source of truth shared by the recorder (snapshot/paper), the `scan`
    report, and the live trader (kalshi-live) so they can't drift: every consumer
    that turns an ensemble forecast into bin probabilities goes through here. The
    bias file (`station_biases.parquet`) is recomputed daily and read via
    `DEFAULT_BIAS_PARQUET`, so refreshing the repo refreshes both code and data.

    Returns `(PredictiveDistribution, bias_applied_f)` where `bias_applied_f` is the
    bias subtracted (or None when no correction applied). Corrected distributions
    have their model name suffixed with `+biascorr` for downstream attribution.
    """
    from polymarket_model.model import PredictiveDistribution

    bias = biases.get((station_id, kind)) if station_id else None
    if bias is not None:
        dist = PredictiveDistribution(
            samples=apply_bias_to_samples(ex.values, bias),
            model=f"empirical_{ex.model}+biascorr",
        )
        return dist, float(bias)
    return PredictiveDistribution.from_ensemble(ex), None
