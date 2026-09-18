import pytest
from utils.number_utils import round_to_tick

@pytest.mark.parametrize('amount, increment', [(1, 0), (1, -0.1), (1, float('nan')), (1, float('inf')), (float('inf'), 0.1)])
def test_invalid_rounding_inputs(amount, increment):
    with pytest.raises(ValueError):
        round_to_tick(amount, increment)

def test_negative_amount_still_rounds():
    assert round_to_tick(-1.25, 0.1) == -1.3
