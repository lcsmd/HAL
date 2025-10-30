$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

$programs = @("FIN.STANDARDIZE.PAYEES.V2", "FIN.TAG.REIMBURSABLE.V2", "FIN.REPORT.REIMBURSABLE.V2")

foreach ($prog in $programs) {
    Write-Host "Compiling $prog..."
    $body = @{cmd = "BASIC FIN.BP $prog NO.PAGE"} | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    
    Write-Host "Cataloging $prog..."
    $body2 = @{cmd = "CATALOG FIN.BP $prog NO.PAGE"} | ConvertTo-Json
    $r2 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json"
    Write-Host ""
}

Write-Host "Done! Try running the programs now."
