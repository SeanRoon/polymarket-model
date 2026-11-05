# Model diagnostics

_Generated 2026-11-05 20:32 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**90 flag(s):** 10 warn, 80 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Atlanta / high | Brier worsened 0.101 -> 0.141 (+0.040) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Austin / high | Brier worsened 0.000 -> 0.042 (+0.042) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Austin / low | Brier worsened 0.193 -> 0.239 (+0.046) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Dallas / high | Brier worsened 0.138 -> 0.181 (+0.044) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Las Vegas / high | Brier worsened 0.111 -> 0.172 (+0.062) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Las Vegas / low | Brier worsened 0.118 -> 0.201 (+0.083) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Los Angeles / low | Brier worsened 0.173 -> 0.223 (+0.050) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Miami / low | Brier worsened 0.144 -> 0.173 (+0.029) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Phoenix / high | Brier worsened 0.156 -> 0.196 (+0.040) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | San Antonio / high | Brier worsened 0.000 -> 0.028 (+0.028) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | emos_improves_model | Chicago / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.160 vs model 0.199 vs market 0.071 over n=3072 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.136 vs model 0.173 vs market 0.062 over n=2844 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.131 vs model 0.153 vs market 0.065 over n=2580 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.163 vs model 0.205 vs market 0.077 over n=2724 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.177 vs market 0.068 (gap +0.109) over n=5448. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.190 vs market 0.075 (gap +0.116) over n=5124. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.157 vs market 0.060 (gap +0.097) over n=5358. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.171 vs market 0.063 (gap +0.108) over n=5994. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.161 vs market 0.061 (gap +0.100) over n=6336. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.180 vs market 0.061 (gap +0.119) over n=5922. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.148 vs market 0.076 (gap +0.072) over n=5364. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.170 vs market 0.071 (gap +0.100) over n=6090. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.156 vs market 0.066 (gap +0.090) over n=6030. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.179 vs market 0.071 (gap +0.108) over n=5304. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.185 vs market 0.065 (gap +0.119) over n=5832. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.173 vs market 0.063 (gap +0.110) over n=6108. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.172 vs market 0.068 (gap +0.104) over n=6444. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.176 vs market 0.074 (gap +0.102) over n=6678. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.168 vs market 0.071 (gap +0.097) over n=6630. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.195 vs market 0.064 (gap +0.131) over n=5694. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.117 vs ECMWF 0.236 (gap 0.119) over n=750. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.130 vs ECMWF 0.210 (gap 0.080) over n=168. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.120 vs ECMWF 0.217 (gap 0.097) over n=1386. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.131 vs ECMWF 0.195 (gap 0.064) over n=696. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.135 vs ECMWF 0.190 (gap 0.055) over n=162. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.136 vs ECMWF 0.191 (gap 0.055) over n=1344. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.133 vs ECMWF 0.217 (gap 0.084) over n=690. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.133 vs ECMWF 0.200 (gap 0.066) over n=222. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.133 vs ECMWF 0.190 (gap 0.058) over n=1392. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.117 vs ECMWF 0.150 (gap 0.033) over n=762. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 24-72h | NBM lower Brier 0.123 vs ECMWF 0.144 (gap 0.020) over n=234. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.128 vs ECMWF 0.174 (gap 0.047) over n=702. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.125 vs ECMWF 0.148 (gap 0.023) over n=228. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 6-24h | NBM lower Brier 0.128 vs ECMWF 0.152 (gap 0.024) over n=1398. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 0-6h | NBM lower Brier 0.158 vs ECMWF 0.180 (gap 0.023) over n=642. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 24-72h | NBM lower Brier 0.148 vs ECMWF 0.174 (gap 0.026) over n=318. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.154 vs ECMWF 0.180 (gap 0.026) over n=1236. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.141 vs ECMWF 0.182 (gap 0.041) over n=642. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 24-72h | NBM lower Brier 0.143 vs ECMWF 0.174 (gap 0.032) over n=240. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.140 vs ECMWF 0.178 (gap 0.038) over n=1302. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.132 vs ECMWF 0.178 (gap 0.046) over n=1086. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.128 vs ECMWF 0.186 (gap 0.058) over n=474. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.128 vs ECMWF 0.185 (gap 0.057) over n=1284. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.133 vs ECMWF 0.180 (gap 0.047) over n=1110. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.127 vs ECMWF 0.201 (gap 0.075) over n=450. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.128 vs ECMWF 0.195 (gap 0.067) over n=1254. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Miami / low / 0-6h | NBM lower Brier 0.133 vs ECMWF 0.154 (gap 0.021) over n=666. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Miami / low / 6-24h | NBM lower Brier 0.136 vs ECMWF 0.158 (gap 0.022) over n=1422. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.124 vs ECMWF 0.171 (gap 0.048) over n=648. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / low / 0-6h | NBM lower Brier 0.158 vs ECMWF 0.180 (gap 0.023) over n=672. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / low / 24-72h | NBM lower Brier 0.151 vs ECMWF 0.177 (gap 0.026) over n=234. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / low / 6-24h | NBM lower Brier 0.144 vs ECMWF 0.168 (gap 0.024) over n=1230. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.122 vs ECMWF 0.170 (gap 0.048) over n=1068. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.112 vs ECMWF 0.138 (gap 0.026) over n=186. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.121 vs ECMWF 0.141 (gap 0.020) over n=1320. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 0-6h | NBM lower Brier 0.147 vs ECMWF 0.207 (gap 0.060) over n=606. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 24-72h | NBM lower Brier 0.141 vs ECMWF 0.192 (gap 0.051) over n=180. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 6-24h | NBM lower Brier 0.140 vs ECMWF 0.202 (gap 0.062) over n=1320. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 0-6h | NBM lower Brier 0.141 vs ECMWF 0.189 (gap 0.049) over n=1302. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 6-24h | NBM lower Brier 0.147 vs ECMWF 0.171 (gap 0.024) over n=1128. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 0-6h | NBM lower Brier 0.119 vs ECMWF 0.198 (gap 0.079) over n=750. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 24-72h | NBM lower Brier 0.125 vs ECMWF 0.190 (gap 0.065) over n=168. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.185 (gap 0.063) over n=1392. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.119 vs ECMWF 0.194 (gap 0.074) over n=678. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.137 vs ECMWF 0.177 (gap 0.040) over n=318. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.123 vs ECMWF 0.192 (gap 0.069) over n=1308. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.105 vs ECMWF 0.184 (gap 0.079) over n=714. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.095 vs ECMWF 0.173 (gap 0.078) over n=276. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.105 vs ECMWF 0.187 (gap 0.082) over n=1374. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.118 vs ECMWF 0.196 (gap 0.078) over n=1266. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.123 vs ECMWF 0.182 (gap 0.059) over n=462. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.116 vs ECMWF 0.191 (gap 0.075) over n=1260. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.122 vs ECMWF 0.184 (gap 0.062) over n=1254. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.121 vs ECMWF 0.189 (gap 0.069) over n=444. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.179 (gap 0.055) over n=1224. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 0-6h | NBM lower Brier 0.175 vs ECMWF 0.215 (gap 0.040) over n=1056. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 24-72h | NBM lower Brier 0.165 vs ECMWF 0.197 (gap 0.032) over n=174. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.111 vs ECMWF 0.202 (gap 0.092) over n=738. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.203 (gap 0.079) over n=186. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.112 vs ECMWF 0.189 (gap 0.077) over n=1476. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
