@echo off
REM Complete Installation Script for AI-Enhanced Email Management System (Windows)
REM Sets up Python environment, OpenQM files, and all components

setlocal EnableDelayedExpansion

set "INSTALL_DIR=C:\email_management_system"
set "QM_ACCOUNT=EMAILSYS"

echo ============================================================
echo AI-Enhanced Email Management System - Windows Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is required but not installed
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo [OK] Python found: 
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is required but not installed
    pause
    exit /b 1
)
echo [OK] pip found

REM Check if OpenQM is installed
qm >nul 2>&1
if errorlevel 1 (
    echo [WARNING] OpenQM 'qm' command not found in PATH
    echo Please ensure OpenQM is installed and accessible
    echo You may need to add OpenQM to your PATH environment variable
    pause
)
echo [OK] OpenQM found

REM Create installation directory
echo.
echo Creating installation directory: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
cd /d "%INSTALL_DIR%"
echo [OK] Installation directory created

REM Create directory structure
echo.
echo Creating directory structure...
mkdir config 2>nul
mkdir templates 2>nul
mkdir attachments 2>nul
mkdir html_objects 2>nul
mkdir bodies 2>nul
mkdir logs 2>nul
mkdir temp 2>nul
echo [OK] Directory structure created

REM Create Python virtual environment
echo.
echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo [OK] Virtual environment created

REM Create requirements.txt
echo.
echo Creating requirements.txt...
(
echo # Google API
echo google-auth-oauthlib^>=1.0.0
echo google-auth-httplib2^>=0.1.0
echo google-api-python-client^>=2.0.0
echo.
echo # Microsoft Graph API
echo msal^>=1.20.0
echo.
echo # Web framework
echo flask^>=2.3.0
echo flask-cors^>=4.0.0
echo.
echo # Utilities
echo requests^>=2.28.0
echo beautifulsoup4^>=4.11.0
echo lxml^>=4.9.0
echo python-magic-bin^>=0.4.14
echo.
echo # AI
echo anthropic^>=0.18.0
echo.
echo # Scheduling
echo schedule^>=1.2.0
) > requirements.txt
echo [OK] requirements.txt created

REM Install Python dependencies
echo.
echo Installing Python dependencies (this may take a few minutes)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

REM Create configuration file
echo.
echo Creating configuration file...
(
echo [openqm]
echo account = %QM_ACCOUNT%
echo host = localhost
echo port = 4243
echo.
echo [gmail]
echo # Place your Gmail OAuth2 credentials.json in the config directory
echo credentials_file = config\gmail_credentials.json
echo token_file = config\gmail_token.pickle
echo.
echo [exchange]
echo # Microsoft Graph API configuration
echo tenant_id = your-tenant-id
echo client_id = your-client-id
echo client_secret = your-client-secret
echo.
echo [ai]
echo # Anthropic API key for Claude
echo anthropic_api_key = your-api-key-here
echo.
echo [system]
echo base_dir = %INSTALL_DIR%
echo attachment_dir = %INSTALL_DIR%\attachments
echo html_objects_dir = %INSTALL_DIR%\html_objects
echo bodies_dir = %INSTALL_DIR%\bodies
echo log_dir = %INSTALL_DIR%\logs
echo.
echo [processing]
echo # Batch size for email processing
echo batch_size = 100
echo # Maximum attachment size (MB)
echo max_attachment_size = 25
echo # Enable deduplication
echo enable_dedup = true
echo.
echo [daemon]
echo # Check for new emails every N minutes
echo check_interval_minutes = 15
echo # Batch size for processing
echo batch_size = 50
echo # Automatically categorize with AI
echo auto_categorize = true
echo # Run AI categorization when N uncategorized emails accumulate
echo ai_categorize_threshold = 100
) > config\config.ini
echo [OK] Configuration file created

REM Create startup scripts
echo.
echo Creating startup scripts...

REM start_web.bat
(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python app.py
echo pause
) > start_web.bat

REM start_daemon.bat
(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python email_processor_daemon.py
echo pause
) > start_daemon.bat

REM ingest_emails.bat
(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python gmail_ingestion.py --max 100
echo pause
) > ingest_emails.bat

REM run_demo.bat
(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python demo_testing_script.py
echo pause
) > run_demo.bat

echo [OK] Startup scripts created

