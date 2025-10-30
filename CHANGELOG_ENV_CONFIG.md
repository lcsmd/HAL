# Environment Configuration Update - Changelog

## Date: October 13, 2025

## Summary

Replaced hardcoded paths in `ask.ai.b` with environment variable configuration to improve portability and maintainability.

## Changes Made

### 1. Modified `HAL.BP\ask.ai.b`

**Before:**
- Hardcoded Python path: `C:\DATA\PYTHON\venv\Scripts\python.exe`
- Hardcoded script path: `C:\DATA\PYTHON\PY\ai_handler.py`
- Hardcoded Ollama host: `ubuai.q.lcs.ai`
- Hardcoded Ollama port: `11434`

**After:**
- Reads `HAL_PYTHON_PATH` environment variable (fallback: `C:\Python312\python.exe`)
- Reads `HAL_SCRIPT_PATH` environment variable (fallback: `C:\QMSYS\HAL\PY\ai_handler.py`)
- Reads `OLLAMA_HOST` environment variable (fallback: `ubuai.q.lcs.ai`)
- Reads `OLLAMA_PORT` environment variable (fallback: `11434`)

### 2. New Files Created

#### Configuration Documentation
- **`CONFIGURATION.md`** - Comprehensive guide for setting environment variables
  - Windows PowerShell instructions
  - Windows Command Prompt instructions
  - Windows GUI instructions
  - Verification steps
  - Troubleshooting guide

#### Setup Scripts
- **`setup_environment.ps1`** - PowerShell script for interactive configuration
  - Prompts for each variable with defaults
  - Validates paths
  - Supports User/Machine/Process scope
  - Provides verification output

- **`setup_environment.bat`** - Batch file for interactive configuration
  - Command Prompt compatible
  - Same functionality as PowerShell version
  - Easier for users without PowerShell

#### Updated Documentation
- **`README.md`** - Updated setup section
  - Added environment configuration as Step 1
  - Documented all three setup options (PowerShell/Batch/Manual)
  - Fixed markdown formatting issues

## Environment Variables

### New Variables

| Variable | Purpose | Default Value |
|----------|---------|---------------|
| `HAL_PYTHON_PATH` | Path to Python executable | `C:\Python312\python.exe` |
| `HAL_SCRIPT_PATH` | Path to AI handler script | `C:\QMSYS\HAL\PY\ai_handler.py` |
| `OLLAMA_HOST` | Ollama server hostname | `ubuai.q.lcs.ai` |
| `OLLAMA_PORT` | Ollama server port | `11434` |

## Benefits

1. **Portability**: System can be deployed on different machines without code changes
2. **Flexibility**: Users can easily switch between Python versions or installations
3. **Maintainability**: Configuration changes don't require recompiling QM Basic programs
4. **Multi-environment**: Different users can have different configurations
5. **Best Practice**: Follows industry standard for configuration management

## Migration Guide

### For Existing Users

1. **Option 1: Use Setup Script (Recommended)**
   ```powershell
   cd C:\QMSYS\HAL
   .\setup_environment.ps1
   ```

2. **Option 2: Manual Configuration**
   - Set environment variables as documented in `CONFIGURATION.md`
   - Restart OpenQM session

3. **Recompile Programs**
   ```qm
   LOGTO HAL
   BASIC HAL.BP ask.ai.b
   CATALOG HAL.BP ask.ai.b
   ```

### For New Users

Follow the updated setup instructions in `README.md`, starting with environment configuration.

## Testing

After configuration:

1. Verify environment variables:
   ```powershell
   echo $env:HAL_PYTHON_PATH
   echo $env:HAL_SCRIPT_PATH
   echo $env:OLLAMA_HOST
   echo $env:OLLAMA_PORT
   ```

2. Test AI integration:
   ```qm
   LOGTO HAL
   ask.b what is 2+2
   ask.b gpt-4o hello
   ask.b claude-3.5-sonnet hello
   ```

## Backward Compatibility

The system maintains backward compatibility through fallback defaults:
- If environment variables are not set, the system uses sensible defaults
- Existing installations will continue to work (though paths may need adjustment)

## Known Issues

None at this time.

## Future Enhancements

Potential improvements for future versions:
1. Configuration file support (`.ini` or `.yaml`)
2. Per-user configuration profiles
3. Configuration validation tool
4. Automatic path detection
5. Integration with OpenQM environment variables

## Related Files

- `HAL.BP\ask.ai.b` - Modified QM Basic program
- `CONFIGURATION.md` - Configuration documentation
- `setup_environment.ps1` - PowerShell setup script
- `setup_environment.bat` - Batch setup script
- `README.md` - Updated main documentation

## Rollback Instructions

If you need to revert to hardcoded paths:

1. Restore the original `ask.ai.b` from backup
2. Or manually edit lines 62-73 to use hardcoded paths
3. Recompile: `BASIC HAL.BP ask.ai.b` and `CATALOG HAL.BP ask.ai.b`
