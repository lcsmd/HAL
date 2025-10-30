#!/bin/bash
#
# Complete Installation Script for AI-Enhanced Email Management System
# Sets up OpenQM, Python environment, and all components
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/email_management_system"
QM_ACCOUNT="EMAILSYS"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

print_header "AI-Enhanced Email Management System - Installation"

# Check prerequisites
print_info "Checking prerequisites..."

# Check Python
if ! command_exists python3; then
    print_error "Python 3 is required but not installed"
    exit 1
fi
print_success "Python 3 found: $(python3 --version)"

# Check pip
if ! command_exists pip3; then
    print_error "pip3 is required but not installed"
    exit 1
fi
print_success "pip3 found"

# Check OpenQM
if ! command_exists qm; then
    print_warning "OpenQM not found. Please install OpenQM first."
    print_info "Visit: https://www.openqm.com/ for installation instructions"
    exit 1
fi
print_success "OpenQM found"

# Create installation directory
print_info "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
print_success "Installation directory created"

# Create directory structure
print_info "Creating directory structure..."
mkdir -p config
mkdir -p templates
mkdir -p attachments
mkdir -p html_objects
mkdir -p bodies
mkdir -p logs
mkdir -p temp
print_success "Directory structure created"

# Create Python virtual environment
print_info "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
print_success "Virtual environment created"

# Create requirements.txt
print_info "Creating requirements.txt..."
cat > requirements.txt << 'EOF'
# Google API
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0

# Microsoft Graph API
msal>=1.20.0

# Web framework
flask>=2.3.0
flask-cors>=4.0.0

# Utilities
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
python-magic>=0.4.27

# AI
anthropic>=0.18.0

# Scheduling
schedule>=1.2.0

# CSV processing
papaparse
EOF
print_success "requirements.txt created"

# Install Python dependencies
print_info "Installing Python dependencies (this may take a few minutes)..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Python dependencies installed"

# Create configuration file
print_info "Creating configuration file..."
cat > config/config.ini << EOF
[openqm]
account = $QM_ACCOUNT
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
base_dir = $INSTALL_DIR
attachment_dir = $INSTALL_DIR/attachments
html_objects_dir = $INSTALL_DIR/html_objects
bodies_dir = $INSTALL_DIR/bodies
log_dir = $INSTALL_DIR/logs

[processing]
# Batch size for email processing
batch_size = 100
# Maximum attachment size (MB)
max_attachment_size = 25
# Enable deduplication
enable_dedup = true

[daemon]
# Check for new emails every N minutes
check_interval_minutes = 15
# Batch size for processing
batch_size = 50
# Automatically categorize with AI
auto_categorize = true
# Run AI categorization when N uncategorized emails accumulate
ai_categorize_threshold = 100
EOF
print_success "Configuration file created"

# Setup OpenQM files
print_info "Setting up OpenQM database files..."
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')

# Import and run setup (assuming openqm_setup.py is in current dir)
try:
    from openqm_setup import OpenQMSetup
    setup = OpenQMSetup(qm_account='EMAILSYS')
    setup.create_openqm_files()
    setup.initialize_schema()
    print("OpenQM setup completed")
except Exception as e:
    print(f"Error setting up OpenQM: {e}")
    print("You may need to run openqm_setup.py manually")
PYEOF
print_success "OpenQM database initialized"

# Create systemd service file
print_info "Creating systemd service file..."
SERVICE_FILE="/tmp/email-processor.service"
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=AI-Enhanced Email Management System Processor
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/email_processor_daemon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
print_success "Systemd service file created at $SERVICE_FILE"

# Create startup script
print_info "Creating startup scripts..."
cat > start_web.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python app.py
EOF
chmod +x start_web.sh

cat > start_daemon.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python email_processor_daemon.py
EOF
chmod +x start_daemon.sh

cat > ingest_emails.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python gmail_ingestion.py --max 100
EOF
chmod +x ingest_emails.sh

print_success "Startup scripts created"

# Create README
print_info "Creating README..."
cat > README.md << 'EOF'
# AI-Enhanced Email Management System

## Quick Start

### 1. Configure API Keys

Edit `config/config.ini` and add:
- Gmail OAuth credentials
- Anthropic API key (for AI features)
- Exchange credentials (if using)

### 2. Gmail Setup

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `config/gmail_credentials.json`

### 3. Start the Web Interface

```bash
./start_web.sh
```

Access at: http://localhost:5000

### 4. Import Emails

```bash
./ingest_emails.sh
```

### 5. Start Background Processor (Optional)

```bash
./start_daemon.sh
```

Or install as a service:
```bash
sudo cp /tmp/email-processor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable email-processor
sudo systemctl start email-processor
```

## Components

- `app.py` - Flask web application
- `gmail_ingestion.py` - Gmail email import
- `ai_categorization_engine.py` - AI-powered categorization
- `rule_engine.py` - Automated rule application
- `email_processor_daemon.py` - Background processor
- `openqm_interface.py` - OpenQM database wrapper
- `openqm_setup.py` - Database initialization

## Directory Structure

- `config/` - Configuration files
- `templates/` - HTML templates
- `attachments/` - Email attachments
- `bodies/` - Email body content
- `logs/` - Application logs
- `venv/` - Python virtual environment

## Documentation

See the documentation artifacts for detailed guides on:
- AI Categorization
- Rule Engine
- API Reference
- Web Interface

## Support

For issues, check the logs in `logs/` directory.
EOF
print_success "README created"

# Create .gitignore
print_info "Creating .gitignore..."
cat > .gitignore << 'EOF'
# Virtual environment
venv/

# Configuration with secrets
config/config.ini
config/*credentials*.json
config/*token*.pickle

# Data directories
attachments/
bodies/
html_objects/

# Logs
logs/
*.log

# Temporary files
temp/
*.pyc
__pycache__/

# OS files
.DS_Store
Thumbs.db
EOF
print_success ".gitignore created"

# Final instructions
print_header "Installation Complete!"

echo ""
print_success "Installation directory: $INSTALL_DIR"
echo ""
print_info "Next steps:"
echo "  1. Edit config/config.ini and add your API keys"
echo "  2. Set up Gmail OAuth credentials in config/"
echo "  3. Run: cd $INSTALL_DIR && source venv/bin/activate"
echo "  4. Import emails: ./ingest_emails.sh"
echo "  5. Start web interface: ./start_web.sh"
echo ""
print_info "Optional:"
echo "  - Install as system service: sudo cp /tmp/email-processor.service /etc/systemd/system/"
echo "  - Enable service: sudo systemctl enable email-processor"
echo "  - Start service: sudo systemctl start email-processor"
echo ""
print_info "Web interface will be available at: http://localhost:5000"
echo ""
print_warning "Don't forget to configure your API keys in config/config.ini!"
echo ""
print_header "Happy email managing!"
