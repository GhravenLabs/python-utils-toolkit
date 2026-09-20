import pytest
from utils.cache_utils import TTLCache

@pytest.mark.parametrize("ttl", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_ttl_rejected_without_eviction(ttl):
    with pytest.raises(ValueError, match="finite"):
        TTLCache(ttl=ttl)
    cache = TTLCache(maxsize=1)
    cache.set("existing", "keep")
    with pytest.raises(ValueError, match="finite"):
        cache.set("new", "bad", ttl=ttl)
    assert cache.get("existing") == "keep"
