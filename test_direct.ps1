$output = & "C:\QMSYS\bin\qm.exe" -account HAL -command "LIST IMPORT.LOG" 2>&1
Write-Host "Direct execution:"
Write-Host $output
