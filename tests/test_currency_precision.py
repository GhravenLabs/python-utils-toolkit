import pytest
from utils.number_utils import format_currency

@pytest.mark.parametrize('decimals', [True, False, 1.5, -1])
def test_invalid_precision_rejected(decimals):
    with pytest.raises(ValueError, match='decimals'):
        format_currency(12.34, decimals=decimals)

def test_zero_decimal_currency():
    assert format_currency(12.34, decimals=0) == '$12'
