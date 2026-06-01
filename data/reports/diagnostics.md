# Model diagnostics

_Generated 2026-06-01 18:39 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**9 flag(s):** 2 warn, 7 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Chicago / high | Brier worsened 0.158 -> 0.208 (+0.050) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / low | Brier worsened 0.096 -> 0.132 (+0.036) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.237 vs market 0.066 (gap +0.171) over n=2676. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.218 vs market 0.060 (gap +0.158) over n=2220. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.139 vs market 0.068 (gap +0.071) over n=2562. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.136 vs ECMWF 0.186 (gap 0.050) over n=660. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 24-72h | NBM lower Brier 0.156 vs ECMWF 0.179 (gap 0.023) over n=150. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 6-24h | NBM lower Brier 0.149 vs ECMWF 0.171 (gap 0.022) over n=558. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.128 vs ECMWF 0.162 (gap 0.034) over n=672. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
