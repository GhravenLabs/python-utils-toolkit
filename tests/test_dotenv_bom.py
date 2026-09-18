from utils.env import Env

def test_first_setting_in_bom_file(tmp_path, monkeypatch):
    monkeypatch.delenv('BOM_CASE', raising=False)
    path = tmp_path / '.env'
    path.write_text('BOM_CASE=ready', encoding='utf-8-sig')
    assert Env(path).str('BOM_CASE') == 'ready'
