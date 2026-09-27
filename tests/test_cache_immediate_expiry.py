import pytest

from utils.cache_utils import TTLCache


@pytest.mark.parametrize("ttl", [0, -1])
def test_immediately_expired_insert_preserves_live_entry(ttl):
    cache = TTLCache(maxsize=1)
    cache.set("useful", "keep")
    cache.set("expired", "discard", ttl=ttl)
    assert cache.get("useful") == "keep"
    assert "expired" not in cache


@pytest.mark.parametrize("ttl", [0, -1])
def test_immediate_expiry_invalidates_existing_key(ttl):
    cache = TTLCache(maxsize=2)
    cache.set("old", "stale")
    cache.set("other", "keep")
    cache.set("old", "discard", ttl=ttl)
    assert "old" not in cache
    assert cache.get("other") == "keep"


def test_zero_default_ttl_does_not_evict_positive_override():
    cache = TTLCache(ttl=0, maxsize=1)
    cache.set("useful", "keep", ttl=60)
    cache.set("expired", "discard")
    assert cache.get("useful") == "keep"
