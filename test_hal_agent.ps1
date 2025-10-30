$headers = @{
    "X-Auth" = "CHANGEME-STRONG-TOKEN"
}

$body = @{
    cmd = "LIST IMPORT.LOG"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body -ContentType "application/json"

Write-Output $response | ConvertTo-Json -Depth 10
