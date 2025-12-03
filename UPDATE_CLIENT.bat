@echo off
title Update HAL Client
echo ================================================
echo HAL Client Update Script
echo ================================================
echo.
echo This will copy the updated client files from:
echo   C:\qmsys\hal\voice_assistant_v2\client\
echo.
echo To your client directory at:
echo   C:\HAL\VOICE_ASSISTANT_V2\CLIENT\
echo.
pause

REM Check if source directory exists
if not exist "C:\qmsys\hal\voice_assistant_v2\client" (
    echo [ERROR] Source directory not found!
    echo Are you running this on the HAL server?
    pause
    exit /b 1
)

REM Check if destination directory exists
if not exist "C:\HAL\VOICE_ASSISTANT_V2\CLIENT" (
    echo [ERROR] Client directory not found at C:\HAL\VOICE_ASSISTANT_V2\CLIENT
    echo.
    echo Please create it first or run this on the client PC after copying files.
    pause
    exit /b 1
)

echo.
echo Copying updated files...
echo.

REM Copy the main client file
echo [1/4] Copying hal_voice_client_gui.py...
copy /Y "C:\qmsys\hal\voice_assistant_v2\client\hal_voice_client_gui.py" "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\"

REM Copy the launcher
echo [2/4] Copying START_CLIENT.bat...
copy /Y "C:\qmsys\hal\voice_assistant_v2\client\START_CLIENT.bat" "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\"

REM Copy other Python files
echo [3/4] Copying other client files...
copy /Y "C:\qmsys\hal\voice_assistant_v2\client\hal_voice_client.py" "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\" 2>nul
copy /Y "C:\qmsys\hal\voice_assistant_v2\client\voice_client.py" "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\" 2>nul
copy /Y "C:\qmsys\hal\voice_assistant_v2\client\requirements.txt" "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\" 2>nul

REM Copy documentation
echo [4/4] Copying documentation...
copy /Y "C:\qmsys\hal\voice_assistant_v2\client\GUI_CLIENT.md" "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\" 2>nul
copy /Y "C:\qmsys\hal\voice_assistant_v2\client\READY_TO_USE.md" "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\" 2>nul

echo.
echo ================================================
echo Update Complete!
echo ================================================
echo.
echo The client at C:\HAL\VOICE_ASSISTANT_V2\CLIENT\ has been updated.
echo.
echo You can now run:
echo   cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
echo   START_CLIENT.bat
echo.
echo Or:
echo   python hal_voice_client_gui.py
echo.
pause
