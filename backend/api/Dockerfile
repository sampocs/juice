FROM python:3.9-slim

WORKDIR /app

COPY ./api/app /app
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]