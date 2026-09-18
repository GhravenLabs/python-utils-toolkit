from utils.env import Env

def test_empty_key_does_not_block_valid_settings(tmp_path, monkeypatch):
    monkeypatch.delenv('VALID_CASE', raising=False)
    path = tmp_path / '.env'
    path.write_text('=ignored\n  =ignored\nVALID_CASE=ready', encoding='utf-8')
    assert Env(path).str('VALID_CASE') == 'ready'
