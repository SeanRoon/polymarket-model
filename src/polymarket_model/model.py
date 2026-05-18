"""Predictive distributions over daily high/low temperature.

Phase 1 ships only the empirical CDF over ensemble members (no bias correction,
no calibration). EMOS / KDE / isotonic land in Phase 3.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from polymarket_model.config import settings
from polymarket_model.markets.discovery import Bin, WeatherEvent
from polymarket_model.weather.nbm import NBMQuantileForecast
from polymarket_model.weather.openmeteo import EnsembleDailyExtreme


@dataclass(frozen=True)
class PredictiveDistribution:
    """Empirical predictive distribution over daily high/low temperature in °F.

    Phase 1: backed by an array of ensemble-member values. Later phases will add
    a parametric `cdf` callable so the same `prob_in_bin` API serves EMOS too.
    Laplace-smoothed bin counts: p_smoothed = (count + alpha) / (n + alpha * n_bins)
    is applied at the event level in `evaluate_event`, not on the raw samples.
    """
    samples: np.ndarray            # shape (n_members,)
    model: str                     # e.g. 'empirical_ecmwf_ifs025'

    @classmethod
    def from_ensemble(cls, ex: EnsembleDailyExtreme) -> "PredictiveDistribution":
        return cls(
            samples=np.asarray(ex.values, dtype=float),
            model=f"empirical_{ex.model}",
        )

    @property
    def n(self) -> int:
        return int(self.samples.shape[0])

    def prob_in_bin(self, lo: float, hi: float) -> float:
        """Return raw (unsmoothed) P(lo <= X < hi) under the empirical distribution."""
        if hi <= lo:
            return 0.0
        if math.isinf(lo) and lo < 0:
            mask = self.samples < hi
        elif math.isinf(hi):
            mask = self.samples >= lo
        else:
            mask = (self.samples >= lo) & (self.samples < hi)
        return float(mask.mean())


@dataclass(frozen=True)
class BinProb:
    bin: Bin
    p: float


@dataclass(frozen=True)
class EventModelOutput:
    event: WeatherEvent
    distribution: PredictiveDistribution
    bin_probs: list[BinProb]
    outside_bin_mass: float
    sum_of_bin_probs: float

    @property
    def passes_qc(self) -> bool:
        return self.outside_bin_mass <= settings.outside_bin_mass_max


def _bin_iter_values(bin_: Bin, samples: np.ndarray) -> np.ndarray:
    if bin_.is_open_low:
        return samples < bin_.hi_f
    if bin_.is_open_high:
        return samples >= bin_.lo_f
    return (samples >= bin_.lo_f) & (samples < bin_.hi_f)


def evaluate_event(
    event: WeatherEvent,
    distribution: PredictiveDistribution,
    *,
    laplace_alpha: float = 0.5,
) -> EventModelOutput:
    """Compute P(bin) for every bin in the event under the given predictive distribution.

    Uses Laplace (add-alpha) smoothing on the bin counts so probabilities never hit hard
    0% or 100% from a 51-member ensemble — that would over-confidently size full-Kelly bets
    on outcomes the ensemble simply hasn't sampled. With alpha=0.5 and 6 bins:
      smoothed_p = (count + 0.5) / (51 + 3)  =>  floor ~0.009, ceiling ~0.95.
    """
    samples = distribution.samples
    n = samples.shape[0]
    if n == 0:
        raise ValueError("distribution has no samples")
    n_bins = len(event.bins)

    masks = [_bin_iter_values(b, samples) for b in event.bins]
    counts = np.array([mask.sum() for mask in masks], dtype=float)

    union_mask = np.zeros(n, dtype=bool)
    for mask in masks:
        union_mask |= mask
    outside = float((~union_mask).mean())

    # Laplace-smoothed bin probabilities (renormalised within the bin support).
    smoothed = (counts + laplace_alpha) / (n + laplace_alpha * n_bins)

    bin_probs = [BinProb(b, float(p)) for b, p in zip(event.bins, smoothed, strict=True)]
    return EventModelOutput(
        event=event,
        distribution=distribution,
        bin_probs=bin_probs,
        outside_bin_mass=outside,
        sum_of_bin_probs=float(smoothed.sum()),
    )


def _quantile_cdf_anchors(quantiles: dict[int, float]) -> tuple[np.ndarray, np.ndarray]:
    """Return (x, y) arrays for a piecewise-linear CDF anchored to F=0 and F=1.

    Tail anchors extend the *local edge slope* outward until F hits 0 (below) and 1 (above).
    This preserves the density implied by the outermost quantile pair, which is more honest
    than truncating mass at q_min / q_max but less prescriptive than fitting a parametric tail.
    """
    pcts = sorted(quantiles.keys())
    if len(pcts) < 2:
        raise ValueError("Need at least 2 quantiles to build a CDF")
    qx = np.array([quantiles[p] for p in pcts], dtype=float)
    qy = np.array([p / 100.0 for p in pcts], dtype=float)
    # Edge slopes; guard against degenerate (qx[0] == qx[1]) which can happen if NBM emits
    # tied percentile values for an extremely narrow-spread forecast.
    span_lo = qx[1] - qx[0]
    span_hi = qx[-1] - qx[-2]
    eps = 1e-6
    slope_lo = (qy[1] - qy[0]) / span_lo if span_lo > eps else (qy[1] - qy[0]) / eps
    slope_hi = (qy[-1] - qy[-2]) / span_hi if span_hi > eps else (qy[-1] - qy[-2]) / eps
    x_low = qx[0] - qy[0] / slope_lo if slope_lo > 0 else qx[0] - 1.0
    x_high = qx[-1] + (1.0 - qy[-1]) / slope_hi if slope_hi > 0 else qx[-1] + 1.0
    full_x = np.concatenate(([x_low], qx, [x_high]))
    full_y = np.concatenate(([0.0], qy, [1.0]))
    return full_x, full_y


def _cdf_eval(full_x: np.ndarray, full_y: np.ndarray, x: float) -> float:
    if math.isinf(x):
        return 0.0 if x < 0 else 1.0
    if x <= full_x[0]:
        return 0.0
    if x >= full_x[-1]:
        return 1.0
    return float(np.interp(x, full_x, full_y))


def evaluate_event_nbm(
    event: WeatherEvent,
    forecast: NBMQuantileForecast,
    *,
    floor: float = 0.005,
    ceiling: float = 0.995,
    n_synth_samples: int = 200,
) -> EventModelOutput:
    """Compute P(bin) for every bin under the NBM quantile-derived CDF.

    NBM QMD only exposes instantaneous TMP percentiles, so the underlying forecast is a
    peak-hour proxy for daily Tmax/Tmin (see `weather/nbm` module docstring). Bin probs
    come from F(hi) - F(lo) on the piecewise-linear CDF; we clip to [floor, ceiling] so
    a single near-zero-density bin doesn't blow up downstream Kelly sizing.

    The `distribution` field of the returned EventModelOutput holds a samples-backed
    `PredictiveDistribution` synthesized via inverse-CDF interpolation. The samples are
    cosmetic — they satisfy the type so the same recorder/evaluator code paths work, but
    bin_probs is the authoritative output and is computed analytically from the CDF.
    """
    full_x, full_y = _quantile_cdf_anchors(forecast.quantiles)

    raw_probs: list[float] = []
    for b in event.bins:
        lo = -math.inf if b.is_open_low else b.lo_f
        hi = math.inf if b.is_open_high else b.hi_f
        raw = _cdf_eval(full_x, full_y, hi) - _cdf_eval(full_x, full_y, lo)
        raw_probs.append(max(0.0, raw))

    union = float(sum(raw_probs))
    outside = max(0.0, 1.0 - union)

    clipped = [min(max(p, floor), ceiling) for p in raw_probs]
    bin_probs = [BinProb(b, p) for b, p in zip(event.bins, clipped, strict=True)]

    # Synthesize representative samples by inverting the CDF on a uniform grid.
    u = np.linspace(0.005, 0.995, n_synth_samples)
    samples = np.interp(u, full_y, full_x)
    dist = PredictiveDistribution(samples=samples, model=forecast.model)

    return EventModelOutput(
        event=event,
        distribution=dist,
        bin_probs=bin_probs,
        outside_bin_mass=outside,
        sum_of_bin_probs=float(sum(clipped)),
    )


def assert_bins_cover_support(bins: Iterable[Bin]) -> tuple[bool, str]:
    """Sanity-check that bins partition (-inf, +inf) with no gaps and no overlaps.
    Returns (ok, reason)."""
    sorted_bins = sorted(bins, key=lambda b: (b.lo_f, b.hi_f))
    if not sorted_bins:
        return False, "no bins"
    if not sorted_bins[0].is_open_low:
        return False, "no open-low bin"
    if not sorted_bins[-1].is_open_high:
        return False, "no open-high bin"
    for a, b in zip(sorted_bins[:-1], sorted_bins[1:], strict=False):
        if a.hi_f != b.lo_f:
            return False, f"gap or overlap between {a.subtitle!r} (hi={a.hi_f}) and {b.subtitle!r} (lo={b.lo_f})"
    return True, "ok"
