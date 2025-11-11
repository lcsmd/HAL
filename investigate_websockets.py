#!/usr/bin/env python
"""Investigate QM socket functions using COMMAND.EXECUTOR"""
from qm_exec import execute_qm_commands
from datetime import datetime
import os

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
base_dir = "C:\\qmsys\\hal\\COM"

# Create list of investigation commands
investigations = [
    {
        "name": "check_phantom_status",
        "commands": [
            "WHO",
            "LIST.READU"
        ]
    },
    {
        "name": "check_voice_listener_compiled",
        "commands": [
            "LISTF BP.OUT VOICE.LISTENER"
        ]
    },
    {
        "name": "check_socket_help",
        "commands": [
            "HELP READ.SOCKET",
            "HELP WRITE.SOCKET",
            "HELP ACCEPT.SOCKET.CONNECTION",
            "HELP CREATE.SERVER.SOCKET"
        ]
    },
    {
        "name": "list_voice_listener_source",
        "commands": [
            "LIST BP VOICE.LISTENER"
        ]
    },
    {
        "name": "check_compilation_listing",
        "commands": [
            "LIST BP.OUT VOICE.LISTENER.LIS"
        ]
    }
]

for investigation in investigations:
    inv_name = investigation["name"]
    commands = investigation["commands"]
    
    # Create input file
    input_filename = f"CMD_INPUT_{inv_name}_{timestamp}.txt"
    input_path = os.path.join(base_dir, input_filename)
    
    with open(input_path, 'w') as f:
        f.write('\n'.join(commands))
    
    print(f"Created: {input_filename}")
    print(f"  Commands: {len(commands)}")
    
    # Execute via COMMAND.EXECUTOR
    results = execute_qm_commands(commands)
    
    # Create output file
    output_filename = f"CMD_OUTPUT_{inv_name}_{timestamp}.txt"
    output_path = os.path.join(base_dir, output_filename)
    
    with open(output_path, 'w') as f:
        for r in results:
            f.write(f"COMMAND: {r['command']}\n")
            f.write(f"STATUS: {r['status']}\n")
            f.write(f"OUTPUT:\n{r['output']}\n")
            f.write("="*70 + "\n\n")
    
    print(f"Created: {output_filename}")
    print()

print(f"\nAll command/output files created with timestamp: {timestamp}")
print(f"Review files in: {base_dir}")
