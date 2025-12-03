#!/usr/bin/env python3
"""
HAL Client - Hybrid Mode
Text always works, voice optional (graceful degradation)
"""

import tkinter as tk
from tkinter import scrolledtext
import asyncio
import websockets
import json
import threading
import queue
from datetime import datetime

class HALHybridClient:
    def __init__(self, root):
        self.root = root
        self.root.title("HAL Voice Assistant")
        self.root.geometry("700x500")
        
        self.server_url = 'ws://10.1.34.103:8768'
        self.session_id = None
        self.ws = None
        self.message_queue = queue.Queue()
        
        # Voice components (optional)
        self.voice_ready = False
        try:
            import pyaudio
            import openwakeword
            import webrtcvad
            from openwakeword.model import Model as OWWModel
            
            self.pyaudio = pyaudio
            self.oww_model = OWWModel(wakeword_models=['hey_jarvis_v0.1'], inference_framework='onnx')
            self.vad = webrtcvad.Vad(3)
            self.voice_ready = True
            print("[OK] Voice components initialized")
        except Exception as e:
            print(f"[WARN] Voice not available: {e}")
            self.voice_ready = False
        
        self.setup_gui()
        self.start_connection()
        self.process_messages()
    
    def setup_gui(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=80, height=25, font=('Consolas', 10)
        )
        self.chat_display.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        # Voice button (if available)
        if self.voice_ready:
            self.voice_btn = tk.Button(
                input_frame, text="🎤 Voice", 
                command=self.toggle_voice, width=10
            )
            self.voice_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.text_input = tk.Entry(input_frame, font=('Consolas', 10))
        self.text_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        self.text_input.bind('<Return>', lambda e: self.send_message())
        
        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message, width=10)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Status
        self.status_label = tk.Label(
            self.root, 
            text="Voice: Ready to say 'Hey Jarvis'" if self.voice_ready else "Text mode only", 
            anchor=tk.W
        )
        self.status_label.pack(padx=10, pady=(0, 5), fill=tk.X)
    
    def toggle_voice(self):
        # TODO: Implement voice toggle
        pass
    
    def add_message(self, msg, prefix="", color="black"):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{prefix}{msg}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        text = self.text_input.get().strip()
        if not text:
            return
        
        self.text_input.delete(0, tk.END)
        self.add_message(text, "YOU: ")
        
        if self.ws and self.session_id:
            query = {
                'type': 'text_input',
                'text': text,
                'session_id': self.session_id
            }
            self.message_queue.put(('send', json.dumps(query)))
    
    def start_connection(self):
        def run_async():
            asyncio.run(self.connection_loop())
        
        thread = threading.Thread(target=run_async, daemon=True)
        thread.start()
    
    async def connection_loop(self):
        try:
            self.ws = await websockets.connect(self.server_url)
            
            # Get initial message
            msg = await self.ws.recv()
            data = json.loads(msg)
            self.session_id = data.get('session_id')
            
            self.root.after(0, lambda: self.status_label.config(
                text=f"Connected! {'Say Hey Jarvis or type' if self.voice_ready else 'Type your message'}"
            ))
            self.root.after(0, lambda: self.add_message("Connected to HAL", "SYSTEM: "))
            
            # Message loop
            while True:
                try:
                    # Check outgoing
                    while not self.message_queue.empty():
                        cmd, data = self.message_queue.get_nowait()
                        if cmd == 'send':
                            await self.ws.send(data)
                    
                    # Check incoming
                    msg = await asyncio.wait_for(self.ws.recv(), timeout=0.1)
                    resp = json.loads(msg)
                    
                    if resp.get('type') == 'response':
                        text = resp.get('text', 'No response')
                        self.root.after(0, lambda t=text: self.add_message(t, "HAL: "))
                    elif resp.get('type') == 'processing':
                        self.root.after(0, lambda: self.status_label.config(text="HAL is thinking..."))
                    
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    break
        
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"Error: {e}"))
            self.root.after(0, lambda: self.add_message(f"Connection error: {e}", "ERROR: "))
    
    def process_messages(self):
        self.root.after(100, self.process_messages)

if __name__ == "__main__":
    root = tk.Tk()
    app = HALHybridClient(root)
    root.mainloop()
