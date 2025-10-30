# Compare !CALLHTTP vs Python requests
Write-Host "Starting echo server..."
$echoServer = Start-Process python -ArgumentList "C:\QMSYS\HAL\PY\http_echo_server.py" -PassThru -WindowStyle Hidden
Start-Sleep 3

Write-Host "`n1. Testing Python requests..."
python "C:\QMSYS\HAL\PY\test_python_request.py"

Start-Sleep 2

Write-Host "`n2. Testing QM !CALLHTTP..."
qm -kHAL -c":test.callhttp.b"

Start-Sleep 2

Write-Host "`nStopping echo server..."
Stop-Process -Id $echoServer.Id -Force
