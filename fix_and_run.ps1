$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

Write-Host "Step 1: Recompiling fixed report..."
$body1 = @{cmd = "BASIC FIN.BP FIN.REPORT.REIMBURSABLE.V2 NO.PAGE"} | ConvertTo-Json
$r1 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body1 -ContentType "application/json"
Write-Host $r1.stdout

Write-Host "`nStep 2: Cataloging report..."
$body2 = @{cmd = "CATALOG FIN.BP FIN.REPORT.REIMBURSABLE.V2 NO.PAGE"} | ConvertTo-Json
$r2 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json"
Write-Host $r2.stdout

Write-Host "`nStep 3: Building schema (creating RULE file)..."
$body3 = @{cmd = "BUILD.SCHEMA"} | ConvertTo-Json
$r3 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body3 -ContentType "application/json"
Write-Host $r3.stdout

Write-Host "`n`nStep 4: Running standardize payees..."
$body4 = @{cmd = "FIN.STANDARDIZE.PAYEES.V2 21118-5588"} | ConvertTo-Json
$r4 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body4 -ContentType "application/json"
Write-Host $r4.stdout

Write-Host "`nStep 5: Tagging reimbursable..."
$body5 = @{cmd = "FIN.TAG.REIMBURSABLE.V2 21118-5588"} | ConvertTo-Json
$r5 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body5 -ContentType "application/json"
Write-Host $r5.stdout

Write-Host "`nStep 6: Generating report..."
$body6 = @{cmd = "FIN.REPORT.REIMBURSABLE.V2 SUMMARY"} | ConvertTo-Json
$r6 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body6 -ContentType "application/json"
Write-Host $r6.stdout

Write-Host "`n`nAll done!"
