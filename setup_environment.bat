@echo off
REM HAL Environment Setup Script (Batch version)
REM This script configures environment variables for the HAL AI Assistant

echo =============================================
echo HAL AI Assistant - Environment Configuration
echo =============================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges.
    set ADMIN=1
) else (
    echo Running without administrator privileges.
    echo System-wide variables will not be available.
    set ADMIN=0
)
echo.

REM Get Python path
set DEFAULT_PYTHON=C:\Python312\python.exe
echo Python executable path
echo Current default: %DEFAULT_PYTHON%
set /p PYTHON_PATH="Enter path (press Enter for default): "
if "%PYTHON_PATH%"=="" set PYTHON_PATH=%DEFAULT_PYTHON%

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo WARNING: Python executable not found at: %PYTHON_PATH%
    echo Please verify the path is correct.
)
echo.

REM Get Script path
set DEFAULT_SCRIPT=C:\QMSYS\HAL\PY\ai_handler.py
echo AI handler script path
echo Current default: %DEFAULT_SCRIPT%
set /p SCRIPT_PATH="Enter path (press Enter for default): "
if "%SCRIPT_PATH%"=="" set SCRIPT_PATH=%DEFAULT_SCRIPT%

REM Check if script exists
if not exist "%SCRIPT_PATH%" (
    echo WARNING: Script not found at: %SCRIPT_PATH%
    echo Please verify the path is correct.
)
echo.

REM Get Ollama host
set DEFAULT_HOST=ubuai.q.lcs.ai
echo Ollama server hostname or IP
echo Current default: %DEFAULT_HOST%
set /p OLLAMA_HOST_VAR="Enter hostname (press Enter for default): "
if "%OLLAMA_HOST_VAR%"=="" set OLLAMA_HOST_VAR=%DEFAULT_HOST%
echo.

REM Get Ollama port
set DEFAULT_PORT=11434
echo Ollama server port
echo Current default: %DEFAULT_PORT%
set /p OLLAMA_PORT_VAR="Enter port (press Enter for default): "
if "%OLLAMA_PORT_VAR%"=="" set OLLAMA_PORT_VAR=%DEFAULT_PORT%
echo.

echo =====================
echo Configuration Summary
echo =====================
echo HAL_PYTHON_PATH: %PYTHON_PATH%
echo HAL_SCRIPT_PATH: %SCRIPT_PATH%
echo OLLAMA_HOST: %OLLAMA_HOST_VAR%
echo OLLAMA_PORT: %OLLAMA_PORT_VAR%
echo.

echo Setting environment variables...
echo.

REM Set for current session
set HAL_PYTHON_PATH=%PYTHON_PATH%
set HAL_SCRIPT_PATH=%SCRIPT_PATH%
set OLLAMA_HOST=%OLLAMA_HOST_VAR%
set OLLAMA_PORT=%OLLAMA_PORT_VAR%

REM Set permanently for user
setx HAL_PYTHON_PATH "%PYTHON_PATH%" >nul 2>&1
setx HAL_SCRIPT_PATH "%SCRIPT_PATH%" >nul 2>&1
setx OLLAMA_HOST "%OLLAMA_HOST_VAR%" >nul 2>&1
setx OLLAMA_PORT "%OLLAMA_PORT_VAR%" >nul 2>&1

if %errorLevel% == 0 (
    echo Environment variables set successfully for current user.
) else (
    echo WARNING: Failed to set permanent environment variables.
    echo Variables are set for current session only.
)
echo.

echo Verification:
echo HAL_PYTHON_PATH = %HAL_PYTHON_PATH%
echo HAL_SCRIPT_PATH = %HAL_SCRIPT_PATH%
echo OLLAMA_HOST = %OLLAMA_HOST%
echo OLLAMA_PORT = %OLLAMA_PORT%
echo.

echo Configuration completed!
echo.
echo NOTE: You may need to restart OpenQM or your terminal
echo       for permanent changes to take effect.
echo.

pause
