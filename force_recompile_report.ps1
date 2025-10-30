$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

Write-Host "Deleting object file..."
$body1 = @{cmd = "DELETE FIN.BP.OUT FIN.REPORT.REIMBURSABLE.V2"} | ConvertTo-Json
$r1 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body1 -ContentType "application/json"

Write-Host "Deleting VOC entry..."
$body2 = @{cmd = "DELETE VOC FIN.REPORT.REIMBURSABLE.V2"} | ConvertTo-Json
$r2 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json"

Write-Host "Recompiling..."
$body3 = @{cmd = "BASIC FIN.BP FIN.REPORT.REIMBURSABLE.V2 NO.PAGE"} | ConvertTo-Json
$r3 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body3 -ContentType "application/json"
Write-Host "Stdout: $($r3.stdout)"
Write-Host "Stderr: $($r3.stderr)"

Write-Host "Cataloging..."
$body4 = @{cmd = "CATALOG FIN.BP FIN.REPORT.REIMBURSABLE.V2 LOCAL NO.PAGE"} | ConvertTo-Json
$r4 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body4 -ContentType "application/json"
Write-Host "Stdout: $($r4.stdout)"

Write-Host "`nDone! Try running FIN.REPORT.REIMBURSABLE.V2 SUMMARY now."
