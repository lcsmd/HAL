#!/usr/bin/env python3
"""
Compile and run SETUP.COMMON.FIELDS program
"""
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("Compiling BP SETUP.COMMON.FIELDS...")
result = qm.Execute("BASIC BP SETUP.COMMON.FIELDS")
print(result[0])

print("\nCataloging BP SETUP.COMMON.FIELDS...")
result = qm.Execute("CATALOG BP SETUP.COMMON.FIELDS LOCAL")
print(result[0])

print("\nRunning SETUP.COMMON.FIELDS...")
result = qm.Execute("RUN BP SETUP.COMMON.FIELDS")
print(result[0])

print("\n" + "="*60)
print("Verifying FIELDS file...")
print("="*60)
result = qm.Execute("COUNT FIELDS")
print(result[0])

qm.Disconnect()
print("\nDone!")
