"""Typer CLI: scan + (later) snapshot + fetch-resolution + backtest."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import typer
from rich.console import Console

from polymarket_model.cache import connect
from polymarket_model.config import settings
from polymarket_model.edge.report import render_table, write_csv, write_markdown
from polymarket_model.edge.signals import signals_for_event
from polymarket_model.logging_setup import configure_logging, get_logger
from polymarket_model.markets.discovery import discover_weather_events
from polymarket_model.markets.prices import fetch_event_prices
from polymarket_model.model import PredictiveDistribution, evaluate_event
from polymarket_model.recorder import snapshot_once
from polymarket_model.weather.nws import fetch_cli_for_date
from polymarket_model.weather.openmeteo import DEFAULT_MODEL, fetch_daily_extreme

app = typer.Typer(help="Polymarket weather edge model.", no_args_is_help=True)


@app.callback()
def _root() -> None:
    """Root callback so single-subcommand invocation parses correctly."""
    return None


@app.command()
def scan(
    max_lead_days: int = typer.Option(
        settings.max_lead_days_for_signal,
        "--max-lead-days",
        help="Skip events resolving more than this many days out.",
    ),
    min_edge: float = typer.Option(
        settings.min_edge,
        "--min-edge",
        help="Minimum |model_p - market_mid| to emit a signal.",
    ),
    model: str = typer.Option(
        DEFAULT_MODEL,
        "--model",
        help="Open-Meteo ensemble model id.",
    ),
    csv_path: Path | None = typer.Option(None, "--csv", help="Write signals to this CSV."),
    markdown_path: Path | None = typer.Option(None, "--markdown", help="Write signals to this markdown file."),
    cities: list[str] | None = typer.Option(None, "--city", help="Filter to one or more cities (substring match)."),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress progress lines; print only the table."),
) -> None:
    """Scan all active US °F weather markets and print +EV edge candidates."""
    configure_logging()
    log = get_logger(__name__)
    console = Console()

    now = datetime.now(UTC)
    deadline = now + timedelta(days=max_lead_days)

    events = discover_weather_events()
    if not quiet:
        console.print(f"[dim]Discovered {len(events)} active F-unit weather events.[/dim]")

    if cities:
        wanted = [c.lower() for c in cities]
        events = [e for e in events if any(w in e.city.lower() for w in wanted)]

    in_window = [e for e in events if now <= e.end_date_utc <= deadline]
    if not quiet:
        console.print(f"[dim]Within signal window (lead <= {max_lead_days}d): {len(in_window)} events.[/dim]")

    signals: list = []
    for e in in_window:
        if not e.station_id:
            log.warning("event_without_station", slug=e.slug)
            continue
        try:
            prices = fetch_event_prices(e, with_book=False)
        except Exception:
            log.exception("price_fetch_failed", slug=e.slug)
            continue
        if not prices.passes_qc:
            log.info("qc_failed_prices", slug=e.slug, sum_of_mids=prices.sum_of_mids)
            continue
        try:
            ex = fetch_daily_extreme(e.station_id, e.target_date_local, e.kind, unit=e.unit, model=model)
        except Exception:
            log.exception("forecast_fetch_failed", slug=e.slug, station=e.station_id)
            continue
        dist = PredictiveDistribution.from_ensemble(ex)
        out = evaluate_event(e, dist)
        if not out.passes_qc:
            log.info("qc_failed_model", slug=e.slug, outside_mass=out.outside_bin_mass)
            continue
        ev_signals = signals_for_event(out, prices, min_edge=min_edge, now=now)
        signals.extend(ev_signals)
        if not quiet:
            console.print(
                f"[dim]  {e.target_date_local} {e.kind:>4} {e.city:<22} "
                f"sum_mids={prices.sum_of_mids:.3f} outside={out.outside_bin_mass:.3f} "
                f"signals={len(ev_signals)}[/dim]"
            )

    render_table(signals, console=console)

    if csv_path:
        out_path = write_csv(signals, csv_path)
        console.print(f"[dim]Wrote CSV: {out_path}[/dim]")
    if markdown_path:
        out_path = write_markdown(signals, markdown_path)
        console.print(f"[dim]Wrote markdown: {out_path}[/dim]")


@app.command()
def snapshot(
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress per-event progress."),
    parquet_dir: Path | None = typer.Option(
        None,
        "--parquet-dir",
        help="Write a self-contained Parquet for this bucket under this directory. "
             "Used by the GitHub Actions workflow to commit snapshots back to the repo.",
    ),
    no_duckdb: bool = typer.Option(
        False,
        "--no-duckdb",
        help="Skip the local DuckDB write. Set by the ephemeral GitHub Actions runner.",
    ),
) -> None:
    """One-shot price snapshot: persist current midpoints+book for every active weather market."""
    configure_logging()
    console = Console()
    result = snapshot_once(parquet_dir=parquet_dir, write_duckdb=not no_duckdb)
    if not quiet:
        msg = (
            f"snapshot: events={result.events_seen} bins={result.bins_seen} "
            f"rows_inserted={result.rows_inserted} errors={result.errors} "
            f"duration={(result.ended_utc - result.started_utc).total_seconds():.1f}s"
        )
        if result.parquet_path:
            msg += f" parquet={result.parquet_path}"
        console.print(f"[dim]{msg}[/dim]")


@app.command("fetch-resolution")
def fetch_resolution(
    days_back: int = typer.Option(
        7,
        "--days-back",
        help="Look up CLI resolutions for any unresolved (station, date, kind) within the last N days.",
    ),
    station: list[str] | None = typer.Option(None, "--station", help="Limit to specific stations."),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
) -> None:
    """Pull NWS CLI daily-extreme observations for past markets and persist as ground truth."""
    configure_logging()
    console = Console()
    log_ = get_logger(__name__)
    today_local = date.today()
    earliest = today_local - timedelta(days=days_back)
    rows_inserted = 0
    rows_skipped = 0
    errors = 0

    with connect() as con:
        # Find (station_id, target_date_local, kind) tuples from the markets table that are
        # in the lookback window and not already resolved.
        params: list = [earliest]
        sql = """
            SELECT DISTINCT m.station_id, m.target_date_local, m.kind
            FROM markets m
            LEFT JOIN resolutions r
              ON r.station_id = m.station_id
             AND r.valid_date_local = m.target_date_local
             AND r.kind = m.kind
            WHERE m.station_id IS NOT NULL
              AND m.target_date_local >= ?
              AND m.target_date_local <= CURRENT_DATE
              AND r.station_id IS NULL
        """
        if station:
            sql += " AND m.station_id IN (" + ",".join(["?"] * len(station)) + ")"
            params.extend([s.upper() for s in station])
        rows = con.execute(sql, params).fetchall()
        if not quiet:
            console.print(f"[dim]Looking up {len(rows)} unresolved (station, date, kind) tuples.[/dim]")

        # Cache CLI results per (station, date) so we don't fetch twice for high+low.
        cache: dict[tuple[str, date], object] = {}
        for sid, target_date, kind in rows:
            key = (sid, target_date)
            try:
                obs = cache.get(key)
                if obs is None:
                    obs = fetch_cli_for_date(sid, target_date)
                    cache[key] = obs
                if obs is None:
                    rows_skipped += 1
                    if not quiet:
                        console.print(f"[dim]  {sid} {target_date} {kind:>4}: not in CLI archive[/dim]")
                    continue
                value = obs.max_f if kind == "high" else obs.min_f
                if value is None:
                    rows_skipped += 1
                    log_.warning("cli_value_missing", station_id=sid, date=target_date.isoformat(), kind=kind)
                    continue
                con.execute(
                    """
                    INSERT INTO resolutions (
                        station_id, valid_date_local, kind, value_f, source, fetched_at_utc, raw_text
                    ) VALUES (?, ?, ?, ?, 'nws_cli', ?, ?)
                    ON CONFLICT (station_id, valid_date_local, kind) DO UPDATE SET
                        value_f = EXCLUDED.value_f,
                        fetched_at_utc = EXCLUDED.fetched_at_utc,
                        raw_text = EXCLUDED.raw_text
                    """,
                    [sid, target_date, kind, value, obs.fetched_at_utc, obs.raw_text],
                )
                rows_inserted += 1
                if not quiet:
                    console.print(f"  [green]{sid} {target_date} {kind:>4}[/green] = {value:.0f}°F")
            except Exception:
                errors += 1
                log_.exception("resolution_fetch_failed", station_id=sid, date=target_date.isoformat())

    if not quiet:
        console.print(
            f"[dim]fetch-resolution: inserted={rows_inserted} skipped={rows_skipped} errors={errors}[/dim]"
        )


@app.command("migrate-snapshots-to-parquet")
def migrate_snapshots_to_parquet(
    parquet_dir: Path = typer.Option(
        Path("data/snapshots"),
        "--parquet-dir",
        help="Output root directory.",
    ),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite Parquet files that already exist."),
) -> None:
    """One-shot: export existing DuckDB price_snapshots into per-bucket Parquet files."""
    import duckdb
    import pyarrow.parquet as pq

    configure_logging()
    console = Console()
    parquet_dir.mkdir(parents=True, exist_ok=True)

    sql = """
        SELECT
            ps.snapshot_bucket_utc,
            ps.snapshot_ts_utc,
            m.condition_id AS event_id,
            m.condition_id,
            m.slug,
            m.city,
            m.kind,
            'F' AS unit,
            m.target_date_local,
            m.end_date_utc,
            m.station_id,
            m.resolution_source,
            mb.outcome_index,
            mb.token_id AS yes_token_id,
            CAST(NULL AS VARCHAR) AS no_token_id,
            mb.outcome_label AS bin_label,
            mb.lo_f,
            mb.hi_f,
            mb.is_open_low,
            mb.is_open_high,
            ps.midpoint,
            ps.best_bid,
            ps.best_ask,
            ps.bid_size,
            ps.ask_size
        FROM price_snapshots ps
        JOIN market_bins mb ON mb.token_id = ps.token_id
        JOIN markets m ON m.condition_id = ps.condition_id
        WHERE ps.midpoint IS NOT NULL
    """
    with connect(read_only=True) as con:
        buckets = [row[0] for row in con.execute("SELECT DISTINCT snapshot_bucket_utc FROM price_snapshots ORDER BY snapshot_bucket_utc").fetchall()]
        if not buckets:
            console.print("[yellow]No snapshots found in cache.duckdb.[/yellow]")
            return
        written = skipped = 0
        for bucket in buckets:
            out = parquet_dir / bucket.strftime("%Y-%m-%d") / f"{bucket.strftime('%H%M')}.parquet"
            if out.exists() and not overwrite:
                skipped += 1
                continue
            reader = con.execute(sql + " AND ps.snapshot_bucket_utc = ?", [bucket]).fetch_arrow_table()
            out.parent.mkdir(parents=True, exist_ok=True)
            pq.write_table(reader, out, compression="zstd")
            written += 1
        console.print(f"[dim]migrate: {written} written, {skipped} skipped (already existed) of {len(buckets)} buckets[/dim]")


if __name__ == "__main__":
    app()
