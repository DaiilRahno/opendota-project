from fastapi import APIRouter, Path, Query
from requests.exceptions import ConnectionError, HTTPError, Timeout

from backend.errors import handle_error
from backend.matches import get_player_recent_matches
from backend.schemas import MatchResponse

router = APIRouter()


@router.get(
    "/matches/{account_id}",
    response_model=list[MatchResponse],
)
def matches(
    account_id: int = Path(ge=1),
    count: int = Query(7, ge=1, le=50),
):
    try:
        return get_player_recent_matches(account_id, count)
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)
