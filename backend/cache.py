import time


CACHE_TTL_SECONDS = 60

summary_cache = {}


def get_cached_summary(account_id: int, count: int):
    key = (account_id, count)

    cached = summary_cache.get(key)

    if cached is None:
        return None

    expires_at, data = cached

    if time.monotonic() >= expires_at:
        summary_cache.pop(key, None)
        return None

    return data


def set_cached_summary(account_id: int, count: int, data):
    key = (account_id, count)

    expires_at = time.monotonic() + CACHE_TTL_SECONDS

    summary_cache[key] = (expires_at, data)
