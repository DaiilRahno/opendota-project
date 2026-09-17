from backend.api import make_request


def get_winrate(account_id):
    return make_request(
        f"https://api.opendota.com/api/players/{account_id}/wl"
    )


def calculate_winrate(wins, games):
    if games == 0:
        return 0

    return round(wins / games * 100, 2)


def prepare_winrate(data):
    wins = data["win"]
    losses = data["lose"]
    games = wins + losses

    return {
        "wins": wins,
        "losses": losses,
        "games": games,
        "winrate": calculate_winrate(wins, games),
    }
