#!/usr/bin/env python3
"""
HAL Voice Client - Unified Implementation
Combines robust features from existing client with new architecture

Architecture:
    Client (Mac/PC) → Voice Server (10.1.10.20:8585) → AI Server (10.1.34.103:8745)
"""
import asyncio
import time
import struct
import wave
import tempfile
import os
import sys
from pathlib import Path
from typing import Optional
from enum import Enum

import numpy as np
import sounddevice as sd
import webrtcvad
import websockets
import simpleaudio as sa

# Try to import OpenWakeWord (optional for wake word detection)
USE_WAKEWORD = True
try:
    from openwakeword.model import Model as OWWModel
except ImportError:
    USE_WAKEWORD = False
    print("⚠ OpenWakeWord not available - using keyboard mode")

# Configuration - UNIFIED ARCHITECTURE
VOICE_SERVER_URL = os.getenv('VOICE_SERVER_URL', 'ws://10.1.10.20:8585')
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 512  # ~32ms at 16kHz
SILENCE_THRESHOLD = 3.0  # seconds of silence before stopping
FOLLOW_UP_WINDOW = 10.0  # seconds of passive listening after response (RLM)
VAD_AGGRESSIVENESS = 2  # 0-3, higher = more aggressive

class ClientState(Enum):
    """Client state machine - Matches specification"""
    PASSIVE = "PLM"      # Passive Listening Mode - waiting for wake word
    ACTIVE = "ALM"       # Active Listening Mode - recording user speech
    SPEAKING = "ASM"     # Active Speaking Mode - playing response
    RESPONSE = "RLM"     # Response Listening Mode - 10s follow-up window

