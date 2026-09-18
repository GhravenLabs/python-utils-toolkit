from utils.env import Env

def test_export_prefix_and_existing_environment(tmp_path, monkeypatch):
    monkeypatch.delenv('EXPORTED_CASE', raising=False)
    monkeypatch.delenv('TAB_CASE', raising=False)
    monkeypatch.setenv('EXISTING_CASE', 'environment')
    path = tmp_path / '.env'
    path.write_text('export EXPORTED_CASE=yes\nexport\tTAB_CASE=ok\nexport EXISTING_CASE=file', encoding='utf-8')
    env = Env(path)
    assert env.str('EXPORTED_CASE') == 'yes'
    assert env.str('TAB_CASE') == 'ok'
    assert env.str('EXISTING_CASE') == 'environment'
