"""Catalog with LOCAL option and restart PHANTOM"""
import sys
import os
import time
import subprocess

sys.path.insert(0, "C:\\QMSYS\\SYSCOM")

# Load 64-bit QM DLL
import ctypes
print("Loading 64-bit qmclilib.dll...")
qm_dll = ctypes.cdll.LoadLibrary("C:\\QMSYS\\bin\\qmclilib.dll")
print("[OK] Loaded")

# Import and patch qmclient
import qmclient as qm
qm.__qm_lib = qm_dll
def patched_load():
    qm.__qm_lib = qm_dll
qm.__LoadQMCliLib = patched_load
print("[OK] QMClient patched")

# Connect
print("\nConnecting to QM...")
session = qm.ConnectLocal('HAL')
if not session:
    print("[ERROR] Connection failed")
    sys.exit(1)
print("[OK] Connected")

# Kill existing phantom
print("\nKilling existing VOICE.LISTENER phantom...")
try:
    qm.Execute("KILL.PHANTOM 14")
    time.sleep(2)
    print("[OK] Phantom killed")
except:
    print("  (may not have been running)")

# Catalog with LOCAL option
print("\nCataloging with LOCAL option...")
try:
    qm.Execute("LOGTO HAL")
    time.sleep(0.5)
    qm.Execute("CATALOG BP VOICE.LISTENER LOCAL")
    time.sleep(1)
    print("[OK] Cataloged with LOCAL")
except Exception as e:
    print(f"  Error (may be OK): {e}")

# Start new phantom
print("\nStarting PHANTOM VOICE.LISTENER...")
try:
    qm.Execute("PHANTOM VOICE.LISTENER")
    time.sleep(2)
    print("[OK] PHANTOM started")
except Exception as e:
    print(f"  Error (may be OK): {e}")

# Disconnect
qm.Disconnect()
print("[OK] Disconnected")

# Verify
print("\n" + "="*60)
print("Checking if listener started...")
print("="*60)

time.sleep(3)

result = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if result.returncode == 0 and "LISTENING" in result.stdout:
    print("[SUCCESS] Voice Listener is running on port 8767!")
    print(result.stdout)
else:
    print("[WARNING] Port 8767 not listening")

# Check phantoms
result2 = subprocess.run("C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 LIST.READU", 
                        shell=True, capture_output=True, text=True)
print("\nQM Processes:")
for line in result2.stdout.split('\n'):
    if 'VOICE' in line or 'phantom' in line.lower():
        print(line)
