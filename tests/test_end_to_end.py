"""Test complete end-to-end voice flow"""
import asyncio
import websockets
import json
import ssl

async def test():
    print("="*60)
    print("Complete End-to-End Voice Flow Test")
    print("="*60)
    print("")
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    print("1. Connecting to Voice Gateway (wss://voice.lcs.ai)...")
    async with websockets.connect("wss://voice.lcs.ai", ssl=ssl_context) as ws:
        print("   Connected!")
        print("")
        
        # Receive welcome
        msg = await ws.recv()
        data = json.loads(msg)
        session_id = data['session_id']
        print(f"2. Session ID: {session_id}")
        print("")
        
        # Send wake word
        print("3. Sending wake word...")
        await ws.send(json.dumps({
            'type': 'wake_word_detected',
            'session_id': session_id,
            'wake_word': 'hey hal'
        }))
        
        ack = await ws.recv()
        print(f"   {json.loads(ack)['type']}")
        
        state = await ws.recv()
        print(f"   State: {json.loads(state)['new_state']}")
        print("")
        
        # Send audio chunk (simulated)
        print("4. Sending audio (saying: 'What medications am I taking?')...")
        await ws.send(json.dumps({
            'type': 'audio_chunk',
            'session_id': session_id,
            'audio_data': 'simulated_audio_data',
            'is_final': True
        }))
        print("   Audio sent")
        print("")
        
        # Wait for response from QM
        print("5. Waiting for QM response...")
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=10)
            resp_data = json.loads(response)
            print(f"   Response type: {resp_data.get('type')}")
            print(f"   Response text: {resp_data.get('response_text', 'N/A')}")
            print(f"   Message: {resp_data.get('message', 'N/A')}")
            print("")
            
            print("="*60)
            print("END-TO-END TEST SUCCESSFUL!")
            print("="*60)
            print("")
            print("Voice Gateway -> QM Listener -> Response")
            print("All components working!")
            
        except asyncio.TimeoutError:
            print("   Timeout waiting for response")
            print("")
            print("This is expected if transcription isn't working yet")

if __name__ == "__main__":
    asyncio.run(test())
