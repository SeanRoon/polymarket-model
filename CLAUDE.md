# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Research-only model for finding +EV trades on Polymarket's daily city-temperature high/low markets by comparing model probabilities (built from free ensemble weather forecasts) against live Polymarket midpoints. **No order placement.** US °F city markets only for now (NYC/LAX/MIA/etc., scoped via the `Weather` tag, id=84). The detailed plan lives at `C:\Users\Sean\.claude\plans\i-want-to-create-distributed-dongarra.md`.

## Commands

Python 3.12 managed by `uv`. The venv lives at `.venv` and is created on first `uv sync`.

```
uv sync                                     # install / update dependencies from uv.lock
uv run pytest                               # run unit tests (fast, fully offline)
uv run pytest tests/unit/test_<file>.py -v  # run a single file
uv run ruff check .                         # lint
uv run mypy src                             # type-check
uv run polymarket scan --max-lead-days 7    # generate today's edge signals (network)
uv run polymarket snapshot                  # one-shot price snapshot to data/cache.duckdb
uv run polymarket fetch-resolution          # backfill NWS CLI ground truth for resolved markets
.\scripts\windows_task.ps1                  # register the 15-min snapshot recorder (Task Scheduler)
.\scripts\windows_task.ps1 -Unregister      # remove it
```

DuckDB cache is at `data/cache.duckdb` (gitignored). Inspect with `uv run python -c "import duckdb; print(duckdb.connect('data/cache.duckdb').execute('SELECT COUNT(*) FROM price_snapshots').fetchone())"`.

## Architecture

The pipeline runs left-to-right; each stage feeds the next via plain dataclasses, and DuckDB is the persistence boundary in the middle.

```
markets/discovery → markets/prices ─┐
                                     ├→ edge/signals → edge/report (rich/CSV/markdown)
weather/openmeteo → model.evaluate ─┘                       │
                                                            ↓
                                                    cache.duckdb (signals)
recorder.snapshot_once  ──────────────→ cache.duckdb (markets, market_bins, price_snapshots)
weather/nws.fetch_cli_for_date ───────→ cache.duckdb (resolutions)
```

### Data shape

- A Polymarket weather **event** (e.g. "Highest temperature in NYC on May 8?") is split into **bins** — each bin is its own binary YES/NO market. `markets/discovery.py` parses the event-and-bins shape into a `WeatherEvent` whose `bins: list[Bin]` carry half-open intervals `[lo_f, hi_f)` plus open-low / open-high flags. **Bin labels are unit-aware** (`°F` US / `°C` international); the discovery layer filters to °F by default.
- The **predictive distribution** is currently the empirical CDF over an Open-Meteo ensemble (51-member ECMWF IFS by default; see `DEFAULT_MODEL` in `weather/openmeteo.py`). `model.evaluate_event` integrates the distribution over each bin's interval with Laplace smoothing (`alpha=0.5`) so the 51-member sample never produces hard 0% / 100% probabilities (which would otherwise demand full-Kelly bets).
- An **edge signal** is one row per bin where `|model_p − market_mid| ≥ min_edge`. Quarter-Kelly sizing is applied to whichever side has the edge — `BUY_YES` if `model_p > market_mid`, otherwise `BUY_NO` at `(1 − market_mid)`.

### Two non-obvious invariants

- **`resolutionSource` is per-market, not per-city.** A NYC market may resolve to KLGA, KJFK, or KNYC depending on what Polymarket put in `resolutionSource`. Always read the field from the live market metadata; never hardcode a city → station map. `markets/discovery._extract_station_id` matches the literal `K[A-Z]{3}` ICAO code in the source URL.
- **Local-day timezone cutoff.** Each station has its own IANA timezone (looked up via NWS `/stations/{id}` with a hardcoded fallback in `weather/stations._FALLBACK`). `weather/openmeteo.fetch_daily_extreme` requests the forecast in that timezone and reduces over the local-midnight-to-local-midnight window. Storage is UTC throughout; conversion happens only at this boundary. The unit test in `tests/unit/test_timezone_cutoff.py` covers the boundary case.

### Snapshot recorder is the single highest-leverage component

Polymarket's public APIs return *current* prices only — there is no clean public midpoint history. The backtest substrate must be built locally over weeks. `recorder.snapshot_once` polls every active weather market's midpoint+book in parallel (10-thread pool, ~95s for ~38 events × 11 bins) and writes idempotent rows keyed by `(token_id, snapshot_bucket_utc)` (5-min floor). `scripts/windows_task.ps1` registers a 15-minute recurrence under the current user. The laptop-asleep gap is accepted by design.

### Phase status

The project follows the vertical-slice plan:

- **Phase 1 (done):** discovery → prices → ensemble → empirical-CDF baseline → edge → CLI report.
- **Phase 2 (done):** snapshot recorder + Task Scheduler script + NWS CLI scraper + `fetch-resolution`.
- **Phase 3 (not started):** KDE+climatology, EMOS / NGR, `calibration.py` (isotonic / Platt). The `model.PredictiveDistribution` interface is intentionally narrow (`prob_in_bin(lo, hi)`) so a parametric distribution can replace the empirical one without changing callers.
- **Phase 4 (not started):** walk-forward backtest in `evaluation.py` over the accumulating snapshot log; CLI `backtest` subcommand.
- **Phase 5 (deferred):** direct GEFS/ECMWF GRIB ingestion via Herbie, only if Open-Meteo's free tier becomes a bottleneck.

## Conventions

- **Git workflow:** every meaningful change is committed locally with a short message focused on the *why* and pushed to `origin/main` (`SeanRoon/polymarket-model`, private). One coherent commit per logical unit of work — don't bundle the markets layer with the model layer.
- **Tests are offline.** Network calls (Gamma, CLOB, Open-Meteo, NWS) live in production code; tests use synthetic samples and HTML fixtures. Don't add tests that hit live endpoints.
- **YES side only** for edge math. NO complementarity is unreliable due to fees and stale quotes.
- **Lead-time is a first-class column** on every forecast / signal. Skill collapses past day 7; production signals filter on it.
- **Storage is DuckDB+Parquet on disk**, schema bootstrapped by `cache.bootstrap()`. Don't add an ORM. Schema lives as raw SQL in `cache.SCHEMA_SQL` so it can be inspected and replayed onto a new file.
- **Don't run `polymarket snapshot` while the Task Scheduler job is firing** — concurrent inserts into the same 5-min bucket are deduped by ON CONFLICT, but two parallel scans waste API calls.
