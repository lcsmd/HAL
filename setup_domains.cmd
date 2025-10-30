@echo off
echo Compiling SETUP.DOMAINS...
qm -kHAL -c"BASIC BP SETUP.DOMAINS"
if errorlevel 1 (
    echo Compilation failed!
    pause
    exit /b 1
)

echo.
echo Cataloging SETUP.DOMAINS...
qm -kHAL -c"CATALOG BP SETUP.DOMAINS"
if errorlevel 1 (
    echo Catalog failed!
    pause
    exit /b 1
)

echo.
echo Running SETUP.DOMAINS...
qm -kHAL -c"SETUP.DOMAINS"

echo.
echo Done!
pause
