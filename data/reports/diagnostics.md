# Model diagnostics

_Generated 2026-06-18 16:34 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**9 flag(s):** 2 warn, 7 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Los Angeles / high | Brier worsened 0.252 -> 0.277 (+0.024) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Miami / high | Brier worsened 0.083 -> 0.114 (+0.031) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.248 vs market 0.066 (gap +0.181) over n=4110. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.177 vs market 0.058 (gap +0.119) over n=3390. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.167 vs market 0.071 (gap +0.096) over n=3942. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.132 vs ECMWF 0.172 (gap 0.039) over n=1296. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.128 vs ECMWF 0.190 (gap 0.062) over n=1326. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.125 vs ECMWF 0.181 (gap 0.056) over n=210. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.129 vs ECMWF 0.180 (gap 0.051) over n=1188. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
