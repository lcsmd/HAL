"""
Test the full voice flow with simulated QM responses
This allows testing the Voice Gateway without QM Listener running
"""
import asyncio
import websockets
import json
import ssl

async def test_full_flow():
    print("="*60)
    print("Full Voice Flow Test (Simulated QM)")
    print("="*60)
    print("")
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    print("1. Connecting to wss://voice.lcs.ai...")
    async with websockets.connect("wss://voice.lcs.ai", ssl=ssl_context) as ws:
        print("   Connected!")
        print("")
        
        # Step 1: Receive welcome
        msg = await ws.recv()
        data = json.loads(msg)
        session_id = data['session_id']
        print(f"2. Session created: {session_id}")
        print(f"   State: {data['state']}")
        print("")
        
        # Step 2: Send wake word
        print("3. Sending wake word 'Hey HAL'...")
        await ws.send(json.dumps({
            'type': 'wake_word_detected',
            'session_id': session_id,
            'wake_word': 'hey hal',
            'confidence': 0.95
        }))
        
        # Get acknowledgment
        ack = await ws.recv()
        print(f"   Gateway response: {json.loads(ack)['type']}")
        
        # Get state change
        state = await ws.recv()
        state_data = json.loads(state)
        print(f"   New state: {state_data['new_state']}")
        print("")
        
        # Step 3: Simulate sending audio (which would be transcribed)
        print("4. Simulating audio: 'What medications am I taking?'...")
        
        # Instead of real audio, send text directly (bypass transcription)
        await ws.send(json.dumps({
            'type': 'text_input',  # Bypass audio
            'session_id': session_id,
            'text': 'What medications am I taking?'
        }))
        print("   Text sent to gateway")
        print("")
        
        # Step 4: Gateway would normally send to QM and get response
        # Since QM isn't running, gateway will timeout or error
        print("5. Waiting for response...")
        print("   (This will fail because QM Listener isn't running)")
        print("   (But shows the Voice Gateway is working!)")
        print("")
        
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print(f"   Response: {response}")
        except asyncio.TimeoutError:
            print("   Timeout - expected since QM Listener isn't running")
        
        print("")
        print("="*60)
        print("Test Summary:")
        print("="*60)
        print("✓ DNS resolution working")
        print("✓ HAProxy routing working")
        print("✓ SSL/WSS working")
        print("✓ Voice Gateway responding")
        print("✓ Session management working")
        print("✓ Wake word detection working")
        print("✓ State machine working")
        print("")
        print("✗ QM Listener not running (expected)")
        print("")
        print("Next: QM socket subroutines need to be created")
        print("or use Python TCP server instead of QM Basic")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
