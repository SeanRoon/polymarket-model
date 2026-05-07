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
    """Empirical predictive distribution over daily high/low temperature.

    Phase 1: backed by an array of ensemble-member values. Later phases will add
    a parametric `cdf` callable so the same `prob_in_bin` API serves EMOS too.
    """
    samples: np.ndarray            # shape (n_members,)
    unit: str                      # 'F' | 'C'
    model: str                     # e.g. 'empirical_ecmwf_ifs025'

    @classmethod
    def from_ensemble(cls, ex: EnsembleDailyExtreme) -> "PredictiveDistribution":
        return cls(
            samples=np.asarray(ex.values, dtype=float),
            unit=ex.unit,
            model=f"empirical_{ex.model}",
        )

    @property
    def n(self) -> int:
        return int(self.samples.shape[0])

    def prob_in_bin(self, lo: float, hi: float) -> float:
        """Return P(lo <= X < hi) under the empirical distribution."""
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
) -> EventModelOutput:
    """Compute P(bin) for every bin in the event under the given predictive distribution."""
    if event.unit != distribution.unit:
        raise ValueError(
            f"unit mismatch: event.unit={event.unit!r} distribution.unit={distribution.unit!r}"
        )
    samples = distribution.samples
    n = samples.shape[0]
    if n == 0:
        raise ValueError("distribution has no samples")

    masks = [_bin_iter_values(b, samples) for b in event.bins]
    counts = np.array([mask.sum() for mask in masks], dtype=float)
    probs = counts / n

    # outside mass: any sample not captured by ANY bin
    union_mask = np.zeros(n, dtype=bool)
    for mask in masks:
        union_mask |= mask
    outside = float((~union_mask).mean())

    bin_probs = [BinProb(b, float(p)) for b, p in zip(event.bins, probs, strict=True)]
    return EventModelOutput(
        event=event,
        distribution=distribution,
        bin_probs=bin_probs,
        outside_bin_mass=outside,
        sum_of_bin_probs=float(probs.sum()),
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
            return False, f"gap or overlap between {a.label!r} (hi={a.hi_f}) and {b.label!r} (lo={b.lo_f})"
    return True, "ok"
