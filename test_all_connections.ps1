# Test all three connection types

Write-Host "="*60
Write-Host "Testing !CALLHTTP with different targets"
Write-Host "="*60

Write-Host "`n1. Testing localhost:8443 (echo server)..."
qm -kHAL -c":test.localhost.b"

Write-Host "`n2. Testing Ollama (ubuai.q.lcs.ai:11434)..."
qm -kHAL -c":test.ollama.b"

Write-Host "`n3. Checking echo server log for localhost request..."
$log = Get-Content "c:\QMSYS\HAL\requests_8443.log" -ErrorAction SilentlyContinue
if ($log -match "test.*data") {
    Write-Host "✓ localhost request WAS received by echo server"
} else {
    Write-Host "✗ localhost request was NOT received by echo server"
}
