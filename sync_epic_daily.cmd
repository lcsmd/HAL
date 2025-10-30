@echo off
REM Epic FHIR API Daily Sync
REM Run this via Windows Task Scheduler

cd /d C:\QMSYS\HAL

REM Create logs directory if needed
if not exist logs mkdir logs

REM Run sync and log output
echo ================================================ >> logs\epic_sync.log
echo Sync started: %date% %time% >> logs\epic_sync.log
echo ================================================ >> logs\epic_sync.log

python PY\epic_api_sync.py P001 >> logs\epic_sync.log 2>&1

echo. >> logs\epic_sync.log
echo Sync completed: %date% %time% >> logs\epic_sync.log
echo. >> logs\epic_sync.log
