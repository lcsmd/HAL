import os, json, asyncio, base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
import websockets as wsclient
import requests
from dotenv import load_dotenv
import pyttsx3

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
OPENQM_ROUTE_WS = os.getenv("OPENQM_ROUTE_WS", "ws://10.1.34.103:8765/route")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "Bryan")

app = FastAPI()

# ---- Stubs: replace with real GPU transcription ----
def transcribe_pcm16(audio_bytes: bytes) -> str:
    # Placeholder: integrate Faster-Whisper GPU here
    # e.g., use faster_whisper. For now, return empty to avoid false content.
    return ""

async def route_to_openqm(session_id: str, text: str, wakeword: str = "HAL"):
    payload = {"session_id": session_id, "text": text, "wakeword": wakeword}
    async with wsclient.connect(OPENQM_ROUTE_WS, max_size=None) as sock:
        await sock.send(json.dumps(payload))
        reply = await sock.recv()
        try:
            return json.loads(reply)
        except Exception:
            return {"session_id": session_id, "text": str(reply), "voice": "Bryan"}

def tts_elevenlabs(text: str) -> bytes:
    if not ELEVENLABS_API_KEY or not text.strip():
        return b""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
    r = requests.post(url, headers=headers, json=data, timeout=30)
    if r.status_code == 200: return r.content
    return b""

def tts_pyttsx3_to_wav_bytes(text: str) -> bytes:
    # Simple offline fallback: synthesize to file, read back
    import tempfile, wave, audioop
    engine = pyttsx3.init()
    fd, path = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    try:
        engine.save_to_file(text, path); engine.runAndWait()
        with open(path, "rb") as f: data = f.read()
        return data
    finally:
        try: os.remove(path)
        except Exception: pass

@app.websocket("/transcribe")
async def transcribe_ws(websocket: WebSocket):
    await websocket.accept()
    session_id = "s-" + str(id(websocket))
    audio_buf = bytearray()
    try:
        while True:
            msg = await websocket.receive()
            if "bytes" in msg and msg["bytes"]:
                # Accumulate PCM16 audio
                audio_buf.extend(msg["bytes"])
                continue
            if "text" in msg and isinstance(msg["text"], str):
                # Ignore text control messages here
                if msg["text"] == "__PING__":
                    await websocket.send_text("__PONG__")
                continue
            # Fallback: no-op
    except WebSocketDisconnect:
        pass
    finally:
        # End of stream implied by disconnect or client sent stop marker before close
        text = transcribe_pcm16(bytes(audio_buf))
        if not text:
            await websocket.close()
            return
        # Route to OpenQM for reply
        reply = await route_to_openqm(session_id, text, "HAL")
        # Synthesize
        audio = tts_elevenlabs(reply.get("text","")) or tts_pyttsx3_to_wav_bytes(reply.get("text",""))
        # We don't stream back over this WS in this minimal skeleton
        # In production, keep a separate WS to push audio to client
        try:
            await websocket.send_bytes(audio[:1024])  # small ack chunk
        except Exception:
            pass
        await websocket.close()

@app.post("/speak")
async def speak_http(req: Request):
    body = await req.json()
    text = body.get("text","")
    voice = body.get("voice","Bryan")
    audio = tts_elevenlabs(text) or tts_pyttsx3_to_wav_bytes(text)
    return JSONResponse({"ok": True, "len": len(audio), "voice": voice})
