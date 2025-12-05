"""
HAL Voice Gateway - Web Client Support
WebSocket server with server-side wake word detection
Handles audio streaming from web browsers
"""

import asyncio
import websockets
import json
import base64
import uuid
import requests
import socket
import numpy as np
import io
from datetime import datetime
from typing import Dict, Set
from enum import Enum
import sys
import os

# Add PY directory to path
PY_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PY_DIR)
sys.path.insert(0, os.path.dirname(PY_DIR))  # Add parent directory too

# Try to import wake word detection (optional)
WAKE_WORD_AVAILABLE = False
try:
    from openwakeword.model import Model as OWWModel
    import webrtcvad
    WAKE_WORD_AVAILABLE = True
    print("[OK] Wake word detection available")
except ImportError as e:
    print(f"[WARN] Wake word detection not available: {e}")

# Import query router
try:
    from query_router import get_router
    print("[OK] Query router imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import query_router: {e}")
    print(f"[ERROR] Current sys.path: {sys.path}")
    print(f"[ERROR] PY_DIR: {PY_DIR}")
    raise

# Configuration
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8768
WHISPER_URL = "http://10.1.10.20:8001/v1/audio/transcriptions"
TTS_URL = "http://10.1.10.20:8002/v1/audio/speech"  # TTS endpoint
QM_LISTENER_HOST = "10.1.34.103"  # mv1 Windows server
QM_LISTENER_PORT = 8745
MAX_CONNECTIONS = 50

# Conversation logging
ENABLE_CONVERSATION_LOG = True

class ClientState(Enum):
    PASSIVE = "passive_listening"  # Listening for wake word
    ACTIVE = "active_listening"     # Recording command
    PROCESSING = "processing"       # Processing request
    RESPONDING = "responding"       # Sending response

class VoiceSession:
    def __init__(self, session_id: str, websocket):
        self.session_id = session_id
        self.websocket = websocket
        self.state = ClientState.PASSIVE
        self.audio_buffer = []
        self.recording_buffer = []
        self.context = []
        self.last_activity = datetime.now()
        self.silence_chunks = 0
        
        # Wake word detection
        if WAKE_WORD_AVAILABLE:
            self.oww_model = OWWModel()  # Loads all pre-trained models by default
            self.wake_word_name = 'hey_jarvis'  # Use hey_jarvis model
            self.vad = webrtcvad.Vad(2)
        else:
            self.oww_model = None
            self.vad = None
        
    def update_activity(self):
        self.last_activity = datetime.now()

