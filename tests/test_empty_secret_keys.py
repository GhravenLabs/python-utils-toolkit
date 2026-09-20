from utils.redaction_utils import redact_mapping

def test_empty_rules_are_not_default_rules():
    data = {"password": "ordinary", "nested": {"password": "ordinary"}}
    assert redact_mapping(data, secret_keys=set()) == data
    assert redact_mapping(data)["password"] == "[REDACTED]"
