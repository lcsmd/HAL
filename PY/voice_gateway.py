"""
HAL Voice Gateway
WebSocket server for voice interface clients
Handles audio streaming, transcription, and message routing
"""

import asyncio
import websockets
import json
import base64
import uuid
import requests
import socket
from datetime import datetime
from typing import Dict, Set
from enum import Enum
import sys
sys.path.insert(0, '.')
from qm_client_sync import query_qm

# Configuration
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8768  # Using 8768 (8765-8767 in use)
WHISPER_URL = "http://10.1.10.20:8001/transcribe"  # Whisper on port 8001
QM_LISTENER_HOST = "localhost"
QM_LISTENER_PORT = 8745  # AI.SERVER port
MAX_CONNECTIONS = 50
ACTIVE_TIMEOUT = 30000  # 30 seconds
FOLLOW_UP_WINDOW = 10000  # 10 seconds

class ClientState(Enum):
    PASSIVE = "passive_listening"
    ACTIVE = "active_listening"
    PROCESSING = "processing"
    RESPONDING = "responding"

class VoiceSession:
    def __init__(self, session_id: str, websocket):
        self.session_id = session_id
        self.websocket = websocket
        self.state = ClientState.PASSIVE
        self.audio_buffer = []
        self.context = []
        self.last_activity = datetime.now()
        self.last_response = None
        self.client_type = None
        
    def update_activity(self):
        self.last_activity = datetime.now()
        
    def add_audio_chunk(self, audio_data: str):
        self.audio_buffer.append(audio_data)
        self.update_activity()
        
    def clear_audio_buffer(self):
        audio = b''.join([base64.b64decode(chunk) for chunk in self.audio_buffer])
        self.audio_buffer = []
        return audio
        
    def add_to_context(self, utterance: str, response: str):
        self.context.append({
            'utterance': utterance,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        # Keep last 10 turns
        if len(self.context) > 10:
            self.context = self.context[-10:]

class VoiceGateway:
    def __init__(self):
        self.sessions: Dict[str, VoiceSession] = {}
        self.active_connections: Set[websockets.WebSocketServerProtocol] = set()
        
    async def register_client(self, websocket, session_id: str = None):
        if session_id is None:
            session_id = str(uuid.uuid4())
            
        session = VoiceSession(session_id, websocket)
        self.sessions[session_id] = session
        self.active_connections.add(websocket)
        
        print(f"[{datetime.now()}] Client registered: {session_id}")
        return session_id
        
    async def unregister_client(self, websocket):
        # Find and remove session
        session_to_remove = None
        for session_id, session in self.sessions.items():
            if session.websocket == websocket:
                session_to_remove = session_id
                break
                
        if session_to_remove:
            del self.sessions[session_to_remove]
            print(f"[{datetime.now()}] Client unregistered: {session_to_remove}")
            
        self.active_connections.discard(websocket)
        
    async def handle_message(self, websocket, message: str):
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            session_id = data.get('session_id')
            
            if not session_id or session_id not in self.sessions:
                await self.send_error(websocket, "Invalid session ID")
                return
                
            session = self.sessions[session_id]
            
            # Route based on message type
            if msg_type == 'audio_chunk':
                await self.handle_audio_chunk(session, data)
            elif msg_type == 'wake_word_detected':
                await self.handle_wake_word(session, data)
            elif msg_type == 'speech_ended':
                await self.handle_speech_ended(session, data)
            elif msg_type == 'text_input':
                await self.handle_text_input(session, data)
            elif msg_type == 'command':
                await self.handle_command(session, data)
            elif msg_type == 'heartbeat':
                session.update_activity()
            else:
                await self.send_error(websocket, f"Unknown message type: {msg_type}")
                
        except json.JSONDecodeError:
            await self.send_error(websocket, "Invalid JSON")
        except Exception as e:
            print(f"[{datetime.now()}] Error handling message: {e}")
            await self.send_error(websocket, str(e))
            
    async def handle_audio_chunk(self, session: VoiceSession, data: dict):
        if session.state != ClientState.ACTIVE:
            return  # Ignore audio if not in active listening mode
            
        audio_data = data.get('audio')
        session.add_audio_chunk(audio_data)
        
    async def handle_wake_word(self, session: VoiceSession, data: dict):
        if session.state != ClientState.PASSIVE:
            return  # Already active
            
        print(f"[{datetime.now()}] Wake word detected for session {session.session_id}")
        
        # Transition to active listening
        session.state = ClientState.ACTIVE
        session.update_activity()
        
        # Send acknowledgment
        await self.send_message(session.websocket, {
            'type': 'ack',
            'sound': 'chime',
            'timestamp': datetime.now().isoformat()
        })
        
        # Send state change
        await self.send_message(session.websocket, {
            'type': 'state_change',
            'new_state': 'active_listening',
            'timeout_ms': ACTIVE_TIMEOUT,
            'timestamp': datetime.now().isoformat()
        })
        
    async def handle_text_input(self, session: VoiceSession, data: dict):
        """Handle direct text input (bypass audio transcription)"""
        if session.state != ClientState.ACTIVE:
            # Activate if passive
            if session.state == ClientState.PASSIVE:
                session.state = ClientState.ACTIVE
        
        text = data.get('text', '').strip()
        if not text:
            return
            
        print(f"[{datetime.now()}] Text input for session {session.session_id}: {text}")
        
        # Transition to processing
        session.state = ClientState.PROCESSING
        
        # Send processing feedback
        await self.send_message(session.websocket, {
            'type': 'processing',
            'sound': 'working_tone',
            'message': 'Processing your request...',
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            # Send directly to QM listener (bypass transcription)
            response = await self.send_to_qm(session, text)
            
            # Transition to responding
            session.state = ClientState.RESPONDING
            
            # Send response
            await self.send_message(session.websocket, {
                'type': 'response',
                'text': response.get('text', 'I didn\'t understand that.'),
                'action_taken': response.get('action_taken'),
                'timestamp': datetime.now().isoformat()
            })
            
            # Store last response
            session.last_response = response.get('text')
            
            # Add to context
            session.add_to_context(text, response.get('text'))
            
            # Transition to active listening (follow-up window)
            session.state = ClientState.ACTIVE
            await self.send_message(session.websocket, {
                'type': 'state_change',
                'new_state': 'active_listening',
                'countdown_ms': FOLLOW_UP_WINDOW,
                'timestamp': datetime.now().isoformat()
            })
            
            # Schedule return to passive after follow-up window
            await asyncio.sleep(FOLLOW_UP_WINDOW / 1000)
            if session.state == ClientState.ACTIVE:
                session.state = ClientState.PASSIVE
                await self.send_message(session.websocket, {
                    'type': 'state_change',
                    'new_state': 'passive_listening',
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"[{datetime.now()}] Error processing text: {e}")
            await self.send_error(session.websocket, f"Processing failed: {e}")
            session.state = ClientState.PASSIVE
    
    async def handle_speech_ended(self, session: VoiceSession, data: dict):
        if session.state != ClientState.ACTIVE:
            return
            
        print(f"[{datetime.now()}] Speech ended for session {session.session_id}")
        
        # Transition to processing
        session.state = ClientState.PROCESSING
        
        # Send processing feedback
        await self.send_message(session.websocket, {
            'type': 'processing',
            'sound': 'working_tone',
            'message': 'Processing your request...',
            'timestamp': datetime.now().isoformat()
        })
        
        # Get audio buffer
        audio = session.clear_audio_buffer()
        
        # Transcribe
        try:
            transcription = await self.transcribe_audio(audio)
            print(f"[{datetime.now()}] Transcription: {transcription}")
            
            # Send to QM listener
            response = await self.send_to_qm(session, transcription)
            
            # Transition to responding
            session.state = ClientState.RESPONDING
            
            # Send response
            await self.send_message(session.websocket, {
                'type': 'response',
                'text': response.get('text', 'I didn\'t understand that.'),
                'action_taken': response.get('action_taken'),
                'timestamp': datetime.now().isoformat()
            })
            
            # Store last response for "repeat" command
            session.last_response = response.get('text')
            
            # Add to context
            session.add_to_context(transcription, response.get('text'))
            
            # Transition to active listening (follow-up window)
            session.state = ClientState.ACTIVE
            await self.send_message(session.websocket, {
                'type': 'state_change',
                'new_state': 'active_listening',
                'countdown_ms': FOLLOW_UP_WINDOW,
                'timestamp': datetime.now().isoformat()
            })
            
            # Schedule return to passive after follow-up window
            await asyncio.sleep(FOLLOW_UP_WINDOW / 1000)
            if session.state == ClientState.ACTIVE:
                session.state = ClientState.PASSIVE
                await self.send_message(session.websocket, {
                    'type': 'state_change',
                    'new_state': 'passive_listening',
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"[{datetime.now()}] Error processing speech: {e}")
            await self.send_error(session.websocket, f"Processing failed: {e}")
            session.state = ClientState.PASSIVE
            
    async def handle_command(self, session: VoiceSession, data: dict):
        command = data.get('command')
        
        if command == 'hold':
            # Return to passive immediately
            session.state = ClientState.PASSIVE
            session.clear_audio_buffer()
            await self.send_message(session.websocket, {
                'type': 'state_change',
                'new_state': 'passive_listening',
                'timestamp': datetime.now().isoformat()
            })
            
        elif command == 'stop':
            # Cancel current operation
            session.state = ClientState.PASSIVE
            await self.send_message(session.websocket, {
                'type': 'state_change',
                'new_state': 'passive_listening',
                'timestamp': datetime.now().isoformat()
            })
            
        elif command == 'repeat':
            # Repeat last response
            if session.last_response:
                await self.send_message(session.websocket, {
                    'type': 'response',
                    'text': session.last_response,
                    'is_repeat': True,
                    'timestamp': datetime.now().isoformat()
                })
                
        elif command == 'goodbye':
            # End session
            session.state = ClientState.PASSIVE
            await self.send_message(session.websocket, {
                'type': 'goodbye',
                'sound': 'goodbye',
                'message': 'Goodbye!',
                'timestamp': datetime.now().isoformat()
            })
            
    async def transcribe_audio(self, audio: bytes) -> str:
        """Send audio to Faster-Whisper for transcription using OpenAI API format"""
        try:
            # Whisper expects multipart/form-data with audio file
            # Use OpenAI-compatible API: /v1/audio/transcriptions
            whisper_endpoint = "http://10.1.10.20:8001/v1/audio/transcriptions"
            
            # Create form data
            files = {
                'file': ('audio.wav', audio, 'audio/wav')
            }
            data = {
                'model': 'whisper-1',
                'language': 'en'
            }
            
            response = requests.post(
                whisper_endpoint,
                files=files,
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', '').strip()
            else:
                raise Exception(f"Whisper server error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"[{datetime.now()}] Transcription error: {e}")
            raise
            
    async def send_to_qm(self, session: VoiceSession, transcription: str) -> dict:
        """Send transcription to intelligent query router"""
        try:
            print(f"[{datetime.now()}] Routing query: {transcription[:50]}")
            
            # Use intelligent router instead of direct QM connection
            from query_router import route_query
            
            # Use router in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                route_query,
                transcription,
                session.session_id,
                session.context,
                'config/router_config.json'
            )
            
            intent = response.get('intent', 'unknown')
            text = response.get('text', '')[:50]
            print(f"[{datetime.now()}] Router response (intent: {intent}): {text}")
            return response
            
        except Exception as e:
            print(f"[{datetime.now()}] Router error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return {
                'text': 'Sorry, I\'m having trouble processing your request.',
                'action_taken': 'ERROR',
                'status': 'error'
            }
            
    async def send_message(self, websocket, message: dict):
        try:
            await websocket.send(json.dumps(message))
        except Exception as e:
            print(f"[{datetime.now()}] Error sending message: {e}")
            
    async def send_error(self, websocket, error_message: str):
        await self.send_message(websocket, {
            'type': 'error',
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        })
        
    async def handle_client(self, websocket):
        session_id = None
        try:
            # Register client
            session_id = await self.register_client(websocket)
            
            # Send initial state
            await self.send_message(websocket, {
                'type': 'connected',
                'session_id': session_id,
                'state': 'passive_listening',
                'timestamp': datetime.now().isoformat()
            })
            
            # Handle messages
            async for message in websocket:
                await self.handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            print(f"[{datetime.now()}] Client disconnected: {session_id}")
        except Exception as e:
            print(f"[{datetime.now()}] Error handling client: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.unregister_client(websocket)
            
    async def start(self):
        print(f"[{datetime.now()}] Starting Voice Gateway on {WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
        async with websockets.serve(self.handle_client, WEBSOCKET_HOST, WEBSOCKET_PORT):
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    gateway = VoiceGateway()
    asyncio.run(gateway.start())
