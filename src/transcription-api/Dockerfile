FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y git
RUN apt-get update
RUN apt-get -y install gcc
RUN apt update && apt install ffmpeg -y
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY routers/ ./routers/

CMD uvicorn main:app --host 0.0.0.0 --port 8000

