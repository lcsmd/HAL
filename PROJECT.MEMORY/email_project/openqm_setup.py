#!/usr/bin/env python3
"""
AI-Enhanced Email Management System - OpenQM Setup
Creates OpenQM file structure and initializes the environment
"""

import os
import subprocess
import sys
from pathlib import Path

class OpenQMSetup:
    def __init__(self, qm_account='EMAILSYS'):
        self.qm_account = qm_account
        self.base_dir = Path.home() / 'email_management_system'
        
        # OpenQM file definitions: (filename, modulo, separation)
        self.qm_files = {
            'EMAILS': (101, 1),
            'ATTACHMENTS': (101, 1),
            'HTML.OBJECTS': (101, 1),
            'DISCLAIMERS': (101, 1),
            'BODIES': (101, 1),
            'THREADS': (101, 1),
            'CONTACTS': (101, 1),
            'GROUPS': (101, 1),
            'DOMAINS': (101, 1),
            'RULES': (101, 1),
            'CATEGORIES': (101, 1),
            'KEYWORDS': (101, 1),
            'SYSTEM.CONFIG': (3, 1)
        }
        
        # Directory structure for binary files
        self.directories = [
            'attachments',
            'html_objects', 
            'bodies',
            'logs',
            'config',
            'temp'
        ]
        
    def create_directory_structure(self):
        """Create application directory structure"""
        print("Creating directory structure...")
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        for directory in self.directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(exist_ok=True)
            print(f"  ✓ Created: {dir_path}")
            
        print(f"\nBase directory: {self.base_dir}\n")
        
    def create_openqm_files(self):
        """Create OpenQM file structure"""
        print("Creating OpenQM files...")
        
        for filename, (modulo, separation) in self.qm_files.items():
            try:
                result = subprocess.run(
                    ['qm', '-A', self.qm_account, '-KCREATE.FILE', filename, str(modulo), str(separation)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0 or 'already exists' in result.stdout.lower():
                    print(f"  ✓ {filename}")
                else:
                    print(f"  ✗ {filename}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"  ✗ {filename}: Timeout")
            except Exception as e:
                print(f"  ✗ {filename}: {e}")
                
    def initialize_schema(self):
        """Initialize OpenQM with schema definitions"""
        print("\nInitializing schema...")
        
        schema_script = """
* Initialize system configuration
OPEN 'SYSTEM.CONFIG' TO CONFIG.FILE ELSE STOP 'Cannot open SYSTEM.CONFIG'

* Store schema version
CONFIG.REC = ''
CONFIG.REC<1> = '1.0.0'
CONFIG.REC<2> = DATE()
CONFIG.REC<3> = TIME()
WRITE CONFIG.REC TO CONFIG.FILE, 'SCHEMA.VERSION'

* Initialize counters
COUNTERS = ''
COUNTERS<1> = 0  ;* EMAIL.COUNT
COUNTERS<2> = 0  ;* THREAD.COUNT
COUNTERS<3> = 0  ;* ATTACHMENT.COUNT
COUNTERS<4> = 0  ;* CONTACT.COUNT
WRITE COUNTERS TO CONFIG.FILE, 'COUNTERS'

PRINT 'Schema initialized'
"""
        
        script_file = self.base_dir / 'temp' / 'init_schema.bas'
        with open(script_file, 'w') as f:
            f.write(schema_script)
            
        try:
            result = subprocess.run(
                ['qm', '-A', self.qm_account, '-K', str(script_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("  ✓ Schema initialized")
            else:
                print(f"  ✗ Schema initialization failed: {result.stderr}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            
    def create_python_venv(self):
        """Create Python virtual environment"""
        print("\nCreating Python virtual environment...")
        
        venv_path = self.base_dir / 'venv'
        
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
            print(f"  ✓ Virtual environment created at {venv_path}")
            
            # Create requirements.txt
            requirements = [
                'google-auth-oauthlib>=1.0.0',
                'google-auth-httplib2>=0.1.0',
                'google-api-python-client>=2.0.0',
                'msal>=1.20.0',
                'requests>=2.28.0',
                'beautifulsoup4>=4.11.0',
                'lxml>=4.9.0',
                'python-magic>=0.4.27',
                'anthropic>=0.18.0',
                'flask>=2.3.0',
                'flask-cors>=4.0.0'
            ]
            
            req_file = self.base_dir / 'requirements.txt'
            with open(req_file, 'w') as f:
                f.write('\n'.join(requirements))
                
            print(f"  ✓ requirements.txt created")
            
            # Provide installation instructions
            pip_path = venv_path / 'bin' / 'pip'
            print(f"\nTo install dependencies, run:")
            print(f"  {pip_path} install -r {req_file}")
            
        except Exception as e:
            print(f"  ✗ Error creating virtual environment: {e}")
            
    def create_config_template(self):
        """Create configuration file template"""
        print("\nCreating configuration template...")
        
        config_content = """# Email Management System Configuration

[openqm]
account = EMAILSYS
host = localhost
port = 4243

[gmail]
# Place your Gmail OAuth2 credentials.json in the config directory
credentials_file = config/gmail_credentials.json
token_file = config/gmail_token.pickle

[exchange]
# Microsoft Graph API configuration
tenant_id = your-tenant-id
client_id = your-client-id
client_secret = your-client-secret

[ai]
# Anthropic API key for Claude
anthropic_api_key = your-api-key-here

[system]
base_dir = {base_dir}
attachment_dir = {base_dir}/attachments
html_objects_dir = {base_dir}/html_objects
bodies_dir = {base_dir}/bodies
log_dir = {base_dir}/logs

[processing]
# Batch size for email processing
batch_size = 100
# Maximum attachment size (MB)
max_attachment_size = 25
# Enable deduplication
enable_dedup = true
"""
        
        config_file = self.base_dir / 'config' / 'config.ini'
        with open(config_file, 'w') as f:
            f.write(config_content.format(base_dir=self.base_dir))
            
        print(f"  ✓ Configuration template created at {config_file}")
        print(f"\n  IMPORTANT: Edit {config_file} and add your credentials!")
        
    def run_setup(self):
        """Execute complete setup process"""
        print("="*60)
        print("AI-Enhanced Email Management System - OpenQM Setup")
        print("="*60)
        print()
        
        self.create_directory_structure()
        self.create_openqm_files()
        self.initialize_schema()
        self.create_python_venv()
        self.create_config_template()
        
        print("\n" + "="*60)
        print("Setup Complete!")
        print("="*60)
        print("\nNext Steps:")
        print(f"1. Edit configuration: {self.base_dir}/config/config.ini")
        print(f"2. Activate virtual environment:")
        print(f"   source {self.base_dir}/venv/bin/activate")
        print(f"3. Install dependencies:")
        print(f"   pip install -r {self.base_dir}/requirements.txt")
        print(f"4. Set up Gmail/Exchange OAuth credentials")
        print(f"5. Run the email ingestion module")
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup AI Email Management System with OpenQM')
    parser.add_argument('--account', default='EMAILSYS', help='OpenQM account name')
    
    args = parser.parse_args()
    
    setup = OpenQMSetup(qm_account=args.account)
    setup.run_setup()


if __name__ == '__main__':
    main()
