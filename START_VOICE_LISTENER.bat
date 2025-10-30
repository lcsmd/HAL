@echo off
echo Starting QM Voice Listener...
cd C:\qmsys\bin
qm -account HAL -command "PHANTOM VOICE.LISTENER"
echo.
echo Voice Listener should now be running as a phantom process.
echo Check with: LIST.READU
pause
