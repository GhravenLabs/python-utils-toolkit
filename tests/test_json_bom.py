from utils.file_helpers import read_json

def test_reads_bom_prefixed_export(tmp_path):
    path = tmp_path / 'export.json'
    path.write_text('{"name": "café"}', encoding='utf-8-sig')
    assert read_json(path) == {'name': 'café'}
