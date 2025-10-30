# Safe cleanup of empty Windows directories
# This script ONLY deletes directories if they are completely empty

$directories = @("FIN.BP", "FIN.PY", "MED.BP", "MED.PY", "SEC.BP", "SEC.PY", "COM.BP", "COM.PY", "UTIL.BP", "UTIL.PY")

Write-Host "Checking directories for safe deletion..." -ForegroundColor Cyan
Write-Host ""

foreach ($dir in $directories) {
    $path = Join-Path $PSScriptRoot $dir
    
    if (Test-Path $path) {
        $items = Get-ChildItem $path -Force
        
        if ($items.Count -eq 0) {
            Write-Host "EMPTY: $dir - SAFE TO DELETE" -ForegroundColor Green
            Remove-Item $path -Force
            Write-Host "  Deleted: $dir" -ForegroundColor Yellow
        } else {
            Write-Host "HAS FILES: $dir - KEEPING (contains $($items.Count) items)" -ForegroundColor Red
            Write-Host "  Files:" -ForegroundColor Red
            $items | ForEach-Object { Write-Host "    - $($_.Name)" -ForegroundColor Red }
        }
    } else {
        Write-Host "NOT FOUND: $dir - Skipping" -ForegroundColor Gray
    }
    Write-Host ""
}

Write-Host "Cleanup complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Run QM commands to create proper directory files" -ForegroundColor Yellow
