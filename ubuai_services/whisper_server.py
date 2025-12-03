#!/usr/bin/env python3
"""
Faster-Whisper STT Server
Runs on port 9000, provides HTTP endpoint for speech-to-text
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from faster_whisper import WhisperModel
import base64
import numpy as np
import io
import wave
import uvicorn
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Faster-Whisper STT Service")

# Global model (loaded on startup)
model = None
MODEL_NAME = "large-v3"
DEVICE = "cuda"  # or "cpu" if no GPU
COMPUTE_TYPE = "float16"  # or "int8" for CPU

class TranscriptionRequest(BaseModel):
    audio: str  # Base64 encoded audio
    language: str = "en"
    task: str = "transcribe"  # or "translate"

@app.on_event("startup")
async def load_model():
    """Load Whisper model on startup"""
    global model
    logger.info(f"Loading Whisper model: {MODEL_NAME} on {DEVICE}")
    try:
        model = WhisperModel(
            MODEL_NAME,
            device=DEVICE,
            compute_type=COMPUTE_TYPE,
            download_root="/opt/faster-whisper/models"
        )
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "running",
        "model": MODEL_NAME,
        "device": DEVICE,
        "service": "Faster-Whisper STT"
    }

@app.get("/health")
async def health():
    """Health check alias"""
    return await health_check()

@app.post("/transcribe")
async def transcribe(request: TranscriptionRequest):
    """Transcribe audio to text"""
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Decode base64 audio
        audio_bytes = base64.b64decode(request.audio)
        
        # Convert to numpy array (assuming PCM16 format)
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        logger.info(f"Transcribing audio ({len(audio_array)} samples)")
        
        # Transcribe
        segments, info = model.transcribe(
            audio_array,
            language=request.language if request.language != "auto" else None,
            task=request.task,
            vad_filter=True,
            vad_parameters={
                "threshold": 0.5,
                "min_silence_duration_ms": 500
            }
        )
        
        # Collect all text
        text = " ".join([segment.text for segment in segments]).strip()
        
        logger.info(f"Transcription: {text[:100]}...")
        
        return {
            "text": text,
            "language": info.language,
            "language_probability": info.language_probability,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000,
        log_level="info"
    )
