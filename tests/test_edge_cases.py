"""Behavioral regressions for invalid bounds and edge-case inputs."""
import asyncio
import importlib
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from utils.async_utils import async_retry
from utils.cache_utils import TTLCache
from utils.datetime_utils import humanize_delta, parse_date
from utils.dict_utils import safe_get
from utils.list_utils import chunk
from utils.rate_limiter import AsyncRateLimiter, RateLimiter
from utils.retry import retry
from utils.string_utils import slugify, truncate
from utils.validation_utils import is_valid_email, is_valid_symbol


def test_zero_ttl_expires_at_current_time(monkeypatch):
    monkeypatch.setattr("utils.cache_utils.time.monotonic", lambda: 100.0)
    cache = TTLCache(ttl=60)
    cache.set("value", "stale", ttl=0)
    assert cache.get("value", "missing") == "missing"


@pytest.mark.parametrize("capacity", [0, -1, 1.5, True])
def test_cache_rejects_invalid_capacity(capacity):
    with pytest.raises(ValueError):
        TTLCache(maxsize=capacity)


@pytest.mark.parametrize("cls", [RateLimiter, AsyncRateLimiter])
def test_fractional_rate_allows_default_token(cls, monkeypatch):
    monkeypatch.setattr("utils.rate_limiter.time.sleep", lambda _: pytest.fail("unfillable bucket"))
    monkeypatch.setattr("utils.rate_limiter.asyncio.sleep", AsyncMock(side_effect=AssertionError("unfillable bucket")))
    limiter = cls(0.5)
    if cls is AsyncRateLimiter:
        asyncio.run(limiter.acquire())
    else:
        limiter.acquire()


@pytest.mark.parametrize("cls", [RateLimiter, AsyncRateLimiter])
@pytest.mark.parametrize("kwargs", [{"calls_per_second": 0}, {"calls_per_second": -1},
    {"calls_per_second": float("nan")}, {"calls_per_second": float("inf")},
    {"calls_per_second": 1, "burst": 0}, {"calls_per_second": 1, "burst": -1}])
def test_invalid_limiter_configuration_fails_early(cls, kwargs):
    with pytest.raises(ValueError):
        cls(**kwargs)


@pytest.mark.parametrize("cls", [RateLimiter, AsyncRateLimiter])
@pytest.mark.parametrize("tokens", [-1, 0, 3, float("nan"), float("inf")])
def test_invalid_token_request_does_not_wait(cls, tokens, monkeypatch):
    monkeypatch.setattr("utils.rate_limiter.time.sleep", lambda _: pytest.fail("must reject before waiting"))
    monkeypatch.setattr("utils.rate_limiter.asyncio.sleep", AsyncMock(side_effect=AssertionError("must reject before waiting")))
    limiter = cls(1, burst=2)
    with pytest.raises(ValueError):
        if cls is AsyncRateLimiter:
            asyncio.run(limiter.acquire(tokens))
        else:
            limiter.acquire(tokens)


def test_retry_jitter_obeys_max_delay(monkeypatch):
    module = importlib.import_module("utils.retry")
    waits = []
    monkeypatch.setattr(module.random, "uniform", lambda *_: 1.25)
    monkeypatch.setattr(module.time, "sleep", waits.append)

    @retry(max_attempts=2, base_delay=60, max_delay=60)
    def fail():
        raise ValueError("expected")

    with pytest.raises(ValueError):
        fail()
    assert waits == [60]


@pytest.mark.parametrize("factory", [retry, async_retry])
@pytest.mark.parametrize("kwargs", [{"max_attempts": 0}, {"max_attempts": -1},
    {"base_delay": -1}, {"base_delay": float("nan")}, {"backoff": -1}])
def test_retry_rejects_invalid_configuration(factory, kwargs):
    with pytest.raises(ValueError):
        factory(**kwargs)


def test_parse_date_preserves_offset_instant():
    assert parse_date("2026-09-18 14:00 +0200", "%Y-%m-%d %H:%M %z") == datetime(2026, 9, 18, 12, tzinfo=timezone.utc)


def test_negative_duration_has_one_leading_sign():
    assert humanize_delta(-3661) == "-1h 1m 1s"
    assert humanize_delta(-1) == "-1s"


def test_identifier_rejects_trailing_newline():
    assert not is_valid_symbol("CLIENT42\n")


def test_email_rejects_nonstring_input():
    assert not is_valid_email(None)
    assert not is_valid_email(42)


def test_slug_punctuation_preserves_word_boundary():
    assert slugify("docs/api:v2") == "docs-api-v2"


def test_negative_truncation_length_is_rejected():
    with pytest.raises(ValueError):
        truncate("abcdef", -1)


def test_negative_chunk_size_is_rejected():
    with pytest.raises(ValueError):
        list(chunk([1, 2], -1))


def test_safe_get_does_not_confuse_fallback_with_present_object():
    shared = {"answer": 42}
    assert safe_get({"nested": shared}, "nested", "answer", default=shared) == 42
