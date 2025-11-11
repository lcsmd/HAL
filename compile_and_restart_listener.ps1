# Compile and restart QM Voice Listener with full version
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "Compiling and Restarting QM Voice Listener (Full Version)" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Already copied, now compile
Write-Host "Step 1: Compiling VOICE.LISTENER..." -ForegroundColor Yellow
$compileOutput = & "C:\qmsys\bin\qm.exe" HAL "BASIC BP VOICE.LISTENER" 2>&1
Write-Host $compileOutput
Write-Host "Done." -ForegroundColor Green
Write-Host ""

# Step 2: Catalog
Write-Host "Step 2: Cataloging VOICE.LISTENER..." -ForegroundColor Yellow
$catalogOutput = & "C:\qmsys\bin\qm.exe" HAL "CATALOG BP VOICE.LISTENER" 2>&1
Write-Host $catalogOutput
Write-Host "Done." -ForegroundColor Green
Write-Host ""

# Step 3: Find and kill current phantom
Write-Host "Step 3: Finding current VOICE.LISTENER phantom..." -ForegroundColor Yellow
$phantomList = & "C:\qmsys\bin\qm.exe" HAL "LIST.READU" 2>&1
Write-Host $phantomList
Write-Host ""

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "Manual Step Required:" -ForegroundColor Red
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "1. Look at the LIST.READU output above"
Write-Host "2. Find the phantom number for VOICE.LISTENER"
Write-Host "3. Run: qm HAL 'KILL.PHANTOM [number]'"
Write-Host "4. Run: qm HAL 'PHANTOM VOICE.LISTENER'"
Write-Host ""
Write-Host "OR: The current listener may work without restart (will pick up on next request)"
Write-Host ""
