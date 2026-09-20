from utils.redaction_utils import redact_mapping

def test_separated_keys_and_custom_rules():
    assert redact_mapping({"API KEY": "x", "api-key": "y", "name": "ok"}) == {"API KEY": "[REDACTED]", "api-key": "[REDACTED]", "name": "ok"}
    assert redact_mapping({"client secret": "x"}, {"client-secret"}) == {"client secret": "[REDACTED]"}
    assert redact_mapping({"name": "ok"}, {"---"}) == {"name": "ok"}
