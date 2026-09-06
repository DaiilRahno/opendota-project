from winrate import calculate_winrate

def get_result(data):
    wins = 0
    loses = 0

    for match in data:
        if match['Результат'] == 'Победа':
            wins += 1
        else:
            loses += 1

    return wins, loses


def get_average_kda(data):
    kills = 0
    deaths = 0
    assists = 0

    for match in data:
        kills += match['Убийства']
        deaths += match['Смерти']
        assists += match['Помощи']

    games = len(data)

    return (
        kills / games,
        deaths / games,
        assists / games
    )


def get_recent_stats(data):
    wins, loses = get_result(data)

    games = wins + loses
    winrate = calculate_winrate(wins, games)

    avg_kills, avg_deaths, avg_assists = get_average_kda(data)

    return (
        wins,
        loses,
        winrate,
        avg_kills,
        avg_deaths,
        avg_assists
    )


def print_recent_stats(matches):
    (
        wins,
        loses,
        winrate,
        avg_kills,
        avg_deaths,
        avg_assists
    ) = get_recent_stats(matches)

    print(f'===== ИТОГИ ПОСЛЕДНИХ {len(matches)} МАТЧЕЙ =====')

    print(f'Побед: {wins}')
    print(f'Поражений: {loses}')
    print(f'Процент побед: {winrate} %')
    print()

    print(f'Средние убийства: {avg_kills}')
    print(f'Средние смерти: {avg_deaths}')
    print(f'Средние помощи: {avg_assists}')

