"""
UBUAI Voice Server - FastAPI
Handles audio transcription (Faster-Whisper GPU), QM routing, and TTS
"""
import os
import json
import asyncio
import base64
import socket
import tempfile
import wave
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import Response, JSONResponse
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Configuration
OPENQM_HOST = os.getenv("OPENQM_HOST", "10.1.34.103")
OPENQM_PORT = int(os.getenv("OPENQM_PORT", "8767"))
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "nPczCjzI2devNBz1zQrb")  # Bryan
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cuda")  # or "cpu"

app = FastAPI(title="UBUAI Voice Server")

# Global Whisper model (lazy loaded)
whisper_model = None

def get_whisper_model():
    """Lazy load Faster-Whisper model"""
    global whisper_model
    if whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            print(f"Loading Faster-Whisper model: {WHISPER_MODEL} on {WHISPER_DEVICE}")
            whisper_model = WhisperModel(
                WHISPER_MODEL,
                device=WHISPER_DEVICE,
                compute_type="float16" if WHISPER_DEVICE == "cuda" else "int8"
            )
            print("✓ Whisper model loaded")
        except ImportError:
            print("⚠ faster-whisper not available, using fallback")
            whisper_model = "fallback"
        except Exception as e:
            print(f"⚠ Error loading Whisper: {e}")
            whisper_model = "fallback"
    return whisper_model

def transcribe_audio(audio_bytes: bytes, sample_rate: int = 16000) -> str:
    """
    Transcribe audio using Faster-Whisper
    
    Args:
        audio_bytes: Raw PCM16 audio data
        sample_rate: Sample rate (default 16000)
    
    Returns:
        Transcribed text
    """
    model = get_whisper_model()
    
    if model == "fallback":
        # Fallback: return placeholder
        return "[transcription not available]"
    
    try:
        # Save to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            
            # Write WAV header + PCM data
            with wave.open(tmp_path, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(audio_bytes)
        
        # Transcribe
        segments, info = model.transcribe(
            tmp_path,
            language="en",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        # Combine segments
        text = " ".join([segment.text for segment in segments])
        
        # Cleanup
        os.unlink(tmp_path)
        
        return text.strip()
    
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return ""

def route_to_qm_tcp(session_id: str, text: str, timestamp: str = None) -> dict:
    """
    Send text to OpenQM listener via TCP
    
    Args:
        session_id: Session identifier
        text: Transcribed text
        timestamp: Optional timestamp
    
    Returns:
        Response dict from QM
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    payload = {
        "session_id": session_id,
        "text": text,
        "timestamp": timestamp
    }
    
    try:
        # Connect to QM listener
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((OPENQM_HOST, OPENQM_PORT))
        
        # Send JSON + newline
        message = json.dumps(payload) + "\n"
        sock.sendall(message.encode('utf-8'))
        
        # Receive response
        response_data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
            # Check if we have complete JSON (ends with })
            if response_data.strip().endswith(b'}'):
                break
        
        sock.close()
        
        # Parse response
        if response_data:
            response = json.loads(response_data.decode('utf-8'))
            return response
        else:
            return {
                "response_text": "I didn't receive a response.",
                "action_taken": "ERROR",
                "intent": "unknown"
            }
    
    except socket.timeout:
        print(f"❌ QM connection timeout")
        return {
            "response_text": "Sorry, I'm taking too long to think.",
            "action_taken": "TIMEOUT",
            "intent": "unknown"
        }
    except Exception as e:
        print(f"❌ QM connection error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "response_text": "Sorry, I'm having trouble connecting right now.",
            "action_taken": "ERROR",
            "intent": "unknown"
        }

def tts_elevenlabs(text: str, voice_id: str = None) -> Optional[bytes]:
    """
    Generate speech using ElevenLabs API
    
    Args:
        text: Text to synthesize
        voice_id: ElevenLabs voice ID
    
    Returns:
        Audio bytes (MP3) or None
    """
    if not ELEVENLABS_API_KEY or not text.strip():
        return None
    
    if voice_id is None:
        voice_id = ELEVENLABS_VOICE_ID
    
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            return response.content
        else:
            print(f"⚠ ElevenLabs error: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"⚠ ElevenLabs error: {e}")
        return None

def tts_pyttsx3(text: str) -> Optional[bytes]:
    """
    Generate speech using pyttsx3 (offline fallback)
    
    Args:
        text: Text to synthesize
    
    Returns:
        Audio bytes (WAV) or None
    """
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        
        # Configure voice
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 175)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        engine.save_to_file(text, tmp_path)
        engine.runAndWait()
        
        # Read back
        with open(tmp_path, "rb") as f:
            audio_data = f.read()
        
        # Cleanup
        os.unlink(tmp_path)
        
        return audio_data
    
    except Exception as e:
        print(f"⚠ pyttsx3 error: {e}")
        return None

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "UBUAI Voice Server",
        "status": "running",
        "whisper_model": WHISPER_MODEL,
        "whisper_device": WHISPER_DEVICE,
        "qm_host": OPENQM_HOST,
        "qm_port": OPENQM_PORT
    }

@app.websocket("/transcribe")
async def transcribe_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for audio transcription
    
    Protocol:
    1. Client connects
    2. Client sends binary audio chunks (PCM16, 16kHz, mono)
    3. Client sends "__END__" text message to signal end
    4. Server transcribes audio
    5. Server routes to QM
    6. Server generates TTS response
    7. Server sends response audio back
    8. Server closes connection
    """
    await websocket.accept()
    session_id = f"s-{id(websocket)}"
    
    print(f"[{datetime.now()}] Client connected: {session_id}")
    
    audio_buffer = bytearray()
    
    try:
        while True:
            message = await websocket.receive()
            
            if "bytes" in message:
                # Accumulate audio data
                audio_buffer.extend(message["bytes"])
            
            elif "text" in message:
                text_msg = message["text"]
                
                if text_msg == "__END__":
                    # End of audio stream - process it
                    break
                elif text_msg == "__PING__":
                    # Heartbeat
                    await websocket.send_text("__PONG__")
    
    except WebSocketDisconnect:
        print(f"[{datetime.now()}] Client disconnected during upload: {session_id}")
        return
    
    # Process audio
    print(f"[{datetime.now()}] Processing {len(audio_buffer)} bytes of audio")
    
    try:
        # Transcribe
        text = transcribe_audio(bytes(audio_buffer))
        print(f"[{datetime.now()}] Transcribed: {text}")
        
        if not text:
            await websocket.send_text(json.dumps({
                "error": "Transcription failed or empty audio"
            }))
            await websocket.close()
            return
        
        # Route to QM
        qm_response = route_to_qm_tcp(session_id, text)
        response_text = qm_response.get("response_text", "I didn't understand that.")
        
        print(f"[{datetime.now()}] QM response: {response_text[:50]}...")
        
        # Generate TTS
        audio_bytes = tts_elevenlabs(response_text)
        
        if not audio_bytes:
            # Fallback to pyttsx3
            print(f"[{datetime.now()}] Using pyttsx3 fallback")
            audio_bytes = tts_pyttsx3(response_text)
        
        if audio_bytes:
            # Send response audio
            await websocket.send_bytes(audio_bytes)
            print(f"[{datetime.now()}] Sent {len(audio_bytes)} bytes of response audio")
        else:
            # Send text response only
            await websocket.send_text(json.dumps({
                "text": response_text,
                "intent": qm_response.get("intent"),
                "action": qm_response.get("action_taken")
            }))
    
    except Exception as e:
        print(f"❌ Error processing request: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            await websocket.send_text(json.dumps({
                "error": str(e)
            }))
        except:
            pass
    
    finally:
        await websocket.close()
        print(f"[{datetime.now()}] Session closed: {session_id}")

