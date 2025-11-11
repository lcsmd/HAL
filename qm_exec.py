"""Execute QM commands via COMMAND.EXECUTOR"""
import subprocess
import time
import os

def execute_qm_commands(commands):
    """Execute one or more QM commands"""
    if isinstance(commands, str):
        commands = [commands]
    
    input_file = "C:\\qmsys\\hal\\COM\\input.txt"
    output_file = "C:\\qmsys\\hal\\COM\\output.txt"
    
    # Clean up old output
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Write commands
    with open(input_file, 'w') as f:
        f.write('\n'.join(commands))
    
    # Execute
    result = subprocess.run(
        'C:\\qmsys\\bin\\qm.exe -aHAL "RUN BP COMMAND.EXECUTOR"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # Wait for output
    time.sleep(0.5)
    
    # Read output
    if not os.path.exists(output_file):
        return []
    
    with open(output_file, 'r') as f:
        content = f.read()
    
    # Parse results
    results = []
    lines = content.split('\n')
    current = {}
    
    for line in lines:
        if line.startswith("COMMAND:"):
            if current:
                results.append(current)
            current = {"command": line[8:]}
        elif line.startswith("STATUS:"):
            current["status"] = int(line[7:]) if line[7:].isdigit() else -1
        elif line.startswith("OUTPUT:"):
            current["output"] = line[7:]
        elif line == "---":
            if current:
                results.append(current)
                current = {}
    
    return results

if __name__ == "__main__":
    print("Testing QM Command Executor...")
    print("="*60)
    
    results = execute_qm_commands(["WHO", "COUNT MEDICATION", "LIST.READU"])
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['command']}")
        print(f"   Status: {r['status']}")
        print(f"   Output: {r['output'][:100]}")
    
    print("\n" + "="*60)
    print(f"Executed {len(results)} commands successfully!")
