$client = New-Object System.Net.Sockets.TcpClient("localhost", 4242)
$stream = $client.GetStream()
$reader = New-Object System.IO.StreamReader($stream)
$writer = New-Object System.IO.StreamWriter($stream)
$writer.AutoFlush = $true

# Read initial prompt
Start-Sleep -Milliseconds 500
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Send username
$writer.WriteLine("lawr")
Start-Sleep -Milliseconds 500
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Send password
$writer.WriteLine("apgar-66")
Start-Sleep -Milliseconds 1000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Send account
$writer.WriteLine("HAL")
Start-Sleep -Milliseconds 1000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Compile TEST.PATH
Write-Host "`nCompiling TEST.PATH..."
$writer.WriteLine("BASIC BP TEST.PATH")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Catalog TEST.PATH
Write-Host "`nCataloging TEST.PATH..."
$writer.WriteLine("CATALOG BP TEST.PATH")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Answer N to catalog question
$writer.WriteLine("N")
Start-Sleep -Milliseconds 1000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Run TEST.PATH
Write-Host "`nRunning TEST.PATH..."
$writer.WriteLine("TEST.PATH")
Start-Sleep -Milliseconds 3000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Logout
$writer.WriteLine("LOGTO")
Start-Sleep -Milliseconds 500

$client.Close()
Write-Host "`nSession closed"
