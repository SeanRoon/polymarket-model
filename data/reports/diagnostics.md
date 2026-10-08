# Model diagnostics

_Generated 2026-10-08 19:13 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**95 flag(s):** 15 warn, 80 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Atlanta / high | Brier worsened 0.133 -> 0.195 (+0.061) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Atlanta / low | Brier worsened 0.209 -> 0.242 (+0.033) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Austin / low | Brier worsened 0.156 -> 0.193 (+0.037) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Boston / high | Brier worsened 0.161 -> 0.240 (+0.079) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Boston / low | Brier worsened 0.190 -> 0.239 (+0.049) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / low | Brier worsened 0.182 -> 0.244 (+0.062) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Dallas / high | Brier worsened 0.122 -> 0.178 (+0.055) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Denver / high | Brier worsened 0.031 -> 0.062 (+0.031) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Houston / low | Brier worsened 0.146 -> 0.203 (+0.057) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Las Vegas / high | Brier worsened 0.111 -> 0.172 (+0.061) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Miami / high | Brier worsened 0.148 -> 0.194 (+0.045) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New Orleans / low | Brier worsened 0.151 -> 0.189 (+0.038) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Oklahoma City / high | Brier worsened 0.138 -> 0.189 (+0.051) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Phoenix / low | Brier worsened 0.155 -> 0.224 (+0.068) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Seattle / low | Brier worsened 0.148 -> 0.179 (+0.030) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | emos_improves_model | Chicago / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.151 vs model 0.193 vs market 0.061 over n=6858 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.132 vs model 0.240 vs market 0.067 over n=6318 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.175 vs model 0.203 vs market 0.038 over n=6954 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Miami / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.098 vs model 0.136 vs market 0.071 over n=5010 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.154 vs model 0.189 vs market 0.064 over n=4944 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.190 vs market 0.071 (gap +0.120) over n=12630. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.153 vs market 0.068 (gap +0.085) over n=11634. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.172 vs market 0.061 (gap +0.111) over n=11556. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.193 vs market 0.071 (gap +0.122) over n=13116. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.139 vs market 0.055 (gap +0.084) over n=13944. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.221 vs market 0.052 (gap +0.168) over n=13272. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.138 vs market 0.075 (gap +0.063) over n=11640. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.161 vs market 0.075 (gap +0.086) over n=13920. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.137 vs market 0.067 (gap +0.070) over n=14256. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.164 vs market 0.067 (gap +0.097) over n=12438. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.155 vs market 0.073 (gap +0.082) over n=13272. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.174 vs market 0.075 (gap +0.099) over n=11172. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.150 vs market 0.072 (gap +0.078) over n=14088. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.158 vs market 0.071 (gap +0.087) over n=15510. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.184 vs market 0.071 (gap +0.114) over n=15522. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.186 vs market 0.075 (gap +0.111) over n=12888. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.114 vs ECMWF 0.237 (gap 0.123) over n=1914. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.128 vs ECMWF 0.202 (gap 0.074) over n=516. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.209 (gap 0.087) over n=2964. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.098 vs ECMWF 0.160 (gap 0.062) over n=1776. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.097 vs ECMWF 0.142 (gap 0.044) over n=462. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.109 vs ECMWF 0.153 (gap 0.043) over n=2808. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.117 vs ECMWF 0.204 (gap 0.087) over n=1674. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.119 vs ECMWF 0.178 (gap 0.060) over n=606. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.121 vs ECMWF 0.188 (gap 0.067) over n=3042. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.111 vs ECMWF 0.142 (gap 0.031) over n=1608. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 24-72h | NBM lower Brier 0.123 vs ECMWF 0.152 (gap 0.029) over n=570. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.092 vs ECMWF 0.202 (gap 0.110) over n=1632. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.105 vs ECMWF 0.169 (gap 0.064) over n=636. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 6-24h | NBM lower Brier 0.098 vs ECMWF 0.178 (gap 0.080) over n=3114. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 24-72h | NBM lower Brier 0.153 vs ECMWF 0.178 (gap 0.025) over n=702. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.156 vs ECMWF 0.179 (gap 0.023) over n=2808. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 0-6h | NBM lower Brier 0.155 vs ECMWF 0.175 (gap 0.020) over n=2970. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 24-72h | NBM lower Brier 0.140 vs ECMWF 0.177 (gap 0.037) over n=630. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.089 vs ECMWF 0.225 (gap 0.136) over n=1572. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 24-72h | NBM lower Brier 0.100 vs ECMWF 0.217 (gap 0.117) over n=606. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.097 vs ECMWF 0.216 (gap 0.119) over n=2922. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.100 vs ECMWF 0.159 (gap 0.060) over n=2292. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.090 vs ECMWF 0.178 (gap 0.088) over n=1044. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.091 vs ECMWF 0.181 (gap 0.091) over n=3006. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.114 vs ECMWF 0.214 (gap 0.101) over n=2358. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.199 (gap 0.075) over n=1002. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.123 vs ECMWF 0.201 (gap 0.077) over n=2898. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.113 vs ECMWF 0.201 (gap 0.087) over n=1524. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 24-72h | NBM lower Brier 0.129 vs ECMWF 0.180 (gap 0.051) over n=708. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 6-24h | NBM lower Brier 0.121 vs ECMWF 0.166 (gap 0.045) over n=3186. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.109 vs ECMWF 0.147 (gap 0.038) over n=2544. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.104 vs ECMWF 0.132 (gap 0.028) over n=534. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.108 vs ECMWF 0.133 (gap 0.025) over n=2838. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 0-6h | NBM lower Brier 0.136 vs ECMWF 0.193 (gap 0.057) over n=1728. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 24-72h | NBM lower Brier 0.132 vs ECMWF 0.165 (gap 0.033) over n=504. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 6-24h | NBM lower Brier 0.130 vs ECMWF 0.185 (gap 0.056) over n=3072. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 0-6h | NBM lower Brier 0.132 vs ECMWF 0.190 (gap 0.058) over n=1500. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 24-72h | NBM lower Brier 0.157 vs ECMWF 0.191 (gap 0.033) over n=420. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 6-24h | NBM lower Brier 0.148 vs ECMWF 0.191 (gap 0.043) over n=2520. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.127 vs ECMWF 0.173 (gap 0.046) over n=1626. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.135 vs ECMWF 0.177 (gap 0.042) over n=924. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.131 vs ECMWF 0.186 (gap 0.055) over n=3126. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.099 vs ECMWF 0.216 (gap 0.117) over n=1770. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.111 vs ECMWF 0.186 (gap 0.076) over n=744. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.109 vs ECMWF 0.187 (gap 0.078) over n=3348. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 24-72h | NBM lower Brier 0.148 vs ECMWF 0.170 (gap 0.022) over n=1266. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.100 vs ECMWF 0.150 (gap 0.050) over n=2652. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.115 vs ECMWF 0.138 (gap 0.023) over n=1134. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.109 vs ECMWF 0.151 (gap 0.043) over n=3066. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 0-6h | NBM lower Brier 0.139 vs ECMWF 0.167 (gap 0.028) over n=3438. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 24-72h | NBM lower Brier 0.149 vs ECMWF 0.171 (gap 0.021) over n=1260. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 6-24h | NBM lower Brier 0.141 vs ECMWF 0.162 (gap 0.021) over n=3270. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.128 vs ECMWF 0.212 (gap 0.084) over n=2682. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.127 vs ECMWF 0.199 (gap 0.072) over n=1122. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.132 vs ECMWF 0.208 (gap 0.076) over n=3000. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 0-6h | NBM lower Brier 0.172 vs ECMWF 0.194 (gap 0.021) over n=2472. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.118 vs ECMWF 0.206 (gap 0.088) over n=1890. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.140 vs ECMWF 0.185 (gap 0.045) over n=528. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.128 vs ECMWF 0.183 (gap 0.054) over n=3108. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
