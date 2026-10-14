# Model diagnostics

_Generated 2026-10-14 17:51 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**89 flag(s):** 10 warn, 79 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Dallas / low | Brier worsened 0.121 -> 0.175 (+0.055) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Denver / low | Brier worsened 0.174 -> 0.197 (+0.023) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Las Vegas / low | Brier worsened 0.171 -> 0.192 (+0.021) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Miami / low | Brier worsened 0.135 -> 0.183 (+0.048) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Minneapolis / low | Brier worsened 0.096 -> 0.202 (+0.107) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New Orleans / high | Brier worsened 0.142 -> 0.194 (+0.052) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New York City / high | Brier worsened 0.123 -> 0.185 (+0.062) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Oklahoma City / low | Brier worsened 0.147 -> 0.219 (+0.071) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Philadelphia / high | Brier worsened 0.137 -> 0.160 (+0.022) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | San Francisco / low | Brier worsened 0.165 -> 0.196 (+0.030) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | emos_improves_model | Chicago / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.152 vs model 0.198 vs market 0.060 over n=6012 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.140 vs model 0.229 vs market 0.069 over n=5430 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.171 vs model 0.210 vs market 0.039 over n=6054 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Miami / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.098 vs model 0.141 vs market 0.072 over n=4542 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.154 vs model 0.189 vs market 0.064 over n=5166 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.191 vs market 0.070 (gap +0.121) over n=10974. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.158 vs market 0.070 (gap +0.087) over n=10110. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.168 vs market 0.064 (gap +0.104) over n=9954. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.195 vs market 0.069 (gap +0.126) over n=11388. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.141 vs market 0.048 (gap +0.093) over n=12072. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.219 vs market 0.053 (gap +0.166) over n=11484. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.140 vs market 0.076 (gap +0.064) over n=10332. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.160 vs market 0.078 (gap +0.082) over n=12012. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.145 vs market 0.069 (gap +0.076) over n=12336. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.164 vs market 0.067 (gap +0.097) over n=10848. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.157 vs market 0.074 (gap +0.082) over n=11334. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.171 vs market 0.081 (gap +0.090) over n=9330. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.151 vs market 0.067 (gap +0.083) over n=12168. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.163 vs market 0.072 (gap +0.091) over n=13452. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.181 vs market 0.070 (gap +0.111) over n=13416. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.179 vs market 0.072 (gap +0.107) over n=11208. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.115 vs ECMWF 0.238 (gap 0.123) over n=1650. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.127 vs ECMWF 0.205 (gap 0.079) over n=426. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.121 vs ECMWF 0.211 (gap 0.090) over n=2604. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.116 vs ECMWF 0.167 (gap 0.051) over n=1506. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.122 vs ECMWF 0.167 (gap 0.045) over n=384. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.165 (gap 0.038) over n=2484. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.111 vs ECMWF 0.206 (gap 0.096) over n=1434. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.118 vs ECMWF 0.181 (gap 0.063) over n=528. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.118 vs ECMWF 0.196 (gap 0.077) over n=2682. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.116 vs ECMWF 0.140 (gap 0.024) over n=1338. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 24-72h | NBM lower Brier 0.130 vs ECMWF 0.153 (gap 0.022) over n=468. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.101 vs ECMWF 0.196 (gap 0.095) over n=1404. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.105 vs ECMWF 0.164 (gap 0.059) over n=564. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 6-24h | NBM lower Brier 0.101 vs ECMWF 0.169 (gap 0.069) over n=2736. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 24-72h | NBM lower Brier 0.152 vs ECMWF 0.178 (gap 0.025) over n=612. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.156 vs ECMWF 0.177 (gap 0.021) over n=2472. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 0-6h | NBM lower Brier 0.149 vs ECMWF 0.181 (gap 0.031) over n=2562. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 24-72h | NBM lower Brier 0.135 vs ECMWF 0.180 (gap 0.046) over n=528. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 6-24h | NBM lower Brier 0.147 vs ECMWF 0.170 (gap 0.023) over n=2544. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.092 vs ECMWF 0.223 (gap 0.131) over n=1338. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 24-72h | NBM lower Brier 0.102 vs ECMWF 0.215 (gap 0.113) over n=516. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.098 vs ECMWF 0.217 (gap 0.119) over n=2586. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.088 vs ECMWF 0.170 (gap 0.081) over n=2010. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.085 vs ECMWF 0.185 (gap 0.099) over n=936. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.083 vs ECMWF 0.188 (gap 0.104) over n=2622. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.113 vs ECMWF 0.223 (gap 0.109) over n=2058. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.120 vs ECMWF 0.204 (gap 0.084) over n=882. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.115 vs ECMWF 0.202 (gap 0.087) over n=2526. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.110 vs ECMWF 0.197 (gap 0.087) over n=1302. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.176 (gap 0.051) over n=606. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 6-24h | NBM lower Brier 0.120 vs ECMWF 0.160 (gap 0.040) over n=2784. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.114 vs ECMWF 0.153 (gap 0.039) over n=2202. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 0-6h | NBM lower Brier 0.143 vs ECMWF 0.191 (gap 0.049) over n=1464. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 24-72h | NBM lower Brier 0.137 vs ECMWF 0.171 (gap 0.034) over n=408. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 6-24h | NBM lower Brier 0.135 vs ECMWF 0.186 (gap 0.051) over n=2712. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 0-6h | NBM lower Brier 0.139 vs ECMWF 0.176 (gap 0.037) over n=2286. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 6-24h | NBM lower Brier 0.146 vs ECMWF 0.167 (gap 0.021) over n=2214. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 0-6h | NBM lower Brier 0.149 vs ECMWF 0.181 (gap 0.033) over n=1212. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 24-72h | NBM lower Brier 0.163 vs ECMWF 0.188 (gap 0.025) over n=324. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 6-24h | NBM lower Brier 0.152 vs ECMWF 0.188 (gap 0.035) over n=2136. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.120 vs ECMWF 0.172 (gap 0.052) over n=1404. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.127 vs ECMWF 0.175 (gap 0.048) over n=780. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.123 vs ECMWF 0.186 (gap 0.063) over n=2748. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.112 vs ECMWF 0.206 (gap 0.093) over n=1530. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.126 vs ECMWF 0.172 (gap 0.046) over n=618. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.123 vs ECMWF 0.176 (gap 0.053) over n=2940. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 24-72h | NBM lower Brier 0.150 vs ECMWF 0.174 (gap 0.024) over n=1110. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 6-24h | NBM lower Brier 0.146 vs ECMWF 0.172 (gap 0.026) over n=2808. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.101 vs ECMWF 0.155 (gap 0.054) over n=2310. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.115 vs ECMWF 0.146 (gap 0.031) over n=972. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.110 vs ECMWF 0.153 (gap 0.044) over n=2652. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 6-24h | NBM lower Brier 0.145 vs ECMWF 0.166 (gap 0.020) over n=2844. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.114 vs ECMWF 0.207 (gap 0.093) over n=2334. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.120 vs ECMWF 0.202 (gap 0.082) over n=942. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.208 (gap 0.085) over n=2586. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.121 vs ECMWF 0.197 (gap 0.076) over n=1632. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.137 vs ECMWF 0.180 (gap 0.043) over n=462. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.125 vs ECMWF 0.179 (gap 0.054) over n=2712. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
