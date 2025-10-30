import os
from pathlib import Path

# Rename mapping
renames = {
    'openqm-interface.py': 'openqm_interface.py',
    'openqm-setup.py': 'openqm_setup.py',
    'gmail-ingestion.py': 'gmail_ingestion.py',
    'demo-testing-script.py': 'demo_testing_script.py',
    'email-processor-daemon.py': 'email_processor_daemon.py',
    'windows-installation.txt': 'install_windows.bat',
    'windows-openqm-setup.py': 'openqm_setup.py',
}

project_dir = Path('C:/email_project')

print("Renaming files...")
for old_name, new_name in renames.items():
    old_path = project_dir / old_name
    new_path = project_dir / new_name
    
    if old_path.exists():
        if new_path.exists():
            print(f"⚠️  {new_name} already exists, skipping {old_name}")
        else:
            old_path.rename(new_path)
            print(f"✓ {old_name} → {new_name}")
    else:
        print(f"✗ {old_name} not found")

print("\nDone!")