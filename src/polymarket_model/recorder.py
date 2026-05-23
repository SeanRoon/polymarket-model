"""Snapshot recorder: persist live midpoints + bid/ask for every active Kalshi weather market.

This is the highest-leverage component in the project: without an accumulating
snapshot history, no future modeling work can be backtested. The GitHub Actions
workflow at .github/workflows/snapshot.yml runs this every 15 minutes and
commits a Parquet file back to the repo.

Idempotent on (market_ticker, snapshot_bucket_utc) where the bucket is floor(now, 5 min):
two runs in the same 5-min window won't create duplicate rows.
"""
from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

from polymarket_model.cache import connect
from polymarket_model.calibration.bias import (
    DEFAULT_BIAS_PARQUET,
    apply_bias_to_samples,
    load_biases,
)
from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import KalshiClient
from polymarket_model.markets.discovery import WeatherEvent, discover_weather_events
from polymarket_model.markets.prices import EventPrices, fetch_event_prices, floor_to_bucket
from polymarket_model.model import (
    EventModelOutput,
    PredictiveDistribution,
    evaluate_event,
    evaluate_event_nbm,
)
from polymarket_model.weather.nbm import NBMQuantileForecast, fetch_nbm_quantiles_many
from polymarket_model.weather.openmeteo import EnsembleDailyExtreme, fetch_daily_extreme

log = get_logger(__name__)


PRICE_FETCH_CONCURRENCY = 8
FORECAST_FETCH_CONCURRENCY = 6


@dataclass
class SnapshotResult:
    started_utc: datetime
    ended_utc: datetime
    events_seen: int
    bins_seen: int
    rows_inserted: int
    errors: int
    parquet_path: Path | None = None


def _upsert_event(con: duckdb.DuckDBPyConnection, event: WeatherEvent, now: datetime) -> None:
    con.execute(
        """
        INSERT INTO markets (
            event_ticker, series_ticker, title, city, kind, target_date_local,
            station_id, rules_primary, close_time_utc, first_seen_utc, last_seen_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (event_ticker) DO UPDATE SET
            series_ticker = EXCLUDED.series_ticker,
            title = EXCLUDED.title,
            city = EXCLUDED.city,
            kind = EXCLUDED.kind,
            target_date_local = EXCLUDED.target_date_local,
            station_id = EXCLUDED.station_id,
            rules_primary = EXCLUDED.rules_primary,
            close_time_utc = EXCLUDED.close_time_utc,
            last_seen_utc = EXCLUDED.last_seen_utc
        """,
        [
            event.event_ticker,
            event.series_ticker,
            event.title,
            event.city,
            event.kind,
            event.target_date_local,
            event.station_id,
            event.rules_primary,
            event.close_time_utc,
            now,
            now,
        ],
    )


def _upsert_bins(con: duckdb.DuckDBPyConnection, event: WeatherEvent) -> None:
    for b in event.bins:
        con.execute(
            """
            INSERT INTO market_bins (
                market_ticker, event_ticker, bin_index, subtitle,
                floor_strike, cap_strike, lo_f, hi_f, is_open_low, is_open_high
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (market_ticker) DO UPDATE SET
                event_ticker = EXCLUDED.event_ticker,
                bin_index = EXCLUDED.bin_index,
                subtitle = EXCLUDED.subtitle,
                floor_strike = EXCLUDED.floor_strike,
                cap_strike = EXCLUDED.cap_strike,
                lo_f = EXCLUDED.lo_f,
                hi_f = EXCLUDED.hi_f,
                is_open_low = EXCLUDED.is_open_low,
                is_open_high = EXCLUDED.is_open_high
            """,
            [
                b.market_ticker,
                b.event_ticker,
                b.bin_index,
                b.subtitle,
                b.floor_strike,
                b.cap_strike,
                None if b.is_open_low else b.lo_f,
                None if b.is_open_high else b.hi_f,
                b.is_open_low,
                b.is_open_high,
            ],
        )


