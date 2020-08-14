FROM python:3.8-alpine

WORKDIR /app
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev python3-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt