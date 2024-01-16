FROM python:3.10-slim-buster
COPY application_default_credentials.json .
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install -U sentence-transformers
RUN pip install --upgrade google-cloud-storage

COPY main.py .
COPY routers/ ./routers/

CMD uvicorn main:app --host 0.0.0.0 --port 8080

