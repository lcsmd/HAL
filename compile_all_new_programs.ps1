# Compile all BASIC programs created/modified today
# Reports compilation results

Write-Host "Compiling All New/Modified OpenQM BASIC Programs" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

$programs = @(
    "VIEW.DOC",
    "FIND.DOC",
    "TEST.DOC.ACCESS"
)

$results = @()

foreach ($prog in $programs) {
    Write-Host "Compiling $prog..." -NoNewline
    
    $output = & qm -qhal -k"BASIC BP $prog" 2>&1
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Host " SUCCESS" -ForegroundColor Green
        
        # Try to catalog (LOCAL for account-specific)
        Write-Host "  Cataloging $prog LOCAL..." -NoNewline
        $catOutput = & qm -qhal -k"CATALOG BP $prog LOCAL" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host " SUCCESS" -ForegroundColor Green
            $results += [PSCustomObject]@{
                Program = $prog
                Compile = "SUCCESS"
                Catalog = "SUCCESS"
            }
        } else {
            Write-Host " FAILED" -ForegroundColor Yellow
            Write-Host "  Output: $catOutput" -ForegroundColor Yellow
            $results += [PSCustomObject]@{
                Program = $prog
                Compile = "SUCCESS"
                Catalog = "FAILED"
            }
        }
    } else {
        Write-Host " FAILED" -ForegroundColor Red
        Write-Host "  Output: $output" -ForegroundColor Red
        $results += [PSCustomObject]@{
            Program = $prog
            Compile = "FAILED"
            Catalog = "N/A"
        }
    }
    Write-Host ""
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "=" * 70
$results | Format-Table -AutoSize

$failedCount = ($results | Where-Object { $_.Compile -eq "FAILED" -or $_.Catalog -eq "FAILED" }).Count
if ($failedCount -eq 0) {
    Write-Host ""
    Write-Host "All programs compiled and cataloged successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "$failedCount program(s) had issues" -ForegroundColor Yellow
}
