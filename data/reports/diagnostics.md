# Model diagnostics

_Generated 2026-10-23 17:47 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**95 flag(s):** 19 warn, 76 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| warn | regression_wow | Atlanta / low | Brier worsened 0.184 -> 0.235 (+0.050) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Boston / high | Brier worsened 0.148 -> 0.197 (+0.049) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Boston / low | Brier worsened 0.139 -> 0.160 (+0.021) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / high | Brier worsened 0.162 -> 0.215 (+0.052) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Chicago / low | Brier worsened 0.174 -> 0.242 (+0.068) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Denver / low | Brier worsened 0.184 -> 0.206 (+0.021) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Houston / high | Brier worsened 0.153 -> 0.193 (+0.040) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Los Angeles / low | Brier worsened 0.150 -> 0.228 (+0.078) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Miami / low | Brier worsened 0.144 -> 0.188 (+0.045) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Minneapolis / high | Brier worsened 0.142 -> 0.235 (+0.093) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Minneapolis / low | Brier worsened 0.147 -> 0.201 (+0.054) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New Orleans / low | Brier worsened 0.153 -> 0.266 (+0.112) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | New York City / low | Brier worsened 0.210 -> 0.257 (+0.046) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Oklahoma City / high | Brier worsened 0.165 -> 0.241 (+0.076) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Philadelphia / low | Brier worsened 0.160 -> 0.200 (+0.040) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Phoenix / high | Brier worsened 0.161 -> 0.189 (+0.027) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | San Francisco / low | Brier worsened 0.191 -> 0.247 (+0.056) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Seattle / high | Brier worsened 0.132 -> 0.180 (+0.048) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| warn | regression_wow | Seattle / low | Brier worsened 0.147 -> 0.213 (+0.066) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| info | emos_improves_model | Chicago / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.158 vs model 0.206 vs market 0.066 over n=3792 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.137 vs model 0.190 vs market 0.064 over n=3282 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Los Angeles / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.174 vs model 0.203 vs market 0.057 over n=3684 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | Miami / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.119 vs model 0.145 vs market 0.074 over n=3072 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / high | EMOS beats the raw model but not yet the market: EMOS Brier 0.128 vs model 0.157 vs market 0.062 over n=3204 (same rows). | Keep accruing; no action until the market gap closes. |
| info | emos_improves_model | New York City / low | EMOS beats the raw model but not yet the market: EMOS Brier 0.166 vs model 0.206 vs market 0.068 over n=3444 (same rows). | Keep accruing; no action until the market gap closes. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.180 vs market 0.069 (gap +0.111) over n=6642. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.188 vs market 0.075 (gap +0.113) over n=6234. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.157 vs market 0.067 (gap +0.090) over n=6336. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.178 vs market 0.063 (gap +0.116) over n=7290. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.141 vs market 0.050 (gap +0.091) over n=7566. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.197 vs market 0.060 (gap +0.137) over n=6966. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.141 vs market 0.079 (gap +0.061) over n=6660. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.172 vs market 0.070 (gap +0.102) over n=7398. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.147 vs market 0.074 (gap +0.073) over n=7500. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.182 vs market 0.065 (gap +0.117) over n=6648. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.170 vs market 0.069 (gap +0.100) over n=7032. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Philadelphia (KPHL) | Still miscalibrated: model Brier 0.166 vs market 0.066 (gap +0.100) over n=7650. | Keep KPHL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.166 vs market 0.067 (gap +0.099) over n=7494. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.168 vs market 0.077 (gap +0.091) over n=8220. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.181 vs market 0.072 (gap +0.108) over n=8184. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.192 vs market 0.072 (gap +0.120) over n=6918. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.105 vs ECMWF 0.235 (gap 0.130) over n=912. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 24-72h | NBM lower Brier 0.114 vs ECMWF 0.210 (gap 0.096) over n=264. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.110 vs ECMWF 0.215 (gap 0.105) over n=1656. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.133 vs ECMWF 0.192 (gap 0.059) over n=828. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 24-72h | NBM lower Brier 0.128 vs ECMWF 0.199 (gap 0.071) over n=240. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 6-24h | NBM lower Brier 0.138 vs ECMWF 0.188 (gap 0.050) over n=1602. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 0-6h | NBM lower Brier 0.120 vs ECMWF 0.223 (gap 0.103) over n=828. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 24-72h | NBM lower Brier 0.117 vs ECMWF 0.202 (gap 0.085) over n=324. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / low / 6-24h | NBM lower Brier 0.121 vs ECMWF 0.198 (gap 0.077) over n=1722. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.121 vs ECMWF 0.147 (gap 0.026) over n=864. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.122 vs ECMWF 0.177 (gap 0.055) over n=810. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 24-72h | NBM lower Brier 0.118 vs ECMWF 0.158 (gap 0.039) over n=318. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 6-24h | NBM lower Brier 0.119 vs ECMWF 0.153 (gap 0.034) over n=1716. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 0-6h | NBM lower Brier 0.167 vs ECMWF 0.193 (gap 0.026) over n=762. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 24-72h | NBM lower Brier 0.152 vs ECMWF 0.183 (gap 0.031) over n=420. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.160 vs ECMWF 0.186 (gap 0.027) over n=1500. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.110 vs ECMWF 0.203 (gap 0.092) over n=744. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 24-72h | NBM lower Brier 0.121 vs ECMWF 0.197 (gap 0.076) over n=336. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.201 (gap 0.079) over n=1614. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.094 vs ECMWF 0.144 (gap 0.050) over n=1296. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 24-72h | NBM lower Brier 0.094 vs ECMWF 0.172 (gap 0.078) over n=624. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.091 vs ECMWF 0.168 (gap 0.078) over n=1578. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.127 vs ECMWF 0.198 (gap 0.071) over n=1290. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.211 (gap 0.087) over n=588. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 6-24h | NBM lower Brier 0.123 vs ECMWF 0.207 (gap 0.084) over n=1482. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.115 vs ECMWF 0.201 (gap 0.086) over n=750. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 24-72h | NBM lower Brier 0.129 vs ECMWF 0.183 (gap 0.054) over n=378. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 6-24h | NBM lower Brier 0.124 vs ECMWF 0.175 (gap 0.051) over n=1722. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.109 vs ECMWF 0.168 (gap 0.059) over n=1296. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.102 vs ECMWF 0.144 (gap 0.042) over n=276. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.108 vs ECMWF 0.151 (gap 0.043) over n=1626. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 0-6h | NBM lower Brier 0.146 vs ECMWF 0.203 (gap 0.057) over n=792. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 24-72h | NBM lower Brier 0.129 vs ECMWF 0.203 (gap 0.074) over n=276. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / low / 6-24h | NBM lower Brier 0.131 vs ECMWF 0.208 (gap 0.077) over n=1674. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / high / 0-6h | NBM lower Brier 0.148 vs ECMWF 0.178 (gap 0.030) over n=1446. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 0-6h | NBM lower Brier 0.122 vs ECMWF 0.206 (gap 0.083) over n=930. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 24-72h | NBM lower Brier 0.143 vs ECMWF 0.193 (gap 0.050) over n=264. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Philadelphia / low / 6-24h | NBM lower Brier 0.139 vs ECMWF 0.191 (gap 0.053) over n=1764. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.121 vs ECMWF 0.189 (gap 0.068) over n=792. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 24-72h | NBM lower Brier 0.129 vs ECMWF 0.170 (gap 0.041) over n=474. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.122 vs ECMWF 0.181 (gap 0.058) over n=1662. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.102 vs ECMWF 0.204 (gap 0.102) over n=858. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 24-72h | NBM lower Brier 0.103 vs ECMWF 0.206 (gap 0.103) over n=378. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.109 vs ECMWF 0.207 (gap 0.098) over n=1782. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.124 vs ECMWF 0.180 (gap 0.056) over n=1476. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 24-72h | NBM lower Brier 0.131 vs ECMWF 0.170 (gap 0.040) over n=618. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.129 vs ECMWF 0.179 (gap 0.050) over n=1566. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.111 vs ECMWF 0.189 (gap 0.079) over n=1464. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 24-72h | NBM lower Brier 0.103 vs ECMWF 0.203 (gap 0.099) over n=600. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 6-24h | NBM lower Brier 0.108 vs ECMWF 0.189 (gap 0.080) over n=1536. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / high / 0-6h | NBM lower Brier 0.179 vs ECMWF 0.201 (gap 0.022) over n=1242. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 0-6h | NBM lower Brier 0.126 vs ECMWF 0.204 (gap 0.078) over n=906. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 24-72h | NBM lower Brier 0.132 vs ECMWF 0.206 (gap 0.075) over n=294. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Washington DC / low / 6-24h | NBM lower Brier 0.123 vs ECMWF 0.190 (gap 0.067) over n=1752. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
