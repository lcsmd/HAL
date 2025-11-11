@echo off
echo Starting QM Voice Listener...
cd C:\qmsys\bin
echo LOGTO HAL > "%TEMP%\qm_startup.txt"
echo BASIC BP VOICE.LISTENER >> "%TEMP%\qm_startup.txt"
echo CATALOG BP VOICE.LISTENER >> "%TEMP%\qm_startup.txt"
echo PHANTOM BP VOICE.LISTENER >> "%TEMP%\qm_startup.txt"
type "%TEMP%\qm_startup.txt" | qm HAL
del "%TEMP%\qm_startup.txt"
echo Done!
timeout /t 3
