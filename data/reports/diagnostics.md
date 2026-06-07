# Model diagnostics

_Generated 2026-06-07 14:54 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**13 flag(s):** 4 warn, 9 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Austin / high | Brier worsened 0.000 -> 0.079 (+0.079) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Denver / high | Brier worsened 0.042 -> 0.098 (+0.056) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Los Angeles / high | Brier worsened 0.184 -> 0.236 (+0.052) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New York City / high | Brier worsened 0.137 -> 0.257 (+0.120) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.237 vs market 0.068 (gap +0.168) over n=3126. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.205 vs market 0.059 (gap +0.145) over n=2502. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.156 vs market 0.071 (gap +0.085) over n=2994. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.124 vs ECMWF 0.187 (gap 0.063) over n=858. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 24-72h | NBM lower Brier 0.142 vs ECMWF 0.179 (gap 0.037) over n=198. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 6-24h | NBM lower Brier 0.137 vs ECMWF 0.173 (gap 0.036) over n=744. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.134 vs ECMWF 0.187 (gap 0.053) over n=870. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.123 vs ECMWF 0.165 (gap 0.042) over n=126. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.131 vs ECMWF 0.163 (gap 0.032) over n=780. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