REM Create README
echo.
echo Creating README...
(
echo # AI-Enhanced Email Management System - Windows Installation
echo.
echo ## Quick Start
echo.
echo ### 1. Configure API Keys
echo.
echo Edit `config\config.ini` and add:
echo - Gmail OAuth credentials
echo - Anthropic API key (for AI features^)
echo - Exchange credentials (if using^)
echo.
echo ### 2. Gmail Setup
echo.
echo 1. Go to Google Cloud Console: https://console.cloud.google.com/
echo 2. Create a project
echo 3. Enable Gmail API
echo 4. Create OAuth 2.0 credentials (Desktop app^)
echo 5. Download as `config\gmail_credentials.json`
echo.
echo ### 3. Start the Web Interface
echo.
echo Double-click: `start_web.bat`
echo.
echo Access at: http://localhost:5000
echo.
echo ### 4. Import Emails
echo.
echo Double-click: `ingest_emails.bat`
echo.
echo ### 5. Run Demo (Optional^)
echo.
echo Double-click: `run_demo.bat`
echo.
echo ## Directory Structure
echo.
echo - `config\` - Configuration files
echo - `templates\` - HTML templates
echo - `attachments\` - Email attachments
echo - `bodies\` - Email body content
echo - `logs\` - Application logs
echo - `venv\` - Python virtual environment
echo.
echo ## Support
echo.
echo For issues, check the logs in `logs\` directory.
) > README.md
echo [OK] README created

REM Create .gitignore
echo.
echo Creating .gitignore...
(
echo # Virtual environment
echo venv/
echo.
echo # Configuration with secrets
echo config/config.ini
echo config/*credentials*.json
echo config/*token*.pickle
echo.
echo # Data directories
echo attachments/
echo bodies/
echo html_objects/
echo.
echo # Logs
echo logs/
echo *.log
echo.
echo # Temporary files
echo temp/
echo *.pyc
echo __pycache__/
echo.
echo # OS files
echo Thumbs.db
echo desktop.ini
) > .gitignore
echo [OK] .gitignore created

REM Setup OpenQM files
echo.
echo Setting up OpenQM database files...
echo (This will be done when you run openqm_setup.py^)
echo You can run it manually after installation:
echo   python openqm_setup.py --account %QM_ACCOUNT%
echo.

REM Create Windows service installer script
echo.
echo Creating Windows service installer...
(
echo @echo off
echo REM Install email processor as Windows service
echo REM Requires: NSSM (Non-Sucking Service Manager^)
echo REM Download from: https://nssm.cc/download
echo.
echo set "INSTALL_DIR=%INSTALL_DIR%"
echo set "PYTHON_EXE=%%INSTALL_DIR%%\venv\Scripts\python.exe"
echo set "SCRIPT=%%INSTALL_DIR%%\email_processor_daemon.py"
echo.
echo echo Installing Email Processor as Windows Service...
echo echo.
echo echo Prerequisites:
echo echo - NSSM must be installed and in PATH
echo echo - Download from: https://nssm.cc/download
echo echo.
echo pause
echo.
echo nssm install EmailProcessor "%%PYTHON_EXE%%" "%%SCRIPT%%"
echo nssm set EmailProcessor AppDirectory "%%INSTALL_DIR%%"
echo nssm set EmailProcessor DisplayName "Email Management System Processor"
echo nssm set EmailProcessor Description "AI-Enhanced Email Management Background Processor"
echo nssm set EmailProcessor Start SERVICE_AUTO_START
echo.
echo echo Service installed successfully!
echo echo.
echo echo To start the service:
echo echo   net start EmailProcessor
echo echo.
echo echo To stop the service:
echo echo   net stop EmailProcessor
echo echo.
echo echo To uninstall the service:
echo echo   nssm remove EmailProcessor confirm
echo echo.
echo pause
) > install_service.bat
echo [OK] Service installer created

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Installation directory: %INSTALL_DIR%
echo.
echo Next steps:
echo   1. Edit config\config.ini and add your API keys
echo   2. Set up Gmail OAuth credentials in config\
echo   3. Double-click: run_demo.bat (optional - creates sample data^)
echo   4. Double-click: ingest_emails.bat (import real emails^)
echo   5. Double-click: start_web.bat (start web interface^)
echo.
echo Optional:
echo   - Install as Windows service: install_service.bat
echo   - Requires NSSM: https://nssm.cc/download
echo.
echo Web interface will be available at: http://localhost:5000
echo.
echo [WARNING] Don't forget to configure your API keys in config\config.ini!
echo.
echo ============================================================
echo Happy email managing!
echo ============================================================
echo.
pause
