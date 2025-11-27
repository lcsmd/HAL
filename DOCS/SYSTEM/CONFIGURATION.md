# HAL Configuration Guide

## Environment Variables

The HAL system now uses environment variables for configuration instead of hardcoded paths. This makes the system more portable and easier to configure.

### Required Environment Variables

#### Python Configuration
- **HAL_PYTHON_PATH**: Path to Python executable
  - Default: `C:\Python312\python.exe`
  - Example: `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe`

- **HAL_SCRIPT_PATH**: Path to the AI handler Python script
  - Default: `C:\QMSYS\HAL\PY\ai_handler.py`
  - Example: `C:\QMSYS\HAL\PY\ai_handler.py`

#### Ollama Configuration
- **OLLAMA_HOST**: Hostname or IP address of Ollama server
  - Default: `ubuai.q.lcs.ai`
  - Example: `ubuai.q.lcs.ai` or `192.168.1.100`

- **OLLAMA_PORT**: Port number for Ollama server
  - Default: `11434`
  - Example: `11434`

### Setting Environment Variables

#### Windows (PowerShell)
```powershell
# Set for current session
$env:HAL_PYTHON_PATH = "C:\Python312\python.exe"
$env:HAL_SCRIPT_PATH = "C:\QMSYS\HAL\PY\ai_handler.py"
$env:OLLAMA_HOST = "ubuai.q.lcs.ai"
$env:OLLAMA_PORT = "11434"

# Set permanently (User level)
[System.Environment]::SetEnvironmentVariable("HAL_PYTHON_PATH", "C:\Python312\python.exe", "User")
[System.Environment]::SetEnvironmentVariable("HAL_SCRIPT_PATH", "C:\QMSYS\HAL\PY\ai_handler.py", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "ubuai.q.lcs.ai", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_PORT", "11434", "User")

# Set permanently (System level - requires admin)
[System.Environment]::SetEnvironmentVariable("HAL_PYTHON_PATH", "C:\Python312\python.exe", "Machine")
[System.Environment]::SetEnvironmentVariable("HAL_SCRIPT_PATH", "C:\QMSYS\HAL\PY\ai_handler.py", "Machine")
[System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "ubuai.q.lcs.ai", "Machine")
[System.Environment]::SetEnvironmentVariable("OLLAMA_PORT", "11434", "Machine")
```

#### Windows (Command Prompt)
```cmd
REM Set for current session
set HAL_PYTHON_PATH=C:\Python312\python.exe
set HAL_SCRIPT_PATH=C:\QMSYS\HAL\PY\ai_handler.py
set OLLAMA_HOST=ubuai.q.lcs.ai
set OLLAMA_PORT=11434

REM Set permanently (requires admin for system-wide)
setx HAL_PYTHON_PATH "C:\Python312\python.exe"
setx HAL_SCRIPT_PATH "C:\QMSYS\HAL\PY\ai_handler.py"
setx OLLAMA_HOST "ubuai.q.lcs.ai"
setx OLLAMA_PORT "11434"
```

#### Windows (GUI)
1. Right-click "This PC" or "My Computer" → Properties
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables" or "System variables", click "New"
5. Add each variable name and value
6. Click OK to save

### Verification

To verify your environment variables are set correctly:

```powershell
# PowerShell
echo $env:HAL_PYTHON_PATH
echo $env:HAL_SCRIPT_PATH
echo $env:OLLAMA_HOST
echo $env:OLLAMA_PORT
```

```cmd
REM Command Prompt
echo %HAL_PYTHON_PATH%
echo %HAL_SCRIPT_PATH%
echo %OLLAMA_HOST%
echo %OLLAMA_PORT%
```

### Fallback Behavior

If environment variables are not set, the system will use these defaults:
- **HAL_PYTHON_PATH**: `C:\Python312\python.exe`
- **HAL_SCRIPT_PATH**: `C:\QMSYS\HAL\PY\ai_handler.py`
- **OLLAMA_HOST**: `ubuai.q.lcs.ai`
- **OLLAMA_PORT**: `11434`

### Configuration Priority

1. Environment variables (highest priority)
2. Default values (fallback)

### Troubleshooting

#### Python not found
If you get "Python not found" errors:
1. Verify Python is installed: `python --version`
2. Find Python path: `where python` (Windows)
3. Set HAL_PYTHON_PATH to the correct path

#### Script not found
If you get "Script not found" errors:
1. Verify the script exists: `dir C:\QMSYS\HAL\PY\ai_handler.py`
2. Set HAL_SCRIPT_PATH to the correct path

#### Ollama connection errors
If you get Ollama connection errors:
1. Verify Ollama is running: `curl http://ubuai.q.lcs.ai:11434/api/tags`
2. Check OLLAMA_HOST and OLLAMA_PORT settings
3. Verify firewall allows connections
4. Ensure network connectivity to the Ollama server

### Recompiling After Configuration Changes

After setting environment variables, you may need to restart your OpenQM session:
```
LOGTO HAL
```

The changes will take effect immediately for new QM Basic program executions.

### Advanced Configuration

For more advanced configuration options, see:
- `PY/config.py` - Python configuration
- `.env` - Environment file for Python scripts
- `API.KEYS` file in OpenQM - API key storage

## Security Notes

- Never commit environment variables containing API keys to version control
- Use Windows credential manager for sensitive data when possible
- Restrict file permissions on configuration files
- Consider using encrypted environment variables for production systems
