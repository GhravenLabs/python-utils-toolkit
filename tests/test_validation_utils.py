"""Tests for utils/validation_utils.py"""
import pytest
from utils.validation_utils import (
    is_positive_number, is_valid_symbol, is_valid_email,
    require, require_keys, is_within_range
)


class TestIsPositiveNumber:
    def test_positive_int(self):
        assert is_positive_number(5) is True

    def test_positive_float(self):
        assert is_positive_number(0.01) is True

    def test_zero_is_not_positive(self):
        assert is_positive_number(0) is False

    def test_negative(self):
        assert is_positive_number(-1) is False

    def test_bool_excluded(self):
        assert is_positive_number(True) is False

    def test_string_excluded(self):
        assert is_positive_number("5") is False


class TestIsValidSymbol:
    def test_valid_no_slash(self):
        assert is_valid_symbol("CLIENT42") is True

    def test_valid_with_slash(self):
        assert is_valid_symbol("TEAM/API") is True

    def test_lowercase_normalised(self):
        assert is_valid_symbol("client42") is True

    def test_empty_string(self):
        assert is_valid_symbol("") is False

    def test_too_short(self):
        assert is_valid_symbol("A") is False

    def test_special_chars(self):
        assert is_valid_symbol("BTC-USDT") is False


class TestIsValidEmail:
    def test_valid(self):
        assert is_valid_email("user@example.com") is True

    def test_no_at(self):
        assert is_valid_email("userexample.com") is False

    def test_no_domain(self):
        assert is_valid_email("user@") is False

    def test_empty(self):
        assert is_valid_email("") is False


class TestRequire:
    def test_passes_when_true(self):
        require(True, "should not raise")

    def test_raises_when_false(self):
        with pytest.raises(ValueError, match="must be positive"):
            require(False, "must be positive")


class TestRequireKeys:
    def test_all_present(self):
        require_keys({"a": 1, "b": 2}, "a", "b")

    def test_missing_raises(self):
        with pytest.raises(KeyError):
            require_keys({"a": 1}, "a", "b")


class TestIsWithinRange:
    def test_inclusive_in_range(self):
        assert is_within_range(5, 1, 10) is True

    def test_inclusive_boundary(self):
        assert is_within_range(1, 1, 10) is True
        assert is_within_range(10, 1, 10) is True

    def test_exclusive_boundary(self):
        assert is_within_range(1, 1, 10, inclusive=False) is False

    def test_out_of_range(self):
        assert is_within_range(0, 1, 10) is False
        assert is_within_range(11, 1, 10) is False
