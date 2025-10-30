#!/usr/bin/env python3
"""
Create EMAIL file and build dictionary
"""
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("Setting up EMAIL file...")
print("="*60)

# Create the file
print("\n1. Creating EMAIL file...")
result = qm.Execute("CREATE.FILE EMAIL DYNAMIC")
print(result[0])

# Build dictionary
print("\n2. Building EMAIL dictionary...")
result = qm.Execute("BUILD.DICT EMAIL")
print(result[0])

# Verify
print("\n3. Verifying dictionary...")
result = qm.Execute("LIST DICT EMAIL")
print(result[0])

print("\n" + "="*60)
print("EMAIL file ready for import!")
print("="*60)

qm.Disconnect()
