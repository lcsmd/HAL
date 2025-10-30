$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

Write-Host "Step 1: Running BUILD.SCHEMA..."
$body1 = @{cmd = "BUILD.SCHEMA"} | ConvertTo-Json
$r1 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body1 -ContentType "application/json"
Write-Host "Exit code: $($r1.returncode)"

Write-Host "`nStep 2: Recompiling FIN.REPORT.REIMBURSABLE.V2..."
$body2 = @{cmd = "BASIC FIN.BP FIN.REPORT.REIMBURSABLE.V2 NO.PAGE"} | ConvertTo-Json
$r2 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json"
Write-Host "Exit code: $($r2.returncode)"

Write-Host "`nStep 3: Cataloging FIN.REPORT.REIMBURSABLE.V2..."
$body3 = @{cmd = "CATALOG FIN.BP FIN.REPORT.REIMBURSABLE.V2 NO.PAGE"} | ConvertTo-Json
$r3 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body3 -ContentType "application/json"
Write-Host "Exit code: $($r3.returncode)"

Write-Host "`nDone! Now try running the programs in QM."
