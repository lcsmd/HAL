$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}
$body = @{cmd = "LIST DICT TRANSACTION"} | ConvertTo-Json
$r = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body -ContentType "application/json"
Write-Host $r.stdout
