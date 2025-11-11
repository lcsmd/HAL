#!/usr/bin/env python3
"""
HAL Voice Client for Mac
Connects to HAL Voice Gateway via WebSocket
"""

import asyncio
import websockets
import json
import sys
import os
from datetime import datetime

# Configuration
GATEWAY_URL = os.getenv('VOICE_GATEWAY_URL', 'ws://localhost:8768')

class HALClient:
    def __init__(self, gateway_url):
        self.gateway_url = gateway_url
        self.session_id = None
        self.websocket = None
        
    async def connect(self):
        """Connect to voice gateway"""
        print(f"Connecting to HAL at {self.gateway_url}...")
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            print("✓ Connected to HAL Voice Gateway")
            
            # Wait for initial state message
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data.get('type') == 'state':
                self.session_id = data.get('session_id')
                print(f"✓ Session ID: {self.session_id}")
                print(f"✓ State: {data.get('state')}")
                return True
            
            return False
            
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    async def send_text_query(self, text):
        """Send text query to HAL"""
        if not self.websocket:
            print("Not connected!")
            return None
            
        try:
            # Send text input message
            message = {
                'type': 'text_input',
                'text': text
            }
            
            await self.websocket.send(json.dumps(message))
            
            # Wait for responses
            response_text = None
            
            while True:
                response = await asyncio.wait_for(
                    self.websocket.recv(),
                    timeout=10.0
                )
                
                data = json.loads(response)
                msg_type = data.get('type')
                
                if msg_type == 'response':
                    response_text = data.get('text', '')
                    intent = data.get('intent', 'unknown')
                    action = data.get('action', 'unknown')
                    
                    print(f"\n[HAL Response]")
                    print(f"Intent: {intent}")
                    print(f"Action: {action}")
                    print(f"Text: {response_text}")
                    
                    return response_text
                    
                elif msg_type == 'processing':
                    print("  (HAL is thinking...)")
                    
                elif msg_type == 'error':
                    print(f"✗ Error: {data.get('message')}")
                    return None
                    
        except asyncio.TimeoutError:
            print("✗ Timeout waiting for response")
            return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    async def interactive_text_mode(self):
        """Interactive text chat with HAL"""
        print("\n" + "="*60)
        print("HAL Voice Client - Text Mode")
        print("="*60)
        print("Type your queries (or 'quit' to exit)")
        print()
        
        while True:
            try:
                # Get user input
                query = input("You: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                # Send to HAL
                await self.send_text_query(query)
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    async def close(self):
        """Close connection"""
        if self.websocket:
            await self.websocket.close()
            print("✓ Disconnected")

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HAL Voice Client for Mac')
    parser.add_argument('--url', default=GATEWAY_URL, help='Voice Gateway URL')
    parser.add_argument('--text', action='store_true', help='Text input mode')
    parser.add_argument('--query', help='Single query mode')
    
    args = parser.parse_args()
    
    # Create client
    client = HALClient(args.url)
    
    # Connect
    if not await client.connect():
        print("Failed to connect")
        return 1
    
    try:
        if args.query:
            # Single query mode
            await client.send_text_query(args.query)
        else:
            # Interactive mode
            await client.interactive_text_mode()
    finally:
        await client.close()
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(0)
