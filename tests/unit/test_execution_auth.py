"""KalshiAuth signer: signed message format, header set, RSA-PSS signature validity."""
from __future__ import annotations

import base64

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from polymarket_model.execution.auth import KalshiAuth, sign_message


@pytest.fixture(scope="module")
def keypair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    # 2048 is what Kalshi issues. 1024 would be faster but Kalshi's verifier
    # would reject it; matching the real key size makes the test honest.
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return priv, priv.public_key()


def _verify(pub: rsa.RSAPublicKey, signature_b64: str, message: bytes) -> None:
    sig = base64.b64decode(signature_b64)
    pub.verify(
        sig,
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=hashes.SHA256.digest_size),
        hashes.SHA256(),
    )


def test_sign_message_produces_valid_pss_signature(keypair):
    priv, pub = keypair
    msg = b"1700000000000GET/trade-api/v2/portfolio/balance"
    sig_b64 = sign_message(priv, msg)
    # Should round-trip through base64 cleanly.
    base64.b64decode(sig_b64)
    # Public key verifies the signature.
    _verify(pub, sig_b64, msg)


def test_sign_message_rejects_tampered_message(keypair):
    priv, pub = keypair
    msg = b"1700000000000GET/trade-api/v2/portfolio/balance"
    sig_b64 = sign_message(priv, msg)
    with pytest.raises(InvalidSignature):
        _verify(pub, sig_b64, msg + b"X")


def test_headers_contain_all_three_required_keys_and_signed_string_format(keypair):
    priv, pub = keypair
    auth = KalshiAuth(key_id="abcd-1234", private_key=priv)
    hdrs = auth.headers(method="GET", path="/trade-api/v2/portfolio/balance", now_ms=1700000000000)

    assert hdrs["KALSHI-ACCESS-KEY"] == "abcd-1234"
    assert hdrs["KALSHI-ACCESS-TIMESTAMP"] == "1700000000000"

    # Kalshi-defined signed message: timestamp + METHOD + path. Verify by
    # reconstructing the same string and checking the signature against pub.
    expected_message = b"1700000000000GET/trade-api/v2/portfolio/balance"
    _verify(pub, hdrs["KALSHI-ACCESS-SIGNATURE"], expected_message)


def test_headers_uppercases_lowercase_method(keypair):
    priv, pub = keypair
    auth = KalshiAuth(key_id="k", private_key=priv)
    hdrs = auth.headers(method="get", path="/trade-api/v2/portfolio/balance", now_ms=1)
    _verify(pub, hdrs["KALSHI-ACCESS-SIGNATURE"], b"1GET/trade-api/v2/portfolio/balance")


def test_headers_default_timestamp_is_milliseconds(keypair, monkeypatch):
    priv, _ = keypair
    auth = KalshiAuth(key_id="k", private_key=priv)
    monkeypatch.setattr("polymarket_model.execution.auth.time.time", lambda: 1700000000.123)
    hdrs = auth.headers(method="GET", path="/x")
    assert hdrs["KALSHI-ACCESS-TIMESTAMP"] == "1700000000123"
