@echo off
echo Running HAL test suite...
echo ==================================================
echo HAL Setup and Connection Test
echo ==================================================
echo.

REM Create local directory if it doesn't exist
if not exist "C:\HAL" (
    echo Creating local HAL directory...
    mkdir "C:\HAL"
)
if not exist "C:\HAL\PY" (
    mkdir "C:\HAL\PY"
)

REM Copy all Python files from remote to local
echo Copying files to local directory...
xcopy /y /i "\\mv1.q.lcs.ai\C\QMSYS\HAL\PY\*.py" "C:\HAL\PY"
xcopy /y /i "\\mv1.q.lcs.ai\C\QMSYS\HAL\PY\*.txt" "C:\HAL\PY"
xcopy /y /i "\\mv1.q.lcs.ai\C\QMSYS\HAL\PY\*.bat" "C:\HAL\PY"

REM Change to local directory
cd /d C:\HAL\PY

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call "venv\Scripts\activate.bat"

REM Install core dependencies first
echo Installing core dependencies...
python -m pip install --upgrade pip
python -m pip install python-dotenv==1.0.0 websockets==12.0
python -m pip install numpy==1.24.3
python -m pip install sounddevice==0.4.6 PyAudio==0.2.14

REM Install wake word and visualization dependencies
echo Installing wake word and visualization dependencies...
python -m pip install pvporcupine==2.2.1 tqdm==4.66.1

REM Install remaining requirements
echo Installing remaining requirements...
python -m pip install -r requirements.txt

REM Run setup checks
python setup.py

REM If setup was successful, run voice test
if %ERRORLEVEL% EQU 0 (
    echo.
    REM Verify critical packages are installed
    python -c "import numpy, sounddevice, dotenv, websockets, pvporcupine" 2>nul
    if errorlevel 1 (
        echo Error: One or more critical packages are not properly installed.
        echo Please check your Python environment.
        pause
        exit /b 1
    )
    echo Press any key to start voice test...
    pause >nul
    python test_voice.py
) else (
    echo Setup failed. Please check the errors above.
    pause
)
