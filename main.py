import requests
from player import get_player, print_player
from winrate import get_winrate,print_winrate
from heroes import (
    get_player_heroes,
    print_top_hero_player,
    get_best_and_worst_heroes,
    print_best_and_worst_heroes
)

from matches import (
    get_player_recent_matches,
    print_recent_matches,
    print_best_and_worst_matches
)
from stats import print_recent_stats

account_id = '1008302331'

try:
    count = 5

    player_data = get_player(account_id)
    winrate_data = get_winrate(account_id)
    top_heroes = get_player_heroes(account_id)

    best_and_worst_heroes = get_best_and_worst_heroes(account_id) # кортеж из лдлучшего и худшего героя

    matches = get_player_recent_matches(account_id, count)


    print_player(player_data)

    print_winrate(winrate_data)

    print_top_hero_player(top_heroes)

    if best_and_worst_heroes is None:
        print('Не найдено информации по героям с 20 и более играми.')
        print('Попробуйте сделать другой запрос.')
    else:
        best_hero, worst_hero = best_and_worst_heroes
        print_best_and_worst_heroes(best_hero, worst_hero)


    if matches is None:
        print('Не найдено информации о последних матчах.')
        print('Попробуйте сделать другой запрос.')
    else:
        print_recent_matches(matches)
        print_recent_stats(matches)
        print_best_and_worst_matches(matches)

except requests.exceptions.RequestException:
    print('Не удалось получить данные от OpenDota.')

