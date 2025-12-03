# Remove large files from git history using git filter-repo
# This rewrites history to exclude large directories

Write-Host "Fixing large files in git history..." -ForegroundColor Cyan
Write-Host ""

# Check if git-filter-repo is available
$hasFilterRepo = git filter-repo --help 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing git-filter-repo..." -ForegroundColor Yellow
    pip install git-filter-repo
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Could not install git-filter-repo" -ForegroundColor Red
        Write-Host "Install manually: pip install git-filter-repo" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "Removing large directories from git history..." -ForegroundColor Yellow
Write-Host "  - LIES/" -ForegroundColor Yellow
Write-Host "  - LCS.TXT/" -ForegroundColor Yellow
Write-Host "  - UPLOADS/" -ForegroundColor Yellow
Write-Host ""

# Remove the large directories from all commits
git filter-repo --path LIES/ --invert-paths --force
git filter-repo --path LCS.TXT/ --invert-paths --force
git filter-repo --path UPLOADS/ --invert-paths --force

Write-Host ""
Write-Host "History rewritten successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Now pushing to GitHub..." -ForegroundColor Cyan

# Re-add the remote (filter-repo removes it)
git remote add origin https://github.com/lcsmd/hal.git

# Force push the cleaned history
git push -u origin main --force

Write-Host ""
Write-Host "Done! Repository pushed to GitHub" -ForegroundColor Green
Write-Host "Visit: https://github.com/lcsmd/hal" -ForegroundColor Cyan
