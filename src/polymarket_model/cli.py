"""Typer CLI: scan + (later) snapshot + fetch-resolution + backtest."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import typer
from rich.console import Console

from polymarket_model.config import settings
from polymarket_model.edge.report import render_table, write_csv, write_markdown
from polymarket_model.edge.signals import signals_for_event
from polymarket_model.logging_setup import configure_logging, get_logger
from polymarket_model.markets.discovery import discover_weather_events
from polymarket_model.markets.prices import fetch_event_prices
from polymarket_model.model import PredictiveDistribution, evaluate_event
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


if __name__ == "__main__":
    app()
