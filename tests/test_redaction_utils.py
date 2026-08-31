from utils.redaction_utils import mask_email, redact_mapping, redact_text


def test_mask_email_keeps_debuggable_shape():
    assert mask_email("rolly@example.com") == "r***y@example.com"
    assert mask_email("a@example.com") == "a***@example.com"


def test_redact_text_masks_common_sensitive_values():
    text = "Email rolly@example.com, call +63 917 123 4567, key sk-testSECRET123"

    redacted = redact_text(text)

    assert "rolly@example.com" not in redacted
    assert "sk-testSECRET123" not in redacted
    assert "+63 917 123 4567" not in redacted
    assert "r***y@example.com" in redacted
    assert "[REDACTED_PHONE]" in redacted


def test_redact_mapping_masks_secret_keys_and_nested_strings():
    data = {
        "api_key": "sk-testSECRET123",
        "message": "Contact ops@example.com",
        "nested": {"authorization": "Bearer abc", "phone": "Call 555-111-2222"},
        "events": ["email raven@example.com", {"token": "ghp_abcdefghijklmnop"}],
    }

    redacted = redact_mapping(data)

    assert redacted["api_key"] == "[REDACTED]"
    assert redacted["nested"]["authorization"] == "[REDACTED]"
    assert redacted["message"] == "Contact o***s@example.com"
    assert redacted["nested"]["phone"] == "Call [REDACTED_PHONE]"
    assert redacted["events"][0] == "email r***n@example.com"
    assert redacted["events"][1]["token"] == "[REDACTED]"
