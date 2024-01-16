from fastapi import FastAPI
from routers.healthcheck import router
from io import BytesIO
import whisper
import base64
import torch
import numpy as np
import pandas as pd 
from pydantic import BaseModel
from pydub import AudioSegment
app = FastAPI()

@app.on_event("startup")
def setup():
   app.include_router(router)

### You shouldn't need to edit the above (except for adding imports, of course)!

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = whisper.load_model("small.en")
model = model.to(torch_device)

class Audio(BaseModel):
    audio: str

@app.get("/hello")
def hello_world():
    return "Hello World"

def transcribe_file(filename):
    w_audio = whisper.load_audio(filename)
    pad_w_audio =whisper.pad_or_trim(w_audio)
    #torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    #model = whisper.load_model("small.en")
    #model = model.to(torch_device)
    mel = whisper.log_mel_spectrogram(pad_w_audio).to(model.device)
    decode_options = dict(language="en")
    transcribe_options = dict(task="transcribe", **decode_options)
    transcription = model.transcribe(filename, **transcribe_options)
    result = transcription["text"]
    return result

@app.post("/transcribe")
def transcribe(audio: Audio):
    decoded_audio = audio.audio.encode('utf-8')
    decoded = base64.b64decode(decoded_audio)
    AudioSegment.from_file(BytesIO(decoded)).export('audio.mp3', format='mp3')
    filename = "audio.mp3"
    return transcribe_file(filename)
