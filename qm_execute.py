"""Execute QM commands via file-based executor"""
import subprocess
import time
import os

def execute_qm_command(command, timeout=10):
    """Execute a QM command and return the output"""
    input_file = "C:\\qmsys\\hal\\command_input.txt"
    output_file = "C:\\qmsys\\hal\\command_output.txt"
    
    # Clean up old files
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Write command to input file
    with open(input_file, 'w') as f:
        f.write(command)
    
    # Execute the QM program
    result = subprocess.run(
        f'C:\\qmsys\\bin\\qm.exe -aHAL "RUN BP COMMAND.EXECUTOR"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    
    # Wait a moment for file to be written
    time.sleep(0.5)
    
    # Read output file
    if not os.path.exists(output_file):
        return {"status": -1, "output": "No output file created"}
    
    with open(output_file, 'r') as f:
        content = f.read()
    
    # Parse output
    lines = content.split('\n')
    status_line = lines[0] if lines else ""
    output_text = '\n'.join(lines[1:]) if len(lines) > 1 else ""
    
    status = -1
    if status_line.startswith("STATUS:"):
        try:
            status = int(status_line.split(":")[1])
        except:
            pass
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)
    
    return {"status": status, "output": output_text.strip(), "command": command}

if __name__ == "__main__":
    # Test it
    print("Testing QM Command Executor...")
    print("="*60)
    
    # Test 1: Count records
    print("\n1. COUNT MEDICATION")
    result = execute_qm_command("COUNT MEDICATION")
    print(f"Status: {result['status']}")
    print(f"Output: {result['output']}")
    
    # Test 2: List users
    print("\n2. LIST.READU")
    result = execute_qm_command("LIST.READU")
    print(f"Status: {result['status']}")
    print(f"Output: {result['output']}")
    
    print("\n" + "="*60)
    print("Executor is working!")
