from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.heroes import router as heroes_router
from routers.matches import router as matches_router
from routers.player import router as player_router
from routers.summary import router as summary_router
from routers.winrate import router as winrate_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



app = FastAPI(
    title="Dota Stats API",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return FileResponse("frontend/index.html")


app.include_router(player_router)
app.include_router(winrate_router)
app.include_router(heroes_router)
app.include_router(matches_router)
app.include_router(summary_router)
