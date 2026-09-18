import pytest
from utils.number_utils import clamp

def test_reversed_bounds_are_not_silently_accepted():
    with pytest.raises(ValueError, match='min_val'):
        clamp(5, 10, 0)
    assert clamp(5, 3, 3) == 3
