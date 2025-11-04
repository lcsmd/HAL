"""Test voice.lcs.ai through HAProxy"""
import asyncio
import websockets
import json
import ssl

async def test():
    print("Testing wss://voice.lcs.ai...")
    print("")
    
    # Create SSL context that doesn't verify self-signed certs
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        async with websockets.connect("wss://voice.lcs.ai", ssl=ssl_context) as ws:
            print("[OK] Connected to voice.lcs.ai!")
            print("")
            
            # Receive welcome message
            msg = await ws.recv()
            print(f"Received: {msg}")
            print("")
            
            data = json.loads(msg)
            session_id = data.get('session_id')
            print(f"Session ID: {session_id}")
            print("")
            
            # Send wake word
            wake_msg = {
                'type': 'wake_word_detected',
                'session_id': session_id,
                'wake_word': 'hey hal',
                'confidence': 0.95
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
            
            print("")
            print("=" * 60)
            print("SUCCESS! voice.lcs.ai is working through HAProxy!")
            print("=" * 60)
            
    except Exception as e:
        print(f"ERROR: {e}")
        print("")
        print("Check:")
        print("1. Voice Gateway is running: Get-NetTCPConnection -LocalPort 8765")
        print("2. HAProxy backend is up")

if __name__ == "__main__":
    asyncio.run(test())
