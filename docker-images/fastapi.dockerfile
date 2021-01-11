FROM python:3.7-slim

RUN pip install psycopg2-binary fastapi uvicorn[standard] sqlalchemy 
