@echo off
echo Testing PASSWORD.MENU compilation...
echo.

qm -kHAL -cLIST VOC PASSWORD.MENU

echo.
echo Checking if program is cataloged...
qm -kHAL -c"CT VOC PASSWORD.MENU"

echo.
echo Done!
pause
