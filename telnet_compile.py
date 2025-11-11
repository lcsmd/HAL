"""Use socket to connect to QM and compile VOICE.LISTENER"""
import socket
import time

# Telnet protocol constants
IAC = bytes([255])  # Interpret As Command
DONT = bytes([254])
DO = bytes([253])
WONT = bytes([252])
WILL = bytes([251])

def send_command(sock, cmd):
    print(f"\n>>> {cmd}")
    sock.sendall(cmd.encode() + b"\r\n")
    time.sleep(2)
    try:
        response = sock.recv(8192).decode('utf-8', errors='ignore')
        print(response)
        return response
    except:
        return ""

def read_until(sock, prompt, timeout=5):
    """Read until a prompt is found, filtering telnet negotiation"""
    data = b""
    sock.settimeout(timeout)
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            chunk = sock.recv(1024)
            if not chunk:
                break
            
            # Filter out telnet IAC negotiation sequences
            i = 0
            while i < len(chunk):
                if chunk[i:i+1] == IAC:
                    # Skip IAC command (3 bytes: IAC, command, option)
                    if i + 2 < len(chunk):
                        # Send back WONT/DONT responses
                        if chunk[i+1:i+2] in [DO, DONT]:
                            sock.sendall(IAC + WONT + chunk[i+2:i+3])
                        elif chunk[i+1:i+2] in [WILL, WONT]:
                            sock.sendall(IAC + DONT + chunk[i+2:i+3])
                        i += 3
                    else:
                        i += 1
                else:
                    data += chunk[i:i+1]
                    i += 1
            
            text = data.decode('utf-8', errors='ignore')
            if prompt in text or ">" in text:
                break
        except socket.timeout:
            break
    return data.decode('utf-8', errors='ignore')

print("Connecting to QM via telnet (port 4243)...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 4243))

# Read initial banner and handle telnet negotiation
time.sleep(0.5)
banner = read_until(sock, "Username")
print(f"Banner: {banner}")

# Send username
print("\nSending username: lawr")
sock.sendall(b"lawr\r")
response = read_until(sock, "Password")
print(f"Username response: {response}")

# Send password
print("\nSending password: apgar-66")
sock.sendall(b"apgar-66\r")
response = read_until(sock, "Account")
print(f"Password response: {response}")

# Send account
print("\nSending account: HAL")
sock.sendall(b"HAL\r")
time.sleep(1)
response = read_until(sock, ">")
print(f"Account response: {response}")

# Now execute commands (already in HAL account from login)
send_command(sock, "BASIC BP VOICE.LISTENER")
send_command(sock, "CATALOG BP VOICE.LISTENER")
send_command(sock, "PHANTOM VOICE.LISTENER")
send_command(sock, "QUIT")

sock.close()
print("\n" + "="*60)
print("Session closed")
