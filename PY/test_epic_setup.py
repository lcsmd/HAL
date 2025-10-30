#!/usr/bin/env python3
"""
Test Epic API Setup
Verify all components are ready
"""
import sys
import os
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✓ {description}: {filepath} ({size:,} bytes)")
        return True
    else:
        print(f"  ✗ {description}: {filepath} (NOT FOUND)")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.exists(dirpath):
        print(f"  ✓ {description}: {dirpath}")
        return True
    else:
        print(f"  ✗ {description}: {dirpath} (NOT FOUND)")
        return False

def check_module(module_name):
    """Check if a Python module is installed"""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name} module installed")
        return True
    except ImportError:
        print(f"  ✗ {module_name} module NOT installed")
        return False

def main():
    print("="*60)
    print("Epic API Setup Verification")
    print("="*60)
    
    all_good = True
    
    # Check Python scripts
    print("\n1. Python Scripts:")
    all_good &= check_file("PY/epic_api_setup.py", "OAuth Setup")
    all_good &= check_file("PY/epic_api_sync.py", "Data Sync")
    all_good &= check_file("PY/epic_parser.py", "FHIR Parser")
    all_good &= check_file("PY/epic_scheduler.py", "Scheduler")
    all_good &= check_file("PY/combine_fhir_bundles.py", "Bundle Combiner")
    
    # Check directories
    print("\n2. Directories:")
    all_good &= check_directory("config", "Config Directory")
    all_good &= check_directory("UPLOADS", "Uploads Directory")
    all_good &= check_directory("logs", "Logs Directory")
    
    # Check configuration
    print("\n3. Configuration:")
    if check_file("config/epic_api_config.json", "API Config"):
        import json
        with open("config/epic_api_config.json", 'r') as f:
            config = json.load(f)
        
        if config.get('client_id'):
            print(f"    ✓ Client ID configured: {config['client_id'][:8]}...")
        else:
            print(f"    ⚠ Client ID NOT configured (you need to add this)")
            all_good = False
        
        print(f"    ✓ FHIR Base URL: {config.get('fhir_base_url', 'NOT SET')}")
    
    if os.path.exists("config/epic_tokens.json"):
        print("  ✓ OAuth Tokens: Authorized")
    else:
        print("  ⚠ OAuth Tokens: Not yet authorized (run epic_api_setup.py)")
    
    # Check Python dependencies
    print("\n4. Python Dependencies:")
    all_good &= check_module("requests")
    check_module("schedule")  # Optional
    
    # Check QM integration
    print("\n5. QM Integration:")
    try:
        sys.path.insert(0, r'C:\QMSYS\SYSCOM')
        import qmclient
        print("  ✓ QMClient module available")
    except ImportError:
        print("  ✗ QMClient module NOT available")
        all_good = False
    
    # Check batch file
    print("\n6. Automation:")
    check_file("sync_epic_daily.cmd", "Daily Sync Batch File")
    
    # Check documentation
    print("\n7. Documentation:")
    check_file("README_EPIC_API.md", "Main README")
    check_file("NOTES/epic_api_quickstart.md", "Quick Start Guide")
    check_file("NOTES/epic_api_setup_guide.md", "Setup Guide")
    
    # Summary
    print("\n" + "="*60)
    if all_good:
        print("✓ ALL COMPONENTS READY!")
        print("="*60)
        print("\nNext steps:")
        print("1. Register app at: https://apporchard.epic.com/")
        print("2. Add Client ID to: config/epic_api_config.json")
        print("3. Run: python PY/epic_api_setup.py")
        print("4. Run: python PY/epic_api_sync.py P001")
        print("\nSee README_EPIC_API.md for complete instructions")
    else:
        print("⚠ SOME COMPONENTS MISSING")
        print("="*60)
        print("\nPlease check the items marked with ✗ above")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
