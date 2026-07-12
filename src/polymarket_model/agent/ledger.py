"""Paper ledger for the self-directed agent. PAPER ONLY — no orders, ever.

The agent opens hypothetical positions at live take-side prices (yes_ask for YES,
1 - yes_bid for NO), pays Kalshi's real per-contract fee, and settles against the
market's published result. Every trade carries the agent's thesis and the strategy
version that motivated it, so the performance report can score strategy versions
against each other — that attribution is the learning loop.

Guards are deliberately hard-coded here rather than left to the agent's judgment:
fixed starting bankroll, per-trade cost cap, open-position cap, cash check, and
duplicate refusal. The agent iterates on WHAT to trade, not on its own risk limits.
"""
from __future__ import annotations

import math
import os
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from polymarket_model.agent.scout import num_field, price_dollars
from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger
from polymarket_model.markets.client import KalshiClient

log = get_logger(__name__)

AGENT_DIR = settings.data_dir / "agent"
DEFAULT_AGENT_TRADES_PARQUET = AGENT_DIR / "agent_trades.parquet"
DEFAULT_PERFORMANCE_MD = AGENT_DIR / "performance.md"

STARTING_BANKROLL = 1000.00
MAX_COST_PER_TRADE = 50.00
MAX_OPEN_POSITIONS = 25
MAX_CONTRACTS_PER_TRADE = 200

KALSHI_FEE_RATE = 0.07  # fee = ceil_to_cent(0.07 * C * P * (1-P)), per side

AGENT_TRADES_SCHEMA = pa.schema([
    pa.field("trade_id", pa.string(), nullable=False),
    pa.field("opened_at_utc", pa.timestamp("us", tz="UTC"), nullable=False),
    pa.field("market_ticker", pa.string(), nullable=False),
    pa.field("event_ticker", pa.string(), nullable=True),
    pa.field("category", pa.string(), nullable=True),
    pa.field("title", pa.string(), nullable=True),
    pa.field("side", pa.string(), nullable=False),  # 'yes' | 'no'
    pa.field("count", pa.int32(), nullable=False),
    pa.field("entry_price", pa.float64(), nullable=False),  # $ per contract, our side
    pa.field("fee", pa.float64(), nullable=False),
    pa.field("cost", pa.float64(), nullable=False),  # count*entry_price + fee
    pa.field("yes_bid_at_open", pa.float64(), nullable=True),
    pa.field("yes_ask_at_open", pa.float64(), nullable=True),
    pa.field("volume_24h_at_open", pa.float64(), nullable=True),
    pa.field("close_time_utc", pa.timestamp("us", tz="UTC"), nullable=True),
    pa.field("thesis", pa.string(), nullable=False),
    pa.field("strategy_version", pa.string(), nullable=False),
    pa.field("status", pa.string(), nullable=False),  # OPEN | SETTLED | VOID
    pa.field("settled_at_utc", pa.timestamp("us", tz="UTC"), nullable=True),
    pa.field("result", pa.string(), nullable=True),  # 'yes' | 'no' | 'void'
    pa.field("payoff", pa.float64(), nullable=True),
    pa.field("pnl", pa.float64(), nullable=True),
])


def kalshi_fee(count: int, price: float, fee_rate: float = KALSHI_FEE_RATE) -> float:
    """Kalshi's documented trading fee, rounded up to the next cent."""
    if price <= 0.0 or price >= 1.0 or count <= 0:
        return 0.0
    return math.ceil(fee_rate * count * price * (1.0 - price) * 100.0) / 100.0


def load_trades(path: Path = DEFAULT_AGENT_TRADES_PARQUET) -> list[dict]:
    if not path.exists():
        return []
    return pq.read_table(path).to_pylist()


