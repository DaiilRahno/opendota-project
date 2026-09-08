from fastapi import FastAPI, HTTPException, Path, Query
from requests.exceptions import ConnectionError, HTTPError, Timeout

from heroes import get_player_heroes
from matches import get_player_recent_matches
from player import get_player, prepare_player
from schemas import HeroResponse, MatchResponse, PlayerResponse, WinrateResponse
from winrate import get_winrate, prepare_winrate

app = FastAPI()


def handle_error(error):
    if isinstance(error, HTTPError):
        if error.response is not None and error.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail='Игрок не найден'
            )

        raise HTTPException(
            status_code=502,
            detail='Ошибка OpenDota API'
        )

    if isinstance(error, Timeout):
        raise HTTPException(
            status_code=504,
            detail='OpenDota API не ответил вовремя'
        )

    if isinstance(error, ConnectionError):
        raise HTTPException(
            status_code=502,
            detail='Не удалось подключиться к OpenDota API'
        )


@app.get('/')  # Когда пользователь отправляет GET-запрос на адрес /, вызывай следующую функцию.
def root():
    return {'message': 'OpenDota API is running'}


@app.get('/player/{account_id}', response_model=PlayerResponse)
def player(account_id: int = Path(ge=1)):
    try:
        data = get_player(account_id)
        return prepare_player(data)
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)


@app.get('/winrate/{account_id}', response_model=WinrateResponse)
def winrate(account_id: int = Path(ge=1)):
    try:
        data = get_winrate(account_id)
        return prepare_winrate(data)
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)


@app.get('/heroes/{account_id}', response_model=list[HeroResponse])
def heroes(account_id: int = Path(ge=1)):
    try:
        return get_player_heroes(account_id)
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)


@app.get('/matches/{account_id}', response_model=list[MatchResponse])
def matches(
    account_id: int = Path(ge=1),
    count: int = Query(5, ge=1, le=50)
):
    try:
        data = get_player_recent_matches(account_id, count)
        if data is not None:
            return data
    except (HTTPError, Timeout, ConnectionError) as error:
        handle_error(error)

    raise HTTPException(
        status_code=404,
        detail='Матчи не найдены'
    )
