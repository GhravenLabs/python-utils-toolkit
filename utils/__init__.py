"""python-utils-toolkit — practical Python utilities.

Import individual modules directly:
    from utils.retry import retry
    from utils.rate_limiter import RateLimiter, AsyncRateLimiter
    from utils.logger import get_logger

Or import this package for the public API surface:
    from utils import retry, RateLimiter, get_logger, Env, timer, Timer
"""

from utils.async_utils import async_retry, gather_safe, run_sequential, with_timeout
from utils.cache_utils import TTLCache, memoize
from utils.crypto_utils import generate_nonce, hmac_sha256, md5, sha256, timestamp_nonce
from utils.datetime_utils import humanize_delta, is_market_hours, now_utc, parse_date, timestamp_ms
from utils.dict_utils import deep_merge, safe_get, flatten_dict
from utils.env import Env
from utils.file_helpers import atomic_write, read_json, read_text, write_json, write_text
from utils.list_utils import batch_by, chunk, deduplicate, first, flatten, last
from utils.logger import get_logger
from utils.number_utils import clamp, format_currency, pct_change, round_to_tick, safe_divide
from utils.rate_limiter import RateLimiter, AsyncRateLimiter
from utils.redaction_utils import mask_email, redact_mapping, redact_text
from utils.retry import retry
from utils.string_utils import camel_to_snake, indent, remove_prefix, remove_suffix, slugify, snake_to_camel, truncate
from utils.timer import timer, Timer
from utils.validation_utils import is_positive_number, is_valid_email, is_valid_symbol, is_within_range, require, require_keys

safe_read = read_text
safe_write = write_text
run_with_timeout = with_timeout
gather_with_errors = gather_safe
hmac_sign = hmac_sha256
sha256_hex = sha256
md5_hex = md5
utc_now = now_utc
parse_ts = parse_date
dedup = deduplicate
format_number = format_currency
round_to = round_to_tick

__all__ = [
    # async
    "with_timeout", "gather_safe", "run_sequential", "async_retry",
    "run_with_timeout", "gather_with_errors",
    # cache
    "TTLCache", "memoize",
    # crypto
    "hmac_sha256", "sha256", "md5", "generate_nonce", "timestamp_nonce",
    "hmac_sign", "sha256_hex", "md5_hex",
    # datetime
    "now_utc", "parse_date", "humanize_delta", "timestamp_ms", "is_market_hours",
    "utc_now", "parse_ts",
    # dict
    "deep_merge", "safe_get", "flatten_dict",
    # env
    "Env",
    # file
    "read_text", "write_text", "read_json", "write_json", "atomic_write",
    "safe_read", "safe_write",
    # list
    "chunk", "flatten", "deduplicate", "first", "last", "batch_by",
    "dedup",
    # logger
    "get_logger",
    # number
    "format_currency", "round_to_tick", "pct_change", "clamp", "safe_divide",
    "format_number", "round_to",
    # rate limiter
    "RateLimiter", "AsyncRateLimiter",
    # redaction
    "mask_email", "redact_mapping", "redact_text",
    # retry
    "retry",
    # string
    "slugify", "truncate", "camel_to_snake", "snake_to_camel",
    "indent", "remove_prefix", "remove_suffix",
    # timer
    "timer", "Timer",
    # validation
    "is_positive_number", "is_valid_symbol", "is_valid_email",
    "require", "require_keys", "is_within_range",
]
