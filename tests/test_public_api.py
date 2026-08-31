"""Tests for the package-level public API."""


def test_package_root_imports_public_helpers():
    import utils

    assert utils.retry
    assert utils.RateLimiter
    assert utils.with_timeout
    assert utils.gather_safe
    assert utils.safe_read is utils.read_text
    assert utils.safe_write is utils.write_text
    assert utils.hmac_sign is utils.hmac_sha256
    assert utils.redact_text
    assert utils.redact_mapping
    assert utils.sha256_hex is utils.sha256
    assert utils.utc_now is utils.now_utc
    assert utils.dedup is utils.deduplicate
