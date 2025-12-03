@echo off
REM Copy sound files from existing HAL clients directory
REM Run this if sound files are missing or need to be updated

setlocal

set "CLIENTS_DIR=..\..\clients"

echo ============================================
echo Copying Sound Files
echo ============================================
echo.

if not exist "%CLIENTS_DIR%" (
    echo ERROR: Clients directory not found at: %CLIENTS_DIR%
    echo Please adjust the path in this script or copy files manually
    pause
    exit /b 1
)

echo Source directory: %CLIENTS_DIR%
echo Target directory: %cd%
echo.

REM Copy activation sound
if exist "%CLIENTS_DIR%\activation.mp3" (
    copy /Y "%CLIENTS_DIR%\activation.mp3" activation.mp3
    echo + Copied activation.mp3 (TNG Star Trek sound)
) else (
    echo x activation.mp3 not found
)

REM Copy acknowledgement sound
if exist "%CLIENTS_DIR%\acknowledgement.wav" (
    copy /Y "%CLIENTS_DIR%\acknowledgement.wav" acknowledgement.wav
    echo + Copied acknowledgement.wav
) else if exist "%CLIENTS_DIR%\ack.wav" (
    copy /Y "%CLIENTS_DIR%\ack.wav" acknowledgement.wav
    echo + Copied ack.wav -^> acknowledgement.wav
) else (
    echo x acknowledgement.wav not found
)

REM Optional: Copy error sound if it exists
if exist "%CLIENTS_DIR%\error.wav" (
    copy /Y "%CLIENTS_DIR%\error.wav" error.wav
    echo + Copied error.wav
)

echo.
echo Sound files copied successfully!
echo.
echo Files in current directory:
dir /B *.wav *.mp3 2>nul || echo No sound files found
echo.
pause
