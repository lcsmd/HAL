@echo off
REM Deploy Full QM Voice Listener
echo Deploying Full QM Voice Listener...
echo.

cd C:\qmsys\bin

echo Step 1: Backup current listener...
qm -account HAL -quiet "COPY BP VOICE.LISTENER BP VOICE.LISTENER.BACKUP"

echo Step 2: Copy full version...
qm -account HAL -quiet "COPY BP VOICE.LISTENER.FULL BP VOICE.LISTENER"

echo Step 3: Compile...
qm -account HAL -quiet "BASIC BP VOICE.LISTENER"

echo Step 4: Catalog...
qm -account HAL -quiet "CATALOG BP VOICE.LISTENER"

echo.
echo Full listener deployed!
echo.
echo NOTE: You need to restart the PHANTOM process:
echo   1. Find the PHANTOM ID: LIST.READU
echo   2. Kill it: KILL.PHANTOM [id]
echo   3. Start new: PHANTOM VOICE.LISTENER
echo.
pause
