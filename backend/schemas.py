from typing import Literal

from pydantic import BaseModel, Field


class WinrateResponse(BaseModel):
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    games: int = Field(ge=0)
    winrate: float = Field(ge=0, le=100)


class PlayerResponse(BaseModel):
    nickname: str = Field(min_length=1)
    steam_id: str = Field(min_length=1)
    competitive_mmr: float | None
    turbo_mmr: float | None
    last_login: str | None


class HeroResponse(BaseModel):
    hero_name: str = Field(min_length=1)
    games: int = Field(ge=0)
    wins: int = Field(ge=0)
    winrate: float = Field(ge=0, le=100)
    image: str


class MatchResponse(BaseModel):
    match_id: int = Field(ge=1)
    result: Literal["Победа", "Поражение"]
    hero_name: str = Field(min_length=1)
    kills: int = Field(ge=0)
    deaths: int = Field(ge=0)
    assists: int = Field(ge=0)
    kda: float = Field(ge=0)


class SummaryResponse(BaseModel):
    player: PlayerResponse
    winrate: WinrateResponse
    heroes: list[HeroResponse]
    recent_matches: list[MatchResponse]
    average_kda: float = Field(ge=0)
    best_match: MatchResponse | None
    worst_match: MatchResponse | None