def _insert_price_snapshot(
    con: duckdb.DuckDBPyConnection,
    *,
    market_ticker: str,
    event_ticker: str,
    snapshot_ts_utc: datetime,
    bucket_utc: datetime,
    midpoint: float | None,
    yes_bid: float | None,
    yes_ask: float | None,
    last_price: float | None,
    volume: float | None,
    yes_bid_size: float | None,
    yes_ask_size: float | None,
    model_p: float | None,
    model_lead_hours: int | None,
    model_name: str | None,
    model_n_members: int | None,
    model_outside_bin_mass: float | None,
    nbm_p: float | None = None,
    nbm_q10: float | None = None,
    nbm_q25: float | None = None,
    nbm_q50: float | None = None,
    nbm_q75: float | None = None,
    nbm_q90: float | None = None,
    nbm_cycle_utc: datetime | None = None,
    nbm_lead_hours: int | None = None,
    nbm_model_name: str | None = None,
    nbm_outside_bin_mass: float | None = None,
) -> None:
    con.execute(
        """
        INSERT INTO price_snapshots (
            market_ticker, event_ticker, snapshot_ts_utc, snapshot_bucket_utc,
            midpoint, yes_bid, yes_ask, last_price, volume, yes_bid_size, yes_ask_size,
            model_p, model_lead_hours, model_name, model_n_members, model_outside_bin_mass,
            nbm_p, nbm_q10, nbm_q25, nbm_q50, nbm_q75, nbm_q90,
            nbm_cycle_utc, nbm_lead_hours, nbm_model_name, nbm_outside_bin_mass
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (market_ticker, snapshot_bucket_utc) DO NOTHING
        """,
        [
            market_ticker,
            event_ticker,
            snapshot_ts_utc,
            bucket_utc,
            midpoint,
            yes_bid,
            yes_ask,
            last_price,
            volume,
            yes_bid_size,
            yes_ask_size,
            model_p,
            model_lead_hours,
            model_name,
            model_n_members,
            model_outside_bin_mass,
            nbm_p,
            nbm_q10,
            nbm_q25,
            nbm_q50,
            nbm_q75,
            nbm_q90,
            nbm_cycle_utc,
            nbm_lead_hours,
            nbm_model_name,
            nbm_outside_bin_mass,
        ],
    )


def _parquet_path_for_bucket(parquet_dir: Path, bucket: datetime) -> Path:
    return parquet_dir / f"{bucket.strftime('%Y-%m-%d')}" / f"{bucket.strftime('%H%M')}.parquet"


def _build_snapshot_table(
    *,
    bucket: datetime,
    started: datetime,
    priced_events: list[EventPrices],
    model_outputs: dict[str, EventModelOutput],
    forecasts: dict[tuple[str, date, str], EnsembleDailyExtreme],
    nbm_outputs: dict[str, EventModelOutput],
    nbm_forecasts: dict[tuple[str, date, str], NBMQuantileForecast],
    bias_applied: dict[str, float | None] | None = None,
) -> pa.Table:
    rows: list[dict] = []
    for ep in priced_events:
        e = ep.event
        mo = model_outputs.get(e.event_ticker)
        ex = forecasts.get((e.station_id, e.target_date_local, e.kind)) if e.station_id else None
        bin_to_p: dict[str, float] = {}
        if mo is not None:
            for bp in mo.bin_probs:
                bin_to_p[bp.bin.market_ticker] = bp.p

        nmo = nbm_outputs.get(e.event_ticker)
        nfc = nbm_forecasts.get((e.station_id, e.target_date_local, e.kind)) if e.station_id else None
        nbm_bin_to_p: dict[str, float] = {}
        if nmo is not None:
            for bp in nmo.bin_probs:
                nbm_bin_to_p[bp.bin.market_ticker] = bp.p
        nbm_q = nfc.quantiles if nfc is not None else {}
        nbm_cycle_naive = nfc.cycle_time_utc.replace(tzinfo=None) if nfc is not None else None

        for p in ep.prices:
            if p.midpoint is None:
                continue
            rows.append({
                "snapshot_bucket_utc": bucket,
                "snapshot_ts_utc": started,
                "series_ticker": e.series_ticker,
                "event_ticker": e.event_ticker,
                "market_ticker": p.bin.market_ticker,
                "city": e.city,
                "kind": e.kind,
                "target_date_local": e.target_date_local,
                "close_time_utc": e.close_time_utc.replace(tzinfo=None),
                "station_id": e.station_id,
                "bin_index": p.bin.bin_index,
                "subtitle": p.bin.subtitle,
                "floor_strike": p.bin.floor_strike,
                "cap_strike": p.bin.cap_strike,
                "lo_f": None if p.bin.is_open_low else p.bin.lo_f,
                "hi_f": None if p.bin.is_open_high else p.bin.hi_f,
                "is_open_low": p.bin.is_open_low,
                "is_open_high": p.bin.is_open_high,
                "midpoint": p.midpoint,
                "yes_bid": p.yes_bid,
                "yes_ask": p.yes_ask,
                "last_price": p.last_price,
                "volume": p.volume,
                "yes_bid_size": p.yes_bid_size,
                "yes_ask_size": p.yes_ask_size,
                "model_p": bin_to_p.get(p.bin.market_ticker),
                "model_lead_hours": int(ex.lead_hours) if ex else None,
                "model_name": mo.distribution.model if mo else None,
                "model_n_members": int(mo.distribution.n) if mo else None,
                "model_outside_bin_mass": float(mo.outside_bin_mass) if mo else None,
                "model_bias_applied_f": (bias_applied or {}).get(e.event_ticker) if mo else None,
                "nbm_p": nbm_bin_to_p.get(p.bin.market_ticker),
                "nbm_q10": nbm_q.get(10),
                "nbm_q25": nbm_q.get(25),
                "nbm_q50": nbm_q.get(50),
                "nbm_q75": nbm_q.get(75),
                "nbm_q90": nbm_q.get(90),
                "nbm_cycle_utc": nbm_cycle_naive,
                "nbm_lead_hours": int(nfc.lead_hours) if nfc else None,
                "nbm_model_name": nfc.model if nfc else None,
                "nbm_outside_bin_mass": float(nmo.outside_bin_mass) if nmo else None,
            })
    return pa.Table.from_pylist(rows)


