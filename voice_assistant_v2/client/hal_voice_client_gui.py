#!/usr/bin/env python3
"""
HAL Voice Assistant - GUI Client
Supports both text and voice input with persistent TTS toggle
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import asyncio
import threading
import queue
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Try to import voice components (optional)
try:
    import pyaudio
    import webrtcvad
    from openwakeword.model import Model as OWWModel
    VOICE_AVAILABLE = True
except ImportError as e:
    VOICE_AVAILABLE = False
    print(f"Voice components not available - text-only mode: {e}")

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    print("ERROR: websockets package required")
    sys.exit(1)

# Try to import audio playback
try:
    import pygame
    AUDIO_PLAYBACK = True
except ImportError:
    AUDIO_PLAYBACK = False
    print("pygame not available - TTS playback disabled")


class HALVoiceClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HAL Voice Assistant")
        self.root.geometry("800x600")
        
        # Configuration
        self.voice_server_url = os.getenv('VOICE_SERVER_URL', 'ws://10.1.34.103:8768')
        self.wake_word_model = os.getenv('WAKE_WORD', 'hey_jarvis_v0.1')
        
        # State
        self.tts_enabled = False  # TTS toggle state (persists for session)
        self.voice_listening = False
        self.recording = False
        self.ws_connection = None
        
        # Queues for thread communication
        self.message_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        
        # Setup GUI
        self.setup_gui()
        
        # Initialize voice components if available
        if VOICE_AVAILABLE:
            self.init_voice_components()
        
        # Initialize audio playback
        if AUDIO_PLAYBACK:
            pygame.mixer.init()
        
        # Start background threads
        self.start_background_threads()
        
        # Update GUI from message queue
        self.process_messages()
    
    def setup_gui(self):
        """Create the GUI layout"""
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Chat display area
        chat_frame = ttk.LabelFrame(main_frame, text="Conversation", padding="5")
        chat_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=('Arial', 10)
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure text tags for styling
        self.chat_display.tag_config('user', foreground='blue')
        self.chat_display.tag_config('hal', foreground='green')
        self.chat_display.tag_config('system', foreground='gray')
        self.chat_display.tag_config('error', foreground='red')
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Voice toggle button
        self.voice_toggle_btn = ttk.Button(
            input_frame,
            text="🔇 Voice OFF",
            command=self.toggle_tts,
            width=15
        )
        self.voice_toggle_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Text input field
        self.text_input = ttk.Entry(input_frame, font=('Arial', 10))
        self.text_input.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.text_input.bind('<Return>', self.send_text_message)
        
        # Send button
        self.send_btn = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_text_message,
            width=10
        )
        self.send_btn.grid(row=0, column=2)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Status label
        self.status_label = ttk.Label(
            status_frame,
            text="Initializing...",
            font=('Arial', 9),
            foreground='gray'
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Voice status indicator
        self.voice_status_label = ttk.Label(
            status_frame,
            text="",
            font=('Arial', 9),
            foreground='blue'
        )
        self.voice_status_label.grid(row=0, column=1, sticky=tk.E)
        
        # Focus on text input
        self.text_input.focus()
    
    def init_voice_components(self):
        """Initialize voice detection components"""
        try:
            # Initialize OpenWakeWord
            self.oww_model = OWWModel(
                wakeword_models=[self.wake_word_model],
                inference_framework='onnx'
            )
            self.wake_word_name = list(self.oww_model.models.keys())[0]
            
            # Initialize PyAudio
            self.audio = pyaudio.PyAudio()
            
            # Initialize VAD
            self.vad = webrtcvad.Vad(2)  # Aggressiveness 0-3
            
            self.add_system_message(f"Voice ready: Say '{self.wake_word_model.replace('_', ' ').upper()}'")
            
        except Exception as e:
            self.add_system_message(f"Voice initialization failed: {e}", 'error')
            self.oww_model = None
    
    def toggle_tts(self):
        """Toggle TTS on/off"""
        self.tts_enabled = not self.tts_enabled
        
        if self.tts_enabled:
            self.voice_toggle_btn.config(text="🔊 Voice ON")
            self.add_system_message("TTS enabled - responses will be spoken")
        else:
            self.voice_toggle_btn.config(text="🔇 Voice OFF")
            self.add_system_message("TTS disabled - text only")
    
    def send_text_message(self, event=None):
        """Send text message from input field"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        # Clear input
        self.text_input.delete(0, tk.END)
        
        # Display user message
        self.add_user_message(message)
        
        # Send to server
        self.send_to_server(message, input_type='text')
        
        # TTS remains at current state (user's preference)
        # Don't auto-disable
    
    def send_to_server(self, message, input_type='text'):
        """Send message to voice server"""
        print(f"[DEBUG] Queueing message: {message}")
        # Queue the message for async sending
        self.message_queue.put({
            'type': 'send',
            'message': message,
            'input_type': input_type
        })
        print(f"[DEBUG] Message queued, queue size: {self.message_queue.qsize()}")
    
    async def async_send_to_server(self, message, input_type='text'):
        """Async send message to server"""
        try:
            print(f"[DEBUG] async_send_to_server called with: {message}")
            if not self.ws_connection:
                print(f"[DEBUG] Connecting to {self.voice_server_url}")
                # Connect to voice server
                self.ws_connection = await websockets.connect(
                    self.voice_server_url,
                    ping_interval=20,
                    ping_timeout=10
                )
                print("[DEBUG] Connected!")
            
            # Prepare request
            request = {
                'type': 'text_query',
                'text': message,
                'session_id': 'gui_client_' + datetime.now().strftime('%Y%m%d_%H%M%S'),
                'tts_enabled': self.tts_enabled,
                'input_type': input_type
            }
            
            # Send request
            await self.ws_connection.send(json.dumps(request))
            
            # Wait for response
            response = await self.ws_connection.recv()
            response_data = json.loads(response)
            
            # Handle response
            if response_data.get('type') == 'text_response':
                text = response_data.get('text', '')
                self.message_queue.put({
                    'type': 'response',
                    'text': text
                })
                
                # If TTS enabled and audio provided
                if self.tts_enabled and 'audio' in response_data:
                    self.message_queue.put({
                        'type': 'play_audio',
                        'audio': response_data['audio']
                    })
            
            elif response_data.get('type') == 'error':
                error = response_data.get('error', 'Unknown error')
                self.message_queue.put({
                    'type': 'error',
                    'text': error
                })
        
        except Exception as e:
            self.message_queue.put({
                'type': 'error',
                'text': f"Connection error: {e}"
            })
    
    def start_background_threads(self):
        """Start background threads for voice and async operations"""
        # Voice listening thread
        if VOICE_AVAILABLE and self.oww_model:
            voice_thread = threading.Thread(target=self.voice_listening_loop, daemon=True)
            voice_thread.start()
        
        # Async message handler thread
        async_thread = threading.Thread(target=self.async_message_loop, daemon=True)
        async_thread.start()
        
        self.update_status("Ready")
    
    def voice_listening_loop(self):
        """Background thread for voice wake word detection"""
        try:
            # Audio stream parameters
            RATE = 16000
            CHUNK = 1280  # 80ms at 16kHz
            
            # Find an input device that works
            input_device = None
            for i in range(self.audio.get_device_count()):
                try:
                    info = self.audio.get_device_info_by_index(i)
                    if info['maxInputChannels'] > 0:  # Has input
                        input_device = i
                        print(f"[Audio] Using device {i}: {info['name']}")
                        break
                except:
                    continue
            
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                input_device_index=input_device,
                frames_per_buffer=CHUNK
            )
            
            self.message_queue.put({
                'type': 'voice_status',
                'text': '🎤 Listening for wake word...'
            })
            
            while True:
                # Read audio chunk
                audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
                
                # Check for wake word
                if self.oww_model:
                    # Convert to float32 for OpenWakeWord
                    import numpy as np
                    audio_float = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # Get predictions
                    predictions = self.oww_model.predict(audio_float)
                    
                    # Check if wake word detected
                    score = predictions.get(self.wake_word_name, 0)
                    
                    if score > 0.5:  # Detection threshold
                        self.message_queue.put({
                            'type': 'wake_word_detected'
                        })
                        
                        # Record voice command
                        self.record_voice_command(stream, RATE, CHUNK)
        
        except Exception as e:
            self.message_queue.put({
                'type': 'error',
                'text': f"Voice listening error: {e}"
            })
    
    def record_voice_command(self, stream, rate, chunk):
        """Record voice command after wake word"""
        self.message_queue.put({
            'type': 'voice_status',
            'text': '🎤 Recording...'
        })
        
        # Auto-enable TTS when voice input is used
        if not self.tts_enabled:
            self.message_queue.put({'type': 'enable_tts'})
        
        try:
            import numpy as np
            
            frames = []
            silence_chunks = 0
            max_silence_chunks = 30  # 3 seconds at 100ms chunks
            min_record_chunks = 5  # Minimum 0.5 seconds
            
            # Record until silence detected
            while True:
                audio_chunk = stream.read(chunk, exception_on_overflow=False)
                frames.append(audio_chunk)
                
                # Check for silence using VAD
                is_speech = self.vad.is_speech(audio_chunk, rate)
                
                if not is_speech:
                    silence_chunks += 1
                else:
                    silence_chunks = 0
                
                # Stop if enough silence
                if silence_chunks >= max_silence_chunks and len(frames) >= min_record_chunks:
                    break
                
                # Safety limit: 10 seconds max
                if len(frames) > 125:  # ~10 seconds
                    break
            
            self.message_queue.put({
                'type': 'voice_status',
                'text': '⏳ Processing...'
            })
            
            # Convert to audio data
            audio_data = b''.join(frames)
            
            # Send to server
            self.send_voice_to_server(audio_data, rate)
        
        except Exception as e:
            self.message_queue.put({
                'type': 'error',
                'text': f"Recording error: {e}"
            })
        
        finally:
            self.message_queue.put({
                'type': 'voice_status',
                'text': '🎤 Listening for wake word...'
            })
    
    def send_voice_to_server(self, audio_data, rate):
        """Send voice audio to server"""
        # Queue for async sending
        self.message_queue.put({
            'type': 'send_voice',
            'audio': audio_data,
            'rate': rate
        })
    
    async def async_send_voice_to_server(self, audio_data, rate):
        """Async send voice audio to server"""
        try:
            if not self.ws_connection:
                self.ws_connection = await websockets.connect(
                    self.voice_server_url,
                    ping_interval=20,
                    ping_timeout=10
                )
            
            # Send audio data
            request = {
                'type': 'voice_query',
                'session_id': 'gui_client_' + datetime.now().strftime('%Y%m%d_%H%M%S'),
                'sample_rate': rate,
                'tts_enabled': self.tts_enabled
            }
            
            # Send metadata
            await self.ws_connection.send(json.dumps(request))
            
            # Send audio
            await self.ws_connection.send(audio_data)
            
            # Wait for response
            response = await self.ws_connection.recv()
            response_data = json.loads(response)
            
            # Display transcription
            if 'transcription' in response_data:
                self.message_queue.put({
                    'type': 'user_message',
                    'text': response_data['transcription']
                })
            
            # Display response
            if 'text' in response_data:
                self.message_queue.put({
                    'type': 'response',
                    'text': response_data['text']
                })
            
            # Play TTS if enabled
            if self.tts_enabled and 'audio' in response_data:
                self.message_queue.put({
                    'type': 'play_audio',
                    'audio': response_data['audio']
                })
        
        except Exception as e:
            self.message_queue.put({
                'type': 'error',
                'text': f"Voice send error: {e}"
            })
    
    def async_message_loop(self):
        """Background thread to handle async operations"""
        print("[DEBUG] Async message loop started")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while True:
            try:
                # Check for messages to send
                msg = self.message_queue.get(timeout=0.1)
                print(f"[DEBUG] Got message from queue: {msg.get('type')}")
                
                if msg['type'] == 'send':
                    print(f"[DEBUG] Sending text: {msg['message'][:50]}")
                    loop.run_until_complete(
                        self.async_send_to_server(msg['message'], msg['input_type'])
                    )
                    print("[DEBUG] Send complete")
                
                elif msg['type'] == 'send_voice':
                    print("[DEBUG] Sending voice")
                    loop.run_until_complete(
                        self.async_send_voice_to_server(msg['audio'], msg['rate'])
                    )
            
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Async loop error: {e}")
                import traceback
                traceback.print_exc()
    
    def process_messages(self):
        """Process messages from background threads (runs in main thread)"""
        try:
            while True:
                msg = self.message_queue.get_nowait()
                
                if msg['type'] == 'response':
                    self.add_hal_message(msg['text'])
                
                elif msg['type'] == 'user_message':
                    self.add_user_message(msg['text'])
                
                elif msg['type'] == 'error':
                    self.add_system_message(msg['text'], 'error')
                
                elif msg['type'] == 'voice_status':
                    self.update_voice_status(msg['text'])
                
                elif msg['type'] == 'wake_word_detected':
                    self.add_system_message("Wake word detected!")
                
                elif msg['type'] == 'enable_tts':
                    if not self.tts_enabled:
                        self.tts_enabled = True
                        self.voice_toggle_btn.config(text="🔊 Voice ON")
                        self.add_system_message("TTS auto-enabled (voice input)")
                
                elif msg['type'] == 'play_audio':
                    self.play_tts_audio(msg['audio'])
        
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)
    
    def add_user_message(self, text):
        """Add user message to chat display"""
        self.add_to_chat(f"You: {text}\n", 'user')
    
    def add_hal_message(self, text):
        """Add HAL response to chat display"""
        self.add_to_chat(f"HAL: {text}\n", 'hal')
    
    def add_system_message(self, text, tag='system'):
        """Add system message to chat display"""
        self.add_to_chat(f"[{text}]\n", tag)
    
    def add_to_chat(self, text, tag):
        """Add text to chat display with tag"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, text):
        """Update status label"""
        self.status_label.config(text=text)
    
    def update_voice_status(self, text):
        """Update voice status label"""
        self.voice_status_label.config(text=text)
    
    def play_tts_audio(self, audio_data):
        """Play TTS audio"""
        if not AUDIO_PLAYBACK:
            return
        
        try:
            # Save to temporary file and play
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                f.write(audio_data)
                temp_path = f.name
            
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Clean up after playing (in background)
            def cleanup():
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                try:
                    os.remove(temp_path)
                except:
                    pass
            
            threading.Thread(target=cleanup, daemon=True).start()
        
        except Exception as e:
            self.add_system_message(f"Audio playback error: {e}", 'error')


def main():
    """Main entry point"""
    root = tk.Tk()
    app = HALVoiceClientGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
