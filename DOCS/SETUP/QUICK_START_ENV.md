# Quick Start - Environment Configuration

## 🚀 Fast Setup (2 minutes)

### Step 1: Run Setup Script

**PowerShell:**
```powershell
cd C:\QMSYS\HAL
.\setup_environment.ps1
```

**Command Prompt:**
```cmd
cd C:\QMSYS\HAL
setup_environment.bat
```

### Step 2: Recompile (if updating existing installation)

```qm
LOGTO HAL
BASIC HAL.BP ask.ai.b
CATALOG HAL.BP ask.ai.b
```

### Step 3: Test

```qm
ask.b what is 2+2
```

## 📋 Environment Variables Reference

| Variable | What It Does | Example |
|----------|--------------|---------|
| `HAL_PYTHON_PATH` | Python location | `C:\Python312\python.exe` |
| `HAL_SCRIPT_PATH` | AI script location | `C:\QMSYS\HAL\PY\ai_handler.py` |
| `OLLAMA_HOST` | Ollama server | `ubuai.q.lcs.ai` |
| `OLLAMA_PORT` | Ollama port | `11434` |

## 🔧 Manual Setup (PowerShell)

```powershell
# Set variables
$env:HAL_PYTHON_PATH = "C:\Python312\python.exe"
$env:HAL_SCRIPT_PATH = "C:\QMSYS\HAL\PY\ai_handler.py"
$env:OLLAMA_HOST = "ubuai.q.lcs.ai"
$env:OLLAMA_PORT = "11434"

# Make permanent
[System.Environment]::SetEnvironmentVariable("HAL_PYTHON_PATH", "C:\Python312\python.exe", "User")
[System.Environment]::SetEnvironmentVariable("HAL_SCRIPT_PATH", "C:\QMSYS\HAL\PY\ai_handler.py", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "ubuai.q.lcs.ai", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_PORT", "11434", "User")
```

## ✅ Verify Setup

```powershell
# Check variables
echo $env:HAL_PYTHON_PATH
echo $env:HAL_SCRIPT_PATH
echo $env:OLLAMA_HOST
echo $env:OLLAMA_PORT

# Test Python
& $env:HAL_PYTHON_PATH --version

# Test script exists
Test-Path $env:HAL_SCRIPT_PATH
```

## 🐛 Troubleshooting

### Python not found
```powershell
# Find Python
where.exe python
# Set correct path
$env:HAL_PYTHON_PATH = "C:\Path\To\python.exe"
```

### Script not found
```powershell
# Verify script location
dir C:\QMSYS\HAL\PY\ai_handler.py
# Set correct path
$env:HAL_SCRIPT_PATH = "C:\QMSYS\HAL\PY\ai_handler.py"
```

### Ollama connection failed
```powershell
# Test Ollama
curl http://ubuai.q.lcs.ai:11434/api/tags
# Update host/port if needed
$env:OLLAMA_HOST = "ubuai.q.lcs.ai"
$env:OLLAMA_PORT = "11434"
```

## 📚 More Information

- Full guide: [CONFIGURATION.md](CONFIGURATION.md)
- Main docs: [README.md](README.md)
- Changes: [CHANGELOG_ENV_CONFIG.md](CHANGELOG_ENV_CONFIG.md)

## 💡 Pro Tips

1. **Use the setup scripts** - They handle everything automatically
2. **Restart your terminal** after setting permanent variables
3. **Test immediately** after configuration
4. **Keep defaults** if you're unsure - they work for most setups
