from fastapi import APIRouter, Path
from requests.exceptions import ConnectionError, HTTPError, Timeout

from backend.errors import handle_error
from backend.player import get_player, prepare_player
from backend.schemas import PlayerResponse

router = APIRouter()


@router.get(
    "/player/{account_id}",
    response_model=PlayerResponse,
)
def player(account_id: int = Path(ge=1)):
    try:
        return prepare_player(get_player(account_id))
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)
