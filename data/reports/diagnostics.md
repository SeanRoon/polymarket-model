# Model diagnostics

_Generated 2026-08-17 13:42 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**87 flag(s):** 9 warn, 1 good, 77 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Atlanta / high | Brier worsened 0.133 -> 0.192 (+0.059) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Austin / low | Brier worsened 0.166 -> 0.202 (+0.036) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Boston / low | Brier worsened 0.069 -> 0.140 (+0.070) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Miami / high | Brier worsened 0.071 -> 0.151 (+0.079) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New Orleans / low | Brier worsened 0.101 -> 0.131 (+0.029) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Oklahoma City / high | Brier worsened 0.111 -> 0.170 (+0.059) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Philadelphia / high | Brier worsened 0.147 -> 0.202 (+0.055) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Seattle / high | Brier worsened 0.107 -> 0.127 (+0.021) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Seattle / low | Brier worsened 0.170 -> 0.248 (+0.078) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| good | emos_beats_market | New York City / low | EMOS pilot at/above market out-of-sample: EMOS Brier 0.115 vs model 0.041 vs market 0.180 over n=138 (same rows). | If this holds for ~30 days of settlements, candidate to promote emos_p for this cell (human decision; live cities stay out per operator mandate). |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.113 vs model 0.270 vs market 0.056 over n=4314 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Miami / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.174 vs model 0.255 vs market 0.004 over n=132 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.191 vs market 0.074 (gap +0.117) over n=13692. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.106 vs market 0.053 (gap +0.053) over n=12834. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.180 vs market 0.062 (gap +0.118) over n=13680. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.165 vs market 0.073 (gap +0.092) over n=14838. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.154 vs market 0.055 (gap +0.099) over n=15702. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.224 vs market 0.052 (gap +0.172) over n=14484. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.145 vs market 0.068 (gap +0.077) over n=9828. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.167 vs market 0.076 (gap +0.092) over n=15294. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.134 vs market 0.065 (gap +0.070) over n=15420. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.168 vs market 0.077 (gap +0.090) over n=10410. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.151 vs market 0.074 (gap +0.077) over n=15606. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.178 vs market 0.070 (gap +0.108) over n=9270. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.154 vs market 0.078 (gap +0.076) over n=15486. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.169 vs market 0.068 (gap +0.101) over n=16434. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.171 vs market 0.076 (gap +0.095) over n=16650. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.191 vs market 0.073 (gap +0.118) over n=13920. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.099 vs ECMWF 0.231 (gap 0.132) over n=2238. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.116 vs ECMWF 0.206 (gap 0.090) over n=564. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.111 vs ECMWF 0.210 (gap 0.099) over n=3222. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Austin / low / 6-24h | NBM lower Brier 0.154 vs ECMWF 0.175 (gap 0.021) over n=3276. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.043 vs ECMWF 0.097 (gap 0.055) over n=2238. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.033 vs ECMWF 0.059 (gap 0.027) over n=522. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.042 vs ECMWF 0.074 (gap 0.033) over n=3096. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.127 vs ECMWF 0.184 (gap 0.058) over n=2010. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.125 vs ECMWF 0.159 (gap 0.033) over n=732. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.166 (gap 0.043) over n=3174. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.113 vs ECMWF 0.141 (gap 0.028) over n=2286. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 24-72h | NBM lower Brier 0.120 vs ECMWF 0.149 (gap 0.029) over n=768. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.144 (gap 0.020) over n=3006. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.103 vs ECMWF 0.223 (gap 0.120) over n=1974. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.133 vs ECMWF 0.179 (gap 0.046) over n=708. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 6-24h | NBM lower Brier 0.115 vs ECMWF 0.196 (gap 0.081) over n=3234. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.092 vs ECMWF 0.220 (gap 0.127) over n=1908. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 24-72h | NBM lower Brier 0.101 vs ECMWF 0.218 (gap 0.117) over n=696. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.099 vs ECMWF 0.216 (gap 0.118) over n=3084. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.099 vs ECMWF 0.186 (gap 0.087) over n=2688. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.085 vs ECMWF 0.202 (gap 0.117) over n=1182. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.098 vs ECMWF 0.204 (gap 0.106) over n=3168. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.113 vs ECMWF 0.190 (gap 0.078) over n=2664. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.118 vs ECMWF 0.178 (gap 0.060) over n=1122. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.129 vs ECMWF 0.197 (gap 0.068) over n=3072. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Miami / low / 0-6h | NBM lower Brier 0.123 vs ECMWF 0.171 (gap 0.048) over n=1194. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Miami / low / 6-24h | NBM lower Brier 0.141 vs ECMWF 0.165 (gap 0.024) over n=1938. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 6-24h | NBM lower Brier 0.134 vs ECMWF 0.161 (gap 0.026) over n=3144. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.127 vs ECMWF 0.196 (gap 0.068) over n=1902. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 24-72h | NBM lower Brier 0.129 vs ECMWF 0.174 (gap 0.045) over n=786. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 6-24h | NBM lower Brier 0.126 vs ECMWF 0.173 (gap 0.047) over n=3288. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.115 vs ECMWF 0.150 (gap 0.034) over n=2634. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.125 vs ECMWF 0.167 (gap 0.042) over n=552. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.163 (gap 0.041) over n=2910. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 0-6h | NBM lower Brier 0.130 vs ECMWF 0.195 (gap 0.066) over n=1254. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 24-72h | NBM lower Brier 0.130 vs ECMWF 0.159 (gap 0.030) over n=336. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.173 (gap 0.048) over n=1890. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 0-6h | NBM lower Brier 0.117 vs ECMWF 0.192 (gap 0.075) over n=1368. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 24-72h | NBM lower Brier 0.128 vs ECMWF 0.190 (gap 0.061) over n=354. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 6-24h | NBM lower Brier 0.123 vs ECMWF 0.182 (gap 0.060) over n=1974. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.110 vs ECMWF 0.178 (gap 0.069) over n=1860. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.122 vs ECMWF 0.177 (gap 0.055) over n=990. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.117 vs ECMWF 0.187 (gap 0.070) over n=3156. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.077 vs ECMWF 0.241 (gap 0.164) over n=2106. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.093 vs ECMWF 0.225 (gap 0.133) over n=816. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.086 vs ECMWF 0.231 (gap 0.144) over n=3366. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 0-6h | NBM lower Brier 0.140 vs ECMWF 0.161 (gap 0.021) over n=3714. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 24-72h | NBM lower Brier 0.143 vs ECMWF 0.165 (gap 0.021) over n=1338. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.090 vs ECMWF 0.177 (gap 0.087) over n=3042. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.106 vs ECMWF 0.183 (gap 0.077) over n=1188. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.096 vs ECMWF 0.186 (gap 0.089) over n=3150. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 0-6h | NBM lower Brier 0.122 vs ECMWF 0.143 (gap 0.021) over n=3810. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.119 vs ECMWF 0.206 (gap 0.087) over n=3072. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.120 vs ECMWF 0.191 (gap 0.071) over n=1182. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.195 (gap 0.074) over n=3144. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 0-6h | NBM lower Brier 0.171 vs ECMWF 0.191 (gap 0.021) over n=2976. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.113 vs ECMWF 0.209 (gap 0.096) over n=2148. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.132 vs ECMWF 0.173 (gap 0.042) over n=522. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.184 (gap 0.060) over n=3228. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
