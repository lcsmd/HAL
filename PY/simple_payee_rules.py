"""
Simple Payee Rule Creator
Creates basic standardization rules for common vendors
"""

import sys
sys.path.insert(0, "C:\\QMSYS\\bin")

try:
    import qmclient as qm
except ImportError:
    print("ERROR: qmclient.py not found in C:\\QMSYS\\bin")
    sys.exit(1)

# Connect to QM
print("Connecting to QM on localhost:4243...")
try:
    session = qm.Connect('127.0.0.1', 4243, 'HAL', '', '')
    if not session:
        print("ERROR: Failed to connect to QM")
        print("Connection returned:", session)
        sys.exit(1)
except Exception as e:
    print(f"ERROR: Exception during connect: {e}")
    sys.exit(1)

print("Connected successfully!")

# Open RULE file
fno, err = qm.Open('RULE')
if err != 0:
    print(f"ERROR: Cannot open RULE file (error {err})")
    qm.Disconnect()
    sys.exit(1)

print("Creating standardization rules...")

# Common vendor patterns
rules = [
    ("AMAZON", "PAYEE_STANDARDIZATION", "Y", "AMAZON.*", "Amazon"),
    ("WALMART", "PAYEE_STANDARDIZATION", "Y", "WAL.*MART.*", "Walmart"),
    ("TARGET", "PAYEE_STANDARDIZATION", "Y", "TARGET.*", "Target"),
    ("STARBUCKS", "PAYEE_STANDARDIZATION", "Y", "STARBUCKS.*", "Starbucks"),
    ("MCDONALDS", "PAYEE_STANDARDIZATION", "Y", "MCDONALD.*", "McDonald's"),
    ("SHELL", "PAYEE_STANDARDIZATION", "Y", "SHELL.*", "Shell"),
    ("EXXON", "PAYEE_STANDARDIZATION", "Y", "EXXON.*", "Exxon"),
    ("CVS", "PAYEE_STANDARDIZATION", "Y", "CVS.*", "CVS Pharmacy"),
    ("WALGREENS", "PAYEE_STANDARDIZATION", "Y", "WALGREENS.*", "Walgreens"),
    ("KROGER", "PAYEE_STANDARDIZATION", "Y", "KROGER.*", "Kroger"),
    ("PUBLIX", "PAYEE_STANDARDIZATION", "Y", "PUBLIX.*", "Publix"),
    ("WHOLE_FOODS", "PAYEE_STANDARDIZATION", "Y", "WHOLE.*FOODS.*", "Whole Foods"),
    ("COSTCO", "PAYEE_STANDARDIZATION", "Y", "COSTCO.*", "Costco"),
    ("HOME_DEPOT", "PAYEE_STANDARDIZATION", "Y", "HOME.*DEPOT.*", "Home Depot"),
    ("LOWES", "PAYEE_STANDARDIZATION", "Y", "LOWE.*S.*", "Lowe's"),
]

count = 0
for rule_id, rule_type, active, pattern, std_name in rules:
    # Build record as dynamic array (fields separated by field marks)
    record = f"{rule_id}\xFE{rule_type}\xFE{active}\xFE{pattern}\xFE{std_name}"
    
    # Write rule
    err = qm.Write(fno, rule_id, record)
    if err == 0:
        print(f"  ✓ {rule_id} -> {std_name}")
        count += 1
    else:
        print(f"  ✗ Failed to write {rule_id} (error {err})")

# Close file
qm.Close(fno)

# Disconnect
qm.Disconnect()

print(f"\n✓ Created {count} standardization rules")
print("\nNow run in QM:")
print("  FIN.STANDARDIZE.PAYEES.V2 21118-5588")
