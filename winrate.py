from api import make_request

def get_winrate(account_id):
    return make_request(
        f'https://api.opendota.com/api/players/{account_id}/wl'
    )


def calculate_winrate(wins, games):
    if games == 0:
        return 0

    return round(wins * 100 / games, 2)


def print_winrate(data):
    wins = data['win']
    loses = data['lose']
    games = wins + loses

    winrate = calculate_winrate(wins, games)

    print(f'Побед: {wins}')
    print(f'Поражений: {loses}')
    print(f'Винрейт: {winrate}')
