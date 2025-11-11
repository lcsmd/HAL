@echo off
echo Starting QM Voice Listener (Medium Version)...
cd C:\qmsys\bin
start /min qm HAL -c "PHANTOM BP VOICE.LISTENER"
timeout /t 3 /nobreak >nul
echo Listener should be starting...
echo Check with: netstat -an | findstr 8767
