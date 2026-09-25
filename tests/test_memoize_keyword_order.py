from utils.cache_utils import memoize


def test_keyword_order_is_part_of_cached_result_identity():
    calls = []

    @memoize()
    def columns(**values):
        calls.append(tuple(values))
        return list(values.items())

    forward = [('name', 'Acme'), ('city', 'Manila')]
    reverse = list(reversed(forward))
    assert columns(**dict(forward)) == forward
    assert columns(**dict(reverse)) == reverse
    assert columns(**dict(forward)) == forward
    assert columns(**dict(reverse)) == reverse
    assert calls == [('name', 'city'), ('city', 'name')]
