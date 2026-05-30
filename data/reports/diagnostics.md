# Model diagnostics

_Generated 2026-05-30 14:41 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**7 flag(s):** 2 warn, 5 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Chicago / high | Brier worsened 0.132 -> 0.206 (+0.074) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / low | Brier worsened 0.078 -> 0.117 (+0.039) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.229 vs market 0.069 (gap +0.160) over n=2424. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.224 vs market 0.059 (gap +0.165) over n=2106. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.138 vs market 0.070 (gap +0.067) over n=2316. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.139 vs ECMWF 0.185 (gap 0.047) over n=540. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.109 vs ECMWF 0.162 (gap 0.053) over n=540. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
