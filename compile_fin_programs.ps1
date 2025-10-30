$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

Write-Host "Compiling FIN.BP programs..."
Write-Host "="*70

$programs = @(
    "FIN.STANDARDIZE.PAYEES.V2",
    "FIN.TAG.REIMBURSABLE.V2",
    "FIN.REPORT.REIMBURSABLE.V2"
)

foreach ($prog in $programs) {
    Write-Host "`nCompiling $prog..."
    $body = @{cmd = "BASIC FIN.BP $prog NO.PAGE"} | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host $r.stdout
    if ($r.stderr) { Write-Host "STDERR: $($r.stderr)" }
    
    Write-Host "Cataloging $prog..."
    $body2 = @{cmd = "CATALOG FIN.BP $prog NO.PAGE"} | ConvertTo-Json
    $r2 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json"
    Write-Host $r2.stdout
    if ($r2.stderr) { Write-Host "STDERR: $($r2.stderr)" }
}

Write-Host "`n"
Write-Host "="*70
Write-Host "Compilation complete!"
