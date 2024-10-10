FROM python:3.11-slim-bullseye as base

RUN apt-get update
RUN apt-get install -y vim

WORKDIR /app

COPY requirements.txt src /app/

RUN pip install -r requirements.txt
