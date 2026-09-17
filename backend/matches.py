from backend.api import make_request
from backend.heroes import get_heroes
from backend.stats import calculate_kda


RANKED_ALL_PICK = 22


def get_player_matches_data(account_id,limit = 50):
    return make_request(
        f"https://api.opendota.com/api/players/{account_id}/matches",
        params={"limit": limit},
    )


def prepare_match(match, dota_heroes):
    hero_name = "Unknown"

    for hero in dota_heroes:
        if hero["id"] == match["hero_id"]:
            hero_name = hero["localized_name"]
            break

    kills = match.get("kills", 0)
    deaths = match.get("deaths", 0)
    assists = match.get("assists", 0)

    result = (
        "Победа"
        if match.get("player_slot", 0) < 128 and match.get("radiant_win")
        or match.get("player_slot", 0) >= 128 and not match.get("radiant_win")
        else "Поражение"
    )

    return {
        "match_id": match["match_id"],
        "result": result,
        "hero_name": hero_name,
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "kda": calculate_kda(
            kills,
            deaths,
            assists,
        ),
    }


def get_player_recent_matches(account_id, count=7):
    dota_heroes = get_heroes()
    player_matches = get_player_matches_data(account_id,min(count*2,100))

    ranked_matches = [
        match
        for match in player_matches
        if match.get("game_mode") == RANKED_ALL_PICK
    ]

    selected_matches = ranked_matches[:count] # если матчей меньше count, срез не вернет ошшибку

    return [
        prepare_match(match, dota_heroes)
        for match in selected_matches
    ]
