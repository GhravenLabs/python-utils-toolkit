"""Tests for utils/async_utils.py"""
import asyncio
import pytest
from utils.async_utils import with_timeout, gather_safe, async_retry, run_sequential


@pytest.mark.asyncio
async def test_async_retry_caps_backoff_and_jitter(monkeypatch):
    waits = []

    async def sleep(seconds):
        waits.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", sleep)
    monkeypatch.setattr("utils.async_utils.random.uniform", lambda *_: 1.25)

    @async_retry(max_attempts=4, base_delay=10, backoff=10, max_delay=2)
    async def fail():
        raise ConnectionError("offline")

    with pytest.raises(ConnectionError):
        await fail()
    assert waits == [2, 2, 2]


@pytest.mark.parametrize("delay", [-1, float("inf"), float("nan")])
def test_async_retry_rejects_invalid_max_delay(delay):
    with pytest.raises(ValueError, match="max_delay"):
        async_retry(max_delay=delay)


@pytest.mark.asyncio
async def test_with_timeout_completes():
    async def fast():
        return 42
    result = await with_timeout(fast(), seconds=1.0)
    assert result == 42


@pytest.mark.asyncio
async def test_with_timeout_returns_default_on_timeout():
    async def slow():
        await asyncio.sleep(10)
    result = await with_timeout(slow(), seconds=0.05, default="timed_out")
    assert result == "timed_out"


@pytest.mark.asyncio
async def test_gather_safe_returns_none_for_failed():
    async def ok():
        return 1
    async def bad():
        raise ValueError("boom")
    results = await gather_safe(ok(), bad(), ok())
    assert results == [1, None, 1]


@pytest.mark.asyncio
async def test_gather_safe_all_succeed():
    async def fn(x):
        return x * 2
    results = await gather_safe(fn(1), fn(2), fn(3))
    assert results == [2, 4, 6]


@pytest.mark.asyncio
async def test_async_retry_succeeds_on_first_attempt():
    calls = [0]
    @async_retry(max_attempts=3)
    async def fn():
        calls[0] += 1
        return "ok"
    result = await fn()
    assert result == "ok"
    assert calls[0] == 1


@pytest.mark.asyncio
async def test_async_retry_retries_on_failure():
    calls = [0]
    @async_retry(max_attempts=3, base_delay=0.01)
    async def fn():
        calls[0] += 1
        if calls[0] < 3:
            raise ConnectionError("retry me")
        return "done"
    result = await fn()
    assert result == "done"
    assert calls[0] == 3


@pytest.mark.asyncio
async def test_async_retry_raises_after_max_attempts():
    @async_retry(max_attempts=2, base_delay=0.01)
    async def always_fails():
        raise RuntimeError("fail")
    with pytest.raises(RuntimeError):
        await always_fails()


@pytest.mark.asyncio
async def test_run_sequential():
    async def fn(x):
        return x
    results = await run_sequential([fn(1), fn(2), fn(3)])
    assert results == [1, 2, 3]


@pytest.mark.asyncio
@pytest.mark.parametrize("error", [ValueError, asyncio.CancelledError])
async def test_run_sequential_closes_unstarted_coroutines(error):
    import inspect

    async def fail():
        raise error()

    async def pending():
        pytest.fail("later steps must not execute")

    later = pending()
    with pytest.raises(error):
        await run_sequential([fail(), later])
    assert inspect.getcoroutinestate(later) == inspect.CORO_CLOSED
