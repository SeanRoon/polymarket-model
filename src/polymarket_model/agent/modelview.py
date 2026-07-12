"""The weather model's knowledge, packaged for the self-directed agent.

Two views, both read-only over data the pipeline already collects:

1. **Live edges** — the latest snapshot Parquet's model_p (bias-corrected ECMWF)
   and nbm_p vs the market midpoint, for EVERY city — production exclusions are
   shown as context, not applied as a filter. The agent may trade any cell it
   judges to have a real edge.
2. **Track record by cell** — settled paper trades grouped by (city, kind), so
   the agent can weight the model's live opinion by where it has actually been
   right (Austin/high +27% ROI) vs. where it has burned money (Chicago books).

Entry prices are still taken live by `agent-trade`; the snapshot is at most
~15 min old and a staleness warning is emitted beyond that.
"""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pyarrow.parquet as pq

from polymarket_model.config import settings
from polymarket_model.paper import DEFAULT_PAPER_TRADES_PARQUET

SNAPSHOT_STALE_MINUTES = 40.0


def latest_snapshot_path(snapshots_root: Path | None = None) -> Path | None:
    root = snapshots_root or (settings.data_dir / "snapshots")
    days = sorted(
        (d for d in root.iterdir() if d.is_dir() and not d.name.startswith("_")),
        reverse=True,
    )
    for day in days:
        files = sorted(day.glob("*.parquet"), reverse=True)
        if files:
            return files[0]
    return None


def load_snapshot_rows(path: Path) -> list[dict]:
    return pq.read_table(path).to_pylist()


def cell_track_record(paper_trades_path: Path | None = None) -> dict[tuple[str, str], dict]:
    """Per-(city, kind) settled stats from the model's paper book."""
    path = paper_trades_path or DEFAULT_PAPER_TRADES_PARQUET
    if not path.exists():
        return {}
    out: dict[tuple[str, str], dict] = {}
    for t in pq.read_table(path).to_pylist():
        if t.get("status") != "SETTLED" or t.get("pnl_per_dollar") is None:
            continue
        cell = (str(t["city"]), str(t["kind"]))
        acc = out.setdefault(
            cell, {"n": 0, "wins": 0, "pnl_weighted": 0.0, "kelly_sum": 0.0}
        )
        acc["n"] += 1
        acc["wins"] += 1 if float(t["pnl_per_dollar"]) > 0 else 0
        kel = float(t.get("kelly_sized") or 0.0)
        acc["pnl_weighted"] += float(t["pnl_per_dollar"]) * kel
        acc["kelly_sum"] += kel
    return out


def _excluded_label(station_id: str | None, kind: str | None) -> str:
    """Production trader's status for this cell — context for the agent, not a rule."""
    if station_id and station_id in settings.signal_excluded_stations:
        return "excluded (station)"
    if station_id and kind and (station_id, kind.lower()) in settings.signal_excluded_cells:
        return "excluded (cell)"
    return "LIVE"


