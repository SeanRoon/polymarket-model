# Model diagnostics

_Generated 2026-06-21 15:12 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**29 flag(s):** 1 critical, 2 warn, 26 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| critical | exclude_candidate | Chicago (KMDW) | Model worse than market and losing: Brier 0.147 vs 0.079 (gap +0.069), PnL -2.04 over n=8514. | Consider adding KMDW to signal_excluded_stations until calibration improves. |
| warn | regression_wow | Chicago / low | Brier worsened 0.166 -> 0.210 (+0.044) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Miami / high | Brier worsened 0.083 -> 0.126 (+0.042) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.219 vs market 0.054 (gap +0.165) over n=282. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.074 vs market 0.040 (gap +0.034) over n=294. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.127 vs market 0.061 (gap +0.066) over n=270. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.148 vs market 0.081 (gap +0.066) over n=318. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.221 vs market 0.023 (gap +0.197) over n=354. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.237 vs market 0.065 (gap +0.171) over n=4530. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.173 vs market 0.059 (gap +0.114) over n=3612. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.156 vs market 0.040 (gap +0.116) over n=312. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.197 vs market 0.105 (gap +0.092) over n=318. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.169 vs market 0.071 (gap +0.097) over n=4170. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.169 vs market 0.076 (gap +0.094) over n=330. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.147 vs market 0.045 (gap +0.102) over n=348. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Antonio (KSAT) | Still miscalibrated: model Brier 0.108 vs market 0.067 (gap +0.041) over n=432. | Keep KSAT excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.224 vs market 0.120 (gap +0.105) over n=348. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.151 vs market 0.079 (gap +0.072) over n=354. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.130 vs market 0.088 (gap +0.041) over n=282. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.128 vs ECMWF 0.169 (gap 0.041) over n=1404. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 6-24h | NBM lower Brier 0.136 vs ECMWF 0.158 (gap 0.021) over n=1272. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.194 vs ECMWF 0.261 (gap 0.067) over n=102. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 0-6h | NBM lower Brier 0.079 vs ECMWF 0.151 (gap 0.073) over n=102. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / high / 0-6h | NBM lower Brier 0.130 vs ECMWF 0.248 (gap 0.119) over n=108. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.127 vs ECMWF 0.190 (gap 0.064) over n=1428. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.181 (gap 0.057) over n=228. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.180 (gap 0.053) over n=1296. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / high / 0-6h | NBM lower Brier 0.137 vs ECMWF 0.208 (gap 0.071) over n=108. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 0-6h | NBM lower Brier 0.098 vs ECMWF 0.149 (gap 0.050) over n=108. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
