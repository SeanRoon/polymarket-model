"""Calibration: per-station bias correction and (eventually) isotonic recalibration.

Phase 2.6 — Bias correction subtracts the rolling-window mean forecast error from
each ensemble sample before bins are computed. Catches systematic errors that
calibration alone can't fix (e.g., Open-Meteo's ECMWF 0.25° grid under-forecasts
Miami highs by ~7°F because the cell averages over water).

Phase 3 (later) will add isotonic recalibration on top, which handles
over-confidence in cities where the bias is small but the model is too sharp
(e.g., Los Angeles).
"""
