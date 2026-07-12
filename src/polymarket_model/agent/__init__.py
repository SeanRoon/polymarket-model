"""Self-directed paper-trading agent: whole-venue scan + independent paper ledger.

Everything here is PAPER ONLY — the ledger records hypothetical fills at live
take-side prices; no order-placement code exists in this repo. The agent
(`.claude/commands/self-trader.md`) forms its own strategy and does NOT use the
weather model's probabilities; this package just gives it eyes (scout) and a
scored track record (ledger).
"""
