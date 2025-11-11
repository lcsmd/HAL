"""Use qmclient to compile and start VOICE.LISTENER"""
import sys
import time
import subprocess

sys.path.insert(0, "C:\\QMSYS\\SYSCOM")
import ctypes
qm_dll = ctypes.cdll.LoadLibrary("C:\\QMSYS\\bin\\qmclilib.dll")
import qmclient as qm
qm.__qm_lib = qm_dll
qm.__LoadQMCliLib = lambda: None

print("Connecting to QM with qmclient...")
session = qm.ConnectLocal('HAL')
if not session:
    print("[ERROR] Connection failed")
    sys.exit(1)
print("[OK] Connected to HAL account")

# Execute commands directly via subprocess since qmclient has issues
print("\nCompiling BP VOICE.LISTENER...")
result = subprocess.run("C:\\qmsys\\bin\\qm.exe -aHAL -u lawr -p apgar-66 \"BASIC BP VOICE.LISTENER\"", 
                       shell=True, capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"[WARNING] BASIC returned code {result.returncode}")

time.sleep(2)

print("\nCataloging BP VOICE.LISTENER...")
result = subprocess.run("C:\\qmsys\\bin\\qm.exe -aHAL -u lawr -p apgar-66 \"CATALOG BP VOICE.LISTENER\"", 
                       shell=True, capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"[WARNING] CATALOG returned code {result.returncode}")

time.sleep(2)

print("\nStarting PHANTOM VOICE.LISTENER...")
result = subprocess.run("C:\\qmsys\\bin\\qm.exe -aHAL -u lawr -p apgar-66 \"PHANTOM VOICE.LISTENER\"", 
                       shell=True, capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"[WARNING] PHANTOM returned code {result.returncode}")

qm.Disconnect()

print("\n" + "="*60)
print("Verifying compilation...")
time.sleep(3)

import os
if os.path.exists("C:\\qmsys\\hal\\BP.OUT\\VOICE.LISTENER"):
    info = os.stat("C:\\qmsys\\hal\\BP.OUT\\VOICE.LISTENER")
    print(f"[OK] BP.OUT\\VOICE.LISTENER exists ({info.st_size} bytes)")
else:
    print("[ERROR] BP.OUT\\VOICE.LISTENER not found")

result = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if "LISTENING" in result.stdout:
    print("[OK] Port 8767 is LISTENING")
    print("\nTesting...")
    subprocess.run("python test_qm_direct_newline.py", shell=True, cwd="C:\\qmsys\\hal")
else:
    print("[ERROR] Port 8767 not listening")
