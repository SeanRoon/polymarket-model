# Model diagnostics

_Generated 2026-05-28 02:32 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**11 flag(s):** 1 critical, 3 warn, 7 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| critical | exclude_candidate | New York City (KNYC) | Model worse than market and losing: Brier 0.139 vs 0.068 (gap +0.071), PnL -1.51 over n=2064. | Consider adding KNYC to signal_excluded_stations until calibration improves. |
| warn | regression_wow | Chicago / high | Brier worsened 0.132 -> 0.179 (+0.048) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / low | Brier worsened 0.065 -> 0.116 (+0.051) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New York City / high | Brier worsened 0.127 -> 0.161 (+0.033) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.238 vs market 0.072 (gap +0.166) over n=2160. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.230 vs market 0.054 (gap +0.176) over n=1854. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.138 vs ECMWF 0.170 (gap 0.032) over n=414. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.079 vs ECMWF 0.122 (gap 0.043) over n=102. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / high / 24-72h | NBM lower Brier 0.102 vs ECMWF 0.126 (gap 0.024) over n=126. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / high / 6-24h | NBM lower Brier 0.120 vs ECMWF 0.144 (gap 0.024) over n=390. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.116 vs ECMWF 0.169 (gap 0.053) over n=420. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
