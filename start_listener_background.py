"""Start QM Voice Listener in background using subprocess"""
import subprocess
import time
import socket
import sys

def check_port(port=8767, timeout=1):
    """Check if port is listening"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

print("Starting QM Voice Listener in background...")
print()

# Start QM process that will run the listener
# The process will stay alive as a PHANTOM
proc = subprocess.Popen(
    ['C:\\qmsys\\bin\\qm.exe', 'HAL', 'BP', 'VOICE.LISTENER'],
    creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.DETACHED_PROCESS
)

print(f"Started QM process with PID: {proc.pid}")
print("Waiting for listener to start...")
print()

# Wait up to 10 seconds
for i in range(10):
    time.sleep(1)
    if check_port(8767):
        print("[SUCCESS] Voice Listener is running on port 8767!")
        print()
        # Test it
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(('localhost', 8767))
            test_msg = '{"type":"test","transcription":"hello"}'
            sock.sendall(test_msg.encode())
            response = sock.recv(4096)
            sock.close()
            print(f"Test response: {response[:80].decode()}...")
            print()
            print("="*60)
            print("QM Voice Listener is OPERATIONAL!")
            print("="*60)
            sys.exit(0)
        except Exception as e:
            print(f"Connection test failed: {e}")
            print("But port is listening.")
            sys.exit(0)
    print(f"  Waiting... ({i+1}/10)")

print()
print("[WARNING] Listener did not start within 10 seconds")
print(f"QM process PID: {proc.pid}")
print("Check manually with: netstat -an | findstr 8767")
