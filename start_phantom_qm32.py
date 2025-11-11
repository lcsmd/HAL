"""Start PHANTOM using 32-bit QMClient"""
import sys
import os

# Use 64-bit QM library for 64-bit Python
sys.path.insert(0, "C:\\QMSYS\\SYSCOM")

print("Attempting to load 64-bit qmclilib...")
print(f"Python: {sys.version}")
print(f"Platform: {sys.platform}")

# Explicitly load 64-bit DLL first
import ctypes
print("Loading 64-bit qmclilib.dll...")
try:
    qm_dll = ctypes.cdll.LoadLibrary("C:\\QMSYS\\bin\\qmclilib.dll")
    print("[OK] Loaded 64-bit qmclilib.dll")
except Exception as e:
    print(f"[ERROR] Cannot load 64-bit DLL: {e}")
    sys.exit(1)

# Now import qmclient - patch it to use our pre-loaded DLL
try:
    import qmclient as qm
    # Set the module-level __qm_lib variable to our pre-loaded DLL
    qm.__qm_lib = qm_dll
    # Replace the __LoadQMCliLib function to use our DLL
    def patched_load():
        qm.__qm_lib = qm_dll
    qm.__LoadQMCliLib = patched_load
    print("[OK] QMClient patched with 64-bit DLL")
except Exception as e:
    print(f"[ERROR] Failed to load QMClient: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nConnecting to QM...")
try:
    print("Trying qm.ConnectLocal...")
    session = qm.ConnectLocal('HAL')
    print(f"ConnectLocal returned: {session}")
    
    # Check QM error
    status = qm.Status()
    print(f"QM Status: {status}")
    if status != 0:
        error = qm.Error()
        print(f"QM Error: {error}")
    
    if not session:
        print("[ERROR] Connection failed - trying Connect to localhost...")
        session = qm.Connect('localhost', 4243, 'HAL', 'lawr', 'apgar-66')
        print(f"Connect returned: {session}")
        status = qm.Status()
        if status != 0:
            error = qm.Error()
            print(f"QM Error: {error}")
        if not session:
            print("[ERROR] Both ConnectLocal and Connect failed")
            sys.exit(1)
    
    print("[OK] Connected to QM")
except Exception as e:
    print(f"[ERROR] Connection error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nExecuting commands...")
commands = [
    "LOGTO HAL",
    "PHANTOM VOICE.LISTENER"
]

for cmd in commands:
    print(f"\nExecuting: {cmd}")
    try:
        qm.Execute(cmd)
        
        # Read output - ReadLine doesn't exist, try different approach
        import time
        time.sleep(0.5)
        
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()

print("\nDisconnecting...")
try:
    qm.Disconnect()
    print("[OK] Disconnected")
except Exception as e:
    print(f"  Disconnect error: {e}")

print("\n" + "="*60)
print("Checking if listener started...")
print("="*60)

import time
import subprocess
time.sleep(3)

result = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if result.returncode == 0 and "LISTENING" in result.stdout:
    print("[SUCCESS] Voice Listener is running on port 8767!")
    print(result.stdout)
else:
    print("[WARNING] Port 8767 not listening")
    print("Checking QM processes...")
    result2 = subprocess.run("C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 LIST.READU", 
                            shell=True, capture_output=True, text=True)
    print(result2.stdout)
