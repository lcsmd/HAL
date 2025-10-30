$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

# Get latest batch ID
Write-Host "Getting latest batch ID..."
$body1 = @{cmd = "SSELECT IMPORT.LOG BY @ID DESC"} | ConvertTo-Json
$r1 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body1 -ContentType "application/json"

# Get first ID from select list
$body2 = @{cmd = "READNEXT BATCH.ID ELSE STOP"} | ConvertTo-Json
$r2 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json"

Write-Host "Latest batch: $($r2.stdout)"
$batchId = $r2.stdout.Trim()

if ($batchId) {
    Write-Host "`nStep 1: Standardizing payees..."
    $body3 = @{cmd = "FIN.STANDARDIZE.PAYEES.V2 $batchId"} | ConvertTo-Json
    $r3 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body3 -ContentType "application/json"
    Write-Host $r3.stdout
    
    Write-Host "`nStep 2: Tagging reimbursable transactions..."
    $body4 = @{cmd = "FIN.TAG.REIMBURSABLE.V2 $batchId"} | ConvertTo-Json
    $r4 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body4 -ContentType "application/json"
    Write-Host $r4.stdout
    
    Write-Host "`nStep 3: Generating summary report..."
    $body5 = @{cmd = "FIN.REPORT.REIMBURSABLE.V2 SUMMARY"} | ConvertTo-Json
    $r5 = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body5 -ContentType "application/json"
    Write-Host $r5.stdout
    
    Write-Host "`nProcessing complete!"
} else {
    Write-Host "ERROR: Could not find batch ID"
}
