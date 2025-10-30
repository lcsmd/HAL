#!/usr/bin/env python3
"""
Compile and run SETUP.ALL.FILES program
"""
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("Compiling BP SETUP.ALL.FILES...")
result = qm.Execute("BASIC BP SETUP.ALL.FILES")
print(result[0])

print("\nCataloging BP SETUP.ALL.FILES...")
result = qm.Execute("CATALOG BP SETUP.ALL.FILES LOCAL")
print(result[0])

print("\nRunning SETUP.ALL.FILES...")
result = qm.Execute("RUN BP SETUP.ALL.FILES")
print(result[0])

print("\n" + "="*60)
print("Verifying FILES and DOM_FILE_FIELD...")
print("="*60)

result = qm.Execute("COUNT FILES")
print("FILES:", result[0])

result = qm.Execute("COUNT DOM_FILE_FIELD")
print("DOM_FILE_FIELD:", result[0])

qm.Disconnect()
print("\nDone!")
