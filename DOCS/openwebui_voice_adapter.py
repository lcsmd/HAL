import asyncio
import websockets
import base64
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WHISPER_URL = "http://10.1.10.20:8000/transcribe"
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_PROFILE = "EXAVITQu4vr4xnSDxMaL"  # Default voice ID, can vary per persona

async def handle_client(websocket):
    print("Client connected")
    async for message in websocket:
        print("Received audio, sending to Whisper...")
        audio_data = base64.b64decode(message)
        response = requests.post(WHISPER_URL, files={"file": ("audio.wav", audio_data)})
        text = response.json().get("text", "").strip()
        print(f"Transcript: {text}")

        # Route to ElevenLabs
        print("Sending text to ElevenLabs...")
        payload = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        r = requests.post(f"{ELEVENLABS_URL}/{VOICE_PROFILE}/stream", headers=headers, json=payload)
        if r.status_code == 200:
            print("Streaming back audio to client...")
            await websocket.send(r.content)
        else:
            print("TTS error:", r.text)
            await websocket.send(b"")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8766):
        print("Voice adapter listening on ws://0.0.0.0:8766")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
