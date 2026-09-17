from backend.player import get_player,prepare_player
from unittest.mock import patch # для подмены адреса запроса к api

def test_get_player():
    with patch('backend.player.make_request') as mock_request:
        mock_request.return_value = {'hello':'world'} # подменяем значение ответа
        result = get_player(123)
        assert result == {'hello':'world'}

def test_get_player_url():
    with patch("backend.player.make_request") as mock_request:
        get_player(123)

        print(mock_request.call_args)

        mock_request.assert_called_once_with(
            "https://api.opendota.com/api/players/123"
        )

def test_prepare_player_empty_data():
    res = prepare_player({})

    assert res == {
        "nickname": "Unknown",
        "steam_id": "",
        "competitive_mmr": None,
        "turbo_mmr": None,
        "last_login": None
    }

def test_prepare_player_without_profile():
    res = prepare_player({
        "competitive_rank": 2900,
        "mmr_estimate": {
            "estimate": 3000
        }
    })

    assert res == {
        "nickname": "Unknown",
        "steam_id": "",
        "competitive_mmr": 2900,
        "turbo_mmr": 3000,
        "last_login": None
    }