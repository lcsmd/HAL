#!/usr/bin/env python3
"""
HAL Voice Client - Full Implementation
Supports wake word detection, VAD, interruption handling, and 10s passive window
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

# Configuration
UBUAI_URL = os.getenv('UBUAI_URL', 'ws://10.1.10.20:8001/transcribe')
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 512  # ~32ms at 16kHz
SILENCE_THRESHOLD = 3.0  # seconds of silence before stopping
FOLLOW_UP_WINDOW = 10.0  # seconds of passive listening after response
VAD_AGGRESSIVENESS = 2  # 0-3, higher = more aggressive

class ClientState(Enum):
    """Client state machine"""
    PASSIVE = "passive"  # Waiting for wake word
    ACTIVE = "active"    # Recording user speech
    PROCESSING = "processing"  # Waiting for response

class HALVoiceClient:
    """HAL voice client with full state machine"""
    
    def __init__(self, ubuai_url: str = UBUAI_URL):
        self.ubuai_url = ubuai_url
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
        self.passive_timer_task = None
        
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
        
    def init_wake_word(self):
        """Initialize OpenWakeWord detector"""
        try:
            # Try "hey_jarvis" first (closest to "HAL"), then fallback
            wake_words = ['hey_jarvis_v0.1']
            
            print("Loading wake word model...")
            self.oww_model = OWWModel(wakeword_models=wake_words, inference_framework='onnx')
            
            # Get actual model name
            model_names = list(self.oww_model.models.keys())
            if model_names:
                self.wake_word_name = model_names[0]
                print(f"✓ Wake word loaded: {self.wake_word_name}")
                print("  Say: 'Hey Jarvis' or 'Computer'")
            else:
                raise Exception("No wake word models loaded")
        
        except Exception as e:
            print(f"⚠ Wake word init failed: {e}")
            self.oww_model = None
    
    def load_sounds(self) -> dict:
        """Load audio feedback sounds"""
        sounds = {}
        script_dir = Path(__file__).parent
        
        # Map sound names to filenames (prefer MP3 for activation, WAV for others)
        sound_files = {
            'activation': ['activation.mp3', 'activation.wav', 'TNG_activation.mp3'],
            'acknowledgement': ['acknowledgement.wav', 'ack.wav'],
            'error': ['error.wav', 'acknowledgement.wav']  # Fallback to ack if no error
        }
        
        for name, filenames in sound_files.items():
            sounds[name] = None
            for filename in filenames:
                sound_path = script_dir / filename
                if sound_path.exists():
                    try:
                        # Check if WAV file
                        if filename.endswith('.wav'):
                            sounds[name] = sa.WaveObject.from_wave_file(str(sound_path))
                            print(f"✓ Loaded {name}: {filename}")
                            break
                        else:
                            # For MP3 files, store path for external playback
                            sounds[name] = str(sound_path)
                            print(f"✓ Loaded {name}: {filename} (MP3)")
                            break
                    except Exception as e:
                        print(f"⚠ Could not load {filename}: {e}")
                        continue
        
        return sounds
    
    def play_sound(self, sound_name: str):
        """Play audio feedback sound"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                sound = self.sounds[sound_name]
                
                # Check if it's a WAV object or a file path (MP3)
                if isinstance(sound, str):
                    # MP3 file - play with system command
                    if sys.platform == 'darwin':  # macOS
                        os.system(f'afplay "{sound}" &')
                    elif sys.platform == 'win32':  # Windows
                        os.system(f'start /min "" "{sound}"')
                    else:  # Linux
                        os.system(f'mpg123 -q "{sound}" &')
                else:
                    # WAV object - play with simpleaudio
                    play_obj = sound.play()
                    play_obj.wait_done()
            except Exception as e:
                print(f"⚠ Error playing {sound_name}: {e}")
    
    def play_audio_data(self, audio_data: bytes):
        """Play raw audio data (WAV or MP3 format)"""
        try:
            # Save to temp file and play
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp_path = tmp.name
                tmp.write(audio_data)
            
            # Try to play with simpleaudio (if WAV)
            if audio_data.startswith(b'RIFF'):
                wave_obj = sa.WaveObject.from_wave_file(tmp_path)
                play_obj = wave_obj.play()
                play_obj.wait_done()
            else:
                # For MP3, need external player
                # On Windows: use built-in
                if sys.platform == 'win32':
                    os.system(f'start /min "" "{tmp_path}"')
                    time.sleep(2)  # Wait for playback
                else:
                    # On Mac/Linux, use afplay/mpg123
                    os.system(f'afplay "{tmp_path}" 2>/dev/null || mpg123 -q "{tmp_path}" 2>/dev/null')
            
            # Cleanup
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        except Exception as e:
            print(f"⚠ Error playing audio: {e}")
    
    def detect_wake_word(self, audio_chunk: np.ndarray) -> bool:
        """
        Detect wake word in audio chunk
        
        Args:
            audio_chunk: Audio data (512 samples, int16)
        
        Returns:
            True if wake word detected
        """
        if not self.oww_model:
            return False
        
        try:
            # Convert to float32 format expected by OpenWakeWord
            audio_float = audio_chunk.astype(np.float32) / 32768.0
            
            # Get predictions
            predictions = self.oww_model.predict(audio_float)
            
            # Check threshold (0.5 for primary wake word)
            if predictions.get(self.wake_word_name, 0) > 0.5:
                return True
            
            return False
        
        except Exception as e:
            print(f"⚠ Wake word detection error: {e}")
            return False
    
    def is_speech(self, audio_chunk: bytes) -> bool:
        """
        Check if audio chunk contains speech using VAD
        
        Args:
            audio_chunk: PCM16 audio data (should be 10, 20, or 30ms at 16kHz)
        
        Returns:
            True if speech detected
        """
        try:
            return self.vad.is_speech(audio_chunk, self.sample_rate)
        except Exception as e:
            # Fallback: assume speech if error
            return True
    
    async def on_wake_word_detected(self):
        """Handle wake word detection"""
        
        if self.state == ClientState.PASSIVE:
            # Normal wake word flow
            print("\n👂 Wake word detected")
            self.play_sound('activation')
            
            # Transition to ACTIVE
            self.state = ClientState.ACTIVE
            self.audio_buffer.clear()
            self.recording_start_time = time.time()
            self.last_voice_time = time.time()
            
            # Cancel passive timer if running
            if self.passive_timer_task:
                self.passive_timer_task.cancel()
                self.passive_timer_task = None
            
            print("🎤 Listening... (speak now)")
        
        elif self.state == ClientState.ACTIVE:
            # INTERRUPTION: Wake word during active recording
            elapsed = time.time() - self.recording_start_time
            
            print(f"\n🔄 Interruption detected (after {elapsed:.1f}s) - Restarting")
            
            # Clear buffered audio (discard interrupted message)
            self.audio_buffer.clear()
            
            # Play activation sound again (confirms reset)
            self.play_sound('activation')
            
            # Reset recording timer
            self.recording_start_time = time.time()
            self.last_voice_time = time.time()
            
            print("🎤 Listening... (speak now)")
            
            # Stay in ACTIVE state, continue recording fresh
    
    async def on_silence_detected(self):
        """Handle silence detection (3 seconds)"""
        
        if self.state != ClientState.ACTIVE:
            return
        
        if not self.audio_buffer:
            # No audio captured
            print("⚠ No audio captured")
            self.state = ClientState.PASSIVE
            return
        
        print("🔇 Silence detected - Processing...")
        
        # Play acknowledgement sound
        self.play_sound('acknowledgement')
        
        # Combine audio buffer
        audio_data = b''.join(self.audio_buffer)
        self.audio_buffer.clear()
        
        # Transition to PROCESSING
        self.state = ClientState.PROCESSING
        
        # Send to UBUAI
        await self.send_to_ubuai(audio_data)
    
    async def on_voice_in_passive(self):
        """Handle voice detection during 10s passive window"""
        
        if self.state == ClientState.PASSIVE and self.passive_timer_task:
            print("\n🎤 Follow-up detected (no wake word needed)")
            
            # Cancel timer
            self.passive_timer_task.cancel()
            self.passive_timer_task = None
            
            # Transition to ACTIVE WITHOUT wake word or activation sound
            self.state = ClientState.ACTIVE
            self.audio_buffer.clear()
            self.recording_start_time = time.time()
            self.last_voice_time = time.time()
            
            print("🎤 Listening... (speak now)")
    
    async def send_to_ubuai(self, audio_data: bytes):
        """Send audio to UBUAI for transcription and response"""
        
        try:
            print(f"📤 Sending {len(audio_data)} bytes to UBUAI...")
            
            async with websockets.connect(self.ubuai_url, max_size=None) as ws:
                # Send audio data
                await ws.send(audio_data)
                
                # Send end marker
                await ws.send("__END__")
                
                # Wait for response
                print("⏳ Waiting for response...")
                response = await asyncio.wait_for(ws.recv(), timeout=30.0)
                
                # Check response type
                if isinstance(response, bytes):
                    # Audio response
                    print(f"✓ Received {len(response)} bytes of audio")
                    await self.on_response_received(response)
                else:
                    # Text response (error or fallback)
                    print(f"✓ Received text: {response}")
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
        """Handle response audio from UBUAI"""
        
        print("🔊 Playing response...")
        
        # Play response audio
        self.play_audio_data(audio_data)
        
        # Transition to PASSIVE with 10s follow-up window
        self.state = ClientState.PASSIVE
        
        # Start passive timer
        self.passive_timer_task = asyncio.create_task(self.passive_timer())
    
    async def passive_timer(self):
        """10 second countdown for follow-up window"""
        
        print(f"⏱️  {FOLLOW_UP_WINDOW:.0f}s follow-up window (speak without wake word)")
        
        try:
            await asyncio.sleep(FOLLOW_UP_WINDOW)
            
            if self.state == ClientState.PASSIVE:
                print("⏰ Follow-up window expired (wake word required)")
                self.passive_timer_task = None
        
        except asyncio.CancelledError:
            # Timer was cancelled (user spoke or wake word detected)
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
        
        print("\n" + "="*60)
        print("HAL Voice Client - Full Implementation")
        print("="*60)
        
        if USE_WAKEWORD:
            print("\n✓ Wake word detection enabled")
            print("  Say: 'Hey Jarvis' or 'Computer'")
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
                    
                    # Convert to bytes for processing
                    audio_bytes = audio_chunk.tobytes()
                    
                    # State-specific handling
                    if self.state == ClientState.ACTIVE:
                        # Buffer audio
                        self.audio_buffer.append(audio_bytes)
                        
                        # Check for voice activity (every 20ms chunk)
                        if len(audio_bytes) == 32:  # 20ms at 16kHz = 320 samples = 640 bytes
                            if self.is_speech(audio_bytes):
                                self.last_voice_time = time.time()
                        
                        # Check for silence
                        silence_duration = time.time() - self.last_voice_time
                        if silence_duration >= SILENCE_THRESHOLD:
                            await self.on_silence_detected()
                    
                    elif self.state == ClientState.PASSIVE and self.passive_timer_task:
                        # During 10s follow-up window, check for voice
                        if len(audio_bytes) == 32:  # 20ms chunk
                            if self.is_speech(audio_bytes):
                                await self.on_voice_in_passive()
                    
                    # Small yield to event loop
                    await asyncio.sleep(0.001)
                
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ Error in audio loop: {e}")
                    import traceback
                    traceback.print_exc()
                    await asyncio.sleep(0.1)
    
    async def keyboard_mode(self):
        """Fallback keyboard mode (no wake word detection)"""
        
        print("\n" + "="*60)
        print("HAL Voice Client - Keyboard Mode")
        print("="*60)
        print("\nPress ENTER to start recording")
        print("(Type 'quit' to exit)\n")
        
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                # Wait for ENTER key
                user_input = await loop.run_in_executor(
                    None, input, "Press ENTER to record (or 'quit'): "
                )
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Simulate wake word detection
                await self.on_wake_word_detected()
                
                # Record for fixed duration
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
                self.state = ClientState.PROCESSING
                
                await self.send_to_ubuai(audio_data)
            
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
            
            if self.passive_timer_task:
                self.passive_timer_task.cancel()

async def main():
    """Main entry point"""
    
    import argparse
    parser = argparse.ArgumentParser(description='HAL Voice Client')
    parser.add_argument('--url', default=UBUAI_URL, help='UBUAI WebSocket URL')
    args = parser.parse_args()
    
    client = HALVoiceClient(args.url)
    await client.run()

if __name__ == '__main__':
    asyncio.run(main())
