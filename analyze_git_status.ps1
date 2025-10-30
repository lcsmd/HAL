# Analyze git status and categorize changes
Write-Host "=== Git Status Analysis ===" -ForegroundColor Cyan

$status = git status --short
$deleted = $status | Where-Object { $_ -match '^ D ' }
$untracked = $status | Where-Object { $_ -match '^\?\?' }
$modified = $status | Where-Object { $_ -match '^ M ' }

Write-Host "`nTotal files:" -ForegroundColor Yellow
Write-Host "  Deleted: $($deleted.Count)"
Write-Host "  Untracked: $($untracked.Count)"  
Write-Host "  Modified: $($modified.Count)"

Write-Host "`nDeleted files by category:" -ForegroundColor Yellow
$lcs = $deleted | Where-Object { $_ -match 'LCS' }
$yt = $deleted | Where-Object { $_ -match 'YT' }
$hal = $deleted | Where-Object { $_ -match 'HAL\.BP' }
$ai = $deleted | Where-Object { $_ -match 'AI\.BP' }
$py = $deleted | Where-Object { $_ -match 'PY/' }

Write-Host "  LCS* (legacy system): $($lcs.Count)"
Write-Host "  YT* (YouTube): $($yt.Count)"
Write-Host "  HAL.BP: $($hal.Count)"
Write-Host "  AI.BP: $($ai.Count)"
Write-Host "  PY/: $($py.Count)"
Write-Host "  Other: $(($deleted.Count - $lcs.Count - $yt.Count - $hal.Count - $ai.Count - $py.Count))"

Write-Host "`nUntracked files by category:" -ForegroundColor Yellow
$newBP = $untracked | Where-Object { $_ -match 'BP/' }
$newPY = $untracked | Where-Object { $_ -match 'PY/' }
$newEQU = $untracked | Where-Object { $_ -match 'EQU/' }
$newData = $untracked | Where-Object { $_ -match '\w+/' -and $_ -notmatch '(BP|PY|EQU)/' }
$newDocs = $untracked | Where-Object { $_ -match '\.md$' }

Write-Host "  BP/ programs: $($newBP.Count)"
Write-Host "  PY/ scripts: $($newPY.Count)"
Write-Host "  EQU/ headers: $($newEQU.Count)"
Write-Host "  Data files: $($newData.Count)"
Write-Host "  Documentation: $($newDocs.Count)"

Write-Host "`nRecommendation:" -ForegroundColor Green
Write-Host "  1. Commit deletion of legacy files (LCS, old AI.BP, etc.)"
Write-Host "  2. Add new files (BP, PY, EQU, data, docs)"
Write-Host "  3. Clean commit message describing reorganization"

Write-Host "`nSuggested commands:" -ForegroundColor Cyan
Write-Host "  git add -A  # Stage all changes"
Write-Host "  git status  # Review what will be committed"
Write-Host "  git commit -m 'Clean up repository: remove legacy files, add new schema system'"
