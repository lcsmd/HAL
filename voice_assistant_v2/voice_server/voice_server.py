#!/usr/bin/env python3
"""
Voice Server - STT/TTS and WebSocket Gateway
Runs on Ubuntu GPU server with Faster-Whisper and TTS
Bridges between clients and AI server
"""
import asyncio
import json
import wave
import tempfile
import os
import io
from datetime import datetime
from typing import Dict, Set
import websockets
from websockets.server import WebSocketServerProtocol
from faster_whisper import WhisperModel
import logging

# Configuration
CLIENT_PORT = 8585
AI_SERVER_HOST = "10.1.34.103"
AI_SERVER_PORT = 8745
WHISPER_MODEL = "large-v3"
WHISPER_DEVICE = "cuda"
WHISPER_COMPUTE_TYPE = "float16"
SAMPLE_RATE = 16000

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClientSession:
    """Represents a connected client session"""
    def __init__(self, websocket: WebSocketServerProtocol, client_id: str, 
                 user_id: str, wake_word: str):
        self.websocket = websocket
        self.client_id = client_id
        self.user_id = user_id
        self.wake_word = wake_word
        self.audio_buffer = bytearray()
        self.ai_websocket = None
        self.created_at = datetime.now()
    
    def __str__(self):
        return f"ClientSession(client={self.client_id}, user={self.user_id})"

