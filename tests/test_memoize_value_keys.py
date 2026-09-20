from utils.cache_utils import memoize

def test_identical_representations_do_not_share_cache_entries():
    class Item:
        def __init__(self, value): self.value = value
        def __repr__(self): return "Item"
    calls = []
    @memoize()
    def read(item):
        calls.append(item)
        return item.value
    a, b = Item(1), Item(2)
    assert [read(a), read(b), read(a)] == [1, 2, 1]
    assert len(calls) == 2

def test_unhashable_values_bypass_cache_and_types_stay_distinct():
    @memoize()
    def read(value): return type(value).__name__, str(value)
    assert read(1) != read(1.0)
    value = [1]
    assert read(value)[1] == "[1]"
    value.append(2)
    assert read(value)[1] == "[1, 2]"
