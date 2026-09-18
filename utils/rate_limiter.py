"""Token-bucket rate limiter — sync and async variants.

Usage
-----
Sync:
>>> limiter = RateLimiter(calls_per_second=5)
>>> limiter.acquire()   # blocks if bucket is empty

Async:
>>> limiter = AsyncRateLimiter(calls_per_second=10)
>>> await limiter.acquire()
"""

from __future__ import annotations

import asyncio
import math
import threading
import time


def _capacity(rate: float, burst: int | None) -> float:
    if not math.isfinite(rate) or rate <= 0:
        raise ValueError("calls_per_second must be finite and positive")
    capacity = max(1.0, rate) if burst is None else float(burst)
    if not math.isfinite(capacity) or capacity <= 0:
        raise ValueError("burst must be finite and positive")
    return capacity


def _validate_tokens(tokens: float, capacity: float) -> None:
    if not math.isfinite(tokens) or not 0 < tokens <= capacity:
        raise ValueError("tokens must be finite, positive and no greater than capacity")


class RateLimiter:
    """Thread-safe token-bucket rate limiter.

    Parameters
    ----------
    calls_per_second:
        Maximum sustained call rate.
    burst:
        Maximum tokens that can accumulate (default = max(1, calls_per_second)).
    """

    def __init__(self, calls_per_second: float, burst: int | None = None) -> None:
        self._rate = calls_per_second
        self._capacity = _capacity(calls_per_second, burst)
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
        self._last_refill = now

    def acquire(self, tokens: float = 1.0) -> None:
        """Block for tokens; reject nonpositive, nonfinite or over-capacity requests."""
        _validate_tokens(tokens, self._capacity)
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                wait = (tokens - self._tokens) / self._rate
            time.sleep(wait)

    def __call__(self, tokens: float = 1.0) -> None:
        """Alias for :meth:`acquire` — makes the limiter callable."""
        self.acquire(tokens)


class AsyncRateLimiter:
    """Asyncio-compatible token-bucket rate limiter.

    Parameters
    ----------
    calls_per_second:
        Maximum sustained call rate.
    burst:
        Maximum tokens that can accumulate (default = max(1, calls_per_second)).
    """

    def __init__(self, calls_per_second: float, burst: int | None = None) -> None:
        self._rate = calls_per_second
        self._capacity = _capacity(calls_per_second, burst)
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
        self._last_refill = now

    async def acquire(self, tokens: float = 1.0) -> None:
        """Await tokens; reject nonpositive, nonfinite or over-capacity requests."""
        _validate_tokens(tokens, self._capacity)
        while True:
            async with self._lock:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                wait = (tokens - self._tokens) / self._rate
            await asyncio.sleep(wait)
