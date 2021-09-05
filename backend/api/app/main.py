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

@app.get('/games/past/{year}/')
def get_past_games(year: str):
    pass

@app.get('/games/upcoming/{year}/')
def get_upcoming_games(year: str):
    pass

@app.get('/pbp/{game_id}')
def get_pbp(game_id: str):
    pass