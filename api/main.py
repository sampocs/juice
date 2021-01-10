from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from api import crud, schemas
from database import models
from database.main import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def home():
    response = RedirectResponse(url='/redoc')
    return response

@app.get('/teams', response_model=List[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    teams = crud.get_teams(db=db)
    return teams