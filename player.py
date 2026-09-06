from api import make_request
def get_player(account_id):
    return make_request(
        f'https://api.opendota.com/api/players/{account_id}'
    )


def print_player(data):
    profile = data['profile']

    print(f"Ник: {profile['personaname']}")
    print(f"ММР в Компетив: {data['computed_mmr']}")
    print(f"ММР в Турбо: {data['computed_mmr_turbo']}")
    print(f"Steam ID: {profile['steamid']}")
    print(f"Последний вход: {profile['last_login']}")
