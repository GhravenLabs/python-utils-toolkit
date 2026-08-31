# 🐍 python-utils-toolkit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Pure Python](https://img.shields.io/badge/dependencies-zero-brightgreen?style=flat-square)](requirements.txt)
[![CI](https://github.com/GhravenLabs/python-utils-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/GhravenLabs/python-utils-toolkit/actions/workflows/ci.yml)
[![Changelog](https://img.shields.io/badge/changelog-view-orange?style=flat-square)](CHANGELOG.md)

A collection of practical, production-ready Python utilities built while working on AI agent systems and automation pipelines. **Pure Python — zero external dependencies.**

## Modules

| Module | Description |
|---|---|
| `utils/retry.py` | `@retry` with exponential backoff + jitter |
| `utils/rate_limiter.py` | Token-bucket rate limiter (sync + async) |
| `utils/timer.py` | `@timer` decorator + `Timer` context manager |
| `utils/file_helpers.py` | Safe read/write, atomic saves, JSON helpers |
| `utils/logger.py` | Structured logging with colour + file rotation |
| `utils/env.py` | Typed `.env` / environment variable loader |
| `utils/string_utils.py` | slugify, truncate, camel_to_snake |
| `utils/datetime_utils.py` | UTC helpers, humanize_delta, business-hour helpers |
| `utils/number_utils.py` | Currency format, tick rounding, pct_change |
| `utils/list_utils.py` | chunk, flatten, deduplicate, batch_by |
| `utils/dict_utils.py` | deep_merge, safe_get, flatten_dict |
| `utils/cache_utils.py` | TTLCache + @memoize for API caching |
| `utils/async_utils.py` | async retry, timeout, gather_safe |
| `utils/crypto_utils.py` | HMAC-SHA256 signing, nonce generation |
| `utils/redaction_utils.py` | Redact emails, phone numbers, tokens, and secret mapping keys before logging or sending text to AI |
| `utils/validation_utils.py` | Guard clauses, identifier/email validation |

## Install

```bash
pip install "git+https://github.com/GhravenLabs/python-utils-toolkit"
```

Or for local development:

```bash
git clone https://github.com/GhravenLabs/python-utils-toolkit
cd python-utils-toolkit
pip install -e ".[dev]"
python examples/retry_demo.py
```

## Examples

### Retry with backoff
```python
from utils.retry import retry

@retry(max_attempts=3, base_delay=1.0, exceptions=(ConnectionError,))
def fetch_resource(resource_id: str) -> dict:
    return api.get(resource_id)
```

### Rate limiter (API calls)
```python
from utils.rate_limiter import RateLimiter

limiter = RateLimiter(calls_per_second=5)
for item in work_queue:
    limiter.acquire()
    result = api.process(item)
```

### Sign an API request (HMAC)
```python
from utils.crypto_utils import hmac_sha256, timestamp_nonce

payload = f"user=alice&action=export&timestamp={timestamp_nonce()}"
signature = hmac_sha256(api_secret, payload)
```

### Cache API responses (avoid rate limits)
```python
from utils.cache_utils import memoize

@memoize(ttl=30)
def get_status(service: str) -> dict:
    return api.fetch_status(service)
```

### Redact sensitive text before logging or AI prompts
```python
from utils.redaction_utils import redact_mapping, redact_text

safe_message = redact_text("Contact rolly@example.com with key sk-demo12345678")
safe_payload = redact_mapping({"api_key": "sk-demo12345678", "note": safe_message})
```

### Async retry for streaming connections
```python
from utils.async_utils import async_retry

@async_retry(max_attempts=3, base_delay=0.5)
async def fetch_events(channel: str) -> dict:
    return await ws.get_events(channel)
```

## Why

Built for multi-agent AI systems and automation pipelines. When you're calling external APIs, running LLM chains, processing live streams, or preparing text for an AI model, you need reliable retry logic, rate limiting, privacy-safe redaction, and clean logging — without heavy frameworks.

## Contributing

Found a bug or want to add a utility? See [CONTRIBUTING.md](CONTRIBUTING.md).
PRs welcome — please include a test for any new module.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

---

## AI Assistance Transparency

I use AI-assisted development tools, including Codex and Claude, while building and maintaining this project. All code, design decisions, testing, commits, and releases are reviewed and shipped by me as the repository owner; AI tools are not listed as project contributors.
## License
MIT — see [LICENSE](LICENSE)
