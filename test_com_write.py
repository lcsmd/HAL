#!/usr/bin/env python
"""Test writing to COM hashed file"""
from qm_exec import execute_qm_commands
from datetime import datetime

date_prefix = datetime.now().strftime("%Y%m%d")

# Test 1: Write a simple record
print("Test 1: Writing test record to COM...")
commands = [
    f'WRITE "TEST DATA LINE 1" TO COM, "{date_prefix}-I001"',
    f'WRITE "TEST OUTPUT LINE 1" TO COM, "{date_prefix}-O001"',
    'LIST COM'
]

results = execute_qm_commands(commands)

for r in results:
    print(f"\nCommand: {r['command']}")
    print(f"Status: {r['status']}")
    print(f"Output: {r['output'][:500]}")
