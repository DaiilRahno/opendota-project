from api import make_request
from heroes import get_hero_name, get_heroes

RANKED_ALL_PICK = 22


def get_recent_matches(account_id):
    return make_request(
        f'https://api.opendota.com/api/players/{account_id}/matches'
    )


def get_last_matches(matches, count):
    return matches[:count]


def get_filter_matches(matches, game_mode=RANKED_ALL_PICK):
    return [
        match
        for match in matches
        if match['game_mode'] == game_mode
    ]


def get_matches_result(match):
    player_slot = match['player_slot']
    radiant_win = match['radiant_win']

    if (
        (player_slot < 128 and radiant_win is True)
        or
        (player_slot >= 128 and radiant_win is False)
    ):
        return 'Победа'

    return 'Поражение'


def calculate_kda(kills, deaths, assists):
    if deaths == 0:
        deaths = 1

    return (kills + assists) / deaths


def prepare_match(match, dota_heroes):
    return {
        'match_id': match['match_id'],
        'result': get_matches_result(match),
        'hero_name': get_hero_name(
            match['hero_id'],
            dota_heroes
        ),
        'kills': match['kills'],
        'deaths': match['deaths'],
        'assists': match['assists'],
        'kda': calculate_kda(
            match['kills'],
            match['deaths'],
            match['assists']
        )
    }


def get_player_recent_matches(account_id, count):
    dota_heroes = get_heroes()
    match_list = get_recent_matches(account_id)

    filtered_matches = get_filter_matches(match_list)
    last_matches = get_last_matches(filtered_matches, count)

    if not last_matches:
        return None

    return [
        prepare_match(match, dota_heroes)
        for match in last_matches
    ]


def print_recent_matches(matches):
    print(f'===== ПОСЛЕДНИЕ {len(matches)} МАТЧЕЙ =====')

    for match in matches:
        print_match(match)


def get_best_and_worst_matches(matches):
    best_match = max(
        matches,
        key=lambda match: match['kda']
    )

    worst_match = min(
        matches,
        key=lambda match: match['kda']
    )

    return best_match, worst_match


def print_match(match):
    kills = match['kills']
    deaths = match['deaths']
    assists = match['assists']
    kda = match['kda']

    print(f"ID игры: {match['match_id']}")
    print(f"Результат: {match['result']}")
    print(f"Герой: {match['hero_name']}")
    print(f'КДА: {kills}/{deaths}/{assists}')
    print(f'КДА Рейтинг: {round(kda, 2)}')
    print()


def print_best_and_worst_matches(matches):
    best_match, worst_match = get_best_and_worst_matches(matches)

    print(f'===== ЛУЧШИЙ ИЗ {len(matches)} МАТЧЕЙ =====')
    print_match(best_match)

    print(f'===== ХУДШИЙ ИЗ {len(matches)} МАТЧЕЙ =====')
    print_match(worst_match)
