from api import make_request


def get_winrate(account_id):
    return make_request(
        f'https://api.opendota.com/api/players/{account_id}/wl'
    )


def calculate_winrate(wins, games):
    if games == 0:
        return 0

    return round(wins * 100 / games, 2)


def prepare_winrate(data):
    wins = data['win']
    losses = data['lose']
    games = wins + losses

    winrate = calculate_winrate(wins, games)

    return {
        'wins': wins,
        'losses': losses,
        'games': games,
        'winrate': winrate,
    }


def print_winrate(data):
    result = prepare_winrate(data)

    print(f"Побед: {result['wins']}")
    print(f"Поражений: {result['losses']}")
    print(f"Игр: {result['games']}")
    print(f"Винрейт: {result['winrate']}")
