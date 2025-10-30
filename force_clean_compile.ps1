$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

$programs = @("FIN.STANDARDIZE.PAYEES.V2", "FIN.TAG.REIMBURSABLE.V2", "FIN.REPORT.REIMBURSABLE.V2")

foreach ($prog in $programs) {
    Write-Host "Cleaning $prog..."
    
    # Delete object file
    $body1 = @{cmd = "DELETE FIN.BP.OUT $prog"} | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body1 -ContentType "application/json" | Out-Null
    
    # Delete VOC entry
    $body2 = @{cmd = "DELETE VOC $prog"} | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body2 -ContentType "application/json" | Out-Null
    
    Write-Host "Compiling $prog..."
    $body3 = @{cmd = "BASIC FIN.BP $prog NO.PAGE"} | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body3 -ContentType "application/json" | Out-Null
    
    Write-Host "Cataloging $prog..."
    $body4 = @{cmd = "CATALOG FIN.BP $prog LOCAL NO.PAGE"} | ConvertTo-Json
    Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body4 -ContentType "application/json" | Out-Null
    
    Write-Host "  Done!"
}

Write-Host "`nAll programs cleaned and recompiled!"
Write-Host "Now run in QM:"
Write-Host "  FIN.STANDARDIZE.PAYEES.V2 21118-5588"
