@echo off
echo ============================================
echo Deploy voice.lcs.ai to HAProxy
echo ============================================
echo.
echo This will SSH to ubu6 and configure HAProxy
echo You'll be asked for password: apgar-66
echo.
echo Press Ctrl+C to cancel, or
pause
echo.

echo Connecting to ubu6...
ssh -p 2222 lawr@ubu6 "bash -s" < "%~dp0add_voice_backend.sh"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo SUCCESS! voice.lcs.ai is configured!
    echo ============================================
    echo.
    echo Next: Test with wscat -c wss://voice.lcs.ai
) else (
    echo.
    echo ============================================
    echo Failed to configure HAProxy
    echo ============================================
    echo.
    echo Try manual method - see APPLY_HAPROXY_CONFIG.md
)

echo.
pause
