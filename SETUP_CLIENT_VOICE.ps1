# HAL Voice Client - Complete Setup Script
# Run this on your CLIENT PC

Write-Host "HAL Voice Client Setup" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# For now, let's just use text mode which works perfectly
Write-Host "Voice mode has missing model files from openWakeWord." -ForegroundColor Yellow
Write-Host "Text mode works perfectly and is ready to use!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting text mode client..." -ForegroundColor Cyan
Write-Host ""

# Run simple GUI (text mode)
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python simple_gui.py
