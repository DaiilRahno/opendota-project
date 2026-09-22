from backend.cache import get_cached_summary, set_cached_summary, summary_cache


def test_set_and_get_cached_summary():
    summary_cache.clear()

    data = {
        "player": {
            "nickname": "TestPlayer"
        }
    }

    set_cached_summary(123, 7, data)
    result = get_cached_summary(123, 7)

    assert result == data


def test_cache_uses_account_id_and_count():
    summary_cache.clear()

    data_7 = {"count": 7}
    data_20 = {"count": 20}

    set_cached_summary(123, 7, data_7)
    set_cached_summary(123, 20, data_20)

    assert get_cached_summary(123, 7) == data_7
    assert get_cached_summary(123, 20) == data_20
