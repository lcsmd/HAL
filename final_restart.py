"""Kill all, catalog with LOCAL properly, start ONE phantom"""
import sys
import time
import subprocess

sys.path.insert(0, "C:\\QMSYS\\SYSCOM")
import ctypes
qm_dll = ctypes.cdll.LoadLibrary("C:\\QMSYS\\bin\\qmclilib.dll")
import qmclient as qm
qm.__qm_lib = qm_dll
qm.__LoadQMCliLib = lambda: None

session = qm.ConnectLocal('HAL')
if not session:
    print("[ERROR] Connection failed")
    sys.exit(1)
print("[OK] Connected to QM")

# Logout ALL phantoms using LOGOUT command 
print("\nLogging out ALL VOICE.LISTENER phantoms...")
for uid in [14, 16, 17, 18, 26, 28]:
    try:
        qm.Execute(f"LOGOUT {uid}")
        print(f"  Logged out UID {uid}")
        time.sleep(0.3)
    except:
        pass

time.sleep(2)

# Use FIXED version
print("\nCopying VOICE.LISTENER.FIXED to VOICE.LISTENER...")
import shutil
shutil.copy("C:\\qmsys\\hal\\BP\\VOICE.LISTENER.FIXED", "C:\\qmsys\\hal\\BP\\VOICE.LISTENER")
print("[OK] Copied")

# Compile
print("\nCompiling...")
try:
    qm.Execute("LOGTO HAL")
    time.sleep(0.5)
    qm.Execute("BASIC BP VOICE.LISTENER")
    time.sleep(1)
except Exception as e:
    print(f"  Error: {e}")

# Catalog with LOCAL - This is critical!
print("\nCataloging BP VOICE.LISTENER LOCAL...")
try:
    qm.Execute("CATALOG BP VOICE.LISTENER LOCAL")
    time.sleep(1)
    print("[OK] Cataloged with LOCAL")
except Exception as e:
    print(f"  Error: {e}")

# Start ONE phantom
print("\nStarting PHANTOM VOICE.LISTENER...")
try:
    qm.Execute("PHANTOM VOICE.LISTENER")
    time.sleep(2)
    print("[OK] Started")
except Exception as e:
    print(f"  Error: {e}")

qm.Disconnect()

# Verify
print("\n" + "="*60)
time.sleep(3)

result = subprocess.run("C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 LIST.READU", 
                       shell=True, capture_output=True, text=True)
print("QM Processes with VOICE:")
for line in result.stdout.split('\n'):
    if 'VOICE' in line or 'phantom' in line.lower():
        print(line)

result2 = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
if "LISTENING" in result2.stdout:
    print("\n[SUCCESS] Port 8767 is LISTENING")
    # Test it
    print("\nTesting...")
    time.sleep(1)
    subprocess.run("python C:\\qmsys\\hal\\test_qm_direct_newline.py", shell=True)
else:
    print("\n[ERROR] Port 8767 not listening")
