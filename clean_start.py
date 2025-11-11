"""Clean start - kill ALL phantoms, start ONE"""
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

# Logout ALL UIDs that might be VOICE.LISTENER
print("Logging out ALL phantom UIDs...")
for uid in range(14, 50):
    try:
        qm.Execute(f"LOGOUT {uid}")
        print(f"  Logged out {uid}")
        time.sleep(0.2)
    except:
        pass

time.sleep(3)

# Delete compiled version to force recompile
print("\nDeleting old compiled version...")
try:
    import os
    for f in os.listdir("C:\\qmsys\\hal\\BP.OUT"):
        if "VOICE.LISTENER" in f:
            os.remove(f"C:\\qmsys\\hal\\BP.OUT\\{f}")
            print(f"  Deleted {f}")
except:
    pass

# Copy FIXED version
print("\nCopying FIXED version...")
import shutil
shutil.copy("C:\\qmsys\\hal\\BP\\VOICE.LISTENER.FIXED", "C:\\qmsys\\hal\\BP\\VOICE.LISTENER")

# Compile
print("\nCompiling...")
qm.Execute("LOGTO HAL")
time.sleep(0.5)
qm.Execute("BASIC BP VOICE.LISTENER")
time.sleep(1)

# Catalog LOCAL
print("\nCataloging LOCAL...")
qm.Execute("CATALOG BP VOICE.LISTENER LOCAL")
time.sleep(1)

# Start ONE phantom
print("\nStarting ONE PHANTOM...")
qm.Execute("PHANTOM VOICE.LISTENER")
time.sleep(3)

qm.Disconnect()

# Verify
print("\n" + "="*60)
result = subprocess.run("C:\\QMSYS\\bin\\qm.exe -aHAL -u lawr -p apgar-66 LIST.READU", 
                       shell=True, capture_output=True, text=True)
voice_count = result.stdout.count("VOICE.LISTENER")
print(f"VOICE.LISTENER phantoms running: {voice_count}")

result2 = subprocess.run("netstat -an | findstr :8767", shell=True, capture_output=True, text=True)
listen_count = result2.stdout.count("LISTENING")
print(f"Port 8767 LISTENING count: {listen_count}")

if voice_count == 1 and listen_count == 1:
    print("\n[SUCCESS] Clean state - ONE phantom running!")
    time.sleep(2)
    print("\nTesting...")
    subprocess.run("python test_qm_direct_newline.py", shell=True, cwd="C:\\qmsys\\hal")
else:
    print(f"\n[WARNING] Expected 1 phantom, found {voice_count}")
