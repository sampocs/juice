from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from typing import List
from core import database, schemas
import crud


app = FastAPI()

def get_db():
    db = database.SessionLocal()
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