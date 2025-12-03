#!/usr/bin/env python3
"""
Voice Client - Personal Assistant Client
Runs on Mac/PC and handles voice interaction with wake word detection
"""
import asyncio
import json
import wave
import pyaudio
import websockets
import configparser
import os
import sys
import signal
import time
from pathlib import Path
from collections import deque
import numpy as np

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 500  # Adjust based on environment
MIN_SOUND_DURATION = 1.0  # seconds
SILENCE_TIMEOUT = 3.0  # seconds
RLM_TIMEOUT = 10.0  # seconds

class ListeningMode:
    PASSIVE = "PLM"  # Passive Listening Mode
    ACTIVE = "ALM"   # Active Listening Mode
    SPEAKING = "ASM" # Active Speaking Mode
    RESPONSE = "RLM" # Response Listening Mode

class VoiceClient:
    def __init__(self, config_path="voice_client.config"):
        self.config_path = config_path
        self.config = self.load_config()
        
        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
        # State management
        self.mode = ListeningMode.PASSIVE
        self.recording = []
        self.websocket = None
        self.running = True
        
        # Audio buffer for wake word detection
        self.audio_buffer = deque(maxlen=int(RATE * 3))  # 3 second buffer
        
        # Timing
        self.last_sound_time = time.time()
        self.sound_start_time = None
        self.rlm_start_time = None
        
        print(f"[VoiceClient] Initialized with client_id: {self.config['client_id']}")
        print(f"[VoiceClient] Wake word: {self.config['default_wake_words']}")
        print(f"[VoiceClient] Voice server: {self.config['voice_server_url']}")

    def load_config(self):
        """Load configuration from voice_client.config"""
        config = configparser.ConfigParser()
        
        if not os.path.exists(self.config_path):
            print(f"[ERROR] Config file not found: {self.config_path}")
            sys.exit(1)
        
        config.read(self.config_path)
        
        return {
            'client_id': config.get('client', 'client_id'),
            'default_user_id': config.get('client', 'default_user_id'),
            'default_modality': config.get('client', 'default_modality', fallback='voice'),
            'default_wake_words': config.get('client', 'default_wake_words', fallback='computer').split(','),
            'activation_sound': config.get('sounds', 'activation_sound', fallback='activation_sound.wav'),
            'acknowledgement_sound': config.get('sounds', 'acknowledgement_sound', fallback='acknowledgement_sound.wav'),
            'voice_server_url': config.get('server', 'voice_server_url', fallback='ws://10.1.10.20:8585')
        }

    def play_sound(self, sound_file):
        """Play a WAV or MP3 sound file"""
        if not os.path.exists(sound_file):
            print(f"[WARNING] Sound file not found: {sound_file}")
            return
        
        try:
            # Handle MP3 files (like TNG activation.mp3)
            if sound_file.lower().endswith('.mp3'):
                # Use system player for MP3
                import platform
                system = platform.system()
                
                if system == 'Darwin':  # macOS
                    os.system(f'afplay "{sound_file}" &')
                elif system == 'Linux':
                    os.system(f'mpg123 -q "{sound_file}" &')
                elif system == 'Windows':
                    os.system(f'start /min wmplayer "{sound_file}"')
                return
            
            # Handle WAV files
            with wave.open(sound_file, 'rb') as wf:
                stream = self.audio.open(
                    format=self.audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True
                )
                
                data = wf.readframes(CHUNK)
                while data:
                    stream.write(data)
                    data = wf.readframes(CHUNK)
                
                stream.stop_stream()
                stream.close()
        except Exception as e:
            print(f"[ERROR] Failed to play sound {sound_file}: {e}")

    def is_sound(self, data):
        """Check if audio data contains sound above threshold"""
        audio_data = np.frombuffer(data, dtype=np.int16)
        return np.abs(audio_data).mean() > SILENCE_THRESHOLD

    def detect_wake_word(self, audio_chunk):
        """
        Simple wake word detection using audio patterns
        In production, use pvporcupine or similar library
        """
        # This is a placeholder - in production use proper wake word detection
        # For now, we'll use a keyboard trigger for testing
        return False

    def detect_phrase(self, text, phrases):
        """Detect if any phrase is in the text"""
        text_lower = text.lower()
        for phrase in phrases:
            if phrase.lower() in text_lower:
                return True
        return False

    async def start_audio_stream(self):
        """Start the audio input stream"""
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        print("[VoiceClient] Audio stream started")

    async def stop_audio_stream(self):
        """Stop the audio input stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    async def passive_listening_mode(self):
        """PLM - Listen for wake word only"""
        print("[VoiceClient] Entering Passive Listening Mode (PLM)")
        self.mode = ListeningMode.PASSIVE
        
        while self.running and self.mode == ListeningMode.PASSIVE:
            try:
                # Read audio chunk
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.audio_buffer.append(data)
                
                # Check for wake word
                # In production, use pvporcupine or similar
                # For now, check keyboard input in a non-blocking way
                
                # Simple implementation: press Enter to simulate wake word
                # Replace with actual wake word detection
                
                await asyncio.sleep(0.01)
                
            except KeyboardInterrupt:
                break

    async def active_listening_mode(self, wake_word):
        """ALM - Record user command"""
        print("[VoiceClient] Entering Active Listening Mode (ALM)")
        self.mode = ListeningMode.ACTIVE
        self.recording = []
        self.sound_start_time = None
        self.last_sound_time = time.time()
        
        # Play activation sound
        self.play_sound(self.config['activation_sound'])
        
        # Connect to voice server
        try:
            async with websockets.connect(self.config['voice_server_url']) as websocket:
                self.websocket = websocket
                
                # Send session start
                await websocket.send(json.dumps({
                    'type': 'session_start',
                    'client_id': self.config['client_id'],
                    'user_id': self.config['default_user_id'],
                    'wake_word': wake_word
                }))
                
                recording_started = False
                
                while self.mode == ListeningMode.ACTIVE:
                    # Read audio
                    data = self.stream.read(CHUNK, exception_on_overflow=False)
                    
                    # Check for sound
                    has_sound = self.is_sound(data)
                    
                    if has_sound:
                        if self.sound_start_time is None:
                            self.sound_start_time = time.time()
                        self.last_sound_time = time.time()
                        
                        # Check if sound duration >= 1 second
                        if not recording_started:
                            sound_duration = time.time() - self.sound_start_time
                            if sound_duration >= MIN_SOUND_DURATION:
                                recording_started = True
                                print("[VoiceClient] Recording started")
                        
                        if recording_started:
                            self.recording.append(data)
                            # Stream to voice server
                            await websocket.send(data)
                    
                    else:
                        # No sound detected
                        if recording_started:
                            silence_duration = time.time() - self.last_sound_time
                            
                            if silence_duration >= SILENCE_TIMEOUT:
                                # 3 seconds of silence - end recording
                                print("[VoiceClient] Silence detected, ending recording")
                                break
                    
                    await asyncio.sleep(0.01)
                
                # Send end marker
                await websocket.send(json.dumps({'type': 'audio_end'}))
                
                # Play acknowledgement sound
                self.play_sound(self.config['acknowledgement_sound'])
                
                # Enter Response Listening Mode
                await self.response_listening_mode(websocket)
                
        except Exception as e:
            print(f"[ERROR] ALM error: {e}")
            self.mode = ListeningMode.PASSIVE

    async def response_listening_mode(self, websocket):
        """RLM - Listen for follow-up or timeout"""
        print("[VoiceClient] Entering Response Listening Mode (RLM)")
        self.mode = ListeningMode.RESPONSE
        self.rlm_start_time = time.time()
        self.last_sound_time = time.time()
        
        while self.mode == ListeningMode.RESPONSE:
            # Check for timeout
            if time.time() - self.last_sound_time > RLM_TIMEOUT:
                print("[VoiceClient] RLM timeout, returning to PLM")
                self.mode = ListeningMode.PASSIVE
                break
            
            # Listen for audio from voice server
            try:
                message = await asyncio.wait_for(
                    websocket.recv(),
                    timeout=0.1
                )
                
                # Check if it's audio data
                if isinstance(message, bytes):
                    # Audio received - play it
                    await self.active_speaking_mode(message, websocket)
                elif isinstance(message, str):
                    msg_data = json.loads(message)
                    if msg_data.get('type') == 'audio_complete':
                        # Server finished sending audio
                        pass
                
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"[ERROR] RLM error: {e}")
                break
            
            # Check for user speech
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                if self.is_sound(data):
                    self.last_sound_time = time.time()
                    if self.sound_start_time is None:
                        self.sound_start_time = time.time()
                    
                    sound_duration = time.time() - self.sound_start_time
                    if sound_duration >= MIN_SOUND_DURATION:
                        # User started speaking - switch to ALM
                        print("[VoiceClient] Sound detected in RLM, switching to ALM")
                        self.mode = ListeningMode.ACTIVE
                        # Re-enter ALM with current websocket
                        await self.continue_active_listening(websocket)
                        return
                else:
                    self.sound_start_time = None
            
            except Exception as e:
                print(f"[ERROR] Reading audio in RLM: {e}")
            
            await asyncio.sleep(0.01)

    async def continue_active_listening(self, websocket):
        """Continue ALM from RLM"""
        print("[VoiceClient] Continuing Active Listening Mode")
        self.recording = []
        self.sound_start_time = None
        self.last_sound_time = time.time()
        
        recording_started = False
        
        while self.mode == ListeningMode.ACTIVE:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            
            has_sound = self.is_sound(data)
            
            if has_sound:
                if self.sound_start_time is None:
                    self.sound_start_time = time.time()
                self.last_sound_time = time.time()
                
                if not recording_started:
                    sound_duration = time.time() - self.sound_start_time
                    if sound_duration >= MIN_SOUND_DURATION:
                        recording_started = True
                        print("[VoiceClient] Recording started (follow-up)")
                
                if recording_started:
                    self.recording.append(data)
                    await websocket.send(data)
            
            else:
                if recording_started:
                    silence_duration = time.time() - self.last_sound_time
                    if silence_duration >= SILENCE_TIMEOUT:
                        print("[VoiceClient] Silence detected, ending follow-up")
                        break
            
            await asyncio.sleep(0.01)
        
        await websocket.send(json.dumps({'type': 'audio_end'}))
        self.play_sound(self.config['acknowledgement_sound'])
        
        # Back to RLM
        await self.response_listening_mode(websocket)

    async def active_speaking_mode(self, audio_data, websocket):
        """ASM - Play audio from server while listening for 'wake_word stop'"""
        print("[VoiceClient] Entering Active Speaking Mode (ASM)")
        self.mode = ListeningMode.SPEAKING
        
        # TODO: Play audio_data
        # For now, just print
        print(f"[VoiceClient] Playing audio ({len(audio_data)} bytes)")
        
        # While playing, listen for "wake_word stop"
        # This is a simplified implementation
        
        # After playing, return to RLM
        self.mode = ListeningMode.RESPONSE

    async def run(self):
        """Main run loop"""
        print("[VoiceClient] Starting voice client...")
        
        # Start audio stream
        await self.start_audio_stream()
        
        print(f"[VoiceClient] Listening for wake word: {self.config['default_wake_words']}")
        print("[VoiceClient] Press 'w' + Enter to simulate wake word (for testing)")
        print("[VoiceClient] Press 'q' + Enter to quit")
        
        try:
            while self.running:
                if self.mode == ListeningMode.PASSIVE:
                    # Simple keyboard-based wake word for testing
                    # Replace with actual wake word detection
                    await asyncio.sleep(0.1)
                    
                    # Check stdin (non-blocking would be better)
                    # For production, use pvporcupine or similar
                    
                    # Placeholder: use a flag file for testing
                    if os.path.exists('.wake_trigger'):
                        os.remove('.wake_trigger')
                        await self.active_listening_mode('computer')
                
                await asyncio.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n[VoiceClient] Shutting down...")
        
        finally:
            await self.stop_audio_stream()
            self.audio.terminate()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Voice Assistant Client')
    parser.add_argument('--config', default='voice_client.config',
                       help='Path to config file')
    args = parser.parse_args()
    
    client = VoiceClient(config_path=args.config)
    
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("\n[VoiceClient] Exiting...")

if __name__ == '__main__':
    main()
