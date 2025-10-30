#!/usr/bin/env python3
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("="*60)
print("VERIFICATION OF SCHEMA FILES")
print("="*60)

print("\nDOMAINS:")
r = qm.Execute('COUNT DOMAINS')
print(r[0])

print("\nFILES:")
r = qm.Execute('COUNT FILES')
print(r[0])

print("\nFIELDS:")
r = qm.Execute('COUNT FIELDS')
print(r[0])

print("\nDOM_FILE_FIELD:")
r = qm.Execute('COUNT DOM_FILE_FIELD')
print(r[0])

print("\n" + "="*60)
print("Listing DOM_FILE_FIELD records:")
print("="*60)
r = qm.Execute('LIST DOM_FILE_FIELD')
print(r[0])

qm.Disconnect()
