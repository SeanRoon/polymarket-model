"""Authenticated Kalshi API access (read-only for now).

This module talks to Kalshi's `/portfolio/*` endpoints — balance, positions,
fills. Order placement is intentionally NOT implemented here. When we add
trade execution it goes in a separate private repo (this one is public for
unlimited GHA minutes; we don't want order-placement code paths anywhere
near a public CI environment, even gated).

See CLAUDE.md "Authenticated Kalshi access" for setup.
"""
