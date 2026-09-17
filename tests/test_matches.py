from backend.matches import prepare_match,get_player_recent_matches
from unittest.mock import patch

def test_prepare_match_win_radiant():
    res = prepare_match(
        match={
        "match_id": 123,
        'hero_id':1,
        "kills": 10,
        "deaths": 2,
        "assists": 6,
        'player_slot':50,
        'radiant_win':True
        },
        dota_heroes = [{
            'id':1,
            'localized_name':'Anti-Mage'
        }])
    assert res == {
        "match_id": 123,
        "result": 'Победа',
        "hero_name": 'Anti-Mage',
        "kills": 10,
        "deaths": 2,
        "assists": 6,
        "kda": 8.0
    }

def test_prepare_match_win_dire():
    res = prepare_match(
        match={
        "match_id": 123,
        'hero_id':1,
        "kills": 10,
        "deaths": 2,
        "assists": 6,
        'player_slot':130,
        'radiant_win':False
        },
        dota_heroes = [{
            'id':1,
            'localized_name':'Anti-Mage'
        }])
    assert res == {
        "match_id": 123,
        "result": 'Победа',
        "hero_name": 'Anti-Mage',
        "kills": 10,
        "deaths": 2,
        "assists": 6,
        "kda": 8.0
    }

def test_prepare_match_unknown_id():
    res = prepare_match(
        match={
        "match_id": 123,
        'hero_id':9999999999,
        "kills": 10,
        "deaths": 2,
        "assists": 6,
        'player_slot':130,
        'radiant_win':False
        },
        dota_heroes = [{
            'id':1,
            'localized_name':'Anti-Mage'
        }])
    assert res == {
        "match_id": 123,
        "result": 'Победа',
        "hero_name": 'Unknown',
        "kills": 10,
        "deaths": 2,
        "assists": 6,
        "kda": 8.0
    }

def test_get_player_recent_matches():
    with (
        patch('backend.matches.get_heroes') as mock_heroes,
        patch('backend.matches.get_player_matches_data') as mock_matches
    ):
        mock_heroes.return_value= [
            {
                'id':1,
                'localized_name':'Anti-Mage'
            }
        ]
        mock_matches.return_value = [
            {
                "match_id": 1,
                'hero_id':1,
                'game_mode':22,
                "kills": 5,
                "deaths": 2,
                "assists": 3,
                'player_slot':50,
                'radiant_win':True
            },
            {
                "match_id": 2,
                'hero_id':1,
                'game_mode':1,
                "kills": 5,
                "deaths": 2,
                "assists": 3,
                'player_slot':50,
                'radiant_win':False
            },
            {
                "match_id": 3,
                'hero_id':1,
                'game_mode':22,
                "kills": 5,
                "deaths": 2,
                "assists": 3,
                'player_slot':130,
                'radiant_win':False
            },
        ]
        res = get_player_recent_matches(123,count=1) 
        assert len(res) == 1
        assert res[0]['match_id'] == 1
        assert res[0]['hero_name'] == 'Anti-Mage'
        mock_matches.assert_called_once_with(123,2)
        print(mock_matches.call_args)
        mock_heroes.assert_called_once_with()
    