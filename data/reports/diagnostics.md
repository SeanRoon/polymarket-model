# Model diagnostics

_Generated 2026-06-02 17:24 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**11 flag(s):** 3 warn, 8 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Chicago / high | Brier worsened 0.165 -> 0.200 (+0.034) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / low | Brier worsened 0.098 -> 0.123 (+0.025) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Los Angeles / high | Brier worsened 0.190 -> 0.238 (+0.048) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.238 vs market 0.065 (gap +0.173) over n=2766. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.218 vs market 0.060 (gap +0.158) over n=2220. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.140 vs market 0.068 (gap +0.072) over n=2646. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.132 vs ECMWF 0.183 (gap 0.051) over n=690. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 24-72h | NBM lower Brier 0.146 vs ECMWF 0.179 (gap 0.033) over n=168. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 6-24h | NBM lower Brier 0.142 vs ECMWF 0.169 (gap 0.027) over n=600. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.133 vs ECMWF 0.162 (gap 0.029) over n=696. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.122 vs ECMWF 0.149 (gap 0.027) over n=108. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
