#!/usr/bin/env python3
"""
HAL Voice Client with Wake Word Detection
Listens for "Hey HAL", records audio, transcribes, and sends to gateway
"""
import asyncio
import websockets
import json
import os
import sys
import wave
import struct
from pathlib import Path

try:
    import pyaudio
    import openwakeword
    from openwakeword.model import Model
except ImportError:
    print("Error: Missing dependencies. Install with:")
    print("  pip install pyaudio openwakeword openai-whisper")
    sys.exit(1)

# Try to import TTS library (optional)
TTS_AVAILABLE = False
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    pass

# Configuration
GATEWAY_URL = os.getenv('HAL_GATEWAY_URL', 'ws://10.1.34.103:8768')
WAKE_WORD_MODEL = os.getenv('WAKE_WORD_MODEL', 'hey_jarvis')  # alexa, hey_jarvis, hey_mycroft, ok_naomi
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')  # tiny, base, small, medium, large

# Audio settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 512
CHANNELS = 1
RECORDING_TIMEOUT = 5  # seconds of silence before stopping

class HALVoiceClient:
    def __init__(self, gateway_url):
        self.gateway_url = gateway_url
        self.session_id = None
        self.websocket = None
        self.oww_model = None
        self.audio = None
        self.stream = None
        
        # Load acknowledgement sound
        self.ack_sound, self.ack_sample_rate, self.ack_channels = self.load_acknowledgement_sound()
        
        # Initialize TTS engine (optional)
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Configure voice (optional)
                voices = self.tts_engine.getProperty('voices')
                # Use first available voice
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
                self.tts_engine.setProperty('rate', 175)  # Speed
            except Exception as e:
                print(f"⚠ TTS not available: {e}")
                self.tts_engine = None
        
    def load_acknowledgement_sound(self):
        """Load TNG activation sound from WAV file or generate beep"""
        # Try to load TNG activation sound
        script_dir = Path(__file__).parent
        sound_file = script_dir / 'ack.wav'
        
        if sound_file.exists():
            try:
                with wave.open(str(sound_file), 'rb') as wf:
                    sample_rate = wf.getframerate()
                    channels = wf.getnchannels()
                    audio_data = wf.readframes(wf.getnframes())
                    print(f"✓ Loaded TNG activation sound ({sample_rate}Hz, {channels}ch)")
                    return audio_data, sample_rate, channels
            except Exception as e:
                print(f"⚠ Could not load TNG sound: {e}, using beep")
        
        # Fallback: Generate a simple beep tone (440Hz for 0.2 seconds)
        duration = 0.2
        frequency = 440
        sample_rate = 44100
        channels = 1
        
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            value = int(32767 * 0.5 * 
                       (1 if (i // (sample_rate // frequency)) % 2 == 0 else -1))
            samples.append(struct.pack('h', value))
        
        return b''.join(samples), sample_rate, channels
    
    def play_acknowledgement(self):
        """Play TNG activation acknowledgement sound"""
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                          channels=self.ack_channels,
                          rate=self.ack_sample_rate,
                          output=True)
            stream.write(self.ack_sound)
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("🔊 [TNG Activation Sound]")
        except Exception as e:
            print(f"⚠ Could not play sound: {e}")
    
    async def connect(self):
        """Connect to HAL gateway"""
        print(f"Connecting to HAL at {self.gateway_url}...")
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            print("✓ Connected to HAL")
            response = await self.websocket.recv()
            data = json.loads(response)
            if data.get('type') == 'connected':
                self.session_id = data.get('session_id')
                print(f"✓ Session: {self.session_id}")
                return True
            return False
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def select_microphone(self):
        """Let user select microphone or find best one"""
        p = pyaudio.PyAudio()
        
        # Get all input devices
        input_devices = []
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append((i, info['name']))
        
        p.terminate()
        
        if not input_devices:
            return None
        
        # Try to auto-select best microphone
        # Prefer: USB mics, webcam mics, then built-in
        preferred_keywords = ['brio', 'usb', 'microphone', 'webcam', 'built-in']
        
        for keyword in preferred_keywords:
            for idx, name in input_devices:
                if keyword.lower() in name.lower():
                    return idx
        
        # Default to first device
        return input_devices[0][0]
    
    def init_wake_word_detection(self):
        """Initialize OpenWakeWord detector (free, no API key needed)"""
        try:
            print("Loading wake word model...")
            
            # Initialize OpenWakeWord model
            self.oww_model = Model(wakeword_models=[WAKE_WORD_MODEL], inference_framework='onnx')
            
            # Get the exact model name (it might have version suffix)
            model_names = list(self.oww_model.models.keys())
            if not model_names:
                raise Exception("No wake word models loaded")
            
            self.wake_word_name = model_names[0]
            
            # Select best microphone
            mic_index = self.select_microphone()
            
            self.audio = pyaudio.PyAudio()
            
            if mic_index is not None:
                mic_info = self.audio.get_device_info_by_index(mic_index)
                print(f"  Using microphone: {mic_info['name']}")
                
                self.stream = self.audio.open(
                    rate=16000,
                    channels=CHANNELS,
                    format=pyaudio.paInt16,
                    input=True,
                    input_device_index=mic_index,
                    frames_per_buffer=1280
                )
            else:
                # Fallback to default
                self.stream = self.audio.open(
                    rate=16000,
                    channels=CHANNELS,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=1280
                )
            
            print(f"✓ Wake word detection initialized")
            print(f"  Model: {WAKE_WORD_MODEL}")
            print(f"  Wake phrase: Say 'Hey Jarvis' or 'Computer'")
            print(f"  (Free, open source, no API key needed)")
            return True
            
        except Exception as e:
            print(f"⚠ Could not initialize wake word: {e}")
            print("  Using keyboard input instead...")
            return False
    
    def listen_for_wake_word(self):
        """Listen for wake word (blocking)"""
        if not self.oww_model or not self.stream:
            return False
        
        try:
            # Read audio chunk (1280 samples = 80ms at 16kHz)
            audio_data = self.stream.read(1280, exception_on_overflow=False)
            audio_array = struct.unpack_from("h" * 1280, audio_data)
            
            # Convert to format OpenWakeWord expects
            import numpy as np
            audio_float = np.array(audio_array, dtype=np.float32) / 32768.0
            
            # Get predictions
            predictions = self.oww_model.predict(audio_float)
            
            # Check if wake word detected (threshold 0.5)
            if predictions[self.wake_word_name] > 0.5:
                return True
            
            return False
            
        except Exception as e:
            print(f"Error detecting wake word: {e}")
            return False
    
    def record_audio(self, duration=5):
        """Record audio for specified duration or until silence"""
        print("🎤 Recording...")
        
        audio_data = []
        p = pyaudio.PyAudio()
        
        # Use same microphone as wake word detection
        mic_index = self.select_microphone()
        
        if mic_index is not None:
            stream = p.open(format=pyaudio.paInt16,
                           channels=CHANNELS,
                           rate=SAMPLE_RATE,
                           input=True,
                           input_device_index=mic_index,
                           frames_per_buffer=CHUNK_SIZE)
        else:
            stream = p.open(format=pyaudio.paInt16,
                           channels=CHANNELS,
                           rate=SAMPLE_RATE,
                           input=True,
                           frames_per_buffer=CHUNK_SIZE)
        
        # Record for specified duration
        for i in range(0, int(SAMPLE_RATE / CHUNK_SIZE * duration)):
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            audio_data.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        print("✓ Recording complete")
        
        # Save to temporary WAV file
        temp_file = "/tmp/hal_query.wav" if sys.platform != "win32" else "hal_query.wav"
        with wave.open(temp_file, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(b''.join(audio_data))
        
        return temp_file
    
    def transcribe_audio(self, audio_file):
        """Transcribe audio using Whisper"""
        print("🔄 Transcribing...")
        try:
            import whisper
            
            # Load model (cached after first load)
            if not hasattr(self, 'whisper_model'):
                print(f"Loading Whisper {WHISPER_MODEL} model...")
                self.whisper_model = whisper.load_model(WHISPER_MODEL)
            
            # Transcribe
            result = self.whisper_model.transcribe(audio_file)
            text = result['text'].strip()
            
            print(f"✓ Transcribed: {text}")
            return text
            
        except Exception as e:
            print(f"✗ Transcription error: {e}")
            return None
    
    def speak_text(self, text):
        """Speak text using TTS (if available)"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"⚠ TTS error: {e}")
        else:
            print("ℹ TTS not available (install with: pip3 install pyttsx3)")
    
    async def send_query(self, text):
        """Send transcribed text to gateway"""
        if not self.websocket:
            print("✗ Not connected to gateway")
            return None
        
        try:
            message = {
                'type': 'text_input',
                'text': text,
                'session_id': self.session_id
            }
            
            await self.websocket.send(json.dumps(message))
            print("📤 Query sent to HAL")
            
            # Wait for response
            while True:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=30.0)
                data = json.loads(response)
                msg_type = data.get('type')
                
                if msg_type == 'processing':
                    print("⏳ HAL is thinking...")
                elif msg_type == 'response':
                    response_text = data.get('text', '')
                    intent = data.get('intent', 'unknown')
                    action = data.get('action', 'unknown')
                    
                    # Display response
                    print(f"\n[HAL Response]")
                    print(f"Intent: {intent}")
                    print(f"Action: {action}")
                    print(f"Text: {response_text}\n")
                    
                    # Speak response
                    self.speak_text(response_text)
                    
                    return response_text
                    
        except asyncio.TimeoutError:
            print("✗ Timeout waiting for response")
            return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    async def voice_loop(self):
        """Main voice interaction loop"""
        print("\n" + "="*60)
        print("HAL Voice Client - Wake Word Mode")
        print("="*60)
        
        use_wake_word = self.init_wake_word_detection()
        
        if use_wake_word:
            print("\nListening for wake word...")
            print("Say: 'Hey Jarvis' or 'Computer'")
            print("(Press Ctrl+C to exit)\n")
        else:
            print("\nKeyboard mode: Press ENTER to start recording")
            print("(Type 'quit' to exit)\n")
        
        try:
            while True:
                if use_wake_word:
                    # Listen for wake word
                    if self.listen_for_wake_word():
                        print("\n👂 Wake word detected!")
                        
                        # Play TNG activation sound
                        self.play_acknowledgement()
                        
                        # Record audio query
                        audio_file = self.record_audio(duration=5)
                        
                        # Transcribe query
                        text = self.transcribe_audio(audio_file)
                        
                        if text:
                            # Send to HAL Voice Gateway
                            await self.send_query(text)
                        
                        print(f"\n" + "="*60)
                        print("Listening for wake word: 'Computer'...")
                        print("="*60)
                else:
                    # Keyboard mode
                    user_input = await asyncio.get_event_loop().run_in_executor(
                        None, input, "Press ENTER to record (or type 'quit'): "
                    )
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    self.play_acknowledgement()
                    audio_file = self.record_audio(duration=5)
                    text = self.transcribe_audio(audio_file)
                    
                    if text:
                        await self.send_query(text)
                
        except KeyboardInterrupt:
            print("\n\nShutting down...")
    
    async def close(self):
        """Cleanup resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        if self.websocket:
            await self.websocket.close()

async def main():
    import argparse
    parser = argparse.ArgumentParser(description='HAL Voice Client')
    parser.add_argument('--url', default=GATEWAY_URL, help='Gateway URL')
    parser.add_argument('--query', help='Single text query (no voice)')
    args = parser.parse_args()
    
    client = HALVoiceClient(args.url)
    
    if not await client.connect():
        return 1
    
    try:
        if args.query:
            # Text mode
            await client.send_query(args.query)
        else:
            # Voice mode
            await client.voice_loop()
    finally:
        await client.close()
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
