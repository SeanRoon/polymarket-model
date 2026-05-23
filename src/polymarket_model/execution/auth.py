"""RSA-PSS request signing for Kalshi's authenticated endpoints.

Kalshi requires three headers on every authenticated request:
  KALSHI-ACCESS-KEY        - the API key ID (a UUID-style string)
  KALSHI-ACCESS-TIMESTAMP  - current time in MILLISECONDS since epoch, as a string
  KALSHI-ACCESS-SIGNATURE  - base64(RSA-PSS-SHA256(timestamp + METHOD + path))

The signed message is the byte concatenation of:
  - the timestamp string (same value as the header)
  - the HTTP method, UPPERCASE
  - the request path INCLUDING the API version prefix `/trade-api/v2`, no query string

PSS parameters: MGF1-SHA256, salt length = digest size (32 bytes for SHA-256).

This file lives in a public repo. That's safe: the *signer* being public is fine
(Kalshi's own SDK is open source); the *private key* is what authenticates you,
and that's loaded from a path outside the repo (gitignore covers `*.pem` regardless).
"""
from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from polymarket_model.config import settings


def _normalize_pem(raw: str) -> bytes:
    """Accept the PEM whether it's a real multiline string, has Windows line endings,
    or got pasted as a one-liner with literal `\\n` escape sequences (a common copy
    mishap from JSON snippets or shell quoting). Returns the canonical bytes."""
    s = raw.strip()
    if "-----BEGIN" not in s:
        raise ValueError("kalshi_private_key_pem doesn't look like a PEM (missing BEGIN marker)")
    if "\\n" in s and "\n" not in s:
        s = s.replace("\\n", "\n")
    return s.encode("ascii")


def _load_key_from_pem_bytes(pem: bytes, source: str) -> rsa.RSAPrivateKey:
    key = serialization.load_pem_private_key(pem, password=None)
    if not isinstance(key, rsa.RSAPrivateKey):
        raise TypeError(f"Expected RSA private key from {source}, got {type(key).__name__}")
    return key


def _load_private_key(path: Path) -> rsa.RSAPrivateKey:
    return _load_key_from_pem_bytes(path.read_bytes(), source=str(path))


def sign_message(private_key: rsa.RSAPrivateKey, message: bytes) -> str:
    """Sign `message` with RSA-PSS-SHA256 / MGF1-SHA256 / salt=digest_size; return base64."""
    sig = private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=hashes.SHA256.digest_size),
        hashes.SHA256(),
    )
    return base64.b64encode(sig).decode("ascii")


@dataclass(frozen=True)
class KalshiAuth:
    """Holds the API key ID and loaded private key, builds signed headers per request."""

    key_id: str
    private_key: rsa.RSAPrivateKey

    @classmethod
    def from_settings(cls) -> KalshiAuth:
        if not settings.kalshi_api_key_id:
            raise RuntimeError(
                "Kalshi auth not configured: KALSHI_API_KEY_ID is unset (see CLAUDE.md).",
            )
        if settings.kalshi_private_key_pem:
            key = _load_key_from_pem_bytes(
                _normalize_pem(settings.kalshi_private_key_pem),
                source="KALSHI_PRIVATE_KEY_PEM",
            )
        elif settings.kalshi_private_key_path:
            key = _load_private_key(settings.kalshi_private_key_path)
        else:
            raise RuntimeError(
                "Kalshi auth not configured: set either KALSHI_PRIVATE_KEY_PEM "
                "(inline PEM, recommended) or KALSHI_PRIVATE_KEY_PATH (path to PEM file).",
            )
        return cls(key_id=settings.kalshi_api_key_id, private_key=key)

    def headers(self, *, method: str, path: str, now_ms: int | None = None) -> dict[str, str]:
        """Build the three required auth headers for the given request.

        `path` must include the `/trade-api/v2` prefix and exclude any query string.
        """
        ts = str(now_ms if now_ms is not None else int(time.time() * 1000))
        message = (ts + method.upper() + path).encode("ascii")
        return {
            "KALSHI-ACCESS-KEY": self.key_id,
            "KALSHI-ACCESS-TIMESTAMP": ts,
            "KALSHI-ACCESS-SIGNATURE": sign_message(self.private_key, message),
        }
