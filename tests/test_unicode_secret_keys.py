from utils.redaction_utils import redact_mapping

def test_unicode_custom_keys_survive_separator_normalization():
    assert redact_mapping({"秘密": "private", "public": "ok"}, {"秘密"}) == {"秘密": "[REDACTED]", "public": "ok"}
    assert redact_mapping({"clé secrète": "private"}, {"clé-secrète"}) == {"clé secrète": "[REDACTED]"}
