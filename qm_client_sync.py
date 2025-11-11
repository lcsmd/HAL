#!/usr/bin/env python
"""Simple synchronous QM client for use in voice gateway"""
import socket
import json

def query_qm(transcription, session_id='unknown'):
    """Send query to QM listener and get response"""
    try:
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        
        # Connect
        s.connect(('localhost', 8767))
        
        # Build message
        message = {
            'transcription': transcription,
            'session_id': session_id
        }
        
        # Send
        msg_bytes = json.dumps(message).encode() + b'\n'
        s.sendall(msg_bytes)
        
        # Receive - read until we get newline or connection closes
        response_data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_data += chunk
            if b'\n' in chunk:
                break
        
        # Close
        s.close()
        
        # Parse and return
        if response_data:
            response_text = response_data.decode()
            return json.loads(response_text)
        else:
            raise Exception("No response from QM")
            
    except json.JSONDecodeError as e:
        # Show actual problematic data
        try:
            bad_data = response_data.decode() if response_data else 'No data'
        except:
            bad_data = str(response_data)
        return {
            'response_text': f'JSON error: {e} | Data: {bad_data[:200]}',
            'action_taken': 'ERROR',
            'status': 'error'
        }
    except Exception as e:
        return {
            'response_text': f'QM connection error: {e}',
            'action_taken': 'ERROR',
            'status': 'error'
        }
