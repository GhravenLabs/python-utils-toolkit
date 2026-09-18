from utils.dict_utils import flatten_dict

def test_empty_objects_are_not_silently_lost():
    assert flatten_dict({'config': {}, 'nested': {'empty': {}}}) == {'config': {}, 'nested.empty': {}}
    assert flatten_dict({}) == {}
