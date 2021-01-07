from sqlalchemy.orm import Session
import models

def get_teams(db: Session):
    return db.query(models.Team).all()
