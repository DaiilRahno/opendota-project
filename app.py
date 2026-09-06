from fastapi import FastAPI
from player import get_player
from winrate import get_winrate
from heroes import get_player_heroes
from matches import get_player_recent_matches
app = FastAPI()


@app.get("/") # Когда пользователь отправляет GET-запрос на адрес /, вызывай следующую функцию.
def root():
    return {"message": "OpenDota API is running"}

@app.get('/player/{account_id}')
def player(account_id:str):
    return get_player(account_id)

@app.get('/winrate/{account_id}')
def winrate(account_id:str):
    return get_winrate(account_id)

@app.get('/heroes/{account_id}')
def heroes(account_id:str):
    return get_player_heroes(account_id)

@app.get('/matches/{account_id}')
def matches(account_id:str,count:int = 5):
    data = get_player_recent_matches(account_id,count)
    if data is not None:
        return data
    return {'message':'Матчи не найдены'}
