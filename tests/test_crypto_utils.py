"""Tests for utils/crypto_utils.py"""
import pytest
from utils.crypto_utils import hmac_sha256, sha256, md5, generate_nonce, timestamp_nonce


def test_hmac_sha256_known_value():
    # Known reference: echo -n "client=ACME42" | openssl dgst -sha256 -hmac "secret"
    result = hmac_sha256("secret", "client=ACME42")
    assert isinstance(result, str)
    assert len(result) == 64  # hex-encoded SHA-256 is always 64 chars
    assert result == "0000b930a1653351394e4a4edea00aeb530e4198fe634ebdd557b7d7d3dccb28"


def test_hmac_sha256_deterministic():
    a = hmac_sha256("key", "msg")
    b = hmac_sha256("key", "msg")
    assert a == b


def test_hmac_sha256_different_secrets():
    assert hmac_sha256("key1", "msg") != hmac_sha256("key2", "msg")


def test_sha256_string():
    result = sha256("hello")
    assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_sha256_bytes():
    result = sha256(b"hello")
    assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_md5_string():
    result = md5("hello")
    assert result == "5d41402abc4b2a76b9719d911017c592"


def test_generate_nonce_length():
    nonce = generate_nonce(32)
    assert len(nonce) == 32
    nonce64 = generate_nonce(64)
    assert len(nonce64) == 64


def test_generate_nonce_is_unique():
    assert generate_nonce() != generate_nonce()


def test_timestamp_nonce_is_numeric_string():
    ts = timestamp_nonce()
    assert ts.isdigit()
    assert len(ts) == 13  # milliseconds since epoch
