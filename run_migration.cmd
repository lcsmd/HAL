@echo off
REM HAL Code Reorganization - Run Migration
REM This script runs the QM migration programs

cd /d C:\QMSYS\HAL

echo.
echo ========================================
echo HAL Code Reorganization
echo ========================================
echo.
echo Step 1: Creating QM directory files...
echo.

qm -kHAL -c "BASIC ONCE.BP CREATE.DOMAIN.DIRS"
qm -kHAL -c "RUN ONCE.BP CREATE.DOMAIN.DIRS"

echo.
echo Step 2: Running migration program...
echo.
echo You will be prompted to confirm (type YES)
echo.

qm -kHAL -c "BASIC ONCE.BP MIGRATE.REORGANIZE"
qm -kHAL -c "RUN ONCE.BP MIGRATE.REORGANIZE"

echo.
echo ========================================
echo Migration Complete!
echo ========================================
echo.
echo Review the migration report:
echo   MIGRATION.REPORT.txt
echo.
echo Next steps:
echo   1. Compile programs: BASIC FIN.BP *
echo   2. Catalog programs: CATALOG FIN.BP *
echo   3. Test functionality
echo.
pause
