from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from typing import List, Dict
from core import database, schemas
import crud

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/teams', response_model=List[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    teams = crud.get_teams(db=db)
    return teams

@app.post('/teams', response_model=List[schemas.Team])
def add_teams(teams: List[schemas.Team], db: Session = Depends(get_db)):
    teams = crud.add_teams(db=db, teams=teams)
    return teams

@app.post('/games', response_model=List[schemas.Game])
def add_teams(games: List[schemas.Game], db: Session = Depends(get_db)):
    games = crud.add_games(db=db, games=games)
    return games

@app.get('/games/past/{year}/')
def get_past_games(year: str, db: Session = Depends(get_db)):
    pass

@app.get('/games/upcoming/{year}/')
def get_upcoming_games(year: str, db: Session = Depends(get_db)):
    pass

@app.get('/pbp/{year}')
def get_games_needing_pbp(year: str, db: Session = Depends(get_db)):
    game_ids = crud.get_games_needing_pbp(db=db, year=year)
    return game_ids
