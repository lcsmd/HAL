#!/usr/bin/env python3
"""Simple HAL Client GUI - Text Only, Always Works"""
import tkinter as tk
from tkinter import scrolledtext
import asyncio
import websockets
import json
import threading
import queue

class SimpleHALClient:
    def __init__(self, root):
        self.root = root
        self.root.title("HAL Voice Assistant - Simple Client")
        self.root.geometry("700x500")
        
        self.server_url = 'ws://10.1.34.103:8768'
        self.session_id = None
        self.ws = None
        self.message_queue = queue.Queue()
        
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
        
        self.text_input = tk.Entry(input_frame, font=('Consolas', 10))
        self.text_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        self.text_input.bind('<Return>', lambda e: self.send_message())
        
        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message, width=10)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Status
        self.status_label = tk.Label(self.root, text="Connecting...", anchor=tk.W)
        self.status_label.pack(padx=10, pady=(0, 5), fill=tk.X)
    
    def add_message(self, msg, prefix=""):
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
            
            self.root.after(0, lambda: self.status_label.config(text=f"Connected! Session: {self.session_id[:8]}..."))
            self.root.after(0, lambda: self.add_message("Connected to HAL. Type your message and press ENTER.", "SYSTEM: "))
            
            # Handle messages
            while True:
                try:
                    # Check for outgoing messages
                    while not self.message_queue.empty():
                        cmd, data = self.message_queue.get_nowait()
                        if cmd == 'send':
                            await self.ws.send(data)
                    
                    # Check for incoming messages
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
            self.root.after(0, lambda: self.status_label.config(text=f"Connection error: {e}"))
            self.root.after(0, lambda: self.add_message(f"ERROR: {e}", "SYSTEM: "))
    
    def process_messages(self):
        self.root.after(100, self.process_messages)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleHALClient(root)
    root.mainloop()
