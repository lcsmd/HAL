@echo off
REM Test compilation of documentation programs

echo Starting QM and compiling programs...
echo.

qm -qhal << EOF
LOGTO HAL
BASIC BP VIEW.DOC
BASIC BP FIND.DOC  
BASIC BP TEST.DOC.ACCESS
CATALOG BP VIEW.DOC
CATALOG BP FIND.DOC
CATALOG BP TEST.DOC.ACCESS
QUIT
EOF

echo.
echo Compilation complete!
pause