def _fetch_distributions(
    events: list[WeatherEvent],
    *,
    max_workers: int = FORECAST_FETCH_CONCURRENCY,
) -> tuple[dict[tuple[str, date, str], EnsembleDailyExtreme], int]:
    """Fetch ensemble forecasts in parallel, deduped by (station_id, target_date, kind).

    Returns (cache, error_count). Errors are logged; bins for failed keys get model_p=None.
    """
    keys: list[tuple[str, date, str]] = []
    seen: set[tuple[str, date, str]] = set()
    for e in events:
        if not e.station_id:
            continue
        key = (e.station_id, e.target_date_local, e.kind)
        if key in seen:
            continue
        seen.add(key)
        keys.append(key)

    cache_: dict[tuple[str, date, str], EnsembleDailyExtreme] = {}
    errors = 0
    if not keys:
        return cache_, errors

    def fetch(key: tuple[str, date, str]) -> tuple[tuple[str, date, str], EnsembleDailyExtreme | None]:
        sid, target_date, kind = key
        try:
            return key, fetch_daily_extreme(sid, target_date, kind)
        except Exception:
            log.exception("forecast_fetch_failed", station=sid, target_date=target_date.isoformat(), kind=kind)
            return key, None

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(fetch, k) for k in keys]
        for fut in as_completed(futures):
            key, ex = fut.result()
            if ex is None:
                errors += 1
                continue
            cache_[key] = ex
    return cache_, errors


def _build_model_outputs(
    events: list[WeatherEvent],
    forecasts: dict[tuple[str, date, str], EnsembleDailyExtreme],
    biases: dict[tuple[str, str], float] | None = None,
) -> tuple[dict[str, EventModelOutput], dict[str, float | None]]:
    """Run evaluate_event for each event whose forecast succeeded.

    If `biases` contains a `(station_id, kind)` entry, the ensemble samples are
    shifted by `-bias` before the predictive distribution is built and the model
    name is suffixed with `+biascorr` so downstream eval can distinguish corrected
    rows. Returns `(outputs, bias_applied_per_event)` where the second dict maps
    event_ticker to the bias value that was subtracted (or None if no correction).
    """
    biases = biases or {}
    out: dict[str, EventModelOutput] = {}
    bias_applied: dict[str, float | None] = {}
    for e in events:
        key = (e.station_id, e.target_date_local, e.kind) if e.station_id else None
        ex = forecasts.get(key) if key else None
        if ex is None:
            continue
        try:
            bias = biases.get((e.station_id, e.kind)) if e.station_id else None
            if bias is not None:
                samples = apply_bias_to_samples(ex.values, bias)
                dist = PredictiveDistribution(
                    samples=samples,
                    model=f"empirical_{ex.model}+biascorr",
                )
                bias_applied[e.event_ticker] = float(bias)
            else:
                dist = PredictiveDistribution.from_ensemble(ex)
                bias_applied[e.event_ticker] = None
            out[e.event_ticker] = evaluate_event(e, dist)
        except Exception:
            log.exception("model_evaluation_failed", event_ticker=e.event_ticker)
    return out, bias_applied