class VoiceServer:
    def __init__(self):
        self.whisper_model = None
        self.sessions: Dict[str, ClientSession] = {}
        self.ai_connection = None
        logger.info("Voice Server initializing...")
    
    async def initialize(self):
        """Initialize Faster-Whisper model"""
        logger.info(f"Loading Whisper model: {WHISPER_MODEL} on {WHISPER_DEVICE}")
        try:
            self.whisper_model = WhisperModel(
                WHISPER_MODEL,
                device=WHISPER_DEVICE,
                compute_type=WHISPER_COMPUTE_TYPE
            )
            logger.info("✓ Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    async def transcribe_audio(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio using Faster-Whisper
        
        Args:
            audio_bytes: Raw PCM16 audio data at 16kHz
        
        Returns:
            Transcribed text
        """
        try:
            # Save to temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name
                
                with wave.open(tmp_path, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)  # 16-bit
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(audio_bytes)
            
            # Transcribe
            segments, info = self.whisper_model.transcribe(
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
            
            logger.info(f"Transcribed: {text[:100]}...")
            return text.strip()
        
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""
    
    async def text_to_speech(self, text: str, voice_id: str = "default", 
                            volume: float = 1.0) -> bytes:
        """
        Generate speech from text
        
        For now, this is a placeholder. In production, integrate with:
        - Piper TTS
        - Coqui TTS
        - ElevenLabs API
        - Or other TTS service
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier
            volume: Volume level (0.0-1.0)
        
        Returns:
            Audio bytes (WAV format)
        """
        # Placeholder - return empty audio for now
        # TODO: Implement actual TTS
        logger.info(f"TTS requested: {text[:50]}... (voice={voice_id}, volume={volume})")
        
        # Return silence as placeholder
        duration = 2.0  # seconds
        sample_rate = 16000
        samples = int(duration * sample_rate)
        
        # Create WAV file in memory
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b'\x00' * (samples * 2))
        
        return buffer.getvalue()
    
    async def connect_to_ai_server(self) -> websockets.WebSocketClientProtocol:
        """Establish WebSocket connection to AI server"""
        try:
            uri = f"ws://{AI_SERVER_HOST}:{AI_SERVER_PORT}"
            logger.info(f"Connecting to AI server at {uri}")
            websocket = await websockets.connect(uri)
            logger.info("✓ Connected to AI server")
            return websocket
        except Exception as e:
            logger.error(f"Failed to connect to AI server: {e}")
            raise
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a client connection"""
        session = None
        
        try:
            # Wait for session start message
            first_message = await websocket.recv()
            
            # Handle session start
            if isinstance(first_message, str):
                try:
                    data = json.loads(first_message)
                    
                    if data.get('type') == 'session_start':
                        client_id = data.get('client_id')
                        user_id = data.get('user_id')
                        wake_word = data.get('wake_word')
                        
                        session = ClientSession(websocket, client_id, user_id, wake_word)
                        self.sessions[client_id] = session
                        
                        logger.info(f"New session: {session}")
                        
                        # Connect to AI server
                        session.ai_websocket = await self.connect_to_ai_server()
                        
                        # Send session info to AI server
                        await session.ai_websocket.send(json.dumps({
                            'type': 'session_start',
                            'client_id': client_id,
                            'user_id': user_id,
                            'wake_word': wake_word,
                            'timestamp': datetime.now().isoformat()
                        }))
                        
                        # Start listening for responses from AI server
                        asyncio.create_task(self.relay_ai_to_client(session))
                except json.JSONDecodeError:
                    logger.error("Invalid JSON in session start")
                    return
            else:
                logger.error("Expected session_start JSON message")
                return
            
            # Now session is established, receive audio data
            async for message in websocket:
                if isinstance(message, bytes):
                    # Audio chunk
                    session.audio_buffer.extend(message)
                
                elif isinstance(message, str):
                    try:
                        data = json.loads(message)
                        
                        if data.get('type') == 'audio_end':
                            # Client finished speaking - transcribe and send to AI
                            logger.info(f"Audio complete ({len(session.audio_buffer)} bytes)")
                            
                            # Transcribe
                            text = await self.transcribe_audio(bytes(session.audio_buffer))
                            
                            if text:
                                # Send to AI server
                                await session.ai_websocket.send(json.dumps({
                                    'type': 'text_input',
                                    'client_id': session.client_id,
                                    'user_id': session.user_id,
                                    'text': text,
                                    'timestamp': datetime.now().isoformat()
                                }))
                                logger.info(f"Sent to AI server: {text[:100]}...")
                            else:
                                logger.warning("Transcription resulted in empty text")
                            
                            # Clear buffer
                            session.audio_buffer = bytearray()
                    except json.JSONDecodeError:
                        logger.error("Invalid JSON message from client")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {session.client_id if session else 'unknown'}")
        
        except Exception as e:
            logger.error(f"Error handling client: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if session:
                # Close AI connection
                if session.ai_websocket:
                    try:
                        await session.ai_websocket.close()
                    except:
                        pass
                
                # Remove from sessions
                if session.client_id in self.sessions:
                    del self.sessions[session.client_id]
                
                logger.info(f"Session closed: {session.client_id}")
    
    async def relay_ai_to_client(self, session: ClientSession):
        """Relay messages from AI server to client"""
        try:
            async for message in session.ai_websocket:
                if isinstance(message, str):
                    data = json.loads(message)
                    
                    if data.get('type') == 'text_response':
                        # AI server sent text response - convert to speech
                        text = data.get('text', '')
                        voice_id = data.get('voice_id', 'default')
                        volume = data.get('volume', 1.0)
                        
                        logger.info(f"Generating TTS for: {text[:50]}...")
                        
                        # Generate audio
                        audio_bytes = await self.text_to_speech(text, voice_id, volume)
                        
                        # Send audio to client
                        await session.websocket.send(audio_bytes)
                        
                        # Send completion marker
                        await session.websocket.send(json.dumps({
                            'type': 'audio_complete'
                        }))
                        
                        logger.info("Audio sent to client")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"AI server connection closed for {session.client_id}")
        
        except Exception as e:
            logger.error(f"Error relaying AI to client: {e}")
    
    async def run(self):
        """Start the voice server"""
        # Initialize Whisper
        await self.initialize()
        
        # Start WebSocket server for clients
        logger.info(f"Starting WebSocket server on port {CLIENT_PORT}")
        
        async with websockets.serve(self.handle_client, "0.0.0.0", CLIENT_PORT):
            logger.info("✓ Voice server ready")
            logger.info(f"  - Listening for clients on port {CLIENT_PORT}")
            logger.info(f"  - AI server: {AI_SERVER_HOST}:{AI_SERVER_PORT}")
            logger.info(f"  - Whisper model: {WHISPER_MODEL} ({WHISPER_DEVICE})")
            
            # Run forever
            await asyncio.Future()

def main():
    """Main entry point"""
    server = VoiceServer()
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