class HALVoiceClient:
    """
    HAL Voice Client - Unified Implementation
    
    Features from existing client:
    - OpenWakeWord detection ("Hey Jarvis" / "Computer")
    - WebRTC VAD for silence detection
    - Interruption handling
    - Audio feedback sounds (TNG activation.mp3)
    
    New architecture:
    - Connects to Voice Server on port 8585
    - Voice Server handles STT/TTS
    - AI Server (OpenQM) handles logic
    """
    
    def __init__(self, voice_server_url: str = VOICE_SERVER_URL):
        self.voice_server_url = voice_server_url
        self.state = ClientState.PASSIVE
        
        # Audio configuration
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.chunk_size = CHUNK_SIZE
        
        # Audio buffer
        self.audio_buffer = []
        
        # Timing
        self.recording_start_time = None
        self.last_voice_time = time.time()
        self.rlm_timer_task = None
        
        # VAD
        self.vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
        
        # Wake word detection
        self.oww_model = None
        self.wake_word_name = None
        if USE_WAKEWORD:
            self.init_wake_word()
        
        # Audio feedback
        self.sounds = self.load_sounds()
        
        # Audio stream
        self.stream = None
        
        # Session info
        self.client_id = os.getenv('CLIENT_ID', f'mac_{os.getpid()}')
        self.user_id = os.getenv('USER_ID', 'lawr')
        
    def init_wake_word(self):
        """Initialize OpenWakeWord detector"""
        try:
            # DEFAULT: "HEY JARVIS" - works immediately (no training needed)
            # Can be changed to "COMPUTER" later via environment variable
            
            wake_word_pref = os.getenv('WAKE_WORD', 'hey_jarvis_v0.1')
            
            print("Loading wake word model...")
            
            # Try to load wake word
            try:
                self.oww_model = OWWModel(wakeword_models=[wake_word_pref], inference_framework='onnx')
                model_names = list(self.oww_model.models.keys())
                if model_names:
                    self.wake_word_name = model_names[0]
                    
                    # Display appropriate message based on model
                    if 'jarvis' in self.wake_word_name.lower():
                        print(f"✓ Wake word loaded: {self.wake_word_name}")
                        print(f"  🎤 Say: \"HEY JARVIS\"")
                        print(f"\n  💡 TIP: Change to 'COMPUTER' later:")
                        print(f"     1. Train COMPUTER model (see TRAIN_COMPUTER_WAKE_WORD.md)")
                        print(f"     2. Set: export WAKE_WORD=computer_v0.1")
                    elif 'computer' in self.wake_word_name.lower():
                        print(f"✓ Wake word loaded: {self.wake_word_name}")
                        print(f"  🎤 Say: \"COMPUTER\"")
                    else:
                        print(f"✓ Wake word loaded: {self.wake_word_name}")
                        print(f"  🎤 Say wake word")
                    
                    return  # Success!
            
            except Exception as e:
                print(f"⚠ Wake word model not found: {wake_word_pref}")
                print(f"\n  → Using KEYBOARD MODE as fallback")
                print(f"     Press ENTER to record instead of saying wake word")
                raise  # Fall through to keyboard mode
        
        except Exception as e:
            print(f"\n⚠ Wake word detection not available - using keyboard mode")
            self.oww_model = None
    
    def load_sounds(self) -> dict:
        """Load audio feedback sounds from clients directory"""
        sounds = {}
        
        # Try multiple possible locations
        possible_dirs = [
            Path(__file__).parent,  # Same directory as script
            Path(__file__).parent.parent.parent / 'clients',  # ../../clients
            Path.home() / 'Projects' / 'hal' / 'clients'  # ~/Projects/hal/clients
        ]
        
        sound_files = {
            'activation': ['activation.mp3', 'TNG_activation.mp3', 'activation.wav'],
            'acknowledgement': ['acknowledgement.wav', 'ack.wav'],
            'error': ['error.wav', 'acknowledgement.wav']
        }
        
        for sound_dir in possible_dirs:
            if not sound_dir.exists():
                continue
            
            for name, filenames in sound_files.items():
                if sounds.get(name):
                    continue  # Already found
                
                for filename in filenames:
                    sound_path = sound_dir / filename
                    if sound_path.exists():
                        try:
                            if filename.endswith('.wav'):
                                sounds[name] = sa.WaveObject.from_wave_file(str(sound_path))
                                print(f"✓ Loaded {name}: {filename}")
                            else:
                                # MP3 - store path for system playback
                                sounds[name] = str(sound_path)
                                print(f"✓ Loaded {name}: {filename} (MP3)")
                            break
                        except Exception as e:
                            continue
        
        return sounds
    
    def play_sound(self, sound_name: str):
        """Play audio feedback sound"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                sound = self.sounds[sound_name]
                
                if isinstance(sound, str):
                    # MP3 file - system playback
                    if sys.platform == 'darwin':  # macOS
                        os.system(f'afplay "{sound}" &')
                    elif sys.platform == 'win32':  # Windows
                        os.system(f'start /min "" "{sound}"')
                    else:  # Linux
                        os.system(f'mpg123 -q "{sound}" &')
                else:
                    # WAV object
                    play_obj = sound.play()
                    # Don't wait - non-blocking
            except Exception as e:
                print(f"⚠ Error playing {sound_name}: {e}")
    
    def play_audio_data(self, audio_data: bytes):
        """Play raw audio data from voice server"""
        try:
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp_path = tmp.name
                tmp.write(audio_data)
            
            # Play based on format
            if audio_data.startswith(b'RIFF'):
                # WAV format
                wave_obj = sa.WaveObject.from_wave_file(tmp_path)
                play_obj = wave_obj.play()
                play_obj.wait_done()
            else:
                # MP3 or other format
                if sys.platform == 'darwin':
                    os.system(f'afplay "{tmp_path}"')
                elif sys.platform == 'win32':
                    os.system(f'start /min "" "{tmp_path}"')
                    time.sleep(2)
                else:
                    os.system(f'mpg123 -q "{tmp_path}"')
            
            # Cleanup
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        except Exception as e:
            print(f"⚠ Error playing audio: {e}")
    
    def detect_wake_word(self, audio_chunk: np.ndarray) -> bool:
        """Detect wake word in audio chunk"""
        if not self.oww_model:
            return False
        
        try:
            # Convert to float32
            audio_float = audio_chunk.astype(np.float32) / 32768.0
            
            # Get predictions
            predictions = self.oww_model.predict(audio_float)
            
            # Check threshold
            if predictions.get(self.wake_word_name, 0) > 0.5:
                return True
            
            return False
        
        except Exception as e:
            return False
    
    def is_speech(self, audio_chunk: bytes) -> bool:
        """Check if audio chunk contains speech using VAD"""
        try:
            return self.vad.is_speech(audio_chunk, self.sample_rate)
        except:
            return True
    
    async def on_wake_word_detected(self):
        """Handle wake word detection"""
        
        if self.state == ClientState.PASSIVE:
            # Normal wake word flow (PLM → ALM)
            print("\n👂 Wake word detected")
            self.play_sound('activation')
            
            # Transition to ACTIVE (ALM)
            self.state = ClientState.ACTIVE
            self.audio_buffer.clear()
            self.recording_start_time = time.time()
            self.last_voice_time = time.time()
            
            # Cancel RLM timer if running
            if self.rlm_timer_task:
                self.rlm_timer_task.cancel()
                self.rlm_timer_task = None
            
            print("🎤 Listening... (speak now)")
        
        elif self.state == ClientState.ACTIVE:
            # INTERRUPTION: "belay that" equivalent
            elapsed = time.time() - self.recording_start_time
            
            print(f"\n🔄 Interruption detected (after {elapsed:.1f}s) - Restarting")
            
            # Clear buffer (delete recording)
            self.audio_buffer.clear()
            
            # Play activation sound again
            self.play_sound('activation')
            
            # Reset timers
            self.recording_start_time = time.time()
            self.last_voice_time = time.time()
            
            print("🎤 Listening... (speak now)")
        
        elif self.state == ClientState.SPEAKING:
            # "wake_word stop" - stop playback
            print("\n🛑 Stop command detected")
            # TODO: Implement audio playback interruption
            self.state = ClientState.RESPONSE
            await self.start_rlm()
    
    async def on_silence_detected(self):
        """Handle silence detection (3 seconds) - end of ALM"""
        
        if self.state != ClientState.ACTIVE:
            return
        
        if not self.audio_buffer:
            print("⚠ No audio captured")
            self.state = ClientState.PASSIVE
            return
        
        print("🔇 Silence detected - Processing...")
        
        # Play acknowledgement sound
        self.play_sound('acknowledgement')
        
        # Combine audio buffer
        audio_data = b''.join(self.audio_buffer)
        self.audio_buffer.clear()
        
        # Send to voice server
        await self.send_to_voice_server(audio_data)
    
    async def on_voice_in_rlm(self):
        """Handle voice detection during RLM (10s follow-up window)"""
        
        if self.state == ClientState.RESPONSE and self.rlm_timer_task:
            print("\n🎤 Follow-up detected (no wake word needed)")
            
            # Cancel RLM timer
            self.rlm_timer_task.cancel()
            self.rlm_timer_task = None
            
            # Transition to ACTIVE (ALM) without wake word
            self.state = ClientState.ACTIVE
            self.audio_buffer.clear()
            self.recording_start_time = time.time()
            self.last_voice_time = time.time()
            
            print("🎤 Listening... (speak now)")
    
    async def send_to_voice_server(self, audio_data: bytes):
        """Send audio to voice server for STT → AI processing → TTS"""
        
        try:
            print(f"📤 Sending {len(audio_data)} bytes to voice server...")
            
            async with websockets.connect(self.voice_server_url, max_size=None) as ws:
                # Send session start
                await ws.send_json({
                    'type': 'session_start',
                    'client_id': self.client_id,
                    'user_id': self.user_id,
                    'wake_word': 'computer'
                })
                
                # Send audio data
                await ws.send(audio_data)
                
                # Send end marker
                await ws.send_json({'type': 'audio_end'})
                
                print("⏳ Waiting for response...")
                
                # Wait for response
                response = await asyncio.wait_for(ws.recv(), timeout=30.0)
                
                # Check response type
                if isinstance(response, bytes):
                    # Audio response
                    print(f"✓ Received {len(response)} bytes of audio")
                    await self.on_response_received(response)
                else:
                    # Text/JSON response
                    print(f"✓ Received: {response}")
                    self.state = ClientState.PASSIVE
        
        except asyncio.TimeoutError:
            print("❌ Timeout waiting for response")
            self.play_sound('error')
            self.state = ClientState.PASSIVE
        
        except Exception as e:
            print(f"❌ Error: {e}")
            self.play_sound('error')
            self.state = ClientState.PASSIVE
    
    async def on_response_received(self, audio_data: bytes):
        """Handle response audio from voice server (enter ASM then RLM)"""
        
        # Enter Active Speaking Mode (ASM)
        self.state = ClientState.SPEAKING
        print("🔊 Playing response...")
        
        # Play response audio
        self.play_audio_data(audio_data)
        
        # After playback, enter Response Listening Mode (RLM)
        await self.start_rlm()
    
    async def start_rlm(self):
        """Start Response Listening Mode (10 second window)"""
        
        self.state = ClientState.RESPONSE
        
        # Start RLM timer
        self.rlm_timer_task = asyncio.create_task(self.rlm_timer())
    
    async def rlm_timer(self):
        """10 second countdown for Response Listening Mode"""
        
        print(f"⏱️  {FOLLOW_UP_WINDOW:.0f}s follow-up window (speak without wake word)")
        
        try:
            await asyncio.sleep(FOLLOW_UP_WINDOW)
            
            if self.state == ClientState.RESPONSE:
                print("⏰ Follow-up window expired (wake word required)")
                self.state = ClientState.PASSIVE
                self.rlm_timer_task = None
        
        except asyncio.CancelledError:
            # Timer cancelled (user spoke or wake word detected)
            pass
    
    async def audio_loop(self):
        """Main audio processing loop"""
        
        # Open audio stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16',
            blocksize=self.chunk_size
        )
        
        print("\n" + "="*70)
        print("HAL Voice Client - Unified Implementation")
        print("="*70)
        print(f"\nVoice Server: {self.voice_server_url}")
        print(f"Client ID: {self.client_id}")
        print(f"User ID: {self.user_id}")
        
        if USE_WAKEWORD:
            print("\n✓ Wake word detection enabled")
            print("  Say: 'HEY JARVIS'")
        else:
            print("\n⚠ Wake word not available - using keyboard mode")
            print("  Press ENTER to start recording")
        
        print("\nListening...")
        print("(Press Ctrl+C to exit)\n")
        
        with self.stream:
            while True:
                try:
                    # Read audio chunk
                    audio_chunk, _ = self.stream.read(self.chunk_size)
                    audio_chunk = audio_chunk.flatten()
                    
                    # Always check for wake word
                    if USE_WAKEWORD and self.detect_wake_word(audio_chunk):
                        await self.on_wake_word_detected()
                    
                    # Convert to bytes
                    audio_bytes = audio_chunk.tobytes()
                    
                    # State-specific handling
                    if self.state == ClientState.ACTIVE:
                        # Buffer audio (ALM)
                        self.audio_buffer.append(audio_bytes)
                        
                        # Check for voice activity
                        if len(audio_bytes) >= 640:  # 20ms at 16kHz
                            chunk_20ms = audio_bytes[:640]
                            if self.is_speech(chunk_20ms):
                                self.last_voice_time = time.time()
                        
                        # Check for silence
                        silence_duration = time.time() - self.last_voice_time
                        if silence_duration >= SILENCE_THRESHOLD:
                            await self.on_silence_detected()
                    
                    elif self.state == ClientState.RESPONSE and self.rlm_timer_task:
                        # During RLM, check for voice (follow-up without wake word)
                        if len(audio_bytes) >= 640:
                            chunk_20ms = audio_bytes[:640]
                            if self.is_speech(chunk_20ms):
                                await self.on_voice_in_rlm()
                    
                    # Yield to event loop
                    await asyncio.sleep(0.001)
                
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ Error in audio loop: {e}")
                    await asyncio.sleep(0.1)
    
    async def keyboard_mode(self):
        """Fallback keyboard mode (no wake word detection)"""
        
        print("\n" + "="*70)
        print("HAL Voice Client - Keyboard Mode")
        print("="*70)
        print("\nPress ENTER to start recording")
        print("(Type 'quit' to exit)\n")
        
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                user_input = await loop.run_in_executor(
                    None, input, "Press ENTER to record (or 'quit'): "
                )
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Simulate wake word
                await self.on_wake_word_detected()
                
                # Record for 5 seconds
                print("🎤 Recording for 5 seconds...")
                
                self.audio_buffer.clear()
                
                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype='int16',
                    blocksize=self.chunk_size
                ) as stream:
                    for _ in range(int(self.sample_rate / self.chunk_size * 5)):
                        audio_chunk, _ = stream.read(self.chunk_size)
                        self.audio_buffer.append(audio_chunk.tobytes())
                
                print("✓ Recording complete")
                
                # Process
                audio_data = b''.join(self.audio_buffer)
                self.audio_buffer.clear()
                
                await self.send_to_voice_server(audio_data)
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def run(self):
        """Run the voice client"""
        
        try:
            if USE_WAKEWORD:
                await self.audio_loop()
            else:
                await self.keyboard_mode()
        
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        
        finally:
            # Cleanup
            if self.stream:
                self.stream.close()
            
            if self.rlm_timer_task:
                self.rlm_timer_task.cancel()

async def main():
    """Main entry point"""
    
    import argparse
    parser = argparse.ArgumentParser(description='HAL Voice Client - Unified')
    parser.add_argument('--url', default=VOICE_SERVER_URL, 
                       help='Voice Server WebSocket URL (default: ws://10.1.10.20:8585)')
    parser.add_argument('--client-id', help='Client ID')
    parser.add_argument('--user-id', help='User ID')
    args = parser.parse_args()
    
    if args.client_id:
        os.environ['CLIENT_ID'] = args.client_id
    if args.user_id:
        os.environ['USER_ID'] = args.user_id
    
    client = HALVoiceClient(args.url)
    await client.run()

if __name__ == '__main__':
    asyncio.run(main())
