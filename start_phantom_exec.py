"""Start PHANTOM using qm.exe with Execute command"""
import subprocess
import time

def run_qm_command(cmd):
    """Execute a QM command using qm.exe"""
    qm_exe = "C:\\qmsys\\bin\\qm.exe"
    account = "HAL"
    
    # Build the command - note PHANTOM doesn't need BP prefix
    full_cmd = f'"{qm_exe}" -aHAL -u lawr -p apgar-66 "{cmd}"'
    
    print(f"Executing: {cmd}")
    print(f"Full command: {full_cmd}")
    
    try:
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("Command timed out (may be normal for PHANTOM)")
        return True  # PHANTOM timing out is OK - it starts in background
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("="*60)
    print("Starting QM Voice Listener PHANTOM")
    print("="*60)
    print()
    
    # First ensure we're in HAL account
    print("Step 1: Logging to HAL account...")
    run_qm_command("LOGTO HAL")
    time.sleep(1)
    
    # Start PHANTOM - just "PHANTOM VOICE.LISTENER" without BP prefix
    print("\nStep 2: Starting PHANTOM VOICE.LISTENER...")
    run_qm_command("PHANTOM VOICE.LISTENER")
    
    # Wait a moment
    print("\nWaiting 3 seconds for listener to start...")
    time.sleep(3)
    
    # Check if it's listening
    print("\nStep 3: Checking if port 8767 is listening...")
    check_cmd = "netstat -an | findstr :8767"
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0 and "LISTENING" in result.stdout:
        print("✅ SUCCESS! Voice Listener is running on port 8767")
        print(result.stdout)
        return True
    else:
        print("⚠️ Port 8767 not listening yet")
        print("The PHANTOM may still be starting...")
        return False

if __name__ == "__main__":
    success = main()
    print()
    print("="*60)
    if success:
        print("Voice Listener is OPERATIONAL!")
        print("Test it with: python tests\\test_text_input.py")
    else:
        print("Listener may need a moment to start")
        print("Check status with: netstat -an | findstr :8767")
    print("="*60)
