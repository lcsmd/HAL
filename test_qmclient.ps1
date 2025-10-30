$headers = @{"X-Auth" = "CHANGEME-STRONG-TOKEN"}

Write-Host "Testing QMClient endpoint..."
Write-Host ""

$body = @{cmd = "LIST IMPORT.LOG"} | ConvertTo-Json
$r = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/client" -Method Post -Headers $headers -Body $body -ContentType "application/json"

Write-Host "Return code: $($r.returncode)"
Write-Host "Output length: $($r.stdout.Length)"
Write-Host ""
Write-Host "Output:"
Write-Host $r.stdout
