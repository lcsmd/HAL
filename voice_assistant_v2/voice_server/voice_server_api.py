#!/usr/bin/env python3
"""
Voice Server - WebSocket Gateway using existing STT/TTS APIs
Bridges between clients and AI server using existing faster-whisper on port 8001/8002
"""
import asyncio
import json
import httpx
import logging
from datetime import datetime
from typing import Dict
import websockets
from websockets.server import WebSocketServerProtocol

# Configuration
CLIENT_PORT = 8585
AI_SERVER_HOST = "10.1.34.103"
AI_SERVER_PORT = 8745
STT_API_URL = "http://localhost:8001/v1/audio/transcriptions"
TTS_API_URL = "http://localhost:8002/v1/audio/speech"
SAMPLE_RATE = 16000

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class VoiceServer:
    def __init__(self):
        self.clients: Dict[str, WebSocketServerProtocol] = {}
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Send audio to existing faster-whisper API on port 8001"""
        try:
            logger.info(f"Sending {len(audio_data)} bytes to STT API on port 8001...")
            
            # Create WAV file in memory
            import io
            import wave
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio_data)
            
            wav_buffer.seek(0)
            
            # Call existing faster-whisper API
            files = {'file': ('audio.wav', wav_buffer, 'audio/wav')}
            data = {'model': 'whisper-1'}
            
            response = await self.http_client.post(
                STT_API_URL,
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                transcription = result.get('text', '')
                logger.info(f"STT result: {transcription}")
                return transcription
            else:
                logger.error(f"STT API error: {response.status_code} - {response.text}")
                return ""
        
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""
    
    async def synthesize_speech(self, text: str) -> bytes:
        """Send text to existing TTS API on port 8002"""
        try:
            logger.info(f"Sending text to TTS API on port 8002: {text[:50]}...")
            
            payload = {
                'model': 'tts-1',
                'input': text,
                'voice': 'alloy'
            }
            
            response = await self.http_client.post(
                TTS_API_URL,
                json=payload
            )
            
            if response.status_code == 200:
                audio_data = response.content
                logger.info(f"TTS returned {len(audio_data)} bytes")
                return audio_data
            else:
                logger.error(f"TTS API error: {response.status_code}")
                return b''
        
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return b''
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle client WebSocket connection"""
        client_addr = websocket.remote_address
        logger.info(f"Client connected: {client_addr}")
        
        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    # Audio data received
                    logger.info(f"Received audio: {len(message)} bytes")
                    
                    # Transcribe using existing API
                    transcription = await self.transcribe_audio(message)
                    
                    if not transcription:
                        await websocket.send(json.dumps({
                            'type': 'error',
                            'error': 'Transcription failed'
                        }))
                        continue
                    
                    # Send to AI server
                    ai_response = await self.query_ai_server(transcription)
                    
                    # Synthesize response if TTS enabled
                    response_data = {
                        'type': 'text_response',
                        'text': ai_response,
                        'transcription': transcription
                    }
                    
                    # Send text response
                    await websocket.send(json.dumps(response_data))
                
                elif isinstance(message, str):
                    # JSON message
                    data = json.loads(message)
                    msg_type = data.get('type')
                    
                    if msg_type == 'text_query':
                        # Direct text query
                        text = data.get('text', '')
                        ai_response = await self.query_ai_server(text)
                        
                        await websocket.send(json.dumps({
                            'type': 'text_response',
                            'text': ai_response
                        }))
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_addr}")
        except Exception as e:
            logger.error(f"Client handler error: {e}")
    
    async def query_ai_server(self, text: str) -> str:
        """Send query to AI server on port 8745"""
        try:
            logger.info(f"Querying AI server: {text[:50]}...")
            
            # Connect to AI server via WebSocket
            async with websockets.connect(f"ws://{AI_SERVER_HOST}:{AI_SERVER_PORT}") as ws:
                # Send query
                await ws.send(json.dumps({
                    'type': 'query',
                    'text': text,
                    'user_id': 'default',
                    'session_id': 'voice_server'
                }))
                
                # Wait for response
                response = await asyncio.wait_for(ws.recv(), timeout=30.0)
                data = json.loads(response)
                
                ai_text = data.get('text', 'No response from AI server')
                logger.info(f"AI response: {ai_text[:50]}...")
                return ai_text
        
        except Exception as e:
            logger.error(f"AI server error: {e}")
            return f"Error: Unable to reach AI server - {e}"
    
    async def start(self):
        """Start the voice server"""
        logger.info("="*60)
        logger.info("Voice Server Starting")
        logger.info("="*60)
        logger.info(f"Client WebSocket: 0.0.0.0:{CLIENT_PORT}")
        logger.info(f"STT API: {STT_API_URL}")
        logger.info(f"TTS API: {TTS_API_URL}")
        logger.info(f"AI Server: ws://{AI_SERVER_HOST}:{AI_SERVER_PORT}")
        logger.info("="*60)
        
        async with websockets.serve(self.handle_client, "0.0.0.0", CLIENT_PORT):
            logger.info("Voice server ready")
            await asyncio.Future()  # Run forever

def main():
    server = VoiceServer()
    asyncio.run(server.start())

if __name__ == '__main__':
    main()
