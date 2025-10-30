$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

# List import log to find batch ID
Write-Host "Finding latest batch..."
$body = @{cmd = "LIST IMPORT.LOG @ID"} | ConvertTo-Json
$r = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body -ContentType "application/json"
Write-Host $r.stdout
Write-Host ""

# Use the most recent batch (you'll need to specify it)
$batchId = "21118-5588"  # Update this with your actual batch ID

Write-Host "Processing batch: $batchId"
Write-Host "="*70
Write-Host ""

Write-Host "Step 1: Standardizing payees..."
$body1 = @{cmd = "FIN.STANDARDIZE.PAYEES.V2 $batchId"} | ConvertTo-Json
$r1 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body1 -ContentType "application/json"
Write-Host $r1.stdout
Write-Host ""

Write-Host "Step 2: Tagging reimbursable transactions..."
$body2 = @{cmd = "FIN.TAG.REIMBURSABLE.V2 $batchId"} | ConvertTo-Json
$r2 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json"
Write-Host $r2.stdout
Write-Host ""

Write-Host "Step 3: Generating summary report..."
$body3 = @{cmd = "FIN.REPORT.REIMBURSABLE.V2 SUMMARY"} | ConvertTo-Json
$r3 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body3 -ContentType "application/json"
Write-Host $r3.stdout
Write-Host ""

Write-Host "="*70
Write-Host "Processing complete!"
