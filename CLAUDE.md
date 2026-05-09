# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Research-only model for finding +EV trades on **Kalshi**'s daily city-temperature high/low markets by comparing model probabilities (built from free ensemble weather forecasts) against live Kalshi midpoints. **No order placement.**

The project was originally built against Polymarket's global weather markets, but those aren't tradable from a US account — Polymarket US is iOS-only and has no public API. The plan that drove the migration lives at `C:\Users\Sean\.claude\plans\i-want-to-create-distributed-dongarra.md`. The Python package and repo names are still `polymarket_model` / `polymarket-model` for now; renaming is deferred until the codebase has stabilized on Kalshi.

## Commands

Python 3.12 managed by `uv`. The venv lives at `.venv` and is created on first `uv sync`.

```
uv sync                                      # install / update deps from uv.lock
uv run pytest                                # run unit tests (offline)
uv run ruff check .                          # lint
uv run mypy src                              # type-check
uv run polymarket scan --max-lead-days 7     # generate today's edge signals (live network)
uv run polymarket snapshot --parquet-dir data/snapshots --no-duckdb   # one-shot Parquet write (same as CI)
uv run polymarket snapshot                                            # legacy: also write to local DuckDB
uv run polymarket fetch-resolution           # backfill NWS CLI ground truth for resolved markets
```

Local DuckDB cache is at `data/cache.duckdb` (gitignored). The source-of-truth for price history is Parquet files under `data/snapshots/` written by the GHA cron and committed back to the repo.

## Architecture

The pipeline runs left-to-right; each stage feeds the next via plain dataclasses, and DuckDB / Parquet are the persistence boundary.

```
markets/discovery → markets/prices ─┐
                                     ├→ edge/signals → edge/report (rich/CSV/markdown)
weather/openmeteo → model.evaluate ─┘                       │
                                                            ↓
                                                    cache.duckdb (signals)
recorder.snapshot_once  ──────────────→ data/snapshots/YYYY-MM-DD/HHMM.parquet
weather/nws.fetch_cli_for_date ───────→ cache.duckdb (resolutions)
```

### Venue: Kalshi (read-only public API)

- **Base URL:** `https://api.elections.kalshi.com/trade-api/v2` (one host serves all of their markets; no auth required for `/series`, `/events`, `/markets`, `/markets/{ticker}/orderbook`).
- **Hierarchy:** Series → Events → Markets. Series we scan are listed in `markets.discovery.WEATHER_SERIES` and currently cover daily high/low for NYC, Chicago, Miami, LAX, Austin, Denver. Each event has 6 mutually-exclusive bin markets.
- **Bin shapes:** ticker prefix `T<X>` = threshold (open-low if `cap_strike` set with `floor_strike=null`, open-high if vice versa), `B<X.5>` = closed bin with both strikes set inclusive.
- **Prices:** `yes_bid_dollars` / `yes_ask_dollars` are decimal strings 0.00–1.00. Midpoint = `(yes_bid + yes_ask) / 2`. When the book is empty, both are `null` — skip that bin.

### Two non-obvious invariants

- **Kalshi settles on Local Standard Time (LST), not local clock time.** During DST the daily window is offset by one hour vs. the IANA timezone. `weather/openmeteo.lst_day_window_utc(target_date_local, tz_name)` computes the LST-aligned window in UTC by always picking the timezone's standard (winter) offset, even in summer. This is unit-tested in `tests/unit/test_timezone_cutoff.py`.
- **Kalshi rules use strict inequalities.** "Greater than 68°" with `floor_strike=68, cap_strike=null` means `≥69` (integer NWS values), so the bin's `lo_f = floor_strike + 1`. Closed bins are inclusive both sides, so `B61.5` with `floor=61, cap=62` covers integers `{61, 62}` → `[61, 63)`. The interval translation lives in `markets.discovery._interval_for_market` and is unit-tested.

### Resolution stations differ from Polymarket

Kalshi's settlement station is **whatever NWS office issues the city's CLI** — usually different from Polymarket's choice:

| City | Polymarket (legacy) | Kalshi |
|------|---------------------|--------|
| New York | KLGA (LaGuardia) | **KNYC (Central Park)** |
| Chicago | KORD (O'Hare) | **KMDW (Midway)** |
| Miami | KMIA | KMIA |
| Los Angeles | KLAX | KLAX |
| Austin | KAUS | KAUS |
| Denver | KDEN | KDEN |

The model only matters if it forecasts the same station the market settles against. The mapping is hard-coded in `markets.discovery.WEATHER_SERIES`; never hardcode by city.

### Snapshot recorder is the single highest-leverage component

There's no public price history endpoint anywhere in this domain (Kalshi doesn't expose historical orderbook, only trades). The backtest substrate must be built ourselves over weeks.

**Source of truth** is `data/snapshots/YYYY-MM-DD/HHMM.parquet`, one self-contained denormalized file per 5-min bucket (~10–40 KB each, zstd-compressed). The GitHub Actions workflow `.github/workflows/snapshot.yml` runs every 15 minutes on a hosted runner, fetches all bin midpoints in parallel (8-thread pool, ~15 s/run since Kalshi's `list_event_markets` returns all bins per event in one call), writes the Parquet, and commits it back to `main`.

**Repo is public** to get unlimited GitHub Actions minutes; on a private repo the 15-min cadence would exceed the 2,000-min/month free tier.

Old Polymarket snapshots are archived under `data/snapshots/_archive_polymarket/` for reference. Don't read from them — schema is incompatible.

### Phase status

- **Phase 1 (done):** discovery → prices → ensemble → empirical-CDF baseline → edge → CLI report.
- **Phase 2 (done):** snapshot recorder + GHA cron + NWS CLI scraper + `fetch-resolution`.
- **Phase 3 (not started):** KDE+climatology, EMOS / NGR, isotonic calibration. The `model.PredictiveDistribution` interface is intentionally narrow (`prob_in_bin(lo, hi)`) so a parametric distribution can replace the empirical one without changing callers.
- **Phase 4 (not started):** walk-forward backtest in `evaluation.py` over the accumulating Parquet snapshots; CLI `backtest` subcommand.

## Conventions

- **Git workflow:** every meaningful change is committed locally with a short message focused on the *why* and pushed to `origin/main`. One coherent commit per logical unit of work.
- **Tests are offline.** Network calls (Kalshi, Open-Meteo, NWS) live in production code; tests use synthetic samples. Don't add tests that hit live endpoints.
- **YES side only** for edge math. The `BUY_NO` direction in `edge/signals` is computed against the implicit complement (`1 - yes_mid`), since Kalshi has only YES tokens.
- **Lead-time is a first-class column** on every forecast / signal. Skill collapses past day 7; production signals filter on it.
- **Storage is DuckDB+Parquet on disk.** Schema lives as raw SQL in `cache.SCHEMA_SQL`. Parquet snapshots are the canonical price history; DuckDB is a local convenience cache.