def render_model_view(
    snapshot_rows: list[dict],
    track: dict[tuple[str, str], dict],
    *,
    now_utc: datetime,
    min_edge: float = 0.05,
    min_lead_hours: int = 6,
    max_lead_hours: int = 24 * 7,
) -> str:
    lines: list[str] = ["# Weather-model view (for the self-trader agent)", ""]

    snap_ts = None
    for r in snapshot_rows:
        ts = r.get("snapshot_ts_utc")
        if isinstance(ts, datetime) and (snap_ts is None or ts > snap_ts):
            snap_ts = ts
    if snap_ts is not None:
        age_min = (now_utc - snap_ts).total_seconds() / 60.0
        lines.append(
            f"_Snapshot {snap_ts.strftime('%Y-%m-%d %H:%M UTC')} ({age_min:.0f} min old). "
            "Production status is context — you may trade excluded cells on your own judgment. "
            "agent-trade fills at the LIVE book, so re-check prices that look too good._"
        )
        if age_min > SNAPSHOT_STALE_MINUTES:
            lines.append("")
            lines.append(
                f"**WARNING: snapshot is {age_min:.0f} min old — prices below are stale; "
                "trust the model_p, verify the market side via agent-scan.**"
            )
    lines += [
        "",
        f"## Model live edges (|model_p - mid| >= {min_edge:.2f}, "
        f"{min_lead_hours}h <= lead <= {max_lead_hours}h)",
        "",
        "_Bins closer than the lead floor are excluded: the day's extreme is already "
        "partly observed there, so a big model-vs-market gap usually means the MARKET "
        "knows and the model is stale — not an edge. Override with --min-lead-hours 0 "
        "only if you understand that._",
        "",
        "| ticker | city/kind | bin | model_p | nbm_p | mid | bid | ask | edge | lead_h | prod_status |",
        "|:-------|:----------|:----|--------:|------:|----:|----:|----:|-----:|-------:|:------------|",
    ]

    def _f(v: float | int | str | None, spec: str = ".2f") -> str:
        return format(float(v), spec) if v is not None else "-"

    edged = []
    for r in snapshot_rows:
        mp, mid = r.get("model_p"), r.get("midpoint")
        lead = r.get("model_lead_hours")
        if mp is None or mid is None:
            continue
        if lead is not None and not (min_lead_hours <= int(lead) <= max_lead_hours):
            continue
        edge = float(mp) - float(mid)
        if abs(edge) >= min_edge:
            edged.append((edge, r))
    edged.sort(key=lambda t: -abs(t[0]))
    for edge, r in edged:
        cell = f"{r.get('city')}/{r.get('kind')}"
        lines.append(
            f"| {r.get('market_ticker')} | {cell} | {str(r.get('subtitle') or '')[:24]} "
            f"| {_f(r.get('model_p'))} | {_f(r.get('nbm_p'))} | {_f(r.get('midpoint'))} "
            f"| {_f(r.get('yes_bid'))} | {_f(r.get('yes_ask'))} | {edge:+.2f} "
            f"| {r.get('model_lead_hours') if r.get('model_lead_hours') is not None else '-'} "
            f"| {_excluded_label(r.get('station_id'), r.get('kind'))} |"
        )
    if not edged:
        lines.append("| _none at this threshold_ | | | | | | | | | | |")

    lines += [
        "",
        "## Model track record by cell (settled paper trades, per-bin)",
        "",
        "| city | kind | n | win_rate | roi | prod_status |",
        "|:-----|:-----|--:|---------:|----:|:------------|",
    ]
    station_by_cell: dict[tuple[str, str], str | None] = {}
    for r in snapshot_rows:
        key = (str(r.get("city")), str(r.get("kind")))
        station_by_cell.setdefault(key, r.get("station_id"))
    for (city, kind), a in sorted(track.items(), key=lambda kv: -(
        kv[1]["pnl_weighted"] / kv[1]["kelly_sum"] if kv[1]["kelly_sum"] else 0.0
    )):
        roi = a["pnl_weighted"] / a["kelly_sum"] if a["kelly_sum"] else None
        roi_s = f"{roi * 100:+.1f}%" if roi is not None else "-"
        wr = f"{a['wins'] / a['n'] * 100:.0f}%" if a["n"] else "-"
        status = _excluded_label(station_by_cell.get((city, kind)), kind)
        lines.append(f"| {city} | {kind} | {a['n']} | {wr} | {roi_s} | {status} |")
    if not track:
        lines.append("| _no settled paper trades yet_ | | | | | |")
    lines.append("")
    return "\n".join(lines)


def model_view(
    *,
    min_edge: float = 0.05,
    min_lead_hours: int = 6,
    max_lead_hours: int = 24 * 7,
    now_utc: datetime | None = None,
) -> str:
    """Assemble the full view from the latest snapshot + paper track record."""
    now_utc = now_utc or datetime.now(UTC)
    path = latest_snapshot_path()
    if path is None:
        return "# Weather-model view\n\n_No snapshots found under data/snapshots/._\n"
    return render_model_view(
        load_snapshot_rows(path),
        cell_track_record(),
        now_utc=now_utc,
        min_edge=min_edge,
        min_lead_hours=min_lead_hours,
        max_lead_hours=max_lead_hours,
    )
