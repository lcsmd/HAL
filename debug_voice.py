from qm_exec import execute_qm_commands

# Check phantom status and compilation
results = execute_qm_commands([
    'LIST.READU',
    'LISTF BP.OUT VOICE.LISTENER',
])

for r in results:
    print(f"{r['command']}")
    print(f"  Status: {r['status']}")
    print(f"  Output: {r['output'][:300]}")
    print()
