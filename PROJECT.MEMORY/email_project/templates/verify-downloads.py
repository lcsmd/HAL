#!/usr/bin/env python3
"""
Download Verification Script
Checks if all required files are present
"""

import os
from pathlib import Path

def check_files():
    """Verify all required files are present"""
    
    print("="*60)
    print("AI-Enhanced Email Management System")
    print("Download Verification Script")
    print("="*60)
    print()
    
    # Check project directory
    project_dir = Path('C:/email_project')
    install_dir = Path('C:/email_management_system')
    
    # Files to check in project directory (before installation)
    project_files = {
        'Python Files': [
            'openqm_interface.py',
            'app.py',
            'gmail_ingestion.py',
            'ai_categorization_engine.py',
            'rule_engine.py',
            'email_processor_daemon.py',
            'openqm_setup.py',
            'demo_testing_script.py'
        ],
        'Batch Files': [
            'install_windows.bat'
        ],
        'HTML Templates': [
            'templates/base.html',
            'templates/dashboard.html',
            'templates/emails.html',
            'templates/email_detail.html',
            'templates/threads.html',
            'templates/categories.html',
            'templates/settings.html',
            'templates/rules.html',
            'templates/ai_categorization.html'
        ]
    }
    
    # Check if installation has been run
    installation_run = install_dir.exists()
    
    if installation_run:
        print(f"✓ Installation directory exists: {install_dir}")
        print()
        check_dir = install_dir
    else:
        print(f"Checking project directory: {project_dir}")
        print("(Installation not yet run)")
        print()
        check_dir = project_dir
    
    # Verify each category
    total_files = 0
    total_found = 0
    
    for category, files in project_files.items():
        print(f"{category}:")
        print("-" * 40)
        
        for filename in files:
            filepath = check_dir / filename
            total_files += 1
            
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"  ✓ {filename} ({size:,} bytes)")
                total_found += 1
            else:
                print(f"  ✗ {filename} - MISSING")
        
        print()
    
    # Summary
    print("="*60)
    print(f"Summary: {total_found}/{total_files} files found")
    print("="*60)
    
    if total_found == total_files:
        print("✓ All files present!")
        print()
        if not installation_run:
            print("Next step: Run install_windows.bat")
        else:
            print("Next step: Update code and configure API keys")
    else:
        missing = total_files - total_found
        print(f"✗ {missing} file(s) missing")
        print()
        print("Please download missing files from Claude conversation")
    
    print()
    
    # Check for code updates if installation run
    if installation_run:
        print("="*60)
        print("Code Update Status")
        print("="*60)
        print()
        
        files_to_check = [
            'app.py',
            'gmail_ingestion.py', 
            'ai_categorization_engine.py',
            'email_processor_daemon.py'
        ]
        
        needs_update = []
        
        for filename in files_to_check:
            filepath = install_dir / filename
            if filepath.exists():
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Check if paths updated
                if "Path.home() / 'email_management_system'" in content:
                    needs_update.append(filename)
        
        if needs_update:
            print("⚠️  These files need path updates:")
            for filename in needs_update:
                print(f"  - {filename}")
            print()
            print("Replace:")
            print("  Path.home() / 'email_management_system'")
            print("With:")
            print("  Path('C:/email_management_system')")
        else:
            print("✓ All path references updated")
        
        print()
        
        # Check config
        config_file = install_dir / 'config' / 'config.ini'
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = f.read()
            
            print("="*60)
            print("Configuration Status")
            print("="*60)
            print()
            
            if 'your-api-key-here' in config:
                print("⚠️  Anthropic API key not configured")
                print(f"   Edit: {config_file}")
            else:
                print("✓ Anthropic API key configured")
            
            gmail_creds = install_dir / 'config' / 'gmail_credentials.json'
            if gmail_creds.exists():
                print("✓ Gmail credentials file present")
            else:
                print("⚠️  Gmail credentials.json missing")
                print(f"   Place at: {gmail_creds}")
            
            print()


if __name__ == '__main__':
    try:
        check_files()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")
