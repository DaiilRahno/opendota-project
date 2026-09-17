from fastapi import APIRouter, Path
from requests.exceptions import ConnectionError, HTTPError, Timeout

from backend.errors import handle_error
from backend.schemas import WinrateResponse
from backend.winrate import get_winrate, prepare_winrate

router = APIRouter()


@router.get(
    "/winrate/{account_id}",
    response_model=WinrateResponse,
)
def winrate(account_id: int = Path(ge=1)):
    try:
        return prepare_winrate(get_winrate(account_id))
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)
