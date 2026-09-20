from utils.redaction_utils import redact_mapping

def test_nested_sequences_redact_without_mutating_input():
    data = {"items": [["sk-exampletoken"], ({"password": "private"},)]}
    assert redact_mapping(data) == {"items": [["[REDACTED]"], ({"password": "[REDACTED]"},)]}
    assert data["items"][0][0] == "sk-exampletoken"
    assert data["items"][1][0]["password"] == "private"
