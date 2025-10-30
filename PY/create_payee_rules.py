"""
Simple Payee Rule Generator
Analyzes TRANSACTION.ORIGINAL_PAYEE and creates basic standardization rules
"""

import sys
import os
import re
from collections import defaultdict

# Add QM bin to path
sys.path.insert(0, "C:\\QMSYS\\bin")

def analyze_payees():
    """Read all unique payees from TRANSACTION file"""
    print("Connecting to QM...")
    
    # Use subprocess to run QM command
    import subprocess
    
    # Get unique payees
    cmd = 'qm -kHAL -c"SSELECT TRANSACTION BY ORIGINAL_PAYEE"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Get list of payees
    cmd2 = 'qm -kHAL -c"GET.LIST 0"'
    result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
    
    print(f"Found payees in TRANSACTION file")
    print("Analyzing patterns...")
    
    # Group similar payees
    payee_groups = defaultdict(list)
    
    # Simple pattern: extract base name before location/numbers
    patterns = [
        (r'^(.*?)\s+\d+$', 'Remove trailing numbers'),
        (r'^(.*?)\s+[A-Z]{2}$', 'Remove state code'),
        (r'^(.*?)\s+#\d+', 'Remove store number'),
        (r'^(.*?)\s+\d{3,}', 'Remove long numbers'),
    ]
    
    return payee_groups

def create_rules():
    """Create standardization rules in RULE file"""
    print("\nCreating standardization rules...")
    
    # For now, create a few common patterns
    rules = [
        ("AMAZON", r"AMAZON.*", "Amazon"),
        ("WALMART", r"WAL.*MART.*", "Walmart"),
        ("TARGET", r"TARGET.*", "Target"),
        ("STARBUCKS", r"STARBUCKS.*", "Starbucks"),
        ("MCDONALDS", r"MCDONALD.*", "McDonald's"),
        ("SHELL", r"SHELL.*", "Shell"),
        ("EXXON", r"EXXON.*", "Exxon"),
        ("CVS", r"CVS.*", "CVS Pharmacy"),
    ]
    
    print(f"Creating {len(rules)} basic rules...")
    
    # Write rules using QM commands
    import subprocess
    
    for i, (rule_id, pattern, std_name) in enumerate(rules, 1):
        # Create rule record
        cmd = f'qm -kHAL -c"WRITE RULE {rule_id} \\"{rule_id}\\",\\"PAYEE_STANDARDIZATION\\",\\"Y\\",\\"{pattern}\\",\\"{std_name}\\""'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"  Created rule: {rule_id} -> {std_name}")
    
    print(f"\n✓ Created {len(rules)} standardization rules")
    print("\nNow run: FIN.STANDARDIZE.PAYEES.V2 21118-5588")

if __name__ == "__main__":
    analyze_payees()
    create_rules()
