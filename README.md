# 🐍 python-utils-toolkit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Pure Python](https://img.shields.io/badge/dependencies-zero-brightgreen?style=flat-square)](requirements.txt)
[![Tests](https://img.shields.io/badge/tests-15%20modules-blue?style=flat-square)](tests/)
[![Changelog](https://img.shields.io/badge/changelog-view-orange?style=flat-square)](CHANGELOG.md)

A collection of practical, production-ready Python utilities built while working on crypto trading bots and AI agent systems. **Pure Python — zero external dependencies.**

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
| `utils/datetime_utils.py` | UTC helpers, humanize_delta, market hours |
| `utils/number_utils.py` | Currency format, tick rounding, pct_change |
| `utils/list_utils.py` | chunk, flatten, deduplicate, batch_by |
| `utils/dict_utils.py` | deep_merge, safe_get, flatten_dict |
| `utils/cache_utils.py` | TTLCache + @memoize for API caching |
| `utils/async_utils.py` | async retry, timeout, gather_safe |
| `utils/crypto_utils.py` | HMAC-SHA256 signing, nonce generation |
| `utils/validation_utils.py` | Guard clauses, symbol/email validation |

## Quick Start

```bash
git clone https://github.com/GhravenLabs/python-utils-toolkit
cd python-utils-toolkit
python examples/retry_demo.py
```

## Examples

### Retry with backoff
```python
from utils.retry import retry

@retry(max_attempts=3, base_delay=1.0, exceptions=(ConnectionError,))
def fetch_price(symbol: str) -> float:
    return api.get_price(symbol)
```

### Rate limiter (Binance API)
```python
from utils.rate_limiter import RateLimiter

limiter = RateLimiter(calls_per_second=5)
for symbol in watchlist:
    limiter.acquire()
    price = fetch_price(symbol)
```

### Sign exchange API request
```python
from utils.crypto_utils import hmac_sha256, timestamp_nonce

params = f"symbol=BTCUSDT&side=BUY&timestamp={timestamp_nonce()}"
signature = hmac_sha256(api_secret, params)
```

### Cache API responses (avoid rate limits)
```python
from utils.cache_utils import memoize

@memoize(ttl=30)
def get_ticker(symbol: str) -> dict:
    return exchange.fetch_ticker(symbol)
```

### Async retry for websocket streams
```python
from utils.async_utils import async_retry

@async_retry(max_attempts=3, base_delay=0.5)
async def fetch_orderbook(symbol: str) -> dict:
    return await ws.get_orderbook(symbol)
```

## Why

Built for a live crypto futures trading bot (BTC/ETH/BNB/SOL on Binance) and multi-agent AI systems. When you're calling exchange APIs, running LLM chains, and processing live streams, you need reliable retry logic, rate limiting, and clean logging — without heavy frameworks.

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
