# Remove all files that might contain API keys from git history

Write-Host "Removing files with potential secrets from git history..." -ForegroundColor Yellow
Write-Host ""

# List of file patterns that might contain secrets
$secretPatterns = @(
    "*.env",
    "PY/.env",
    "API.KEYS",
    "*api_key*",
    "*API_KEY*",
    "*token*",
    "*secret*",
    "*password*",
    "config/*_tokens.json"
)

foreach ($pattern in $secretPatterns) {
    Write-Host "Checking for: $pattern" -ForegroundColor Cyan
    git filter-repo --path-glob "$pattern" --invert-paths --force 2>$null
}

Write-Host ""
Write-Host "Re-adding remote..." -ForegroundColor Cyan
git remote add origin https://github.com/lcsmd/HAL.git

Write-Host ""
Write-Host "Pushing cleaned history..." -ForegroundColor Cyan
git push -u origin main --force

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
