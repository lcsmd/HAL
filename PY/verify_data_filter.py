#!/usr/bin/env python3
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("Verifying DATA_FILTER...")
print("="*60)

result = qm.Execute("COUNT DATA_FILTER")
print(result[0])

print("\nListing filter rules:")
result = qm.Execute("LIST DATA_FILTER")
print(result[0])

print("\nDictionary entries:")
result = qm.Execute("LIST DICT DATA_FILTER")
print(result[0])

qm.Disconnect()
