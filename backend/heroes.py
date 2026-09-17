from functools import lru_cache

from backend.api import make_request
from backend.winrate import calculate_winrate


@lru_cache(maxsize=1)
def get_heroes():
    return make_request(
        "https://api.opendota.com/api/heroes"
    )


@lru_cache(maxsize=1)
def get_hero_stats():
    return make_request(
        "https://api.opendota.com/api/heroStats"
    )


def get_player_heroes_data(account_id):
    return make_request(
        f"https://api.opendota.com/api/players/{account_id}/heroes"
    )


def get_hero_name(hero_id, dota_heroes):
    for hero in dota_heroes:
        if hero["id"] == hero_id:
            return hero["localized_name"]

    return "Unknown"


def get_hero_image(hero_id, hero_stats):
    for hero in hero_stats:
        if hero["id"] == hero_id:
            image = hero.get("img")

            if image:
                return (
                    "https://cdn.cloudflare.steamstatic.com"
                    + image
                )

    return ""


def filter_hero(list_heroes_player):
    return [
        hero
        for hero in list_heroes_player
        if hero["games"] >= 20
    ]


def prepare_hero_data(hero, dota_heroes, hero_stats):
    return {
        "hero_name": get_hero_name(
            hero["hero_id"],
            dota_heroes,
        ),
        "games": hero["games"],
        "wins": hero["win"],
        "winrate": calculate_winrate(
            hero["win"],
            hero["games"],
        ),
        "image": get_hero_image(
            hero["hero_id"],
            hero_stats,
        ),
    }


def get_player_heroes(account_id, limit=15):
    dota_heroes = get_heroes()
    hero_stats = get_hero_stats()
    player_heroes = get_player_heroes_data(account_id)

    heroes_over_20 = filter_hero(player_heroes)

    return [
        prepare_hero_data(
            hero,
            dota_heroes,
            hero_stats,
        )
        for hero in heroes_over_20[:limit]
    ]
