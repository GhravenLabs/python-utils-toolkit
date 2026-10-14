"""Tests for utils/list_utils.py"""
import pytest
from utils.list_utils import chunk, flatten, deduplicate, first, last, batch_by


class TestChunk:
    def test_even_split(self):
        assert list(chunk([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    def test_uneven_split(self):
        assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    def test_chunk_larger_than_list(self):
        assert list(chunk([1, 2], 10)) == [[1, 2]]

    def test_empty_list(self):
        assert list(chunk([], 3)) == []


class TestFlatten:
    def test_one_level(self):
        assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_nested_stops_at_depth(self):
        assert flatten([[1, 2], [3, [4, 5]]]) == [1, 2, 3, [4, 5]]

    def test_deeper_flatten(self):
        assert flatten([[1, [2, [3]]]], depth=2) == [1, 2, [3]]

    def test_empty(self):
        assert flatten([]) == []


class TestDeduplicate:
    def test_preserves_order_for_unhashable_values(self):
        first = {"name": "Acme"}
        assert deduplicate([first, [1, 2], {"name": "Acme"}, [1, 2], [2, 1]]) == [
            first, [1, 2], [2, 1]
        ]

    def test_removes_dupes(self):
        assert deduplicate([1, 2, 1, 3, 2]) == [1, 2, 3]

    def test_preserves_order(self):
        assert deduplicate([3, 1, 2, 1, 3]) == [3, 1, 2]

    def test_no_dupes_unchanged(self):
        assert deduplicate([1, 2, 3]) == [1, 2, 3]

    def test_empty(self):
        assert deduplicate([]) == []


class TestFirstLast:
    def test_first(self):
        assert first([10, 20, 30]) == 10

    def test_first_empty_returns_default(self):
        assert first([], default=0) == 0
        assert first([]) is None

    def test_last(self):
        assert last([10, 20, 30]) == 30

    def test_last_empty_returns_default(self):
        assert last([], default=-1) == -1
        assert last([]) is None


class TestBatchBy:
    def test_group_by_mod(self):
        result = batch_by([1, 2, 3, 4], lambda x: x % 2)
        assert result[1] == [1, 3]
        assert result[0] == [2, 4]

    def test_empty(self):
        assert batch_by([], lambda x: x) == {}

    def test_all_same_group(self):
        result = batch_by([1, 2, 3], lambda x: "all")
        assert result == {"all": [1, 2, 3]}
