from fastapi.testclient import TestClient
from backend.app import app
from unittest.mock import Mock, patch
from requests.exceptions import HTTPError,Timeout,ConnectionError


client = TestClient(app)

def test_player_invalid_account_id():
    response = client.get('/player/0')
    assert response.status_code == 422

def test_player_vald():
    with(
        patch('routers.player.get_player') as mock_get_player
    ):
        mock_get_player.return_value = {
    "profile": {
        "personaname": "TestPlayer",
        "account_id": 123,
        "last_login": None
    },
    "competitive_rank": 3000,
    "mmr_estimate": {
        "estimate": 3200
    }
}
        response = client.get('/player/123')
        assert response.status_code == 200
        print(response.json())
        assert response.json()['nickname'] == 'TestPlayer'
        mock_get_player.assert_called_once_with(123)
        assert response.json() == {
        "nickname": "TestPlayer",
        "steam_id": "123",
        "competitive_mmr": 3000,
        "turbo_mmr": 3200,
        "last_login": None 
        }

def test_player_not_found():
    with (
        patch('routers.player.get_player') as mock_get_player
           
    ):
        response_mock = Mock()
        response_mock.status_code = 404
        error = HTTPError(response = response_mock)
        mock_get_player.side_effect = error
        response = client.get('/player/123')
        assert response.status_code == 404

def test_player_timeout():
    with(
        patch('routers.player.get_player') as mock_get_player
    ):
        mock_get_player.side_effect = Timeout()
        response = client.get('/player/123')
        assert response.status_code == 504

def test_player_connection_error():
    with(
        patch('routers.player.get_player') as mock_get_player
    ):
        mock_get_player.side_effect = ConnectionError()
        response = client.get('/player/123')
        assert response.status_code == 502

def test_summary_invalid_count():
    response = client.get('/summary/123?count=0')
    assert response.status_code == 422

def test_summary_success():
    with patch("routers.summary.load_summary_data") as mock_load_summary:
        mock_load_summary.return_value = ( 
            {
                "profile": {
                    "personaname": "TestPlayer",
                    "account_id": 123,
                    "last_login": None
                },
                "competitive_rank": 3000,
                "mmr_estimate": {
                    "estimate": 3200
                }
            },
            {
                "win": 6,
                "lose": 4
            },
            [
                {
                    "hero_name": "Anti-Mage",
                    "games": 30,
                    "wins": 20,
                    "winrate": 66.67,
                    "image": "/apps/dota2/images/dota_react/heroes/antimage.png"
                }
            ],
            [
                {
                    "match_id": 1,
                    "result": "Победа",
                    "hero_name": "Anti-Mage",
                    "kills": 10,
                    "deaths": 2,
                    "assists": 6,
                    "kda": 8.0
                }
            ]
        )

        response = client.get("/summary/123?count=1")

        assert response.status_code == 200
        data = response.json()
        assert data['player']['nickname'] == 'TestPlayer'
        assert len(data['recent_matches'])== 1
        assert data['average_kda'] == 8.0
        mock_load_summary.assert_called_once_with(123, 1)