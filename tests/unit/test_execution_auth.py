"""KalshiAuth signer: signed message format, header set, RSA-PSS signature validity."""
from __future__ import annotations

import base64

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from polymarket_model.execution.auth import KalshiAuth, _normalize_pem, sign_message


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


def _pem_bytes(priv: rsa.RSAPrivateKey) -> bytes:
    return priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )


def test_from_settings_prefers_inline_pem_over_path(keypair, monkeypatch, tmp_path):
    priv, _ = keypair
    pem = _pem_bytes(priv).decode("ascii")
    # Write a *different* key to disk so we can prove inline wins.
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    bogus_path = tmp_path / "other.pem"
    bogus_path.write_bytes(_pem_bytes(other))

    from polymarket_model.execution import auth as auth_mod
    monkeypatch.setattr(auth_mod.settings, "kalshi_api_key_id", "the-id")
    monkeypatch.setattr(auth_mod.settings, "kalshi_private_key_pem", pem)
    monkeypatch.setattr(auth_mod.settings, "kalshi_private_key_path", bogus_path)

    loaded = KalshiAuth.from_settings()
    assert loaded.key_id == "the-id"
    # The key loaded from inline PEM must match `priv`, not the bogus file.
    assert loaded.private_key.private_numbers().d == priv.private_numbers().d
    assert loaded.private_key.private_numbers().d != other.private_numbers().d


def test_from_settings_falls_back_to_path_when_no_inline_pem(keypair, monkeypatch, tmp_path):
    priv, _ = keypair
    pem_file = tmp_path / "key.pem"
    pem_file.write_bytes(_pem_bytes(priv))

    from polymarket_model.execution import auth as auth_mod
    monkeypatch.setattr(auth_mod.settings, "kalshi_api_key_id", "id-2")
    monkeypatch.setattr(auth_mod.settings, "kalshi_private_key_pem", None)
    monkeypatch.setattr(auth_mod.settings, "kalshi_private_key_path", pem_file)

    loaded = KalshiAuth.from_settings()
    assert loaded.private_key.private_numbers().d == priv.private_numbers().d


def test_from_settings_raises_when_neither_pem_nor_path_set(monkeypatch):
    from polymarket_model.execution import auth as auth_mod
    monkeypatch.setattr(auth_mod.settings, "kalshi_api_key_id", "id")
    monkeypatch.setattr(auth_mod.settings, "kalshi_private_key_pem", None)
    monkeypatch.setattr(auth_mod.settings, "kalshi_private_key_path", None)
    with pytest.raises(RuntimeError, match="set either KALSHI_PRIVATE_KEY_PEM"):
        KalshiAuth.from_settings()


def test_normalize_pem_converts_literal_backslash_n_to_real_newlines(keypair):
    priv, _ = keypair
    pem = _pem_bytes(priv).decode("ascii")
    one_liner = pem.replace("\n", "\\n")
    normalized = _normalize_pem(one_liner)
    # Should load successfully and produce the same key.
    loaded = serialization.load_pem_private_key(normalized, password=None)
    assert isinstance(loaded, rsa.RSAPrivateKey)
    assert loaded.private_numbers().d == priv.private_numbers().d


def test_normalize_pem_rejects_value_missing_begin_marker():
    with pytest.raises(ValueError, match="doesn't look like a PEM"):
        _normalize_pem("notapem")
