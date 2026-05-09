"""Typer CLI: scan, snapshot, fetch-resolution."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import typer
from rich.console import Console

from polymarket_model.cache import connect
from polymarket_model.config import settings
from polymarket_model.edge.report import render_table, write_csv, write_markdown
from polymarket_model.edge.signals import signals_for_event
from polymarket_model.evaluation import EvaluationConfig, aggregate, score_resolutions
from polymarket_model.logging_setup import configure_logging, get_logger
from polymarket_model.markets.discovery import discover_weather_events
from polymarket_model.markets.prices import fetch_event_prices
from polymarket_model.model import PredictiveDistribution, evaluate_event
from polymarket_model.recorder import snapshot_once
from polymarket_model.weather.nws import fetch_cli_for_date
from polymarket_model.weather.openmeteo import DEFAULT_MODEL, fetch_daily_extreme

app = typer.Typer(help="Kalshi weather edge model.", no_args_is_help=True)


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
    """Scan all active Kalshi weather markets and print +EV edge candidates."""
    configure_logging()
    log = get_logger(__name__)
    console = Console()

    now = datetime.now(UTC)
    deadline = now + timedelta(days=max_lead_days)

    events = discover_weather_events()
    if not quiet:
        console.print(f"[dim]Discovered {len(events)} active Kalshi weather events.[/dim]")

    if cities:
        wanted = [c.lower() for c in cities]
        events = [e for e in events if any(w in e.city.lower() for w in wanted)]

    in_window = [e for e in events if now <= e.close_time_utc <= deadline]
    if not quiet:
        console.print(f"[dim]Within signal window (lead <= {max_lead_days}d): {len(in_window)} events.[/dim]")

    signals: list = []
    for e in in_window:
        if not e.station_id:
            log.warning("event_without_station", event_ticker=e.event_ticker)
            continue
        try:
            prices = fetch_event_prices(e)
        except Exception:
            log.exception("price_fetch_failed", event_ticker=e.event_ticker)
            continue
        if not prices.passes_qc:
            log.info("qc_failed_prices", event_ticker=e.event_ticker, sum_of_mids=prices.sum_of_mids)
            continue
        try:
            ex = fetch_daily_extreme(e.station_id, e.target_date_local, e.kind, model=model)
        except Exception:
            log.exception("forecast_fetch_failed", event_ticker=e.event_ticker, station=e.station_id)
            continue
        dist = PredictiveDistribution.from_ensemble(ex)
        out = evaluate_event(e, dist)
        if not out.passes_qc:
            log.info("qc_failed_model", event_ticker=e.event_ticker, outside_mass=out.outside_bin_mass)
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
    """One-shot price snapshot: persist current midpoints+book for every active Kalshi weather market."""
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

        cache_: dict[tuple[str, date], object] = {}
        for sid, target_date, kind in rows:
            key = (sid, target_date)
            try:
                obs = cache_.get(key)
                if obs is None:
                    obs = fetch_cli_for_date(sid, target_date)
                    cache_[key] = obs
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


@app.command("compare-to-resolved")
def compare_to_resolved(
    days_back: int = typer.Option(
        30,
        "--days-back",
        help="Filter to predictions whose target_date_local is within the last N days.",
    ),
    by: str = typer.Option(
        "city,kind,lead_bucket",
        "--by",
        help="Comma-separated grouping dimensions. Empty string => overall only.",
    ),
    min_edge: float = typer.Option(settings.min_edge, "--min-edge"),
    kelly_multiplier: float = typer.Option(settings.kelly_fraction, "--kelly"),
    fee: float = typer.Option(settings.fee_assumption, "--fee"),
    csv_path: Path | None = typer.Option(None, "--csv", help="Write per-row scoring to this CSV."),
    markdown_path: Path | None = typer.Option(None, "--markdown", help="Write the aggregate table to this markdown file."),
) -> None:
    """Score model predictions against NWS resolutions: Brier, log loss, simulated PnL."""
    configure_logging()
    console = Console()

    cfg = EvaluationConfig(min_edge=min_edge, kelly_multiplier=kelly_multiplier, fee=fee)
    df = score_resolutions(cfg=cfg)

    if df.empty:
        console.print("[yellow]No resolved predictions yet. Run `polymarket fetch-resolution` after a market settles, then retry.[/yellow]")
        return

    import pandas as pd
    cutoff = pd.Timestamp(datetime.now(UTC).date() - timedelta(days=days_back))
    df = df[pd.to_datetime(df["target_date_local"]) >= cutoff]
    if df.empty:
        console.print(f"[yellow]No resolved predictions within the last {days_back} days.[/yellow]")
        return

    overall = aggregate(df, by=None)
    console.print("[bold]Overall[/bold]")
    console.print(_df_to_rich_table(overall))

    by_dims = [d.strip() for d in by.split(",") if d.strip()]
    if by_dims:
        grouped = aggregate(df, by=by_dims)
        console.print(f"[bold]By {', '.join(by_dims)}[/bold]")
        console.print(_df_to_rich_table(grouped))

    if csv_path:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False)
        console.print(f"[dim]Wrote per-row scoring CSV: {csv_path}[/dim]")
    if markdown_path:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(
            "# Evaluation\n\n## Overall\n\n" + overall.to_markdown(index=False)
            + (("\n\n## By " + ", ".join(by_dims) + "\n\n" + grouped.to_markdown(index=False)) if by_dims else ""),
            encoding="utf-8",
        )
        console.print(f"[dim]Wrote markdown: {markdown_path}[/dim]")


def _df_to_rich_table(df) -> "Table":  # type: ignore[name-defined]
    from rich.table import Table
    table = Table(show_header=True, header_style="bold", padding=(0, 1))
    for col in df.columns:
        table.add_column(str(col), justify="right" if col != df.columns[0] else "left")
    for _, row in df.iterrows():
        table.add_row(*[
            f"{v:.4f}" if isinstance(v, float)
            else (str(int(v)) if isinstance(v, int) else str(v))
            for v in row
        ])
    return table


if __name__ == "__main__":
    app()
