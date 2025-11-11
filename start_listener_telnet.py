"""Start Voice Listener using raw socket connection to QM"""
import socket
import time

def send_qm_command(sock, cmd):
    """Send a command to QM via telnet protocol"""
    print(f"Sending: {cmd}")
    sock.sendall(cmd.encode('utf-8') + b'\r\n')
    time.sleep(0.5)
    
    # Try to read response
    try:
        sock.settimeout(2)
        response = sock.recv(4096).decode('utf-8', errors='ignore')
        if response:
            print(f"Response: {response[:200]}")
    except socket.timeout:
        pass
    sock.settimeout(None)

def main():
    print("Connecting to QM on localhost:4243...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 4243))
        print("Connected!")
        time.sleep(1)
        
        # Read initial greeting
        try:
            sock.settimeout(2)
            greeting = sock.recv(4096).decode('utf-8', errors='ignore')
            print(f"Greeting: {greeting[:200]}")
        except socket.timeout:
            print("No greeting received")
        sock.settimeout(None)
        
        # Send account name
        print("\nSending account: HAL")
        sock.sendall(b'HAL\r\n')
        time.sleep(1)
        
        # Read response
        try:
            sock.settimeout(2)
            resp = sock.recv(4096).decode('utf-8', errors='ignore')
            print(f"Response: {resp[:200]}")
        except socket.timeout:
            pass
        sock.settimeout(None)
        
        # Send username (blank)
        print("\nSending blank username")
        sock.sendall(b'\r\n')
        time.sleep(1)
        
        # Read response
        try:
            sock.settimeout(2)
            resp = sock.recv(4096).decode('utf-8', errors='ignore')
            print(f"Response: {resp[:200]}")
        except socket.timeout:
            pass
        sock.settimeout(None)
        
        # Send password (blank)
        print("\nSending blank password")
        sock.sendall(b'\r\n')
        time.sleep(1)
        
        # Read prompt
        try:
            sock.settimeout(2)
            resp = sock.recv(4096).decode('utf-8', errors='ignore')
            print(f"Response: {resp[:200]}")
        except socket.timeout:
            pass
        sock.settimeout(None)
        
        print("\n" + "="*60)
        print("Executing QM commands...")
        print("="*60 + "\n")
        
        # Execute commands
        commands = [
            "LOGTO HAL",
            "BASIC BP VOICE.LISTENER",
            "CATALOG BP VOICE.LISTENER",
            "PHANTOM BP VOICE.LISTENER"
        ]
        
        for cmd in commands:
            send_qm_command(sock, cmd)
            time.sleep(2)
        
        # Exit
        print("\nExiting QM...")
        sock.sendall(b'QUIT\r\n')
        time.sleep(1)
        
        sock.close()
        print("\n" + "="*60)
        print("Commands sent! Check if listener is running:")
        print("  netstat -an | findstr :8767")
        print("="*60)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
