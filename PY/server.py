import os
import json
import base64
import asyncio
import websockets
import numpy as np
from typing import Optional
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from elevenlabs import generate, set_api_key
import requests

class HALServer:
    def __init__(self):
        load_dotenv()
        
        # Initialize Whisper model with GPU
        print("Loading Whisper model...")
        self.whisper = WhisperModel("large-v3", device="cuda", compute_type="float16")
        
        # Initialize ElevenLabs
        set_api_key(os.getenv("ELEVENLABS_API_KEY"))
        
        # Initialize Ollama client
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # QM connection settings
        self.qm_host = os.getenv("QM_HOST", "mv1.q.lcs.ai")
        self.qm_port = int(os.getenv("QM_PORT", "4243"))
        
        print("Server initialized and ready!")

    async def handle_client(self, websocket):
        """Handle individual client connection"""
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data["type"] == "audio":
                        # Decode audio from base64
                        audio_bytes = base64.b64decode(data["data"])
                        audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
                        
                        # Convert speech to text
                        segments, _ = self.whisper.transcribe(audio_np, language="en")
                        text = " ".join([s.text for s in segments])
                        print(f"Transcribed: {text}")
                        
                        # Forward transcribed text to QM for processing
                        qm_response = await self.forward_to_qm(text)
                        
                        # Process QM response
                        if qm_response.get("use_llm"):
                            # Process with Ollama using QM-provided prompt
                            llm_response = await self.process_with_ollama(
                                qm_response["prompt"],
                                qm_response.get("model", "mistral")
                            )
                            # Send LLM response back to QM
                            await self.send_llm_response_to_qm(llm_response)
                            response_text = llm_response
                        else:
                            # Use direct QM response
                            response_text = qm_response["response"]
                        
                        print(f"Response: {response_text}")
                        
                        # Convert response to speech
                        audio = generate(
                            text=response_text,
                            voice="Josh",  # or your custom HAL voice
                            model="eleven_monolingual_v1"
                        )
                        
                        # Send audio response back to client
                        response = {
                            "type": "audio",
                            "data": base64.b64encode(audio).decode('utf-8')
                        }
                        await websocket.send(json.dumps(response))
                        
                except Exception as e:
                    error_msg = {
                        "type": "error",
                        "message": str(e)
                    }
                    await websocket.send(json.dumps(error_msg))
                    
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")

    async def forward_to_qm(self, text: str) -> dict:
        """Forward transcribed text to QM for processing"""
        try:
            # Call QM program to process the text
            response = requests.post(
                f"http://{self.qm_host}:{self.qm_port}/hal/process",
                json={
                    "text": text,
                    "timestamp": asyncio.get_event_loop().time()
                }
            )
            return response.json()
        except Exception as e:
            print(f"QM communication error: {e}")
            return {
                "use_llm": True,
                "prompt": text,
                "model": "mistral"
            }

    async def process_with_ollama(self, prompt: str, model: str = "mistral") -> str:
        """Process text with local Ollama instance"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()["response"]
        except Exception as e:
            print(f"Ollama API error: {e}")
            return "I apologize, but I encountered an error processing your request."

    async def send_llm_response_to_qm(self, response: str):
        """Send LLM response back to QM for processing/storage"""
        try:
            requests.post(
                f"http://{self.qm_host}:{self.qm_port}/hal/store_response",
                json={
                    "response": response,
                    "timestamp": asyncio.get_event_loop().time()
                }
            )
        except Exception as e:
            print(f"Error sending response to QM: {e}")

async def main():
    # Initialize server
    server = HALServer()
    
    # Start WebSocket server
    host = "0.0.0.0"  # Listen on all interfaces
    port = 8765
    
    print(f"Starting WebSocket server on {host}:{port}")
    async with websockets.serve(server.handle_client, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
