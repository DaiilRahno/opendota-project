from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Path, Query
from requests.exceptions import ConnectionError, HTTPError, Timeout

from backend.cache import get_cached_summary, set_cached_summary
from backend.errors import handle_error
from backend.heroes import get_player_heroes
from backend.matches import get_player_recent_matches
from backend.player import get_player, prepare_player
from backend.schemas import SummaryResponse
from backend.stats import calculate_average_kda, get_best_and_worst_matches
from backend.winrate import get_winrate, prepare_winrate

router = APIRouter()


def load_summary_data(account_id,count):
    with ThreadPoolExecutor(max_workers=4) as executor:  # для управления потоками
        player_future = executor.submit(get_player, account_id) # позволяет функциям работать одновременно
        winrate_future = executor.submit(get_winrate, account_id)
        heroes_future = executor.submit(get_player_heroes, account_id, 15)
        matches_future = executor.submit(
            get_player_recent_matches,
            account_id,
            count,
        )

        return (
            player_future.result(),
            winrate_future.result(),
            heroes_future.result(),
            matches_future.result(),
        )


@router.get(
    "/summary/{account_id}",
    response_model=SummaryResponse,
)
def summary(account_id: int = Path(ge=1), count: int = Query(7, ge=1, le=100)):
    try:
        cached = get_cached_summary(account_id, count)

        if cached is not None:
            return cached

        (
            player_data,
            winrate_data,
            heroes,
            matches,
        ) = load_summary_data(account_id, count)

        best_match, worst_match = get_best_and_worst_matches(matches)

        summary_data = {
            "player": prepare_player(player_data),
            "winrate": prepare_winrate(winrate_data),
            "heroes": heroes,
            "recent_matches": matches,
            "average_kda": calculate_average_kda(matches),
            "best_match": best_match,
            "worst_match": worst_match,
        }

        set_cached_summary(account_id, count, summary_data)

        return summary_data

    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)
