import pytest
from utils.list_utils import flatten

@pytest.mark.parametrize('depth', [-1, 0.5, True])
def test_invalid_depth_rejected(depth):
    with pytest.raises(ValueError, match='depth'):
        flatten([[1]], depth=depth)

def test_zero_depth_preserves_nesting():
    assert flatten([[1]], depth=0) == [[1]]
