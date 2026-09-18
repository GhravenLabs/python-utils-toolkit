import pytest
from utils.string_utils import indent

@pytest.mark.parametrize('text, expected', [('a\n', '  a\n'), ('a\r\nb\r\n', '  a\r\n  b\r\n'), ('a\nb', '  a\n  b'), ('', '')])
def test_indent_keeps_original_terminators(text, expected):
    assert indent(text, spaces=2) == expected
