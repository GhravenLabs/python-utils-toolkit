import os
import pytest
from utils.env import Env

@pytest.mark.parametrize('raw, expected', [("don't", "don't"), ('"say \"hi\""', 'say \"hi\"'), ("'hello'", 'hello'), ('trailing"', 'trailing"')])
def test_only_matching_outer_quotes_removed(tmp_path, monkeypatch, raw, expected):
    monkeypatch.delenv('QUOTE_CASE', raising=False)
    path = tmp_path / '.env'
    path.write_text('QUOTE_CASE=' + raw, encoding='utf-8')
    assert Env(path).str('QUOTE_CASE') == expected
