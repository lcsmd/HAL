@echo off
REM Start QM Voice Listener
REM This starts the listener as a PHANTOM process in QM

cd C:\qmsys\bin

echo Starting QM Voice Listener...
echo.
echo Commands to run in QM:
echo   LOGTO HAL
echo   COPY BP VOICE.LISTENER.MINIMAL BP VOICE.LISTENER OVERWRITING
echo   BASIC BP VOICE.LISTENER
echo   CATALOG BP VOICE.LISTENER  
echo   PHANTOM BP VOICE.LISTENER
echo.
echo Then test with: python C:\qmsys\hal\tests\test_text_input.py
echo.

qm HAL
