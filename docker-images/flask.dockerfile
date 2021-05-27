FROM python:3.7-slim

COPY ./flask/requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update \
    && apt-get -y install gcc \
    && pip install -r requirements.txt \ 
    && rm -rf /var/lib/apt/lists/*
