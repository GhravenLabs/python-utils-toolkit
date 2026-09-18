"""Async utilities — timeout helpers, gather with error handling, async retry."""

from __future__ import annotations
import asyncio
import functools
import logging
import random
from typing import Any, Callable, Coroutine, TypeVar
from .retry import _validate_retry

logger = logging.getLogger(__name__)
T = TypeVar("T")


async def with_timeout(coro: Coroutine, seconds: float, default: Any = None) -> Any:
    """Run coroutine with a timeout, returning *default* on timeout.

    >>> result = await with_timeout(fetch(), seconds=5.0, default={})
    """
    try:
        return await asyncio.wait_for(coro, timeout=seconds)
    except asyncio.TimeoutError:
        logger.warning("Coroutine timed out after %.1fs", seconds)
        return default


async def gather_safe(*coros: Coroutine) -> list[Any]:
    """Return None for failed/cancelled children; parent cancellation propagates.

    >>> results = await gather_safe(fetch_a(), fetch_b(), fetch_c())
    """
    results = await asyncio.gather(*coros, return_exceptions=True)
    return [None if isinstance(r, (Exception, asyncio.CancelledError)) else r for r in results]


def async_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    backoff: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,),
):
    """Async version of the retry decorator with exponential backoff.

    >>> @async_retry(max_attempts=3, base_delay=0.5)
    ... async def fetch_price(symbol: str) -> float:
    ...     return await api.get_price(symbol)
    """
    _validate_retry(max_attempts, base_delay, backoff)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = base_delay
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt == max_attempts:
                        raise
                    wait = delay * (random.uniform(0.75, 1.25) if jitter else 1.0)
                    logger.warning("%s attempt %d/%d failed. Retrying in %.2fs",
                                   func.__name__, attempt, max_attempts, wait)
                    await asyncio.sleep(wait)
                    delay *= backoff
            raise last_exc  # type: ignore
        return wrapper
    return decorator


async def run_sequential(coros: list[Coroutine]) -> list[Any]:
    """Run coroutines one by one and return all results."""
    return [await coro for coro in coros]
