"""
Home Assistant to HAL Voice Interface Relay
Simple HTTP server that bridges Home Assistant to HAL Voice Gateway
"""
import asyncio
import websockets
from aiohttp import web
import json
import ssl
from datetime import datetime

class HALRelay:
    def __init__(self, hal_url="wss://voice.lcs.ai", port=8766):
        self.hal_url = hal_url
        self.port = port
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
    async def handle_ask(self, request):
        """Handle /ask endpoint from Home Assistant"""
        try:
            data = await request.json()
            text = data.get('text', '')
            
            if not text:
                return web.json_response(
                    {"error": "No text provided"},
                    status=400
                )
            
            print(f"[{datetime.now()}] Received from HA: {text}")
            
            # Connect to HAL and get response
            response = await self.ask_hal(text)
            
            print(f"[{datetime.now()}] Sending to HA: {response}")
            
            return web.json_response(response)
            
        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")
            return web.json_response(
                {"error": str(e)},
                status=500
            )
    
    async def handle_health(self, request):
        """Health check endpoint"""
        return web.json_response({
            "status": "ok",
            "service": "HAL Relay",
            "hal_url": self.hal_url
        })
    
    async def ask_hal(self, text):
        """Send question to HAL and get response"""
        try:
            async with websockets.connect(self.hal_url, ssl=self.ssl_context) as ws:
                # Receive welcome message
                welcome = await ws.recv()
                session_data = json.loads(welcome)
                session_id = session_data.get('session_id')
                
                print(f"[{datetime.now()}] Connected to HAL, session: {session_id}")
                
                # Send wake word
                await ws.send(json.dumps({
                    "type": "wake_word_detected",
                    "session_id": session_id,
                    "wake_word": "hey hal",
                    "confidence": 1.0,
                    "timestamp": datetime.now().isoformat()
                }))
                
                # Receive acknowledgment
                ack = await ws.recv()
                print(f"[{datetime.now()}] Wake word ack: {ack}")
                
                # Receive state change
                state = await ws.recv()
                print(f"[{datetime.now()}] State change: {state}")
                
                # Send the actual text/question
                # For now, we'll send it as a simulated transcription
                await ws.send(json.dumps({
                    "type": "transcription",
                    "session_id": session_id,
                    "text": text,
                    "timestamp": datetime.now().isoformat()
                }))
                
                # Wait for response from HAL
                response_msg = await asyncio.wait_for(ws.recv(), timeout=15)
                response_data = json.loads(response_msg)
                
                return {
                    "status": "success",
                    "response": response_data.get('response_text', ''),
                    "intent": response_data.get('intent', 'unknown'),
                    "session_id": session_id
                }
                
        except asyncio.TimeoutError:
            return {
                "status": "error",
                "error": "Timeout waiting for HAL response"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def start(self):
        """Start the HTTP server"""
        app = web.Application()
        
        # Add routes
        app.router.add_post('/ask', self.handle_ask)
        app.router.add_get('/health', self.handle_health)
        
        # Start server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        
        print("=" * 60)
        print(f"HAL Relay Server Started")
        print("=" * 60)
        print(f"Listening on: http://0.0.0.0:{self.port}")
        print(f"HAL Gateway: {self.hal_url}")
        print("")
        print("Endpoints:")
        print(f"  POST /ask    - Send question to HAL")
        print(f"  GET  /health - Health check")
        print("")
        print("Example usage:")
        print('  curl -X POST http://localhost:8766/ask \\')
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"text":"What medications am I taking?"}\'')
        print("")
        print("Home Assistant configuration:")
        print("  rest_command:")
        print("    ask_hal:")
        print("      url: http://10.1.34.103:8766/ask")
        print("      method: POST")
        print('      payload: \'{"text": "{{ text }}"}\'')
        print("      content_type: application/json")
        print("")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        # Keep running
        await asyncio.Event().wait()

def main():
    """Main entry point"""
    relay = HALRelay()
    
    try:
        asyncio.run(relay.start())
    except KeyboardInterrupt:
        print("\nShutting down HAL Relay...")

if __name__ == "__main__":
    main()
