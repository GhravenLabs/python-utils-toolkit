"""Tests for utils/cache_utils.py"""
import time
import pytest
from utils.cache_utils import TTLCache, memoize


class TestTTLCache:
    def test_none_is_a_present_cached_value(self):
        cache = TTLCache()
        cache.set("empty", None)
        assert "empty" in cache
        assert "missing" not in cache

    def test_updating_existing_key_does_not_evict_another_entry(self):
        cache = TTLCache(maxsize=2)
        cache.set("first", 1, ttl=10)
        cache.set("second", 2, ttl=100)
        cache.set("second", 3)
        assert cache.get("first") == 1
        assert cache.get("second") == 3

    def test_set_and_get(self):
        cache = TTLCache(ttl=10)
        cache.set("key", "value")
        assert cache.get("key") == "value"

    def test_missing_key_returns_default(self):
        cache = TTLCache()
        assert cache.get("missing") is None
        assert cache.get("missing", "fallback") == "fallback"

    def test_expired_entry_returns_default(self):
        cache = TTLCache(ttl=0.05)
        cache.set("k", "v")
        time.sleep(0.1)
        assert cache.get("k") is None

    def test_delete(self):
        cache = TTLCache()
        cache.set("k", 1)
        cache.delete("k")
        assert cache.get("k") is None

    def test_clear(self):
        cache = TTLCache()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.get("a") is None
        assert cache.get("b") is None

    def test_contains(self):
        cache = TTLCache(ttl=10)
        cache.set("x", 99)
        assert "x" in cache
        assert "y" not in cache

    def test_maxsize_evicts_oldest(self):
        cache = TTLCache(ttl=60, maxsize=2)
        cache.set("a", 1)
        time.sleep(0.01)
        cache.set("b", 2)
        time.sleep(0.01)
        cache.set("c", 3)  # should evict "a"
        assert cache.get("c") == 3
        assert cache.get("b") == 2

    def test_per_key_ttl_override(self):
        cache = TTLCache(ttl=60)
        cache.set("short", "v", ttl=0.05)
        time.sleep(0.1)
        assert cache.get("short") is None


class TestMemoize:
    def test_none_result_is_cached(self):
        calls = []

        @memoize()
        def lookup():
            calls.append(True)
            return None

        assert lookup() is None
        assert lookup() is None
        assert len(calls) == 1

    def test_reusing_decorator_keeps_function_caches_separate(self):
        cached = memoize()

        @cached
        def first(value):
            return value + 1

        @cached
        def second(value):
            return value + 2

        assert first(10) == 11
        assert second(10) == 12
        assert first(10) == 11

    def test_caches_result(self):
        call_count = [0]

        @memoize(ttl=10)
        def fn(x):
            call_count[0] += 1
            return x * 2

        assert fn(3) == 6
        assert fn(3) == 6
        assert call_count[0] == 1  # only called once

    def test_different_args_cached_separately(self):
        @memoize(ttl=10)
        def fn(x):
            return x + 1

        assert fn(1) == 2
        assert fn(2) == 3

    def test_expired_result_recalculated(self):
        call_count = [0]

        @memoize(ttl=0.05)
        def fn(x):
            call_count[0] += 1
            return x

        fn("a")
        time.sleep(0.1)
        fn("a")
        assert call_count[0] == 2
