# voice-tracking
Columbia University Captstone Project to build a POC using open source AI technologies to extract food entities from spoken voice.

Portfolio: https://ym2822.wixsite.com/mark-ma/weightwatchers

![WW_capstone_5](https://github.com/Mark10667/ww_capstone/assets/33364324/3a6c5c80-3080-4c3c-84fe-f4328df41b74)

<img width="556" alt="WW_capstone_4" src="https://github.com/Mark10667/ww_capstone/assets/33364324/491fce17-180d-4431-b57e-208c7332efec">

<img width="815" alt="WW_capstone_5" src="https://github.com/Mark10667/ww_capstone/assets/33364324/143d7d4a-6b46-40d2-807f-b4332f30e9f1">

[Project Description](https://docs.google.com/document/d/1Nm5AamvFH7vn2ll0XGY4M_Dmsus8N9Y-Lvr4SLLHH-s/edit#heading=h.jk8x41wnkhgb)

## Requirements
Docker
Docker compose
python 3.10
python virtual environment or package manager (I use pyenv and pyenv virtualenv to manage my python versions and envs, but you are free to use whatever you are comfortable with)

## Run

Here's how to run each layer of the app with example commands:

Running the application with docker-compose:
```
docker-compose up --build
```
This command will build the images for both the Streamlit app and the FastAPI endpoint, and run them as separate containers. The Streamlit app will be available on http://localhost:8501, and the FastAPI apis will be available on http://localhost:8000/docs and http://localhost:8080/docs.

Running the Streamlit app and FastAPI endpoint separately with docker:
You will need to be in the respective `src/app`, `src/transcription-api`, or`src/nlp-api` folder where the dockerfile is located.

Building the image for the Streamlit app:
```
docker build -f Dockerfile -t app .
```
Running the container for the Streamlit app:
```
docker run -p 8501:8501 app
```
Building the image for the FastAPI transcription endpoint:
```
docker build -f Dockerfile -t transcription-api .
```
Running the container for the FastAPI endpoint:

```
docker run -p 8000:8000 transcription-api
```

Building the image for the FastAPI nlp endpoint:
```
docker build -f Dockerfile -t nlp-api .
```
Running the container for the FastAPI endpoint:

```
docker run -p 8080:8080 nlp-api
```

Running the Streamlit app and FastAPI endpoints separately with virtual environment.
Creating and activating a virtual environment for the Streamlit app:
```
pyenv virtualenv <python-version> <environment-name>
pyenv activate <environment-name>
```


Installing the dependencies for the Streamlit app:
```
pip install -r requirements.txt
```
Running the Streamlit app:
```
streamlit run app.py
```

Installing the dependencies for the FastAPI transcription endpoint:

If you have a different env activated:
```
pyenv deactivate
```
then cd into the api directory and run:

```
pyenv virtualenv <python-version> <environment-name>
pyenv activate <environment-name>
pip install -r requirements.txt
```
Running the FastAPI endpoint:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

You would do the same for the nlp endpoint, creating a new virtualenv but running on port 8080.
