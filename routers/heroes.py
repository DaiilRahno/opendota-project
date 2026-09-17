from fastapi import APIRouter, Path, Query
from requests.exceptions import ConnectionError, HTTPError, Timeout

from backend.errors import handle_error
from backend.heroes import get_player_heroes
from backend.schemas import HeroResponse

router = APIRouter()


@router.get(
    "/heroes/{account_id}",
    response_model=list[HeroResponse],
)
def heroes(
    account_id: int = Path(ge=1),
    count: int = Query(15, ge=1, le=30),
):
    try:
        return get_player_heroes(account_id, count)
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)
