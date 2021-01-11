FROM python:3.7-slim

RUN apt-get update
RUN apt-get -y install gcc

RUN pip install flask  

COPY ./flask/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt


