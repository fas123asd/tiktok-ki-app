### Projekt: TikTok KI Video Creator
# Backend (FastAPI) + ElevenLabs Voiceover + Render-kompatibel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import requests
import os
from moviepy.editor import *

app = FastAPI()

# CORS für Frontend-Zugriff erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENV-Vars ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# --- MODELL ---
class VideoRequest(BaseModel):
    thema: str

# --- GPT VIDEO-IDEE UND SKRIPT ---
@app.post("/generate")
def generate_script(req: VideoRequest):
    prompt = f"""
    Erstelle ein virales deutsches TikTok-Skript zum Thema: {req.thema}.
    Es soll eine Hook, eine kurze Story und einen Call-to-Action enthalten. Sprache: modern, TikTok-Stil.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    text = response["choices"][0]["message"]["content"]
    return {"skript": text}

# --- ELEVENLABS VOICEOVER ---
def text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/fK1ZRo0Yzl7nB1mCZoXz"  # Stimme: Chris
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75
        }
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Fehler bei ElevenLabs")
    with open("voice.mp3", "wb") as f:
        f.write(r.content)
    return "voice.mp3"

# --- VIDEO ERSTELLUNG ---
@app.post("/create-video")
def create_video(req: VideoRequest):
    skript_data = generate_script(req)
    text = skript_data["skript"]
    audio_file = text_to_speech(text)

    # Dummy Clip mit schwarzem Hintergrund + Musik + Voice
    clip = ColorClip(size=(720,1280), color=(0,0,0), duration=15)
    audioclip = AudioFileClip(audio_file)
    clip = clip.set_audio(audioclip)

    # Speichern
    final_path = "static/output.mp4"
    clip.write_videofile(final_path, fps=24)
    return {"message": "Video erstellt", "file": final_path, "text": text}

# --- Einfaches Ping für Render ---
@app.get("/")
def root():
    return {"message": "TikTok KI Video Generator ist bereit"}