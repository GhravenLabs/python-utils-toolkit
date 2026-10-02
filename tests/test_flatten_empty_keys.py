import pytest

from utils.dict_utils import flatten_dict


@pytest.mark.parametrize("separator", [".", "/"])
def test_empty_parent_remains_in_flattened_path(separator):
    assert flatten_dict({"": {"name": "nested"}, "name": "root"}, separator) == {
        separator + "name": "nested", "name": "root",
    }


def test_multiple_empty_parents_preserve_each_path_segment():
    assert flatten_dict({"": {"": {"name": 1}}}) == {"..name": 1}


def test_empty_segment_still_detects_real_path_collision():
    with pytest.raises(ValueError, match="collide"):
        flatten_dict({"": {"name": 1}, ".name": 2})