@app.post("/speak")
async def speak_endpoint(request: Request):
    """
    HTTP endpoint for text-to-speech
    
    Request body:
    {
        "text": "Text to synthesize",
        "voice": "Bryan" (optional)
    }
    
    Returns:
        Audio file (MP3 or WAV)
    """
    body = await request.json()
    text = body.get("text", "")
    voice = body.get("voice", ELEVENLABS_VOICE_ID)
    
    if not text:
        return JSONResponse({"error": "No text provided"}, status_code=400)
    
    # Generate audio
    audio_bytes = tts_elevenlabs(text, voice)
    
    if not audio_bytes:
        # Fallback
        audio_bytes = tts_pyttsx3(text)
    
    if audio_bytes:
        # Detect format
        if audio_bytes.startswith(b'RIFF'):
            media_type = "audio/wav"
        else:
            media_type = "audio/mpeg"
        
        return Response(content=audio_bytes, media_type=media_type)
    else:
        return JSONResponse({"error": "TTS failed"}, status_code=500)

@app.post("/transcribe_http")
async def transcribe_http(request: Request):
    """
    HTTP endpoint for transcription (for testing)
    
    Request body:
    {
        "audio": "base64-encoded PCM16 audio"
    }
    
    Returns:
    {
        "text": "transcribed text"
    }
    """
    body = await request.json()
    audio_b64 = body.get("audio", "")
    
    if not audio_b64:
        return JSONResponse({"error": "No audio provided"}, status_code=400)
    
    try:
        audio_bytes = base64.b64decode(audio_b64)
        text = transcribe_audio(audio_bytes)
        
        return JSONResponse({"text": text})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("UBUAI_HOST", "0.0.0.0")
    port = int(os.getenv("UBUAI_PORT", "8001"))
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║           UBUAI Voice Server Starting                     ║
╠═══════════════════════════════════════════════════════════╣
║  Whisper Model: {WHISPER_MODEL:20s}                    ║
║  Whisper Device: {WHISPER_DEVICE:19s}                    ║
║  OpenQM Host: {OPENQM_HOST:22s}                    ║
║  OpenQM Port: {OPENQM_PORT:22d}                    ║
║  ElevenLabs: {'Enabled' if ELEVENLABS_API_KEY else 'Disabled':25s}                    ║
║  Listening: {host}:{port:5d}                              ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host=host, port=port, log_level="info")
