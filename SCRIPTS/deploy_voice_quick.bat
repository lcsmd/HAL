@echo off
echo ========================================
echo Quick Deploy: voice.lcs.ai Backend
echo ========================================
echo.
echo This will SSH to ubu6 and configure HAProxy
echo Password: apgar-66
echo.
pause
echo.

REM Change to scripts directory
cd /d "%~dp0"

REM Run PowerShell script
powershell.exe -ExecutionPolicy Bypass -File "deploy_voice_backend.ps1"

pause
