from api import make_request


def get_player(account_id):
    return make_request(
        f'https://api.opendota.com/api/players/{account_id}'
    )


def prepare_player(data):
    profile = data['profile']

    competitive_mmr = data.get('computed_mmr')
    turbo_mmr = data.get('computed_mmr_turbo')

    return {
        'nickname': profile['personaname'],
        'competitive_mmr': (
            round(competitive_mmr, 2)
            if competitive_mmr is not None
            else None
        ),
        'turbo_mmr': (
            round(turbo_mmr, 2)
            if turbo_mmr is not None
            else None
        ),
        'steam_id': profile['steamid'],
        'last_login': profile.get('last_login'),
    }


def print_player(data):
    player = prepare_player(data)

    print(f"Ник: {player['nickname']}")
    print(f"ММР в Компетив: {player['competitive_mmr']}")
    print(f"ММР в Турбо: {player['turbo_mmr']}")
    print(f"Steam ID: {player['steam_id']}")
    print(f"Последний вход: {player['last_login']}")
