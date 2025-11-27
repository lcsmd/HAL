@echo off
REM Test compilation of documentation programs

echo Starting QM and compiling programs...
echo.

qm -qhal << EOF
LOGTO HAL
BASIC BP VIEW.DOC
BASIC BP FIND.DOC  
BASIC BP TEST.DOC.ACCESS
CATALOG BP VIEW.DOC LOCAL
CATALOG BP FIND.DOC LOCAL
CATALOG BP TEST.DOC.ACCESS LOCAL
QUIT
EOF

echo.
echo Compilation complete!
pause
