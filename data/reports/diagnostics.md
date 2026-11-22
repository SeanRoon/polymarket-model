# Model diagnostics

_Generated 2026-11-22 20:14 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**95 flag(s):** 16 warn, 79 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Austin / high | Brier worsened 0.003 -> 0.047 (+0.044) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Boston / high | Brier worsened 0.148 -> 0.246 (+0.098) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / high | Brier worsened 0.212 -> 0.262 (+0.049) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / low | Brier worsened 0.173 -> 0.232 (+0.058) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Dallas / high | Brier worsened 0.188 -> 0.255 (+0.068) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Dallas / low | Brier worsened 0.169 -> 0.194 (+0.024) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Houston / low | Brier worsened 0.146 -> 0.190 (+0.044) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Las Vegas / high | Brier worsened 0.121 -> 0.166 (+0.046) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Minneapolis / high | Brier worsened 0.154 -> 0.181 (+0.026) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Minneapolis / low | Brier worsened 0.117 -> 0.190 (+0.073) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New Orleans / low | Brier worsened 0.145 -> 0.245 (+0.100) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New York City / high | Brier worsened 0.133 -> 0.270 (+0.137) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Philadelphia / high | Brier worsened 0.153 -> 0.223 (+0.069) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Philadelphia / low | Brier worsened 0.179 -> 0.211 (+0.032) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | San Antonio / high | Brier worsened 0.004 -> 0.032 (+0.027) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Seattle / high | Brier worsened 0.133 -> 0.160 (+0.027) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | emos_improves_model | Chicago / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.162 vs model 0.204 vs market 0.064 over n=2610 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.132 vs model 0.156 vs market 0.060 over n=2406 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.163 vs model 0.196 vs market 0.059 over n=2676 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Miami / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.139 vs model 0.169 vs market 0.076 over n=2412 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.136 vs model 0.158 vs market 0.066 over n=2154 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.166 vs model 0.221 vs market 0.070 over n=2268 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.178 vs market 0.064 (gap +0.114) over n=4566. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.195 vs market 0.071 (gap +0.124) over n=4380. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.161 vs market 0.067 (gap +0.094) over n=4650. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.169 vs market 0.064 (gap +0.106) over n=5124. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.157 vs market 0.061 (gap +0.096) over n=5388. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.177 vs market 0.059 (gap +0.118) over n=5082. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.159 vs market 0.073 (gap +0.086) over n=4548. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.169 vs market 0.070 (gap +0.100) over n=5130. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.160 vs market 0.066 (gap +0.094) over n=5100. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.191 vs market 0.068 (gap +0.123) over n=4422. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.190 vs market 0.064 (gap +0.127) over n=5388. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.176 vs market 0.060 (gap +0.116) over n=5142. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.176 vs market 0.063 (gap +0.113) over n=5412. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.173 vs market 0.077 (gap +0.096) over n=5676. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.162 vs market 0.076 (gap +0.086) over n=5496. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.194 vs market 0.062 (gap +0.132) over n=4818. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.146 vs ECMWF 0.216 (gap 0.070) over n=630. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.146 vs ECMWF 0.212 (gap 0.066) over n=120. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.133 vs ECMWF 0.209 (gap 0.076) over n=1188. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Austin / low / 0-6h | NBM lower Brier 0.161 vs ECMWF 0.187 (gap 0.027) over n=552. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Austin / low / 24-72h | NBM lower Brier 0.147 vs ECMWF 0.189 (gap 0.042) over n=174. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Austin / low / 6-24h | NBM lower Brier 0.147 vs ECMWF 0.191 (gap 0.044) over n=1152. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.126 vs ECMWF 0.205 (gap 0.079) over n=588. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.144 vs ECMWF 0.185 (gap 0.041) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.132 vs ECMWF 0.202 (gap 0.070) over n=1146. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.140 vs ECMWF 0.224 (gap 0.084) over n=570. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.131 vs ECMWF 0.217 (gap 0.086) over n=192. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.133 vs ECMWF 0.198 (gap 0.064) over n=1188. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.142 vs ECMWF 0.168 (gap 0.026) over n=642. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.140 vs ECMWF 0.166 (gap 0.026) over n=576. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.123 vs ECMWF 0.170 (gap 0.047) over n=192. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 0-6h | NBM lower Brier 0.156 vs ECMWF 0.187 (gap 0.031) over n=546. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 24-72h | NBM lower Brier 0.138 vs ECMWF 0.188 (gap 0.049) over n=246. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.153 vs ECMWF 0.184 (gap 0.031) over n=1104. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.136 vs ECMWF 0.171 (gap 0.035) over n=918. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.127 vs ECMWF 0.180 (gap 0.052) over n=384. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.133 vs ECMWF 0.168 (gap 0.035) over n=1110. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.126 vs ECMWF 0.189 (gap 0.063) over n=930. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.113 vs ECMWF 0.206 (gap 0.093) over n=372. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.114 vs ECMWF 0.205 (gap 0.091) over n=1122. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Miami / low / 0-6h | NBM lower Brier 0.143 vs ECMWF 0.170 (gap 0.027) over n=564. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Miami / low / 24-72h | NBM lower Brier 0.150 vs ECMWF 0.175 (gap 0.025) over n=162. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Miami / low / 6-24h | NBM lower Brier 0.142 vs ECMWF 0.172 (gap 0.031) over n=1218. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.129 vs ECMWF 0.156 (gap 0.027) over n=540. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / low / 0-6h | NBM lower Brier 0.159 vs ECMWF 0.197 (gap 0.038) over n=558. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / low / 6-24h | NBM lower Brier 0.141 vs ECMWF 0.186 (gap 0.044) over n=1062. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.139 vs ECMWF 0.178 (gap 0.039) over n=906. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 0-6h | NBM lower Brier 0.146 vs ECMWF 0.239 (gap 0.093) over n=516. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 24-72h | NBM lower Brier 0.145 vs ECMWF 0.204 (gap 0.059) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 6-24h | NBM lower Brier 0.146 vs ECMWF 0.218 (gap 0.072) over n=1068. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 0-6h | NBM lower Brier 0.142 vs ECMWF 0.191 (gap 0.049) over n=1314. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 24-72h | NBM lower Brier 0.152 vs ECMWF 0.187 (gap 0.036) over n=192. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 6-24h | NBM lower Brier 0.147 vs ECMWF 0.177 (gap 0.030) over n=1182. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 0-6h | NBM lower Brier 0.122 vs ECMWF 0.202 (gap 0.080) over n=630. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 24-72h | NBM lower Brier 0.118 vs ECMWF 0.189 (gap 0.071) over n=126. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 6-24h | NBM lower Brier 0.118 vs ECMWF 0.190 (gap 0.071) over n=1176. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.117 vs ECMWF 0.204 (gap 0.087) over n=564. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.140 vs ECMWF 0.182 (gap 0.042) over n=252. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.199 (gap 0.077) over n=1128. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.117 vs ECMWF 0.187 (gap 0.070) over n=594. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.098 vs ECMWF 0.170 (gap 0.072) over n=204. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.114 vs ECMWF 0.181 (gap 0.066) over n=1158. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.133 vs ECMWF 0.192 (gap 0.059) over n=1050. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.131 vs ECMWF 0.172 (gap 0.040) over n=354. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.182 (gap 0.055) over n=1056. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.136 vs ECMWF 0.180 (gap 0.045) over n=1038. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.129 vs ECMWF 0.178 (gap 0.048) over n=342. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.139 vs ECMWF 0.165 (gap 0.026) over n=1038. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 0-6h | NBM lower Brier 0.178 vs ECMWF 0.210 (gap 0.032) over n=948. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 24-72h | NBM lower Brier 0.174 vs ECMWF 0.202 (gap 0.028) over n=126. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.109 vs ECMWF 0.202 (gap 0.094) over n=624. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.116 vs ECMWF 0.200 (gap 0.084) over n=150. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.105 vs ECMWF 0.191 (gap 0.086) over n=1224. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