class VoiceGateway:
    def __init__(self):
        self.sessions: Dict[str, VoiceSession] = {}
        self.router = get_router()
    
    def log_conversation(self, session_id: str, user_text: str, response_text: str, 
                         intent: str = "", latency_ms: int = 0):
        """Log conversation to QM CONVERSATION file via AI.SERVER"""
        if not ENABLE_CONVERSATION_LOG:
            return
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect((QM_LISTENER_HOST, QM_LISTENER_PORT))
            
            log_msg = {
                "type": "log_conversation",
                "session_id": session_id,
                "user_text": user_text,
                "response_text": response_text,
                "intent": intent,
                "latency_ms": latency_ms,
                "timestamp": datetime.now().isoformat()
            }
            s.sendall(json.dumps(log_msg).encode() + b'\n')
            s.close()
            print(f"[LOG] Conversation logged for session {session_id[:8]}")
        except Exception as e:
            print(f"[WARN] Failed to log conversation: {e}")
    
    async def synthesize_speech(self, text: str) -> str:
        """Generate TTS audio and return base64-encoded wav"""
        if not text or not TTS_URL:
            return None
        
        try:
            response = requests.post(
                TTS_URL,
                json={
                    "model": "tts-1",
                    "input": text,
                    "voice": "alloy",
                    "response_format": "wav"
                },
                timeout=30
            )
            if response.status_code == 200:
                return base64.b64encode(response.content).decode('ascii')
            else:
                print(f"[ERROR] TTS error: {response.status_code}")
                return None
        except Exception as e:
            print(f"[ERROR] TTS exception: {e}")
            return None
        
    async def send_message(self, websocket, data: dict):
        """Send message to client"""
        try:
            await websocket.send(json.dumps(data))
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
    
    async def handle_client(self, websocket):
        """Handle WebSocket client connection"""
        session_id = str(uuid.uuid4())
        session = VoiceSession(session_id, websocket)
        self.sessions[session_id] = session
        
        print(f"[{datetime.now()}] New connection: {session_id}")
        
        # Send initial connection message
        await self.send_message(websocket, {
            'type': 'connected',
            'session_id': session_id,
            'state': session.state.value,
            'wake_word_detection': WAKE_WORD_AVAILABLE
        })
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(session, data)
                except json.JSONDecodeError:
                    print(f"[ERROR] Invalid JSON from {session_id}")
                except Exception as e:
                    print(f"[ERROR] Message handling error: {e}")
                    import traceback
                    traceback.print_exc()
        
        except websockets.exceptions.ConnectionClosed:
            print(f"[{datetime.now()}] Client disconnected: {session_id}")
        finally:
            del self.sessions[session_id]
    
    async def handle_message(self, session: VoiceSession, data: dict):
        """Route message to appropriate handler"""
        msg_type = data.get('type')
        
        if msg_type == 'audio_stream':
            await self.handle_audio_stream(session, data)
        elif msg_type == 'text_input':
            await self.handle_text_input(session, data)
        elif msg_type == 'stop_listening':
            await self.stop_recording(session)
        else:
            print(f"[WARN] Unknown message type: {msg_type}")
    
    async def handle_audio_stream(self, session: VoiceSession, data: dict):
        """Handle streaming audio from web client"""
        if not WAKE_WORD_AVAILABLE:
            return
        
        try:
            # Get audio data
            audio_array = data.get('audio', [])
            if not audio_array:
                return
            
            # Convert to numpy array
            audio_int16 = np.array(audio_array, dtype=np.int16)
            audio_float = audio_int16.astype(np.float32) / 32768.0
            
            if session.state == ClientState.PASSIVE:
                # Check for wake word
                predictions = session.oww_model.predict(audio_float)
                score = predictions.get(session.wake_word_name, 0)
                
                if score > 0.5:  # Wake word detected!
                    print(f"[{datetime.now()}] Wake word detected! Score: {score}")
                    session.state = ClientState.ACTIVE
                    session.recording_buffer = []
                    session.silence_chunks = 0
                    
                    await self.send_message(session.websocket, {
                        'type': 'wake_word_detected',
                        'timestamp': datetime.now().isoformat()
                    })
            
            elif session.state == ClientState.ACTIVE:
                # Record audio for command
                session.recording_buffer.append(audio_int16.tobytes())
                
                # Check for silence (end of command)
                audio_bytes = audio_int16.tobytes()
                try:
                    is_speech = session.vad.is_speech(audio_bytes, 16000)
                    if not is_speech:
                        session.silence_chunks += 1
                    else:
                        session.silence_chunks = 0
                    
                    # If 1.5 seconds of silence (15 chunks at ~100ms each)
                    if session.silence_chunks >= 15 and len(session.recording_buffer) > 10:
                        await self.process_recording(session)
                except:
                    # VAD might fail on short buffers
                    pass
        
        except Exception as e:
            print(f"[ERROR] Audio stream error: {e}")
            import traceback
            traceback.print_exc()
    
    async def process_recording(self, session: VoiceSession):
        """Process recorded audio and send to Whisper"""
        print(f"[{datetime.now()}] Processing recording for {session.session_id}")
        
        session.state = ClientState.PROCESSING
        
        await self.send_message(session.websocket, {
            'type': 'processing',
            'message': 'Transcribing...'
        })
        
        try:
            # Combine audio buffers
            audio_data = b''.join(session.recording_buffer)
            session.recording_buffer = []
            
            # Convert to WAV format
            import wave
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)
                wav_file.writeframes(audio_data)
            
            wav_buffer.seek(0)
            
            # Send to Whisper
            response = requests.post(
                WHISPER_URL,
                files={'file': ('audio.wav', wav_buffer, 'audio/wav')},
                data={'model': 'base'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get('text', '').strip()
                
                print(f"[{datetime.now()}] Transcription: {text}")
                
                await self.send_message(session.websocket, {
                    'type': 'transcription',
                    'text': text
                })
                
                # Process the query
                if text:
                    await self.process_query(session, text)
                else:
                    session.state = ClientState.PASSIVE
                    await self.send_message(session.websocket, {
                        'type': 'error',
                        'message': 'No speech detected'
                    })
            else:
                raise Exception(f"Whisper error: {response.status_code}")
        
        except Exception as e:
            print(f"[ERROR] Recording processing error: {e}")
            session.state = ClientState.PASSIVE
            await self.send_message(session.websocket, {
                'type': 'error',
                'message': f'Transcription error: {e}'
            })
    
    async def handle_text_input(self, session: VoiceSession, data: dict):
        """Handle direct text input"""
        text = data.get('text', '').strip()
        if not text:
            return
        
        print(f"[{datetime.now()}] Text input: {text}")
        
        session.state = ClientState.PROCESSING
        
        await self.send_message(session.websocket, {
            'type': 'processing',
            'message': 'Processing...'
        })
        
        await self.process_query(session, text)
    
    async def process_query(self, session: VoiceSession, text: str):
        """Process query through router"""
        start_time = datetime.now()
        
        try:
            # Use query router
            result = self.router.route_query(
                query=text,
                session_id=session.session_id,
                context=session.context[-5:]  # Last 5 exchanges
            )
            
            response_text = result.get('text', 'I didn\'t understand that.')
            intent = result.get('intent', '')
            
            # Calculate latency
            latency_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Add to context
            session.context.append({'query': text, 'response': response_text})
            
            # Log conversation
            self.log_conversation(
                session_id=session.session_id,
                user_text=text,
                response_text=response_text,
                intent=intent,
                latency_ms=latency_ms
            )
            
            # Generate TTS audio
            audio_b64 = await self.synthesize_speech(response_text)
            
            # Send response
            session.state = ClientState.RESPONDING
            await self.send_message(session.websocket, {
                'type': 'response',
                'text': response_text,
                'intent': intent,
                'audio': audio_b64,
                'audio_format': 'wav' if audio_b64 else None,
                'timestamp': datetime.now().isoformat()
            })
            
            # Return to passive listening
            session.state = ClientState.PASSIVE
        
        except Exception as e:
            print(f"[ERROR] Query processing error: {e}")
            import traceback
            traceback.print_exc()
            
            session.state = ClientState.PASSIVE
            await self.send_message(session.websocket, {
                'type': 'error',
                'message': f'Processing error: {e}'
            })
    
    async def stop_recording(self, session: VoiceSession):
        """Stop recording and process immediately"""
        if session.state == ClientState.ACTIVE and session.recording_buffer:
            await self.process_recording(session)
    
    async def start(self):
        """Start the WebSocket server"""
        print(f"[{datetime.now()}] Starting HAL Voice Gateway (Web)")
        print(f"[INFO] WebSocket: {WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
        print(f"[INFO] Whisper: {WHISPER_URL}")
        print(f"[INFO] Wake word detection: {'ENABLED' if WAKE_WORD_AVAILABLE else 'DISABLED'}")
        
        async with websockets.serve(
            self.handle_client,
            WEBSOCKET_HOST,
            WEBSOCKET_PORT,
            max_size=10_000_000,  # 10MB max message size
            ping_interval=20,
            ping_timeout=10
        ):
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    gateway = VoiceGateway()
    asyncio.run(gateway.start())
