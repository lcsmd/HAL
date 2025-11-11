"""Python client for QM Command Helper"""
import socket
import json
import time

def execute_qm_command(command, timeout=10):
    """Execute a QM command via the helper and return the result"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(('localhost', 8766))
        
        # Send command
        sock.sendall(command.encode() + b'\n')
        
        # Read response
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            # Check if we have complete JSON
            try:
                json.loads(response.decode('utf-8'))
                break
            except:
                continue
        
        sock.close()
        
        # Parse JSON response
        result = json.loads(response.decode('utf-8'))
        return result
    except Exception as e:
        return {"status": -1, "output": str(e), "command": command}

if __name__ == "__main__":
    # Test the helper
    print("Testing QM Command Helper...")
    print("="*60)
    
    # Test 1: List users
    print("\n1. LIST.READU")
    result = execute_qm_command("LIST.READU")
    print(f"Status: {result['status']}")
    print(f"Output:\n{result['output']}")
    
    # Test 2: Count records
    print("\n2. COUNT MEDICATION")
    result = execute_qm_command("COUNT MEDICATION")
    print(f"Status: {result['status']}")
    print(f"Output: {result['output']}")
    
    print("\n" + "="*60)
    print("Helper is working!")
