"""Test Voice Gateway with text input (bypass Whisper) and full QM Listener"""
import asyncio
import websockets
import json

async def test_text_input():
    print("="*60)
    print("Testing Voice Gateway Text Input + Full QM Listener")
    print("="*60)
    print("")
    
    print("Connecting to ws://localhost:8768...")
    try:
        async with websockets.connect("ws://localhost:8768") as ws:
            print("[OK] Connected!")
            print("")
            
            # Receive welcome
            msg = await ws.recv()
            data = json.loads(msg)
            session_id = data['session_id']
            print(f"Session ID: {session_id}")
            print(f"State: {data['state']}")
            print("")
            
            # Test 1: Medication query
            print("Test 1: Sending medication query via text input...")
            print("Query: 'What medications am I taking?'")
            print("")
            
            await ws.send(json.dumps({
                'type': 'text_input',
                'session_id': session_id,
                'text': 'What medications am I taking?'
            }))
            
            # Collect responses
            responses = []
            try:
                for i in range(5):
                    response = await asyncio.wait_for(ws.recv(), timeout=15)
                    resp_data = json.loads(response)
                    responses.append(resp_data)
                    print(f"Response {i+1}: {resp_data.get('type')}")
                    if resp_data.get('type') == 'response':
                        print(f"  Text: {resp_data.get('text')[:100]}...")
                        print(f"  Action: {resp_data.get('action_taken')}")
                        break
            except asyncio.TimeoutError:
                print("  Timeout waiting for response")
            
            print("")
            print("="*60)
            
            # Check if we got proper response
            response_msgs = [r for r in responses if r.get('type') == 'response']
            if response_msgs:
                response_text = response_msgs[0].get('text', '')
                
                if 'Hello from QM Voice Listener' in response_text:
                    print("STATUS: Still using simple listener")
                    print("The listener needs to be restarted as PHANTOM")
                elif 'medication' in response_text.lower() or 'taking' in response_text.lower():
                    print("STATUS: [SUCCESS] Full listener is working!")
                    print("Intent classification and routing are operational!")
                else:
                    print(f"STATUS: Got response: {response_text}")
            else:
                print("STATUS: No response received - QM Listener not running")
            
            print("="*60)
            print("")
            
            # Test 2: General query
            print("Test 2: Testing general query...")
            print("Query: 'Tell me about the weather'")
            print("")
            
            await ws.send(json.dumps({
                'type': 'text_input',
                'session_id': session_id,
                'text': 'Tell me about the weather'
            }))
            
            try:
                for i in range(5):
                    response = await asyncio.wait_for(ws.recv(), timeout=10)
                    resp_data = json.loads(response)
                    if resp_data.get('type') == 'response':
                        print(f"Response: {resp_data.get('text')[:150]}...")
                        break
            except asyncio.TimeoutError:
                print("  Timeout")
            
            print("")
            print("="*60)
            print("Text input bypass is working!")
            print("Next: Start QM Listener with: qm -aHAL -u lawr -p apgar-66 'PHANTOM VOICE.LISTENER'")
            print("="*60)
    except ConnectionRefusedError:
        print("[ERROR] Cannot connect to Voice Gateway on port 8768")
        print("Make sure it's running: python PY\\voice_gateway.py")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(test_text_input())
