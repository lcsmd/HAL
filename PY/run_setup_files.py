#!/usr/bin/env python3
"""
Compile and run SETUP.FILES program
"""
import sys
import os
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

# Connect to QM
print("Connecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')
print("Connected!")

# Compile SETUP.FILES
print("\nCompiling BP SETUP.FILES...")
result = qm.Execute("BASIC BP SETUP.FILES")
print(result)

# Catalog it to local catalog
print("\nCataloging BP SETUP.FILES...")
result = qm.Execute("CATALOG BP SETUP.FILES LOCAL")
print(result)

# Run it
print("\nRunning SETUP.FILES...")
result = qm.Execute("RUN BP SETUP.FILES")
print(result)

# Verify the data
print("\n" + "="*50)
print("Verifying FILES file...")
print("="*50)
result = qm.Execute("LIST FILES FILE_ABB FILE_DESCRIPTION DOMAIN")
print(result[0])

# Disconnect
qm.Disconnect()
print("\nDone!")
