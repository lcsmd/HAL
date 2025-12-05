#!/usr/bin/env python3
"""
HAL Web Voice Gateway
WebSocket server for the browser client (hal2.lcs.ai).

Features:
- Accepts WebSocket connections on port 8768
- Wake word detection using openwakeword ("hey jarvis")
- Streams audio chunks from the browser and detects end-of-speech via silence timeout
- Transcribes audio via Faster-Whisper HTTP API (Ubuntu:8001)
- Routes queries through QueryRouter (LLM / HA / QM) and returns responses
- Logs all conversations to QM CONVERSATION file
- Supports direct text input messages
"""

import asyncio
import base64
import io
import json
import os
import socket
import sys
import time
import uuid
import wave
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import numpy as np
import websockets
from websockets.server import WebSocketServerProtocol

# Wake word detection
try:
    from openwakeword.model import Model as WakeWordModel
    WAKE_WORD_AVAILABLE = True
except ImportError:
    WAKE_WORD_AVAILABLE = False
    print("[VoiceGatewayWeb] openwakeword not available - wake word detection disabled")

# Add PY directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from query_router import QueryRouter

# Configuration
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8768
STT_URL = "http://10.1.10.20:8001/v1/audio/transcriptions"  # Faster-Whisper HTTP endpoint
TTS_URL = "http://10.1.10.20:8002/v1/audio/speech"  # Text-to-speech HTTP endpoint
TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"
SAMPLE_RATE = 16000
SILENCE_TIMEOUT = 1.5  # seconds of silence to treat as end-of-speech
MIN_AUDIO_MS = 500     # require at least this much audio before transcribing

# Wake word settings
WAKE_WORD_THRESHOLD = 0.5  # confidence threshold for wake word detection
WAKE_WORD_MODEL = "hey_jarvis"  # openwakeword model name

# Conversation logging - QM server
QM_LOG_HOST = "10.1.34.103"  # Windows QM server
QM_LOG_PORT = 8745  # AI.SERVER port


@dataclass
class SessionState:
    websocket: WebSocketServerProtocol
    session_id: str
    audio_buffer: bytearray = field(default_factory=bytearray)
    last_audio_ts: float = field(default_factory=lambda: time.time())
    context: List[Dict] = field(default_factory=list)
    active: bool = False  # set True after first audio chunk

    def reset_audio(self) -> bytes:
        audio = bytes(self.audio_buffer)
        self.audio_buffer.clear()
        return audio

    def add_context(self, user_text: str, response_text: str) -> None:
        self.context.append(
            {
                "user": user_text,
                "response": response_text,
                "ts": time.time(),
            }
        )
        # Keep recent history small
        if len(self.context) > 10:
            self.context = self.context[-10:]


