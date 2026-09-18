import pytest
from utils.file_helpers import write_json

def test_unserializable_value_keeps_existing_file(tmp_path):
    path = tmp_path / 'data.json'
    path.write_text('{"original": true}', encoding='utf-8')
    with pytest.raises(TypeError):
        write_json(path, {'bad': object()})
    assert path.read_text(encoding='utf-8') == '{"original": true}'

def test_replace_failure_keeps_original_and_cleans_temp(tmp_path, monkeypatch):
    path = tmp_path / 'data.json'
    path.write_text('{}', encoding='utf-8')
    def fail(*args):
        raise PermissionError('locked')
    monkeypatch.setattr('utils.file_helpers.os.replace', fail)
    with pytest.raises(PermissionError):
        write_json(path, {'new': True})
    assert path.read_text() == '{}'
    assert list(tmp_path.glob('.tmp_*')) == []
