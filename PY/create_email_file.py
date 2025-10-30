#!/usr/bin/env python3
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("Creating EMAIL file...")
result = qm.Execute("CREATE.FILE EMAIL DYNAMIC")
print(result[0])

print("\nRecompiling BUILD.DICT...")
result = qm.Execute("BASIC BP BUILD.DICT")
print(result[0])

print("\nCataloging BUILD.DICT...")
result = qm.Execute("CATALOG BP BUILD.DICT LOCAL")
print(result[0])

print("\nRunning BUILD.DICT EMAIL...")
result = qm.Execute("BUILD.DICT EMAIL")
print(result[0])

print("\n" + "="*60)
print("Verifying EMAIL dictionary...")
print("="*60)
result = qm.Execute("LIST DICT EMAIL")
print(result[0])

qm.Disconnect()
print("\nDone!")
