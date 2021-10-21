from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy.sql.functions import mode
from core import models, schemas
from typing import List
from datetime import datetime, timedelta
from pytz import timezone


def add_teams(db: Session, teams: List[schemas.Team]) -> List[models.Team]:
    team_objects = [models.Team(**team.dict()) for team in teams]
    db.bulk_save_objects(team_objects)
    db.commit()
    return teams

def get_teams(db: Session) -> List[models.Team]:
    return db.query(models.Team).all()

def add_games(db: Session, games: List[schemas.Game]) -> List[schemas.Team]:

    def _create_game_record(game: schemas.Game) -> str:
        game_datetime = datetime.strptime(game.datetime, '%Y-%m-%d %H:%M:%S')
        game_date = game_datetime.strftime('%Y%m%d')

        home_team = (
            db.query(models.Team)
            .filter(models.Team.team_id == game.home_team_id)
            .first()
        )
        assert home_team, f'Team {game.home_team_id} not in Teams table'

        prf_game_id = f'{game_date}0{home_team.pfr_id}'

        return models.Game(**game.dict(), prf_game_id=prf_game_id)

    game_objects = [_create_game_record(game) for game in games]

    db.bulk_save_objects(game_objects)
    db.commit()
    
    return games

def get_games(db: Session, year: str) -> List[models.Game]:
    return db.query(models.Game).filter(models.Game.season == int(year)).all()

def get_games_needing_pbp(db: Session, year: str) -> List[str]:

    def _check_game_ended(game: models.Game) -> bool:
        utc = timezone('UTC')
        est = timezone('EST')
        current_time = datetime.now(utc).astimezone()
        game_time = est.localize(game.datetime).astimezone(utc)
        if (current_time - game_time > timedelta(hours=4)):
            return True
        return False

    games = (
        db.query(models.Game)
        .filter(models.Game.season == int(year))
        .filter(models.Game.has_pbp == False)
        .all()
    )

    game_ids = [game.prf_game_id for game in games if _check_game_ended(game)]

    return game_ids
    

