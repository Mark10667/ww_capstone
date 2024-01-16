FROM python:3.10-slim-buster

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

WORKDIR /src/app

COPY app.py /src/app/
COPY .streamlit/ /src/app/.streamlit/

CMD streamlit run app.py
