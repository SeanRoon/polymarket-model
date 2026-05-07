"""Convert (model_p, market_mid) pairs into trade signals with Kelly sizing."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from polymarket_model.config import settings
from polymarket_model.markets.discovery import Bin, WeatherEvent
from polymarket_model.markets.prices import EventPrices
from polymarket_model.model import EventModelOutput


@dataclass(frozen=True)
class Signal:
    emitted_ts_utc: datetime
    event: WeatherEvent
    bin: Bin
    direction: str            # 'BUY_YES' | 'BUY_NO'
    entry_token_id: str       # the token to BUY (yes for BUY_YES, no for BUY_NO)
    entry_price: float        # the price you'd pay to enter (always in [0, 1])
    model_p_yes: float
    market_mid_yes: float
    edge_signed: float        # model_p_yes - market_mid_yes; positive => buy YES
    abs_edge: float
    kelly_full: float         # full-Kelly fraction-of-bankroll
    kelly_sized: float        # kelly_full * settings.kelly_fraction
    lead_hours: int
    outside_bin_mass: float
    sum_of_mids: float
    n_members: int
    model_name: str


def _kelly_buy(p_true: float, p_entry: float) -> float:
    """Classic Kelly fraction for a 1:1 payout where you buy at p_entry hoping outcome holds with prob p_true.
    f* = (p_true - p_entry) / (1 - p_entry).
    Returns 0 if p_entry >= 1 or edge non-positive (caller should screen first).
    """
    if p_entry >= 1.0 or p_entry <= 0.0:
        return 0.0
    f = (p_true - p_entry) / (1.0 - p_entry)
    return max(0.0, f)


def signals_for_event(
    model_out: EventModelOutput,
    prices: EventPrices,
    *,
    min_edge: float | None = None,
    kelly_multiplier: float | None = None,
    now: datetime | None = None,
) -> list[Signal]:
    """Emit one Signal per bin where |model_p - market_mid| >= min_edge."""
    if not model_out.passes_qc or not prices.passes_qc:
        return []
    min_edge = min_edge if min_edge is not None else settings.min_edge
    kelly_multiplier = kelly_multiplier if kelly_multiplier is not None else settings.kelly_fraction
    now = now or datetime.now(UTC)

    lead_hours = max(0, int((model_out.event.end_date_utc - now).total_seconds() // 3600))

    signals: list[Signal] = []
    for bp, pp in zip(model_out.bin_probs, prices.prices, strict=True):
        if pp.midpoint is None:
            continue
        market_yes = float(pp.midpoint)
        model_yes = float(bp.p)
        edge_signed = model_yes - market_yes
        if abs(edge_signed) < min_edge:
            continue
        if edge_signed > 0:
            direction = "BUY_YES"
            entry_token = bp.bin.yes_token_id
            entry_price = market_yes
            kelly_full = _kelly_buy(p_true=model_yes, p_entry=entry_price)
        else:
            direction = "BUY_NO"
            entry_token = bp.bin.no_token_id
            entry_price = 1.0 - market_yes
            kelly_full = _kelly_buy(p_true=1.0 - model_yes, p_entry=entry_price)
        signals.append(Signal(
            emitted_ts_utc=now,
            event=model_out.event,
            bin=bp.bin,
            direction=direction,
            entry_token_id=entry_token,
            entry_price=entry_price,
            model_p_yes=model_yes,
            market_mid_yes=market_yes,
            edge_signed=edge_signed,
            abs_edge=abs(edge_signed),
            kelly_full=kelly_full,
            kelly_sized=kelly_full * kelly_multiplier,
            lead_hours=lead_hours,
            outside_bin_mass=model_out.outside_bin_mass,
            sum_of_mids=prices.sum_of_mids,
            n_members=int(model_out.distribution.n),
            model_name=model_out.distribution.model,
        ))
    return signals
