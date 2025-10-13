# Safe backup script - just copies files, no git operations
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupDir = "C:\QMSYS\HAL_BACKUP_$timestamp"

Write-Host "Creating safe backup at: $backupDir"

# Create backup directory
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Copy important files
Write-Host "Copying HAL.BP files..."
Copy-Item "C:\QMSYS\HAL\HAL.BP\ask.b" "$backupDir\" -Force
Copy-Item "C:\QMSYS\HAL\HAL.BP\ask.ai.b" "$backupDir\" -Force

Write-Host "Copying Python files..."
New-Item -ItemType Directory -Path "$backupDir\PY" -Force | Out-Null
Copy-Item "C:\QMSYS\HAL\PY\ai_handler.py" "$backupDir\PY\" -Force

Write-Host "Copying documentation..."
Copy-Item "C:\QMSYS\HAL\AI_INTEGRATION_SUMMARY.md" "$backupDir\" -Force -ErrorAction SilentlyContinue
Copy-Item "C:\QMSYS\HAL\STUNNEL_SETUP.md" "$backupDir\" -Force -ErrorAction SilentlyContinue

Write-Host "`n✓ Backup complete!"
Write-Host "Location: $backupDir"
Write-Host "`nYour working files are safely backed up."
