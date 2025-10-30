param(
    [Parameter(Mandatory=$true)]
    [string]$Command
)

$headers = @{
    "X-Auth" = "CHANGEME-STRONG-TOKEN"
}

$body = @{
    cmd = $Command
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8766/qm/run" -Method Post -Headers $headers -Body $body -ContentType "application/json"

Write-Output "Command: $Command"
Write-Output "Exit Code: $($response.returncode)"
Write-Output ""
Write-Output "Output:"
Write-Output $response.stdout
if ($response.stderr) {
    Write-Output ""
    Write-Output "Errors:"
    Write-Output $response.stderr
}
