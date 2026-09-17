from fastapi import HTTPException
from requests.exceptions import ConnectionError, HTTPError, Timeout


def handle_error(error):
    if isinstance(error, HTTPError):
        if (
            error.response is not None
            and error.response.status_code == 404
        ):
            raise HTTPException(
                status_code=404,
                detail="Игрок не найден",
            )

        raise HTTPException(
            status_code=502,
            detail="Ошибка OpenDota API",
        )

    if isinstance(error, Timeout):
        raise HTTPException(
            status_code=504,
            detail="OpenDota API не ответил вовремя",
        )

    if isinstance(error, ConnectionError):
        raise HTTPException(
            status_code=502,
            detail="Не удалось подключиться к OpenDota API",
        )

    raise HTTPException(
        status_code=500,
        detail="Внутренняя ошибка сервера",
    )
