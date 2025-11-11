# Compile and start Voice Listener
# This script attempts to automate QM compilation

Write-Host "Compiling VOICE.LISTENER..." -ForegroundColor Cyan

# Try to compile using QM's batch mode
$qmPath = "C:\qmsys\bin\qm.exe"
$accountPath = "C:\qmsys\hal"

# Create a temporary TCL script for QM to execute
$tclScript = @"
LOGTO HAL
COPY BP VOICE.LISTENER.MINIMAL BP VOICE.LISTENER OVERWRITING
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
PHANTOM BP VOICE.LISTENER
QUIT
"@

$tclFile = "C:\qmsys\hal\compile_listener.tcl"
$tclScript | Out-File -FilePath $tclFile -Encoding ASCII

Write-Host "Attempting to execute QM commands..." -ForegroundColor Yellow
Write-Host ""

# Try different methods to execute
try {
    # Method 1: Pipe to qm
    Get-Content $tclFile | & $qmPath HAL 2>&1
} catch {
    Write-Host "Method 1 failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "If automatic compilation failed, run manually:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  cd C:\qmsys\bin" -ForegroundColor White
Write-Host "  qm HAL" -ForegroundColor White
Write-Host ""
Write-Host "Then in QM shell:" -ForegroundColor Yellow
Write-Host "  LOGTO HAL" -ForegroundColor White
Write-Host "  BASIC BP VOICE.LISTENER" -ForegroundColor White
Write-Host "  CATALOG BP VOICE.LISTENER" -ForegroundColor White
Write-Host "  PHANTOM BP VOICE.LISTENER" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# Check if listener is running
Start-Sleep -Seconds 3
$listening = netstat -an | Select-String ":8767.*LISTENING"
if ($listening) {
    Write-Host "SUCCESS: QM Listener is running on port 8767!" -ForegroundColor Green
} else {
    Write-Host "QM Listener not detected on port 8767" -ForegroundColor Red
    Write-Host "Please start manually using commands above" -ForegroundColor Yellow
}