def _fetch_nbm_distributions(
    events: list[WeatherEvent],
) -> tuple[dict[tuple[str, date, str], NBMQuantileForecast], int]:
    """Fetch NBM quantile forecasts via the batched downloader.

    Dedupes by (station_id, target_date_local, kind) and shares GRIB2 downloads across
    requests that hit the same NBM cycle/lead-hour. Failures are logged and skipped — the
    corresponding events get nbm_* columns of NULL.
    """
    keys: list[tuple[str, date, str]] = []
    seen: set[tuple[str, date, str]] = set()
    for e in events:
        if not e.station_id:
            continue
        key = (e.station_id, e.target_date_local, e.kind)
        if key in seen:
            continue
        seen.add(key)
        keys.append(key)

    cache_: dict[tuple[str, date, str], NBMQuantileForecast] = {}
    errors = 0
    if not keys:
        return cache_, errors

    results = fetch_nbm_quantiles_many(keys)
    for key, val in results.items():
        if isinstance(val, Exception):
            errors += 1
            log.warning(
                "nbm_fetch_failed",
                station=key[0],
                target_date=key[1].isoformat(),
                kind=key[2],
                error=repr(val),
            )
        else:
            cache_[key] = val
    return cache_, errors


def _build_nbm_outputs(
    events: list[WeatherEvent],
    nbm_forecasts: dict[tuple[str, date, str], NBMQuantileForecast],
) -> dict[str, EventModelOutput]:
    """Run evaluate_event_nbm for each event whose NBM forecast succeeded."""
    out: dict[str, EventModelOutput] = {}
    for e in events:
        if not e.station_id:
            continue
        key = (e.station_id, e.target_date_local, e.kind)
        forecast = nbm_forecasts.get(key)
        if forecast is None:
            continue
        try:
            out[e.event_ticker] = evaluate_event_nbm(e, forecast)
        except Exception:
            log.exception("nbm_evaluation_failed", event_ticker=e.event_ticker)
    return out


