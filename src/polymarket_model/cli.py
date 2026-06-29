"""Typer CLI: scan, snapshot, fetch-resolution."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import typer
from rich.console import Console

from polymarket_model.cache import connect
from polymarket_model.calibration.bias import (
    DEFAULT_BIAS_PARQUET,
    compute_station_biases,
    distribution_for,
    load_biases,
    write_biases,
)
from polymarket_model.calibration.isotonic import (
    DEFAULT_CALIBRATION_PARQUET,
    fit_station_calibrations,
    write_calibrations,
)
from polymarket_model.config import settings
from polymarket_model.diagnostics import (
    DiagnosticsConfig,
    run_diagnostics,
)
from polymarket_model.diagnostics import (
    render_markdown as render_diagnostics_markdown,
)
from polymarket_model.edge.report import render_table, write_csv, write_markdown
from polymarket_model.edge.signals import signals_for_event
from polymarket_model.evaluation import (
    DEFAULT_RESOLUTIONS_PARQUET,
    EvaluationConfig,
    aggregate,
    discover_unresolved_from_snapshots,
    load_resolutions_parquet,
    score_resolutions,
    write_resolutions_parquet,
)
from polymarket_model.logging_setup import configure_logging, get_logger
from polymarket_model.markets.discovery import discover_weather_events
from polymarket_model.markets.prices import fetch_event_prices
from polymarket_model.model import evaluate_event
from polymarket_model.paper import (
    DEFAULT_PAPER_TRADES_PARQUET,
    PaperTradingConfig,
    derive_paper_trades,
    load_paper_trades,
    select_per_event,
    summarize,
    write_paper_trades,
)
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

    # Same per-station bias correction the snapshot/paper path applies, so scan,
    # paper, and live all forecast identically.
    biases = load_biases(DEFAULT_BIAS_PARQUET)

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
        dist, _ = distribution_for(ex, station_id=e.station_id, kind=e.kind, biases=biases)
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
    resolutions_parquet: Path = typer.Option(
        DEFAULT_RESOLUTIONS_PARQUET,
        "--resolutions-parquet",
        help="Canonical Parquet store for resolutions. Read to skip already-resolved tuples; written atomically.",
    ),
    no_duckdb: bool = typer.Option(
        False,
        "--no-duckdb",
        help="Skip the local DuckDB mirror write. Set by the ephemeral GitHub Actions runner.",
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
) -> None:
    """Pull NWS CLI daily-extreme observations for past markets and persist as ground truth.

    Candidate (station, date, kind) tuples are discovered from the snapshot Parquets
    under `data/snapshots/`, so this runs on a stateless GHA runner without any
    pre-existing DuckDB state.
    """
    configure_logging()
    console = Console()
    log_ = get_logger(__name__)
    today_local = date.today()
    earliest = today_local - timedelta(days=days_back)
    rows_inserted = 0
    rows_skipped = 0
    errors = 0

    existing = load_resolutions_parquet(resolutions_parquet)
    resolved_keys = {
        (r["station_id"], r["valid_date_local"], r["kind"])
        for r in existing
    }
    stations_filter = {s.upper() for s in station} if station else None

    candidates = discover_unresolved_from_snapshots(
        snapshots_root=settings.data_dir / "snapshots",
        earliest_date=earliest,
        latest_date=today_local,
        stations=stations_filter,
        already_resolved=resolved_keys,
    )
    if not quiet:
        console.print(f"[dim]Looking up {len(candidates)} unresolved (station, date, kind) tuples.[/dim]")

    new_rows: list[dict] = []
    cache_: dict[tuple[str, date], object] = {}
    for sid, target_date, kind in candidates:
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
            new_rows.append({
                "station_id": sid,
                "valid_date_local": target_date,
                "kind": kind,
                "value_f": float(value),
                "source": "nws_cli",
                "fetched_at_utc": obs.fetched_at_utc,
                "raw_text": obs.raw_text,
            })
            rows_inserted += 1
            if not quiet:
                console.print(f"  [green]{sid} {target_date} {kind:>4}[/green] = {value:.0f}°F")
        except Exception:
            errors += 1
            log_.exception("resolution_fetch_failed", station_id=sid, date=target_date.isoformat())

    if new_rows:
        merged = existing + new_rows
        write_resolutions_parquet(resolutions_parquet, merged)
        if not quiet:
            console.print(f"[dim]Wrote {len(merged)} total rows to {resolutions_parquet}[/dim]")

        if not no_duckdb:
            with connect() as con:
                for r in new_rows:
                    con.execute(
                        """
                        INSERT INTO resolutions (
                            station_id, valid_date_local, kind, value_f, source, fetched_at_utc, raw_text
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT (station_id, valid_date_local, kind) DO UPDATE SET
                            value_f = EXCLUDED.value_f,
                            fetched_at_utc = EXCLUDED.fetched_at_utc,
                            raw_text = EXCLUDED.raw_text
                        """,
                        [r["station_id"], r["valid_date_local"], r["kind"], r["value_f"],
                         r["source"], r["fetched_at_utc"], r["raw_text"]],
                    )

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
    resolutions_parquet: Path = typer.Option(
        DEFAULT_RESOLUTIONS_PARQUET,
        "--resolutions-parquet",
        help="Path to the canonical resolutions Parquet.",
    ),
    csv_path: Path | None = typer.Option(None, "--csv", help="Write per-row scoring to this CSV."),
    markdown_path: Path | None = typer.Option(None, "--markdown", help="Write the aggregate table to this markdown file."),
) -> None:
    """Score model predictions against NWS resolutions: Brier, log loss, simulated PnL."""
    configure_logging()
    console = Console()

    cfg = EvaluationConfig(min_edge=min_edge, kelly_multiplier=kelly_multiplier, fee=fee)
    df = score_resolutions(cfg=cfg, resolutions_parquet=resolutions_parquet)

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


@app.command()
def diagnose(
    days_back: int = typer.Option(
        60,
        "--days-back",
        help="Filter to predictions whose target_date_local is within the last N days.",
    ),
    min_sample: int = typer.Option(
        100,
        "--min-sample",
        help="Minimum scored rows in a (city,kind)/station cell before it can raise a flag.",
    ),
    min_edge: float = typer.Option(settings.min_edge, "--min-edge"),
    kelly_multiplier: float = typer.Option(settings.kelly_fraction, "--kelly"),
    fee: float = typer.Option(settings.fee_assumption, "--fee"),
    resolutions_parquet: Path = typer.Option(
        DEFAULT_RESOLUTIONS_PARQUET,
        "--resolutions-parquet",
        help="Path to the canonical resolutions Parquet.",
    ),
    markdown_path: Path | None = typer.Option(
        None,
        "--markdown",
        help="Write the flag table to this markdown file (read by the model-watch agent).",
    ),
) -> None:
    """Surface where the model is weak: model-vs-market, regressions, NBM, calibration.

    Deterministic layer of the model-watch loop. Reuses `score_resolutions`, then runs
    the thresholded `diagnostics` flag families and renders them critical-first.
    """
    configure_logging()
    console = Console()

    cfg = EvaluationConfig(min_edge=min_edge, kelly_multiplier=kelly_multiplier, fee=fee)
    df = score_resolutions(cfg=cfg, resolutions_parquet=resolutions_parquet)
    if df.empty:
        console.print("[yellow]No resolved predictions yet. Run `polymarket fetch-resolution` first.[/yellow]")
        return

    import pandas as pd
    cutoff = pd.Timestamp(datetime.now(UTC).date() - timedelta(days=days_back))
    df = df[pd.to_datetime(df["target_date_local"]) >= cutoff]
    if df.empty:
        console.print(f"[yellow]No resolved predictions within the last {days_back} days.[/yellow]")
        return

    flags = run_diagnostics(df, DiagnosticsConfig(min_sample=min_sample))
    if not flags:
        console.print("[green]No flags — model health within thresholds across all monitored cells.[/green]")
    else:
        from rich.table import Table
        _sev_color = {"critical": "red", "warn": "yellow", "good": "green", "info": "dim"}
        table = Table(show_header=True, header_style="bold", padding=(0, 1))
        for c in ("severity", "code", "dimension", "detail", "suggestion"):
            table.add_column(c, overflow="fold")
        for f in flags:
            color = _sev_color.get(f.severity, "white")
            table.add_row(
                f"[{color}]{f.severity}[/{color}]", f.code, f.dimension, f.detail, f.suggestion
            )
        console.print(table)

    if markdown_path is not None:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_diagnostics_markdown(flags), encoding="utf-8")
        console.print(f"[dim]Wrote markdown: {markdown_path}[/dim]")


@app.command("compute-bias")
def compute_bias(
    window_days: int = typer.Option(
        7,
        "--window-days",
        help="Rolling window length for the per-(station,kind) mean error.",
    ),
    min_days: int = typer.Option(
        3,
        "--min-days",
        help="Minimum paired records per station to emit a bias estimate.",
    ),
    snapshots_root: Path = typer.Option(
        settings.data_dir / "snapshots",
        "--snapshots-root",
        help="Root directory holding YYYY-MM-DD/HHMM.parquet snapshots.",
    ),
    resolutions_parquet: Path = typer.Option(
        DEFAULT_RESOLUTIONS_PARQUET,
        "--resolutions-parquet",
        help="Canonical NWS-CLI resolutions Parquet.",
    ),
    biases_parquet: Path = typer.Option(
        DEFAULT_BIAS_PARQUET,
        "--biases-parquet",
        help="Output Parquet for per-station bias estimates. Read by the recorder on next snapshot.",
    ),
) -> None:
    """Recompute per-(station,kind) ensemble bias from recent snapshot vs resolution pairs."""
    configure_logging()
    console = Console()
    biases = compute_station_biases(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions_parquet,
        window_days=window_days,
        min_days=min_days,
    )
    write_biases(biases_parquet, biases)
    if not biases:
        console.print(f"[yellow]No biases computed (need >= {min_days} paired days per station).[/yellow]")
        console.print(f"[dim]Wrote empty: {biases_parquet}[/dim]")
        return
    from rich.table import Table
    table = Table(show_header=True, header_style="bold", padding=(0, 1))
    for c in ("station_id", "kind", "bias_f", "n_days_used"):
        table.add_column(c, justify="right" if c != "station_id" else "left")
    for b in biases:
        table.add_row(b.station_id, b.kind, f"{b.bias_f:+.2f}", str(b.n_days_used))
    console.print(table)
    console.print(f"[dim]Wrote {biases_parquet}[/dim]")


@app.command("compute-calibration")
def compute_calibration(
    days_back: int = typer.Option(
        60,
        "--days-back",
        help="Use paired (model_p, outcome) records whose target_date_local is within N days.",
    ),
    min_samples: int = typer.Option(
        100,
        "--min-samples",
        help="Minimum paired records per (station,kind) before a calibration map is emitted.",
    ),
    stations: str = typer.Option(
        "",
        "--stations",
        help="Comma-separated station ids to calibrate. Empty = settings.calibration_stations.",
    ),
    snapshots_root: Path = typer.Option(
        settings.data_dir / "snapshots",
        "--snapshots-root",
        help="Root directory holding YYYY-MM-DD/HHMM.parquet snapshots.",
    ),
    resolutions_parquet: Path = typer.Option(
        DEFAULT_RESOLUTIONS_PARQUET,
        "--resolutions-parquet",
        help="Canonical NWS-CLI resolutions Parquet.",
    ),
    calibration_parquet: Path = typer.Option(
        DEFAULT_CALIBRATION_PARQUET,
        "--calibration-parquet",
        help="Output Parquet for isotonic maps. Read by the recorder on next snapshot.",
    ),
) -> None:
    """Fit per-(station,kind) isotonic recalibration from snapshot vs resolution pairs.

    Phase 3 pilot: marine stations KLAX/KMIA. Writes `data/station_calibration.parquet`;
    the recorder applies it as a recorded `calibrated_p` column (signals are unchanged).
    The before/after Brier shown is IN-SAMPLE — a sanity check, not the real evaluation,
    which comes from the forward-recorded calibrated_p resolving over the next weeks.
    """
    configure_logging()
    console = Console()
    target = (
        frozenset(s.strip() for s in stations.split(",") if s.strip())
        if stations
        else settings.calibration_stations
    )
    fits = fit_station_calibrations(
        snapshots_root=snapshots_root,
        resolutions_parquet=resolutions_parquet,
        stations=target,
        days_back=days_back,
        min_samples=min_samples,
    )
    write_calibrations(calibration_parquet, fits)
    if not fits:
        console.print(
            f"[yellow]No calibration maps (need >= {min_samples} paired records per "
            f"(station,kind) in {sorted(target)}).[/yellow]"
        )
        console.print(f"[dim]Wrote empty: {calibration_parquet}[/dim]")
        return
    from rich.table import Table
    table = Table(show_header=True, header_style="bold", padding=(0, 1))
    for c in ("station_id", "kind", "n_samples", "brier_before", "brier_after", "delta"):
        table.add_column(c, justify="right" if c not in ("station_id", "kind") else "left")
    for f in fits:
        delta = f.brier_after - f.brier_before
        table.add_row(
            f.station_id, f.kind, str(f.n_samples),
            f"{f.brier_before:.4f}", f"{f.brier_after:.4f}", f"{delta:+.4f}",
        )
    console.print(table)
    console.print("[dim]Brier before/after are in-sample; real signal is forward calibrated_p.[/dim]")
    console.print(f"[dim]Wrote {calibration_parquet}[/dim]")


@app.command("paper-trade")
def paper_trade(
    min_edge: float = typer.Option(settings.min_edge, "--min-edge"),
    kelly_multiplier: float = typer.Option(settings.kelly_fraction, "--kelly"),
    max_lead_days: int = typer.Option(
        settings.max_lead_days_for_signal,
        "--max-lead-days",
        help="Skip signals further out than this many days.",
    ),
    paper_trades_parquet: Path = typer.Option(
        DEFAULT_PAPER_TRADES_PARQUET,
        "--paper-trades-parquet",
        help="Canonical Parquet store for paper trades. Idempotent: existing trades aren't reopened.",
    ),
    resolutions_parquet: Path = typer.Option(
        DEFAULT_RESOLUTIONS_PARQUET,
        "--resolutions-parquet",
        help="Resolutions Parquet used to settle trades.",
    ),
    markdown_path: Path | None = typer.Option(None, "--markdown", help="Write the summary table to this file."),
) -> None:
    """Replay snapshots into one paper trade per market at the first edge-crossing bucket."""
    configure_logging()
    console = Console()

    cfg = PaperTradingConfig(
        min_edge=min_edge,
        kelly_multiplier=kelly_multiplier,
        max_lead_hours=max_lead_days * 24,
    )
    existing = load_paper_trades(paper_trades_parquet)
    existing_count = len(existing)
    trades = derive_paper_trades(
        snapshots_root=settings.data_dir / "snapshots",
        resolutions_parquet=resolutions_parquet,
        cfg=cfg,
        existing=existing,
    )
    write_paper_trades(paper_trades_parquet, trades)

    new_count = len(trades) - existing_count
    stats = summarize(trades)
    console.print(
        f"[bold]paper-trade[/bold] total={stats['n_total']} (new={new_count}) "
        f"open={stats['n_open']} settled={stats['n_settled']}"
    )
    if stats["n_settled"]:
        wr = stats["win_rate"] or 0.0
        roi = stats["weighted_roi"] or 0.0
        console.print(
            f"  wins={stats['n_wins']}/{stats['n_settled']} win_rate={wr:.1%} "
            f"weighted_pnl=${stats['weighted_pnl']:.4f} weighted_roi={roi:.2%}"
        )
    console.print(f"[dim]Wrote {paper_trades_parquet}[/dim]")

    if markdown_path is not None:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(_paper_summary_markdown(trades, stats), encoding="utf-8")
        console.print(f"[dim]Wrote markdown: {markdown_path}[/dim]")


def _paper_summary_markdown(trades: list, stats: dict) -> str:
    import pandas as pd
    overall_rows = [
        ("total trades", stats["n_total"]),
        ("open", stats["n_open"]),
        ("settled", stats["n_settled"]),
        ("wins", stats["n_wins"]),
        ("win rate", f"{stats['win_rate']:.1%}" if stats["win_rate"] is not None else "—"),
        ("Σ pnl_per_dollar (unweighted)", f"{stats['pnl_per_dollar_sum']:.4f}"),
        ("Σ kelly_sized (settled)", f"{stats['kelly_sized_sum_settled']:.4f}"),
        ("weighted pnl ($/bankroll)", f"{stats['weighted_pnl']:.4f}"),
        ("weighted ROI", f"{stats['weighted_roi']:.2%}" if stats["weighted_roi"] is not None else "—"),
    ]
    overall_md = pd.DataFrame(overall_rows, columns=["metric", "value"]).to_markdown(index=False)

    if not trades:
        return f"# Paper trading\n\n## Overall\n\n{overall_md}\n"

    df = pd.DataFrame(trades)
    settled = df[df["status"] == "SETTLED"].copy()

    def _by_cell_table(sub) -> str:
        if sub.empty:
            return "No settled trades."
        sub = sub.copy()
        sub["pnl_weighted"] = sub["pnl_per_dollar"] * sub["kelly_sized"]
        agg = sub.groupby(["city", "kind"], dropna=False).agg(
            n=("trade_id", "size"),
            wins=("pnl_per_dollar", lambda s: int((s > 0).sum())),
            win_rate=("pnl_per_dollar", lambda s: float((s > 0).mean())),
            kelly_sum=("kelly_sized", "sum"),
            pnl_weighted_sum=("pnl_weighted", "sum"),
        ).reset_index()
        agg["roi"] = agg.apply(
            lambda r: (r["pnl_weighted_sum"] / r["kelly_sum"]) if r["kelly_sum"] else 0.0,
            axis=1,
        )
        return agg.to_markdown(index=False, floatfmt=".4f")

    sections = ""
    if not settled.empty:
        # Per-bin: every signaled bin (the original paper strategy). Per-event: the
        # one max-EV bin per event the live trader actually holds (like-for-like with
        # kalshi-live). Both kept so the live-vs-paper comparison has both baselines.
        per_event = pd.DataFrame(select_per_event(settled.to_dict("records")))
        sections = (
            "\n\n## By city, kind — per-bin (every signaled bin)\n\n"
            + _by_cell_table(settled)
            + "\n\n## By city, kind — per-event (one max-EV bin/event, mirrors live)\n\n"
            + _by_cell_table(per_event)
        )

    return f"# Paper trading\n\n## Overall\n\n{overall_md}{sections}\n"


def _df_to_rich_table(df) -> Table:  # type: ignore[name-defined]
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


# ---------------------------------------------------------------------------
# `polymarket exec ...` — read-only authenticated calls to Kalshi /portfolio/*.
# Order placement is intentionally not implemented here; see execution/__init__.py.
# ---------------------------------------------------------------------------
exec_app = typer.Typer(help="Read-only authenticated Kalshi calls (balance, positions, fills).", no_args_is_help=True)
app.add_typer(exec_app, name="exec")


def _authed_client():
    from polymarket_model.execution.client import KalshiAuthedClient
    try:
        return KalshiAuthedClient()
    except RuntimeError as exc:
        raise typer.BadParameter(str(exc)) from exc


@exec_app.command("balance")
def exec_balance() -> None:
    """Print the current Kalshi account balance."""
    configure_logging()
    console = Console()
    client = _authed_client()
    data = client.get_balance() or {}
    if not data:
        console.print("[yellow]No balance data returned.[/yellow]")
        return
    cents = data.get("balance")
    if isinstance(cents, (int, float)):
        console.print(f"balance: ${cents / 100:.2f}  ([dim]{cents} cents[/dim])")
    else:
        console.print(data)


@exec_app.command("positions")
def exec_positions() -> None:
    """List current open positions."""
    configure_logging()
    console = Console()
    client = _authed_client()
    positions = client.get_positions()
    if not positions:
        console.print("[dim]No open positions.[/dim]")
        return
    from rich.table import Table
    table = Table(show_header=True, header_style="bold", padding=(0, 1))
    cols = ["ticker", "position", "market_exposure", "realized_pnl", "fees_paid"]
    for c in cols:
        table.add_column(c, justify="right" if c != "ticker" else "left")
    for p in positions:
        table.add_row(
            str(p.get("ticker", "")),
            str(p.get("position", "")),
            str(p.get("market_exposure", "")),
            str(p.get("realized_pnl", "")),
            str(p.get("fees_paid", "")),
        )
    console.print(table)


@exec_app.command("fills")
def exec_fills(
    limit: int = typer.Option(50, "--limit", help="Max number of fills to show (most recent first)."),
) -> None:
    """List recent fills."""
    configure_logging()
    console = Console()
    client = _authed_client()
    fills = client.get_fills()[:limit]
    if not fills:
        console.print("[dim]No fills.[/dim]")
        return
    from rich.table import Table
    table = Table(show_header=True, header_style="bold", padding=(0, 1))
    cols = ["created_time", "ticker", "side", "action", "count", "yes_price", "no_price"]
    for c in cols:
        table.add_column(c, justify="right" if c != "ticker" else "left")
    for f in fills:
        table.add_row(*[str(f.get(c, "")) for c in cols])
    console.print(table)


if __name__ == "__main__":
    app()
