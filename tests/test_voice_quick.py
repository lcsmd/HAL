"""Quick test of Voice Gateway"""
import asyncio
import websockets
import json

async def test():
    print("Connecting to ws://localhost:8765...")
    async with websockets.connect("ws://localhost:8765") as ws:
        print("Connected!")
        
        # Receive welcome message
        msg = await ws.recv()
        print(f"Received: {msg}")
        
        data = json.loads(msg)
        session_id = data.get('session_id')
        print(f"Session ID: {session_id}")
        
        # Send wake word
        wake_msg = {
            'type': 'wake_word_detected',
            'session_id': session_id,
            'wake_word': 'hey hal',
            'confidence': 0.95,
            'timestamp': '2025-10-30T10:00:00Z'
        }
        
        print("Sending wake word...")
        await ws.send(json.dumps(wake_msg))
        
        # Get responses
        for i in range(3):
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=2)
                print(f"Response {i+1}: {response}")
            except asyncio.TimeoutError:
                break

if __name__ == "__main__":
    asyncio.run(test())
