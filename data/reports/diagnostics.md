# Model diagnostics

_Generated 2026-10-29 18:52 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**90 flag(s):** 13 warn, 77 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Boston / high | Brier worsened 0.179 -> 0.230 (+0.051) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Boston / low | Brier worsened 0.164 -> 0.226 (+0.061) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Dallas / high | Brier worsened 0.089 -> 0.144 (+0.055) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Dallas / low | Brier worsened 0.153 -> 0.178 (+0.025) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Denver / high | Brier worsened 0.000 -> 0.061 (+0.060) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Houston / low | Brier worsened 0.146 -> 0.219 (+0.073) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Los Angeles / high | Brier worsened 0.074 -> 0.200 (+0.127) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New Orleans / high | Brier worsened 0.106 -> 0.129 (+0.024) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New York City / high | Brier worsened 0.154 -> 0.212 (+0.058) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Philadelphia / high | Brier worsened 0.121 -> 0.266 (+0.145) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Philadelphia / low | Brier worsened 0.191 -> 0.223 (+0.032) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Washington DC / high | Brier worsened 0.206 -> 0.245 (+0.039) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Washington DC / low | Brier worsened 0.184 -> 0.226 (+0.042) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | emos_improves_model | Chicago / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.166 vs model 0.200 vs market 0.066 over n=3282 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.139 vs model 0.178 vs market 0.064 over n=3036 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.163 vs model 0.191 vs market 0.059 over n=3222 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Miami / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.126 vs model 0.147 vs market 0.075 over n=2598 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.131 vs model 0.152 vs market 0.062 over n=2724 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.163 vs model 0.196 vs market 0.075 over n=2910 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.177 vs market 0.070 (gap +0.106) over n=5664. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.186 vs market 0.077 (gap +0.109) over n=5214. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.154 vs market 0.061 (gap +0.094) over n=5610. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.172 vs market 0.064 (gap +0.108) over n=6282. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.149 vs market 0.056 (gap +0.093) over n=6732. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.185 vs market 0.062 (gap +0.123) over n=6258. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.146 vs market 0.078 (gap +0.067) over n=5640. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.171 vs market 0.072 (gap +0.099) over n=6366. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.155 vs market 0.068 (gap +0.087) over n=6432. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.175 vs market 0.069 (gap +0.106) over n=5634. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.183 vs market 0.066 (gap +0.116) over n=6186. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.173 vs market 0.065 (gap +0.108) over n=6462. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.165 vs market 0.068 (gap +0.097) over n=6852. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.174 vs market 0.074 (gap +0.100) over n=7050. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.173 vs market 0.071 (gap +0.101) over n=7026. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.190 vs market 0.070 (gap +0.120) over n=5952. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.113 vs ECMWF 0.238 (gap 0.125) over n=804. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.122 vs ECMWF 0.213 (gap 0.090) over n=186. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.119 vs ECMWF 0.219 (gap 0.101) over n=1434. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.132 vs ECMWF 0.186 (gap 0.054) over n=714. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.132 vs ECMWF 0.188 (gap 0.056) over n=168. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.135 vs ECMWF 0.182 (gap 0.047) over n=1380. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.123 vs ECMWF 0.219 (gap 0.096) over n=732. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.194 (gap 0.070) over n=234. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.193 (gap 0.067) over n=1494. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.120 vs ECMWF 0.144 (gap 0.025) over n=804. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.130 vs ECMWF 0.171 (gap 0.041) over n=726. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.126 vs ECMWF 0.148 (gap 0.022) over n=234. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.155 (gap 0.028) over n=1476. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 0-6h | NBM lower Brier 0.159 vs ECMWF 0.181 (gap 0.022) over n=678. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 24-72h | NBM lower Brier 0.149 vs ECMWF 0.179 (gap 0.029) over n=336. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.154 vs ECMWF 0.181 (gap 0.027) over n=1290. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.131 vs ECMWF 0.193 (gap 0.061) over n=666. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 24-72h | NBM lower Brier 0.138 vs ECMWF 0.178 (gap 0.040) over n=258. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.136 vs ECMWF 0.187 (gap 0.052) over n=1368. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.115 vs ECMWF 0.161 (gap 0.045) over n=1158. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.120 vs ECMWF 0.178 (gap 0.058) over n=504. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.117 vs ECMWF 0.171 (gap 0.054) over n=1356. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.138 vs ECMWF 0.186 (gap 0.048) over n=1176. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.127 vs ECMWF 0.202 (gap 0.075) over n=480. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.130 vs ECMWF 0.196 (gap 0.067) over n=1290. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 24-72h | NBM lower Brier 0.157 vs ECMWF 0.180 (gap 0.023) over n=264. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.126 vs ECMWF 0.183 (gap 0.057) over n=672. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.114 vs ECMWF 0.168 (gap 0.054) over n=1158. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.110 vs ECMWF 0.136 (gap 0.027) over n=204. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.114 vs ECMWF 0.143 (gap 0.029) over n=1356. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 0-6h | NBM lower Brier 0.148 vs ECMWF 0.195 (gap 0.046) over n=666. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 24-72h | NBM lower Brier 0.141 vs ECMWF 0.185 (gap 0.044) over n=204. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 6-24h | NBM lower Brier 0.138 vs ECMWF 0.194 (gap 0.056) over n=1410. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 0-6h | NBM lower Brier 0.144 vs ECMWF 0.184 (gap 0.040) over n=1374. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 0-6h | NBM lower Brier 0.117 vs ECMWF 0.201 (gap 0.084) over n=810. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 24-72h | NBM lower Brier 0.123 vs ECMWF 0.185 (gap 0.062) over n=186. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.183 (gap 0.060) over n=1464. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.114 vs ECMWF 0.188 (gap 0.074) over n=714. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.133 vs ECMWF 0.174 (gap 0.041) over n=360. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.120 vs ECMWF 0.185 (gap 0.065) over n=1386. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.109 vs ECMWF 0.190 (gap 0.081) over n=756. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.101 vs ECMWF 0.185 (gap 0.084) over n=288. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.109 vs ECMWF 0.193 (gap 0.084) over n=1464. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.127 vs ECMWF 0.194 (gap 0.068) over n=1344. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.134 vs ECMWF 0.190 (gap 0.056) over n=486. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.191 (gap 0.063) over n=1296. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.120 vs ECMWF 0.187 (gap 0.067) over n=1338. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.117 vs ECMWF 0.193 (gap 0.076) over n=474. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.121 vs ECMWF 0.185 (gap 0.064) over n=1272. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 0-6h | NBM lower Brier 0.175 vs ECMWF 0.207 (gap 0.032) over n=1062. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 24-72h | NBM lower Brier 0.164 vs ECMWF 0.191 (gap 0.027) over n=186. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 6-24h | NBM lower Brier 0.165 vs ECMWF 0.186 (gap 0.021) over n=1446. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.125 vs ECMWF 0.200 (gap 0.075) over n=804. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.136 vs ECMWF 0.197 (gap 0.061) over n=210. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.183 (gap 0.061) over n=1530. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
