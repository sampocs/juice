from sqlalchemy.orm import Session
from sqlalchemy import insert
from core import models, schemas
from typing import List

def add_games(db: Session, games):
    game_objects = [models.Game(**game.dict()) for game in games]
    db.bulk_save_objects(game_objects)
    db.commit()
    return games

def add_teams(db: Session, teams: List[schemas.Team]):
    team_objects = [models.Team(**team.dict()) for team in teams]
    db.bulk_save_objects(team_objects)
    db.commit()
    return teams

def get_teams(db: Session):
    return db.query(models.Team).all()
