from sqlalchemy.orm import Session
from api import models

def get_teams(db: Session):
    return db.query(models.Team).all()
