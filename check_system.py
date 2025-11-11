#!/usr/bin/env python
"""Use COMMAND.EXECUTOR to check system status"""
from qm_exec import execute_qm_commands
import os

print("=" * 70)
print("SYSTEM STATUS CHECK")
print("=" * 70)

# Check what's running
commands = [
    "WHO",
    "LISTF BP.OUT VOICE.LISTENER",
    "COUNT $COMO WITH @ID LIKE 'PH...'",
]

results = execute_qm_commands(commands)

for r in results:
    print(f"\n{r['command']}")
    print(f"Status: {r['status']}")
    print(f"Output:\n{r['output']}")
    print("-" * 70)

# Check recent COMO files
print("\nRecent COMO files:")
como_dir = "C:\\qmsys\\hal\\$COMO"
files = sorted(os.listdir(como_dir), reverse=True)[:5]
for f in files:
    if f.startswith('PH'):
        fpath = os.path.join(como_dir, f)
        mtime = os.path.getmtime(fpath)
        print(f"  {f} - {os.path.getsize(fpath)} bytes")

print("\n" + "=" * 70)
