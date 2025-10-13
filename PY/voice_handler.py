import os
import time
import queue
import threading
import base64
import json
import websockets
import numpy as np
from typing import Optional
from dotenv import load_dotenv
import sounddevice as sd
import pvporcupine
from voice_visualizer import VoiceVisualizer
import asyncio

class VoiceSystem:
    def __init__(self, device_id: Optional[int] = None):
        load_dotenv()
        
        # Server configuration
        self.server_url = os.getenv("HAL_SERVER_URL", "ws://ollama.lcs.ai:8765")
        
        # Initialize wake word detection
        self.porcupine = pvporcupine.create(
            access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
            keywords=["hal"]
        )
        
        # Audio settings
        self.sample_rate = 16000  # Required by Porcupine
        self.frame_duration = 30  # ms
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000)
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.is_listening = False
        
        # Select audio device
        self.device_id = device_id
        if device_id is None:
            # Use default devices
            devices = sd.query_devices()
            for i, dev in enumerate(devices):
                if dev['max_input_channels'] > 0:
                    self.device_id = i
                    break
        
        # Initialize visualizer
        self.visualizer = VoiceVisualizer()
        
    async def connect_to_server(self):
        """Establish WebSocket connection with the server"""
        try:
            self.ws = await websockets.connect(self.server_url)
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
            
    def start_listening(self):
        """Start listening for wake word"""
        self.is_listening = True
        self.visualizer.start()
        self._record_thread = threading.Thread(target=self._record_and_process)
        self._record_thread.start()
        print("Listening for wake word 'hal'...")
        
    def stop_listening(self):
        """Stop listening and cleanup"""
        self.is_listening = False
        self.is_recording = False
        if hasattr(self, '_record_thread'):
            self._record_thread.join()
        self.visualizer.stop()
        
    def _record_and_process(self):
        """Record audio and process for wake word"""
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Error in audio callback: {status}")
            # Update visualizer with audio level
            self.visualizer.update(np.max(np.abs(indata)))
            # Add audio to queue for wake word processing
            self.audio_queue.put(bytes(indata))
            
        with sd.InputStream(
            device=self.device_id,
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            dtype=np.int16,
            callback=audio_callback
        ):
            while self.is_listening:
                try:
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    pcm = np.frombuffer(audio_chunk, dtype=np.int16)
                    
                    # Check for wake word
                    keyword_index = self.porcupine.process(pcm)
                    if keyword_index >= 0:
                        print("Wake word detected! Recording command...")
                        self.visualizer.set_wake_word_detected(True)
                        self._record_command()
                        self.visualizer.set_wake_word_detected(False)
                        
                except queue.Empty:
                    continue
                    
    def _record_command(self):
        """Record command after wake word detection"""
        command_audio = []
        silence_threshold = 0.03
        silence_frames = 0
        max_silence_frames = 30  # About 1 second of silence
        
        def command_callback(indata, frames, time, status):
            if status:
                print(f"Error in command callback: {status}")
            audio_chunk = bytes(indata)
            command_audio.append(audio_chunk)
            # Update visualizer
            level = np.max(np.abs(indata))
            self.visualizer.update(level)
            return level < silence_threshold
            
        with sd.InputStream(
            device=self.device_id,
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            dtype=np.int16,
            callback=command_callback
        ):
            print("Listening for command...")
            while silence_frames < max_silence_frames:
                try:
                    chunk = command_audio[-1]
                    pcm = np.frombuffer(chunk, dtype=np.int16)
                    if np.max(np.abs(pcm)) < silence_threshold:
                        silence_frames += 1
                    else:
                        silence_frames = 0
                    time.sleep(0.01)
                except (IndexError, queue.Empty):
                    continue
                    
        if command_audio:
            # Combine all audio chunks
            audio_data = b"".join(command_audio)
            # Send to server
            asyncio.run(self._process_command(audio_data))
            
    async def _process_command(self, audio_data: bytes):
        """Send audio to server for processing and handle response"""
        try:
            if not hasattr(self, 'ws'):
                if not await self.connect_to_server():
                    print("Failed to connect to server")
                    return
                    
            # Convert audio to base64 for transmission
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Send audio to server
            await self.ws.send(json.dumps({
                "type": "audio",
                "data": audio_b64
            }))
            
            # Wait for response
            response = await self.ws.recv()
            response_data = json.loads(response)
            
            if response_data["type"] == "error":
                print(f"Server error: {response_data['message']}")
            elif response_data["type"] == "audio":
                # Play response audio
                audio_bytes = base64.b64decode(response_data["data"])
                audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
                sd.play(audio_array, self.sample_rate)
                sd.wait()
                
        except Exception as e:
            print(f"Error processing command: {e}")
            
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()
        if hasattr(self, 'ws'):
            asyncio.run(self.ws.close())
