"""Render Signal lists as rich tables, CSV, or markdown."""
from __future__ import annotations

import csv
from pathlib import Path

from rich.console import Console
from rich.table import Table

from polymarket_model.edge.signals import Signal


def render_table(signals: list[Signal], *, console: Console | None = None) -> None:
    console = console or Console()
    if not signals:
        console.print("[dim]No signals (no bin had |edge| above threshold).[/dim]")
        return
    table = Table(show_header=True, header_style="bold", padding=(0, 1), title="Kalshi weather edge candidates")
    table.add_column("Date")
    table.add_column("City")
    table.add_column("Kind", justify="center")
    table.add_column("Bin")
    table.add_column("Ticker")
    table.add_column("Side", justify="center")
    table.add_column("Entry $", justify="right")
    table.add_column("Model p", justify="right")
    table.add_column("Mkt mid", justify="right")
    table.add_column("Edge", justify="right")
    table.add_column("Kelly", justify="right")
    table.add_column("Lead h", justify="right")
    for s in sorted(signals, key=lambda x: x.abs_edge, reverse=True):
        edge_sign = "+" if s.edge_signed > 0 else ""
        side_style = "green" if s.direction == "BUY_YES" else "red"
        edge_style = "green" if s.edge_signed > 0 else "red"
        table.add_row(
            str(s.event.target_date_local),
            s.event.city,
            s.event.kind,
            s.bin.subtitle,
            s.market_ticker,
            f"[{side_style}]{s.direction}[/{side_style}]",
            f"{s.entry_price:.3f}",
            f"{s.model_p_yes:.3f}",
            f"{s.market_mid_yes:.3f}",
            f"[{edge_style}]{edge_sign}{s.edge_signed:.3f}[/{edge_style}]",
            f"{s.kelly_sized:.3f}",
            str(s.lead_hours),
        )
    console.print(table)


CSV_FIELDS = [
    "emitted_ts_utc",
    "target_date_local",
    "city",
    "kind",
    "station_id",
    "subtitle",
    "lo_f",
    "hi_f",
    "direction",
    "market_ticker",
    "event_ticker",
    "series_ticker",
    "entry_price",
    "model_p_yes",
    "market_mid_yes",
    "edge_signed",
    "abs_edge",
    "kelly_full",
    "kelly_sized",
    "lead_hours",
    "outside_bin_mass",
    "sum_of_mids",
    "n_members",
    "model_name",
]


def write_csv(signals: list[Signal], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for s in signals:
            w.writerow({
                "emitted_ts_utc": s.emitted_ts_utc.isoformat(),
                "target_date_local": s.event.target_date_local.isoformat(),
                "city": s.event.city,
                "kind": s.event.kind,
                "station_id": s.event.station_id or "",
                "subtitle": s.bin.subtitle,
                "lo_f": s.bin.lo_f,
                "hi_f": s.bin.hi_f,
                "direction": s.direction,
                "market_ticker": s.market_ticker,
                "event_ticker": s.event.event_ticker,
                "series_ticker": s.event.series_ticker,
                "entry_price": s.entry_price,
                "model_p_yes": s.model_p_yes,
                "market_mid_yes": s.market_mid_yes,
                "edge_signed": s.edge_signed,
                "abs_edge": s.abs_edge,
                "kelly_full": s.kelly_full,
                "kelly_sized": s.kelly_sized,
                "lead_hours": s.lead_hours,
                "outside_bin_mass": s.outside_bin_mass,
                "sum_of_mids": s.sum_of_mids,
                "n_members": s.n_members,
                "model_name": s.model_name,
            })
    return path


def write_markdown(signals: list[Signal], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_sig = sorted(signals, key=lambda x: x.abs_edge, reverse=True)
    lines = ["# Kalshi weather edge candidates", ""]
    lines.append("| Date | City | Kind | Bin | Ticker | Side | Entry | Model p | Market | Edge | Kelly | Lead h |")
    lines.append("|------|------|------|-----|--------|------|------:|--------:|-------:|-----:|------:|------:|")
    for s in sorted_sig:
        lines.append(
            f"| {s.event.target_date_local} | {s.event.city} | {s.event.kind} | "
            f"{s.bin.subtitle} | {s.market_ticker} | {s.direction} | {s.entry_price:.3f} | {s.model_p_yes:.3f} | "
            f"{s.market_mid_yes:.3f} | {s.edge_signed:+.3f} | {s.kelly_sized:.3f} | {s.lead_hours} |"
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
