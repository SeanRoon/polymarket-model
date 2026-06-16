# Model diagnostics

_Generated 2026-06-16 18:05 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**11 flag(s):** 1 critical, 1 warn, 9 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| critical | exclude_candidate | Chicago (KMDW) | Model worse than market and losing: Brier 0.145 vs 0.079 (gap +0.066), PnL -0.93 over n=7722. | Consider adding KMDW to signal_excluded_stations until calibration improves. |
| warn | regression_wow | Los Angeles / high | Brier worsened 0.246 -> 0.288 (+0.042) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.247 vs market 0.066 (gap +0.181) over n=3966. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.179 vs market 0.058 (gap +0.121) over n=3318. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.168 vs market 0.071 (gap +0.098) over n=3810. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.130 vs ECMWF 0.173 (gap 0.043) over n=1230. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 24-72h | NBM lower Brier 0.141 vs ECMWF 0.163 (gap 0.021) over n=294. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 6-24h | NBM lower Brier 0.139 vs ECMWF 0.162 (gap 0.023) over n=1098. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.128 vs ECMWF 0.192 (gap 0.065) over n=1260. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.187 (gap 0.063) over n=198. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.128 vs ECMWF 0.182 (gap 0.054) over n=1134. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
