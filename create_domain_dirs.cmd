@echo off
REM Create QM directory files for domain organization

cd /d C:\QMSYS\HAL

echo Creating QM directory files...

qm -kHAL -c "CREATE.FILE FIN.BP DIRECTORY"
qm -kHAL -c "CREATE.FILE MED.BP DIRECTORY"
qm -kHAL -c "CREATE.FILE SEC.BP DIRECTORY"
qm -kHAL -c "CREATE.FILE COM.BP DIRECTORY"
qm -kHAL -c "CREATE.FILE UTIL.BP DIRECTORY"

echo.
echo QM directory files created successfully!
echo.
pause