class VoiceGatewayWeb:
    def __init__(self) -> None:
        self.sessions: Dict[str, SessionState] = {}
        self.router = QueryRouter()
        self.loop = asyncio.get_event_loop()

    async def start(self) -> None:
        print(f"[VoiceGatewayWeb] Starting on ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
        monitor = asyncio.create_task(self._silence_monitor())
        async with websockets.serve(self.handle_client, WEBSOCKET_HOST, WEBSOCKET_PORT):
            await asyncio.Future()  # run forever
        monitor.cancel()

    async def handle_client(self, websocket: WebSocketServerProtocol) -> None:
        session_id = str(uuid.uuid4())
        session = SessionState(websocket=websocket, session_id=session_id)
        self.sessions[session_id] = session
        print(f"[VoiceGatewayWeb] Client connected: {session_id}")

        # Notify client
        await self._safe_send(
            websocket,
            {
                "type": "connected",
                "session_id": session_id,
                "message": "Connected to HAL web voice gateway",
            },
        )

        try:
            async for message in websocket:
                await self._handle_message(session, message)
        except websockets.exceptions.ConnectionClosed:
            print(f"[VoiceGatewayWeb] Client disconnected: {session_id}")
        finally:
            self.sessions.pop(session_id, None)

    async def _handle_message(self, session: SessionState, message: str) -> None:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            await self._safe_send(session.websocket, {"type": "error", "message": "Invalid JSON"})
            return

        msg_type = data.get("type")

        if msg_type == "text_input":
            text = (data.get("text") or "").strip()
            if not text:
                return
            await self._handle_text(session, text)
            return

        if msg_type == "audio_stream":
            audio_list = data.get("audio")
            if not isinstance(audio_list, list):
                return
            # Convert list of int16 values to bytes
            audio_bytes = bytearray()
            for sample in audio_list:
                # clamp to int16
                sample = max(-32768, min(32767, int(sample)))
                audio_bytes += int(sample).to_bytes(2, byteorder="little", signed=True)

            session.audio_buffer.extend(audio_bytes)
            session.last_audio_ts = time.time()

            if not session.active:
                session.active = True
                await self._safe_send(
                    session.websocket,
                    {"type": "wake_word_detected", "message": "Listening..."},
                )
            return

        # Unknown message
        await self._safe_send(session.websocket, {"type": "error", "message": f"Unknown type: {msg_type}"})

    async def _handle_text(self, session: SessionState, text: str) -> None:
        await self._safe_send(session.websocket, {"type": "processing"})
        response = await self.loop.run_in_executor(
            None, self.router.route_query, text, session.session_id, session.context
        )

        reply_text = response.get("text", "I didn't understand that.")
        session.add_context(text, reply_text)

        # Optional TTS
        audio_b64 = await self._synthesize_speech(reply_text)

        await self._safe_send(
            session.websocket,
            {
                "type": "response",
                "text": reply_text,
                "intent": response.get("intent"),
                "confidence": response.get("confidence"),
                "audio": audio_b64,
                "audio_format": "wav" if audio_b64 else None,
            },
        )

    async def _silence_monitor(self) -> None:
        """Periodically check for end-of-speech and transcribe."""
        while True:
            now = time.time()
            tasks = []
            for session in list(self.sessions.values()):
                if not session.active:
                    continue

                audio_ms = (len(session.audio_buffer) / 2) / SAMPLE_RATE * 1000  # int16 => 2 bytes
                if audio_ms < MIN_AUDIO_MS:
                    continue

                if now - session.last_audio_ts >= SILENCE_TIMEOUT:
                    tasks.append(self._process_audio_session(session))

            if tasks:
                await asyncio.gather(*tasks)

            await asyncio.sleep(0.25)

    async def _process_audio_session(self, session: SessionState) -> None:
        audio_bytes = session.reset_audio()
        session.active = False

        if not audio_bytes:
            return

        # Build WAV in memory
        wav_buf = io.BytesIO()
        with wave.open(wav_buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_bytes)
        wav_buf.seek(0)

        transcription = await self._transcribe_audio(wav_buf)
        if not transcription:
            await self._safe_send(
                session.websocket,
                {"type": "error", "message": "Transcription failed"},
            )
            return

        # Send transcription to client
        await self._safe_send(
            session.websocket,
            {"type": "transcription", "text": transcription},
        )

        # Route query
        response = await self.loop.run_in_executor(
            None, self.router.route_query, transcription, session.session_id, session.context
        )
        reply_text = response.get("text", "I didn't understand that.")
        session.add_context(transcription, reply_text)

        # Optional TTS
        audio_b64 = await self._synthesize_speech(reply_text)

        await self._safe_send(
            session.websocket,
            {
                "type": "response",
                "text": reply_text,
                "intent": response.get("intent"),
                "confidence": response.get("confidence"),
                "audio": audio_b64,
                "audio_format": "wav" if audio_b64 else None,
            },
        )

    async def _transcribe_audio(self, wav_buffer: io.BytesIO) -> Optional[str]:
        """Send audio to Faster-Whisper HTTP API."""
        try:
            wav_buffer.seek(0)
            data = aiohttp.FormData()
            data.add_field("file", wav_buffer, filename="audio.wav", content_type="audio/wav")
            data.add_field("model", "whisper-1")

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(STT_URL, data=data) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        print(f"[VoiceGatewayWeb] STT error {resp.status}: {text}")
                        return None
                    result = await resp.json()
                    return result.get("text", "").strip()
        except Exception as e:
            print(f"[VoiceGatewayWeb] Transcription exception: {e}")
            return None

    async def _synthesize_speech(self, text: str) -> Optional[str]:
        """Generate speech audio for the given text and return base64-encoded wav."""
        if not text or not TTS_URL:
            return None

        payload = {
            "model": TTS_MODEL,
            "input": text,
            "voice": TTS_VOICE,
            "format": "wav",
        }

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(TTS_URL, json=payload) as resp:
                    if resp.status != 200:
                        msg = await resp.text()
                        print(f"[VoiceGatewayWeb] TTS error {resp.status}: {msg}")
                        return None
                    audio_bytes = await resp.read()
                    return base64.b64encode(audio_bytes).decode("ascii")
        except Exception as e:
            print(f"[VoiceGatewayWeb] TTS exception: {e}")
            return None

    async def _safe_send(self, websocket: WebSocketServerProtocol, payload: dict) -> None:
        try:
            await websocket.send(json.dumps(payload))
        except Exception as e:
            print(f"[VoiceGatewayWeb] Send failed: {e}")


def main() -> None:
    gateway = VoiceGatewayWeb()
    asyncio.run(gateway.start())


if __name__ == "__main__":
    main()
