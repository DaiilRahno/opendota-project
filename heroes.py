from api import make_request
from winrate import calculate_winrate


def get_heroes():
    return make_request(
        'https://api.opendota.com/api/heroes'
    )


def get_player_heroes_data(account_id):
    return make_request(
        f'https://api.opendota.com/api/players/{account_id}/heroes'
    )


def get_hero_name(hero_id, dota_heroes):
    for hero in dota_heroes:
        if hero['id'] == hero_id:
            return hero['localized_name']


def filter_hero(list_heroes_player):
    return [
        hero
        for hero in list_heroes_player
        if hero['games'] >= 20
    ]


def prepare_hero_data(hero, dota_heroes):
    return {
        'hero_name': get_hero_name(
            hero['hero_id'],
            dota_heroes
        ),
        'games': hero['games'],
        'wins': hero['win'],
        'winrate': calculate_winrate(
            hero['win'],
            hero['games']
        )
    }


def get_player_heroes(account_id):
    dota_heroes = get_heroes()
    player_heroes = get_player_heroes_data(account_id)

    top_heroes = player_heroes[:3]

    return [
        prepare_hero_data(hero, dota_heroes)
        for hero in top_heroes
    ]


def print_hero(hero):
    print(f"Герой: {hero['hero_name']}")
    print(f"Кол-во игр: {hero['games']}")
    print(f"Кол-во побед: {hero['wins']}")
    print(f"Процент побед: {hero['winrate']}")
    print()


def print_top_hero_player(top_hero):
    print('===== ТОП-3 ГЕРОЕВ =====')

    for index, hero in enumerate(top_hero, start=1):
        print(f'{index}.', end=' ')
        print_hero(hero)


def get_best_and_worst_heroes(account_id):
    player_heroes = get_player_heroes_data(account_id)
    heroes_over_20 = filter_hero(player_heroes)
    dota_heroes = get_heroes()

    prepared_heroes = [
        prepare_hero_data(hero, dota_heroes)
        for hero in heroes_over_20
    ]

    if not prepared_heroes:
        return None

    best_hero = max(
        prepared_heroes,
        key=lambda hero: hero['winrate']
    )

    worst_hero = min(
        prepared_heroes,
        key=lambda hero: hero['winrate']
    )

    return best_hero, worst_hero


def print_best_and_worst_heroes(best_hero, worst_hero):
    print('Лучший герой:')
    print_hero(best_hero)

    print('Худший герой:')
    print_hero(worst_hero)
