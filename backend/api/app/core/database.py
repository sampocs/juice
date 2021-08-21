from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

JUICE_DB = os.environ['JUICE_DB_NAME']
JUICE_USER = os.environ['JUICE_DB_USER']
JUICE_PASSWORD = os.environ['JUICE_DB_PASSWORD']
SQLALCHEMY_DATABASE_URI = f"postgresql://{JUICE_USER}:{JUICE_PASSWORD}@db:5432/{JUICE_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from core import models

models.Base.metadata.create_all(bind=engine)