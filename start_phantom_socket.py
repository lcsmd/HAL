"""Start PHANTOM via direct socket connection to QM"""
import socket
import time
import struct

def qm_connect(host='localhost', port=4243, account='HAL', username='lawr', password='apgar-66'):
    """Connect to QM server"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to QM on {host}:{port}")
    
    # QM protocol handshake
    # Read greeting
    greeting = sock.recv(1024)
    print(f"Greeting: {greeting.decode('utf-8', errors='ignore')[:50]}")
    
    # Send account
    sock.sendall((account + '\r\n').encode('utf-8'))
    time.sleep(0.5)
    response = sock.recv(1024)
    print(f"Account response: {response.decode('utf-8', errors='ignore')[:50]}")
    
    # Send username
    sock.sendall((username + '\r\n').encode('utf-8'))
    time.sleep(0.5)
    response = sock.recv(1024)
    print(f"Username response: {response.decode('utf-8', errors='ignore')[:50]}")
    
    # Send password
    sock.sendall((password + '\r\n').encode('utf-8'))
    time.sleep(0.5)
    response = sock.recv(1024)
    print(f"Password response: {response.decode('utf-8', errors='ignore')[:100]}")
    
    return sock

def qm_execute(sock, command):
    """Execute a QM command"""
    print(f"\nExecuting: {command}")
    sock.sendall((command + '\r\n').encode('utf-8'))
    time.sleep(1.0)
    
    # Try to read response
    sock.settimeout(2.0)
    try:
        response = sock.recv(8192)
        if response:
            print(f"Response: {response.decode('utf-8', errors='ignore')[:500]}")
        return response
    except socket.timeout:
        print("(no immediate response - normal for PHANTOM)")
        return b''
    finally:
        sock.settimeout(None)

def main():
    print("="*60)
    print("Starting QM Voice Listener via Socket")
    print("="*60)
    print()
    
    try:
        # Connect to QM
        sock = qm_connect()
        time.sleep(1)
        
        # Execute commands
        qm_execute(sock, "LOGTO HAL")
        time.sleep(0.5)
        
        qm_execute(sock, "PHANTOM VOICE.LISTENER")
        time.sleep(2)
        
        # Quit
        qm_execute(sock, "QUIT")
        
        sock.close()
        print("\n" + "="*60)
        print("Commands sent successfully")
        print("="*60)
        
        # Check if listening
        print("\nChecking port 8767...")
        time.sleep(2)
        
        import subprocess
        result = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
        if result.returncode == 0 and "LISTENING" in result.stdout:
            print("✅ SUCCESS! Voice Listener is running on port 8767")
            print(result.stdout)
            return True
        else:
            print("⚠️ Port 8767 not listening yet - may need a moment to start")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
