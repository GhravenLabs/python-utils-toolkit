from utils.redaction_utils import redact_text

def test_literal_replacement_backslashes():
    assert redact_text('sk-exampletoken', replacement=r'\1\private') == r'\1\private'
