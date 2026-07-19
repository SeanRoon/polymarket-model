# Model diagnostics

_Generated 2026-07-19 14:24 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**77 flag(s):** 1 critical, 6 warn, 70 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| critical | exclude_candidate | Chicago (KMDW) | Model worse than market and losing: Brier 0.164 vs 0.076 (gap +0.088), PnL -21.75 over n=11760. | Consider adding KMDW to signal_excluded_stations until calibration improves. |
| warn | regression_wow | Chicago / high | Brier worsened 0.136 -> 0.223 (+0.086) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Denver / low | Brier worsened 0.183 -> 0.220 (+0.037) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New Orleans / low | Brier worsened 0.108 -> 0.132 (+0.024) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New York City / high | Brier worsened 0.101 -> 0.202 (+0.101) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | San Francisco / low | Brier worsened 0.142 -> 0.191 (+0.050) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Washington DC / high | Brier worsened 0.144 -> 0.227 (+0.083) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | emos_improves_model | Chicago / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.142 vs model 0.192 vs market 0.099 over n=228 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Chicago / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.182 vs model 0.218 vs market 0.065 over n=258 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.104 vs model 0.294 vs market 0.102 over n=156 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.182 vs market 0.078 (gap +0.104) over n=5802. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.102 vs market 0.055 (gap +0.047) over n=5580. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.166 vs market 0.074 (gap +0.092) over n=5940. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.152 vs market 0.072 (gap +0.079) over n=6348. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.169 vs market 0.047 (gap +0.122) over n=6684. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.227 vs market 0.059 (gap +0.168) over n=8694. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.142 vs market 0.062 (gap +0.079) over n=4776. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.167 vs market 0.079 (gap +0.088) over n=6516. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.130 vs market 0.073 (gap +0.057) over n=6336. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.178 vs market 0.071 (gap +0.107) over n=5268. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.143 vs market 0.075 (gap +0.068) over n=6384. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.207 vs market 0.059 (gap +0.149) over n=222. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.151 vs market 0.072 (gap +0.079) over n=6600. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.180 vs market 0.076 (gap +0.104) over n=6768. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.173 vs market 0.083 (gap +0.089) over n=6816. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.184 vs market 0.073 (gap +0.110) over n=5610. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.095 vs ECMWF 0.224 (gap 0.129) over n=924. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.116 vs ECMWF 0.204 (gap 0.088) over n=252. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.115 vs ECMWF 0.205 (gap 0.090) over n=1428. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Austin / low / 24-72h | NBM lower Brier 0.136 vs ECMWF 0.166 (gap 0.031) over n=372. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.060 vs ECMWF 0.102 (gap 0.042) over n=924. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.052 vs ECMWF 0.075 (gap 0.023) over n=252. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.058 vs ECMWF 0.084 (gap 0.027) over n=1446. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.139 vs ECMWF 0.163 (gap 0.024) over n=2640. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 24-72h | NBM lower Brier 0.141 vs ECMWF 0.161 (gap 0.021) over n=630. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.124 vs ECMWF 0.175 (gap 0.051) over n=1512. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.128 vs ECMWF 0.158 (gap 0.030) over n=2574. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.111 vs ECMWF 0.209 (gap 0.098) over n=834. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.145 vs ECMWF 0.168 (gap 0.023) over n=372. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 6-24h | NBM lower Brier 0.131 vs ECMWF 0.180 (gap 0.049) over n=1422. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.104 vs ECMWF 0.200 (gap 0.096) over n=816. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 24-72h | NBM lower Brier 0.104 vs ECMWF 0.199 (gap 0.095) over n=288. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.104 vs ECMWF 0.198 (gap 0.095) over n=1326. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.082 vs ECMWF 0.204 (gap 0.122) over n=1188. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.076 vs ECMWF 0.216 (gap 0.141) over n=516. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.085 vs ECMWF 0.222 (gap 0.137) over n=1338. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.098 vs ECMWF 0.187 (gap 0.089) over n=1104. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.102 vs ECMWF 0.180 (gap 0.078) over n=480. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.111 vs ECMWF 0.206 (gap 0.095) over n=1296. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 0-6h | NBM lower Brier 0.123 vs ECMWF 0.144 (gap 0.022) over n=1590. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 24-72h | NBM lower Brier 0.128 vs ECMWF 0.168 (gap 0.041) over n=342. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.160 (gap 0.033) over n=1320. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.121 vs ECMWF 0.193 (gap 0.073) over n=840. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 24-72h | NBM lower Brier 0.125 vs ECMWF 0.160 (gap 0.035) over n=318. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 6-24h | NBM lower Brier 0.125 vs ECMWF 0.168 (gap 0.043) over n=1332. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.121 vs ECMWF 0.175 (gap 0.054) over n=2322. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.116 vs ECMWF 0.179 (gap 0.063) over n=414. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.121 vs ECMWF 0.178 (gap 0.057) over n=2424. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 0-6h | NBM lower Brier 0.110 vs ECMWF 0.133 (gap 0.022) over n=1590. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 24-72h | NBM lower Brier 0.114 vs ECMWF 0.137 (gap 0.023) over n=360. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 6-24h | NBM lower Brier 0.113 vs ECMWF 0.134 (gap 0.021) over n=1386. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.105 vs ECMWF 0.160 (gap 0.055) over n=792. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.110 vs ECMWF 0.164 (gap 0.054) over n=372. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.105 vs ECMWF 0.173 (gap 0.068) over n=1206. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.084 vs ECMWF 0.240 (gap 0.156) over n=876. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.095 vs ECMWF 0.238 (gap 0.143) over n=294. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.097 vs ECMWF 0.230 (gap 0.133) over n=1272. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.092 vs ECMWF 0.186 (gap 0.094) over n=1272. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.102 vs ECMWF 0.193 (gap 0.091) over n=492. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.095 vs ECMWF 0.188 (gap 0.093) over n=1278. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 0-6h | NBM lower Brier 0.135 vs ECMWF 0.157 (gap 0.022) over n=1548. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.096 vs ECMWF 0.175 (gap 0.078) over n=1302. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.109 vs ECMWF 0.205 (gap 0.096) over n=474. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.100 vs ECMWF 0.195 (gap 0.095) over n=1272. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.120 vs ECMWF 0.210 (gap 0.091) over n=906. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.133 vs ECMWF 0.170 (gap 0.037) over n=204. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.130 vs ECMWF 0.182 (gap 0.052) over n=1368. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
