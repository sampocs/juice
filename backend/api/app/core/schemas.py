from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Team(BaseModel):
    team_id: str
    org_id: str
    city: str
    mascot: str
    start_year: int
    active: bool
    pfr_id: str

    class Config:
        orm_mode = True


class Game(BaseModel):
    game_id: str
    season: int
    week: int
    datetime: str
    home_team_id: str
    away_team_id: str
    home_score: Optional[int]
    away_score: Optional[int]
    has_pbp: bool = False

    class Config:
        orm_mode = True