def snapshot_once(
    *,
    now: datetime | None = None,
    max_workers: int = PRICE_FETCH_CONCURRENCY,
    parquet_dir: Path | None = None,
    write_duckdb: bool = True,
    biases_path: Path | None = None,
) -> SnapshotResult:
    """Single shot: discover, fetch prices in parallel, persist to Parquet and/or DuckDB.

    parquet_dir: if provided, write a self-contained Parquet at
        {parquet_dir}/YYYY-MM-DD/HHMM.parquet. Each row is fully denormalized.
    write_duckdb: if True (default), also write to data/cache.duckdb. The GHA runner
        sets this False because the runner is ephemeral.
    biases_path: optional path to the station-bias Parquet. If present, the ensemble
        samples are shifted by `-bias` per (station_id, kind) before bin probabilities
        are computed. Defaults to DEFAULT_BIAS_PARQUET; missing file = no correction.
    """
    started = now or datetime.now(UTC)
    bucket = floor_to_bucket(started, minutes=5)
    run_id = uuid.uuid4().hex
    client = KalshiClient()
    events = discover_weather_events(client)

    biases = load_biases(biases_path or DEFAULT_BIAS_PARQUET)
    if biases:
        log.info("biases_loaded", n_stations=len(biases))

    errors = 0

    # Fetch each event's prices in parallel; Kalshi returns all bins in one /markets call,
    # so concurrency is per-event, not per-bin.
    priced_events: list[EventPrices] = []
    if events:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(fetch_event_prices, e, client): e for e in events}
            for fut in as_completed(futures):
                e = futures[fut]
                try:
                    priced_events.append(fut.result())
                except Exception:
                    errors += 1
                    log.exception("event_price_fetch_failed", event_ticker=e.event_ticker)

    # Fetch ensemble forecasts (deduped per station+date+kind) and run the model. Bins
    # for events whose forecast failed get model_p=None — we still record price.
    forecasts, forecast_errors = _fetch_distributions(events)
    errors += forecast_errors
    model_outputs, bias_applied = _build_model_outputs(events, forecasts, biases=biases)

    # Fetch NBM probabilistic quantiles in parallel; same deduplication + isolation rules.
    # NBM failures do not block ECMWF columns or price recording — they just leave nbm_* null.
    nbm_forecasts, nbm_errors = _fetch_nbm_distributions(events)
    errors += nbm_errors
    nbm_outputs = _build_nbm_outputs(events, nbm_forecasts)

    rows_written = 0
    bins_with_mid = 0

    parquet_path: Path | None = None
    if parquet_dir is not None:
        try:
            tbl = _build_snapshot_table(
                bucket=bucket,
                started=started,
                priced_events=priced_events,
                model_outputs=model_outputs,
                forecasts=forecasts,
                nbm_outputs=nbm_outputs,
                nbm_forecasts=nbm_forecasts,
                bias_applied=bias_applied,
            )
            parquet_path = _parquet_path_for_bucket(parquet_dir, bucket)
            parquet_path.parent.mkdir(parents=True, exist_ok=True)
            pq.write_table(tbl, parquet_path, compression="zstd")
            rows_written = tbl.num_rows
            bins_with_mid = tbl.num_rows
        except Exception:
            errors += 1
            log.exception("parquet_write_failed", path=str(parquet_path))

    if write_duckdb:
        with connect() as con:
            try:
                for ep in priced_events:
                    e_ = ep.event
                    mo = model_outputs.get(e_.event_ticker)
                    ex = forecasts.get((e_.station_id, e_.target_date_local, e_.kind)) if e_.station_id else None
                    bin_to_p: dict[str, float] = {}
                    if mo is not None:
                        for bp in mo.bin_probs:
                            bin_to_p[bp.bin.market_ticker] = bp.p

                    nmo = nbm_outputs.get(e_.event_ticker)
                    nfc = nbm_forecasts.get((e_.station_id, e_.target_date_local, e_.kind)) if e_.station_id else None
                    nbm_bin_to_p: dict[str, float] = {}
                    if nmo is not None:
                        for bp in nmo.bin_probs:
                            nbm_bin_to_p[bp.bin.market_ticker] = bp.p
                    nbm_q = nfc.quantiles if nfc is not None else {}

                    try:
                        _upsert_event(con, e_, started)
                        _upsert_bins(con, e_)
                        for p in ep.prices:
                            if p.midpoint is None:
                                continue
                            _insert_price_snapshot(
                                con,
                                market_ticker=p.bin.market_ticker,
                                event_ticker=e_.event_ticker,
                                snapshot_ts_utc=started,
                                bucket_utc=bucket,
                                midpoint=p.midpoint,
                                yes_bid=p.yes_bid,
                                yes_ask=p.yes_ask,
                                last_price=p.last_price,
                                volume=p.volume,
                                yes_bid_size=p.yes_bid_size,
                                yes_ask_size=p.yes_ask_size,
                                model_p=bin_to_p.get(p.bin.market_ticker),
                                model_lead_hours=int(ex.lead_hours) if ex else None,
                                model_name=mo.distribution.model if mo else None,
                                model_n_members=int(mo.distribution.n) if mo else None,
                                model_outside_bin_mass=float(mo.outside_bin_mass) if mo else None,
                                nbm_p=nbm_bin_to_p.get(p.bin.market_ticker),
                                nbm_q10=nbm_q.get(10),
                                nbm_q25=nbm_q.get(25),
                                nbm_q50=nbm_q.get(50),
                                nbm_q75=nbm_q.get(75),
                                nbm_q90=nbm_q.get(90),
                                nbm_cycle_utc=nfc.cycle_time_utc.replace(tzinfo=None) if nfc else None,
                                nbm_lead_hours=int(nfc.lead_hours) if nfc else None,
                                nbm_model_name=nfc.model if nfc else None,
                                nbm_outside_bin_mass=float(nmo.outside_bin_mass) if nmo else None,
                            )
                            if parquet_dir is None:  # only count once
                                rows_written += 1
                                bins_with_mid += 1
                    except Exception:
                        errors += 1
                        log.exception("event_record_failed", event_ticker=e_.event_ticker)
                ended = datetime.now(UTC)
                con.execute(
                    """
                    INSERT INTO run_log (run_id, component, started_utc, ended_utc, ok, rows_written, message)
                    VALUES (?, 'snapshot', ?, ?, ?, ?, ?)
                    """,
                    [run_id, started, ended, errors == 0, rows_written,
                     f"events={len(events)} bins_with_mid={bins_with_mid} errors={errors}"],
                )
            except Exception:
                log.exception("snapshot_failed_unrecoverable")
                errors += 1
                ended = datetime.now(UTC)
    else:
        ended = datetime.now(UTC)

    return SnapshotResult(
        started_utc=started,
        ended_utc=ended,
        events_seen=len(events),
        bins_seen=bins_with_mid,
        rows_inserted=rows_written,
        errors=errors,
        parquet_path=parquet_path,
    )
