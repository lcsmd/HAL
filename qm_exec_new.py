#!/usr/bin/env python
"""Execute QM commands using COM file-based COMMAND.EXECUTOR"""
import subprocess
import time
from datetime import datetime

def execute_qm_commands_com(commands):
    """Execute commands using COM-based executor"""
    if isinstance(commands, str):
        commands = [commands]
    
    # Join with field mark (chr 254)
    commands_text = chr(254).join(commands)
    
    # Write to COM INPUT record
    write_cmd = f'OPEN "COM" TO F ELSE STOP; WRITE "{commands_text}" TO F, "INPUT"; CLOSE F'
    subprocess.run(
        ['C:\\qmsys\\bin\\qm.exe', '-aHAL', write_cmd],
        timeout=5
    )
    
    # Run executor
    result = subprocess.run(
        'C:\\qmsys\\bin\\qm.exe -aHAL "RUN BP COMMAND.EXECUTOR"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )
    
    time.sleep(0.2)
    
    # Find the output record by getting latest sequence
    date_prefix = datetime.now().strftime("%Y%m%d")
    
    # Try to read output records
    for seq in range(1, 100):
        output_id = f"{date_prefix}-{seq:03d}O"
        read_cmd = f'OPEN "COM" TO F ELSE STOP; READ REC FROM F, "{output_id}" THEN CRT REC ELSE CRT "NOTFOUND"'
        result = subprocess.run(
            ['C:\\qmsys\\bin\\qm.exe', '-aHAL', read_cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "NOTFOUND" not in result.stdout and result.stdout.strip():
            return result.stdout
    
    return None

# Test
if __name__ == "__main__":
    print("Testing COM-based executor...")
    output = execute_qm_commands_com(["WHO", "TIME"])
    if output:
        print(f"Output:\n{output}")
    else:
        print("No output found")
