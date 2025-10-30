"""
HAL Voice Client for Mac
Desktop voice interface with wake word detection and audio I/O

Requirements:
  pip install websockets sounddevice numpy pvporcupine
"""

import asyncio
import websockets
import sounddevice as sd
import numpy as np
import base64
import json
import uuid
from datetime import datetime
from collections import deque
import sys

# Try to import Porcupine (wake word detection)
try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    print("Warning: pvporcupine not installed. Wake word detection disabled.")
    print("  Install with: pip install pvporcupine")
    print("  Get access key from: https://console.picovoice.ai/")
    PORCUPINE_AVAILABLE = False

# Configuration
GATEWAY_URL = "ws://localhost:8765"  # Change to your QM server IP
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 512
WAKE_WORDS = ["hey computer"]  # Porcupine built-in keywords

# Porcupine access key (get from https://console.picovoice.ai/)
# Replace with your actual key
PORCUPINE_ACCESS_KEY = "YOUR_PICOVOICE_ACCESS_KEY_HERE"

class VoiceClient:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.websocket = None
        self.state = 'passive'
        self.audio_buffer = deque(maxlen=100)  # Buffer last 5 seconds
        self.porcupine = None
        self.stream = None
        
    async def connect(self):
        """Connect to Voice Gateway"""
        print(f"[{datetime.now()}] Connecting to {GATEWAY_URL}...")
        
        try:
            self.websocket = await websockets.connect(GATEWAY_URL)
            
            # Wait for connection acknowledgment
            message = await self.websocket.recv()
            data = json.loads(message)
            
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                self.state = data.get('state', 'passive_listening')
                print(f"[{datetime.now()}] ✓ Connected!")
                print(f"[{datetime.now()}] Session ID: {self.session_id}")
                print(f"[{datetime.now()}] State: {self.state}")
                return True
            else:
                print(f"[{datetime.now()}] ✗ Unexpected response: {data}")
                return False
                
        except Exception as e:
            print(f"[{datetime.now()}] ✗ Connection failed: {e}")
            return False
            
    def init_audio(self):
        """Initialize audio input"""
        print(f"[{datetime.now()}] Initializing audio...")
        
        # Initialize wake word detection if available
        if PORCUPINE_AVAILABLE and PORCUPINE_ACCESS_KEY != "YOUR_PICOVOICE_ACCESS_KEY_HERE":
            try:
                self.porcupine = pvporcupine.create(
                    access_key=PORCUPINE_ACCESS_KEY,
                    keywords=WAKE_WORDS
                )
                print(f"[{datetime.now()}] ✓ Wake word detection enabled: {WAKE_WORDS}")
            except Exception as e:
                print(f"[{datetime.now()}] ✗ Wake word detection failed: {e}")
                print("  Falling back to keyboard activation")
                self.porcupine = None
        else:
            print(f"[{datetime.now()}] Wake word detection disabled (using keyboard)")
            
        # Start audio stream
        try:
            self.stream = sd.InputStream(
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                blocksize=CHUNK_SIZE,
                callback=self.audio_callback
            )
            self.stream.start()
            print(f"[{datetime.now()}] ✓ Audio stream started")
        except Exception as e:
            print(f"[{datetime.now()}] ✗ Audio initialization failed: {e}")
            
    def audio_callback(self, indata, frames, time_info, status):
        """Audio input callback"""
        if status:
            print(f"[{datetime.now()}] Audio status: {status}")
            
        # Convert to int16
        audio_int16 = (indata * 32767).astype(np.int16)
        
        # Add to buffer
        self.audio_buffer.append(audio_int16.copy())
        
        # Wake word detection (passive mode only)
        if self.state == 'passive_listening' and self.porcupine:
            # Porcupine expects 1D array
            audio_1d = audio_int16.flatten()
            
            try:
                keyword_index = self.porcupine.process(audio_1d)
                if keyword_index >= 0:
                    print(f"\n[{datetime.now()}] 🎤 Wake word detected!")
                    asyncio.create_task(self.on_wake_word())
            except Exception as e:
                pass  # Ignore processing errors
                
        # Send audio in active mode
        elif self.state == 'active_listening':
            asyncio.create_task(self.send_audio_chunk(audio_int16))
            
    async def on_wake_word(self):
        """Handle wake word detection"""
        if not self.websocket:
            return
            
        message = {
            'type': 'wake_word_detected',
            'session_id': self.session_id,
            'wake_word': WAKE_WORDS[0],
            'confidence': 0.95,
            'timestamp': datetime.now().isoformat()
        }
        
        await self.websocket.send(json.dumps(message))
        
    async def send_audio_chunk(self, audio_data):
        """Send audio chunk to gateway"""
        if not self.websocket:
            return
            
        # Encode as base64
        audio_b64 = base64.b64encode(audio_data.tobytes()).decode()
        
        message = {
            'type': 'audio_chunk',
            'session_id': self.session_id,
            'audio': audio_b64,
            'format': 'wav',
            'sample_rate': SAMPLE_RATE,
            'timestamp': datetime.now().isoformat()
        }
        
        await self.websocket.send(json.dumps(message))
        
    async def send_command(self, command):
        """Send interrupt command"""
        if not self.websocket:
            return
            
        message = {
            'type': 'command',
            'session_id': self.session_id,
            'command': command,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"[{datetime.now()}] Sending command: {command}")
        await self.websocket.send(json.dumps(message))
        
    async def handle_messages(self):
        """Handle incoming messages from gateway"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                msg_type = data.get('type')
                
                if msg_type == 'ack':
                    print(f"[{datetime.now()}] 🔊 *chime*")
                    
                elif msg_type == 'state_change':
                    new_state = data.get('new_state')
                    self.state = new_state
                    print(f"[{datetime.now()}] → State: {new_state}")
                    
                    if new_state == 'active_listening':
                        countdown = data.get('countdown_ms', 0) / 1000
                        if countdown > 0:
                            print(f"[{datetime.now()}] ⏱️  Follow-up window: {countdown:.0f}s")
                            
                elif msg_type == 'processing':
                    print(f"[{datetime.now()}] 🔄 Processing...")
                    
                elif msg_type == 'response':
                    response_text = data.get('text', '')
                    print(f"\n[{datetime.now()}] 🤖 HAL: {response_text}\n")
                    
                elif msg_type == 'error':
                    error_msg = data.get('message', 'Unknown error')
                    print(f"[{datetime.now()}] ❌ Error: {error_msg}")
                    
                elif msg_type == 'goodbye':
                    print(f"[{datetime.now()}] 👋 Goodbye!")
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"[{datetime.now()}] Connection closed")
        except Exception as e:
            print(f"[{datetime.now()}] Error handling messages: {e}")
            
    async def keyboard_input(self):
        """Handle keyboard commands (alternative to wake word)"""
        print("\nKeyboard commands:")
        print("  [SPACE] - Simulate wake word")
        print("  h - Send 'hold' command")
        print("  s - Send 'stop' command")
        print("  r - Send 'repeat' command")
        print("  g - Send 'goodbye' command")
        print("  q - Quit\n")
        
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                # Run input in executor to avoid blocking
                key = await loop.run_in_executor(None, input, "")
                
                if key == ' ':
                    await self.on_wake_word()
                elif key == 'h':
                    await self.send_command('hold')
                elif key == 's':
                    await self.send_command('stop')
                elif key == 'r':
                    await self.send_command('repeat')
                elif key == 'g':
                    await self.send_command('goodbye')
                elif key == 'q':
                    print("Quitting...")
                    break
                    
            except Exception as e:
                print(f"Error: {e}")
                break
                
    async def run(self):
        """Main run loop"""
        # Connect
        if not await self.connect():
            return
            
        # Initialize audio
        self.init_audio()
        
        # Run message handler and keyboard input concurrently
        try:
            await asyncio.gather(
                self.handle_messages(),
                self.keyboard_input()
            )
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        finally:
            if self.stream:
                self.stream.stop()
                self.stream.close()
            if self.porcupine:
                self.porcupine.delete()
            if self.websocket:
                await self.websocket.close()
                
    def cleanup(self):
        """Cleanup resources"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.porcupine:
            self.porcupine.delete()

def main():
    print("=" * 60)
    print("HAL Voice Client for Mac")
    print("=" * 60)
    print()
    
    # Check if access key is set
    if PORCUPINE_AVAILABLE and PORCUPINE_ACCESS_KEY == "YOUR_PICOVOICE_ACCESS_KEY_HERE":
        print("⚠️  Warning: Porcupine access key not set!")
        print("   Get your free key from: https://console.picovoice.ai/")
        print("   Then edit this file and replace PORCUPINE_ACCESS_KEY")
        print()
        print("   Using keyboard activation instead (press SPACE)\n")
    
    client = VoiceClient()
    
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        client.cleanup()

if __name__ == "__main__":
    main()