def write_trades(rows: list[dict], path: Path = DEFAULT_AGENT_TRADES_PARQUET) -> None:
    ordered = sorted(rows, key=lambda r: (r["opened_at_utc"], r["market_ticker"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    tbl = pa.Table.from_pylist(ordered, schema=AGENT_TRADES_SCHEMA)
    fd, tmp = tempfile.mkstemp(prefix=".agent-", suffix=".parquet", dir=str(path.parent))
    os.close(fd)
    try:
        pq.write_table(tbl, tmp, compression="zstd")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def cash_balance(trades: list[dict]) -> float:
    """Free cash: bankroll minus everything spent plus everything returned."""
    cash = STARTING_BANKROLL
    for t in trades:
        cash -= float(t["cost"])
        if t["status"] == "SETTLED":
            cash += float(t.get("payoff") or 0.0)
        elif t["status"] == "VOID":
            cash += float(t["cost"])  # full refund, fee included
    return cash


class TradeRejectedError(ValueError):
    """A guard refused the trade; message says which one."""


def build_trade(
    *,
    market: dict[str, Any],
    side: str,
    count: int,
    thesis: str,
    strategy_version: str,
    existing: list[dict],
    now_utc: datetime | None = None,
) -> dict:
    """Validate against the guards and price a paper fill from a live market record."""
    now_utc = now_utc or datetime.now(UTC)
    side = side.lower().strip()
    if side not in ("yes", "no"):
        raise TradeRejectedError(f"side must be 'yes' or 'no', got {side!r}")
    if not thesis.strip():
        raise TradeRejectedError("a thesis is required — every trade must cite its reasoning")
    if not strategy_version.strip():
        raise TradeRejectedError("strategy_version is required for attribution")
    if count < 1 or count > MAX_CONTRACTS_PER_TRADE:
        raise TradeRejectedError(f"count must be 1..{MAX_CONTRACTS_PER_TRADE}")
    if market.get("status") not in (None, "open", "active"):
        raise TradeRejectedError(f"market is not open (status={market.get('status')!r})")

    ticker = str(market.get("ticker") or "")
    open_positions = [t for t in existing if t["status"] == "OPEN"]
    if len(open_positions) >= MAX_OPEN_POSITIONS:
        raise TradeRejectedError(f"open-position cap reached ({MAX_OPEN_POSITIONS})")
    if any(t["market_ticker"] == ticker and t["side"] == side for t in open_positions):
        raise TradeRejectedError(f"already holding an open {side.upper()} position in {ticker}")

    yes_bid = price_dollars(market, "yes_bid")
    yes_ask = price_dollars(market, "yes_ask")
    if side == "yes":
        if yes_ask is None or not (0.0 < yes_ask < 1.0):
            raise TradeRejectedError("no tradeable YES ask on the book")
        entry_price = yes_ask
    else:
        if yes_bid is None or not (0.0 < yes_bid < 1.0):
            raise TradeRejectedError("no tradeable YES bid on the book (needed to take NO)")
        entry_price = 1.0 - yes_bid

    fee = kalshi_fee(count, entry_price)
    cost = round(count * entry_price + fee, 2)
    if cost > MAX_COST_PER_TRADE:
        raise TradeRejectedError(
            f"cost ${cost:.2f} exceeds per-trade cap ${MAX_COST_PER_TRADE:.2f}"
        )
    cash = cash_balance(existing)
    if cost > cash:
        raise TradeRejectedError(f"cost ${cost:.2f} exceeds free cash ${cash:.2f}")

    close_raw = market.get("close_time") or market.get("expiration_time")
    close_time = None
    if close_raw:
        try:
            close_time = datetime.fromisoformat(
                str(close_raw).replace("Z", "+00:00")
            ).astimezone(UTC)
        except ValueError:
            close_time = None

    return {
        "trade_id": uuid.uuid4().hex,
        "opened_at_utc": now_utc,
        "market_ticker": ticker,
        "event_ticker": market.get("event_ticker"),
        "category": market.get("category"),
        "title": str(market.get("title") or market.get("subtitle") or "")[:200],
        "side": side,
        "count": count,
        "entry_price": entry_price,
        "fee": fee,
        "cost": cost,
        "yes_bid_at_open": yes_bid,
        "yes_ask_at_open": yes_ask,
        "volume_24h_at_open": num_field(market, "volume_24h"),
        "close_time_utc": close_time,
        "thesis": thesis.strip(),
        "strategy_version": strategy_version.strip(),
        "status": "OPEN",
        "settled_at_utc": None,
        "result": None,
        "payoff": None,
        "pnl": None,
    }


def apply_result(trade: dict, market: dict[str, Any], now_utc: datetime) -> bool:
    """Settle one OPEN trade from a fresh market record. Returns True if it changed."""
    if trade["status"] != "OPEN":
        return False
    status = market.get("status")
    result = str(market.get("result") or "").lower()
    if status in ("settled", "finalized", "determined") and result in ("yes", "no"):
        won = result == trade["side"]
        payoff = float(trade["count"]) * 1.0 if won else 0.0
        trade.update({
            "status": "SETTLED",
            "settled_at_utc": now_utc,
            "result": result,
            "payoff": payoff,
            "pnl": round(payoff - float(trade["cost"]), 2),
        })
        return True
    if status in ("settled", "finalized") and result in ("void", "scratch", "all_no", ""):
        # Voided/scratched: full refund, no PnL impact.
        trade.update({
            "status": "VOID",
            "settled_at_utc": now_utc,
            "result": "void",
            "payoff": None,
            "pnl": 0.0,
        })
        return True
    return False


def settle_open_trades(
    trades: list[dict],
    *,
    client: KalshiClient | None = None,
    now_utc: datetime | None = None,
) -> int:
    """Poll each OPEN trade's market once; settle what has resolved. Returns count."""
    client = client or KalshiClient()
    now_utc = now_utc or datetime.now(UTC)
    changed = 0
    for t in trades:
        if t["status"] != "OPEN":
            continue
        market = client.get_market(t["market_ticker"])
        if market and apply_result(t, market, now_utc):
            changed += 1
    return changed


def _agg(rows: list[dict]) -> dict:
    settled = [t for t in rows if t["status"] == "SETTLED"]
    wins = sum(1 for t in settled if (t.get("pnl") or 0.0) > 0)
    staked = sum(float(t["cost"]) for t in settled)
    pnl = sum(float(t.get("pnl") or 0.0) for t in settled)
    return {
        "n": len(settled),
        "wins": wins,
        "win_rate": wins / len(settled) if settled else None,
        "staked": staked,
        "pnl": pnl,
        "roi": pnl / staked if staked else None,
    }


def render_performance(trades: list[dict], *, now_utc: datetime | None = None) -> str:
    """Markdown scorecard: overall, by strategy version, by category, open book."""
    now_utc = now_utc or datetime.now(UTC)
    overall = _agg(trades)
    cash = cash_balance(trades)
    open_rows = [t for t in trades if t["status"] == "OPEN"]
    open_cost = sum(float(t["cost"]) for t in open_rows)

    def _pct(x: float | None) -> str:
        return f"{x * 100:+.1f}%" if x is not None else "-"

    def _wr(x: float | None) -> str:
        return f"{x * 100:.0f}%" if x is not None else "-"

    lines = [
        "# Agent paper-trading performance",
        "",
        f"_Generated {now_utc.strftime('%Y-%m-%d %H:%M UTC')} by `polymarket agent-report`. "
        "PAPER ONLY. See `strategy.md` for the playbook and `journal.md` for reasoning._",
        "",
        "## Bankroll",
        "",
        "| metric | value |",
        "|:-------|------:|",
        f"| starting bankroll | ${STARTING_BANKROLL:.2f} |",
        f"| free cash | ${cash:.2f} |",
        f"| open positions | {len(open_rows)} (${open_cost:.2f} at risk) |",
        f"| settled | {overall['n']} ({overall['wins']} wins, {_wr(overall['win_rate'])}) |",
        f"| realized PnL | ${overall['pnl']:+.2f} on ${overall['staked']:.2f} staked "
        f"({_pct(overall['roi'])}) |",
        "",
        "## By strategy version",
        "",
        "| version | n | wins | win_rate | staked$ | pnl$ | roi |",
        "|:--------|--:|-----:|---------:|--------:|-----:|----:|",
    ]
    by_version: dict[str, list[dict]] = {}
    for t in trades:
        by_version.setdefault(str(t["strategy_version"]), []).append(t)
    for version in sorted(by_version):
        a = _agg(by_version[version])
        lines.append(
            f"| {version} | {a['n']} | {a['wins']} | {_wr(a['win_rate'])} "
            f"| {a['staked']:.2f} | {a['pnl']:+.2f} | {_pct(a['roi'])} |"
        )
    lines += [
        "",
        "## By category",
        "",
        "| category | n | wins | win_rate | staked$ | pnl$ | roi |",
        "|:---------|--:|-----:|---------:|--------:|-----:|----:|",
    ]
    by_cat: dict[str, list[dict]] = {}
    for t in trades:
        by_cat.setdefault(str(t.get("category") or "Uncategorized"), []).append(t)
    for cat in sorted(by_cat):
        a = _agg(by_cat[cat])
        lines.append(
            f"| {cat} | {a['n']} | {a['wins']} | {_wr(a['win_rate'])} "
            f"| {a['staked']:.2f} | {a['pnl']:+.2f} | {_pct(a['roi'])} |"
        )
    lines += [
        "",
        "## Open positions",
        "",
        "| opened | ticker | side | count | entry$ | cost$ | strategy | thesis |",
        "|:-------|:-------|:-----|------:|-------:|------:|:---------|:-------|",
    ]
    for t in sorted(open_rows, key=lambda t: t["opened_at_utc"]):
        opened = t["opened_at_utc"]
        opened_s = opened.strftime("%m-%d %H:%M") if isinstance(opened, datetime) else str(opened)
        thesis = str(t["thesis"]).replace("|", "/")[:80]
        lines.append(
            f"| {opened_s} | {t['market_ticker']} | {t['side']} | {t['count']} "
            f"| {t['entry_price']:.2f} | {t['cost']:.2f} | {t['strategy_version']} | {thesis} |"
        )
    lines += [
        "",
        "## Last 20 settled",
        "",
        "| settled | ticker | side | entry$ | pnl$ | strategy | thesis |",
        "|:--------|:-------|:-----|-------:|-----:|:---------|:-------|",
    ]
    settled_rows = sorted(
        (t for t in trades if t["status"] == "SETTLED"),
        key=lambda t: t["settled_at_utc"] or now_utc,
        reverse=True,
    )[:20]
    for t in settled_rows:
        ts = t["settled_at_utc"]
        ts_s = ts.strftime("%m-%d") if isinstance(ts, datetime) else str(ts)
        thesis = str(t["thesis"]).replace("|", "/")[:80]
        lines.append(
            f"| {ts_s} | {t['market_ticker']} | {t['side']} | {t['entry_price']:.2f} "
            f"| {(t.get('pnl') or 0.0):+.2f} | {t['strategy_version']} | {thesis} |"
        )
    lines.append("")
    return "\n".join(lines)
