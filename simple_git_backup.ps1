# Simple git backup - just the important files
$RepoPath   = "C:\QMSYS\HAL"
$RemoteName = "origin"
$BranchName = "main"

Set-Location $RepoPath

Write-Host "=== Git Backup - Important Files Only ===" -ForegroundColor Green
Write-Host ""

# Fix ownership
git config --global --add safe.directory C:/QMSYS/HAL 2>$null

# Important files to backup
$files = @(
    "HAL.BP/ask.b",
    "HAL.BP/ask.ai.b",
    "PY/ai_handler.py",
    "AI_INTEGRATION_SUMMARY.md",
    "safe_backup.ps1"
)

Write-Host "Files to commit:" -ForegroundColor Cyan
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  + $file" -ForegroundColor Green
    } else {
        Write-Host "  - $file (not found)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=== Commands to run ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "# Add the important files:" -ForegroundColor Cyan
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "git add `"$file`""
    }
}
Write-Host ""
Write-Host "# Commit:" -ForegroundColor Cyan
Write-Host "git commit -m `"Working AI integration - ask.b with Python for OpenAI/Anthropic`""
Write-Host ""
Write-Host "# Push:" -ForegroundColor Cyan
Write-Host "git push $RemoteName $BranchName"
Write-Host ""
Write-Host "Copy and paste these commands to backup your work." -ForegroundColor Green
