import pytest
from utils.dict_utils import flatten_dict

@pytest.mark.parametrize('data', [{'a': {'b': 1}, 'a.b': 2}, {'a.b': 2, 'a': {'b': 1}}])
def test_collision_raises_instead_of_losing_value(data):
    with pytest.raises(ValueError, match='collide'):
        flatten_dict(data)
