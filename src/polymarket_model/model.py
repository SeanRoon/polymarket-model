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
