from sqlalchemy.orm import Session
from core import models

def get_teams(db: Session):
    return db.query(models.Team).all()
