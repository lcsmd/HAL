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

# Send BASIC command
Write-Host "`nSending: BASIC BP BUILD.SCHEMA"
$writer.WriteLine("BASIC BP BUILD.SCHEMA")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Send CATALOG command
Write-Host "`nSending: CATALOG BP BUILD.SCHEMA"
$writer.WriteLine("CATALOG BP BUILD.SCHEMA")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Answer N to remove from local catalog question
$writer.WriteLine("N")
Start-Sleep -Milliseconds 1000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Run the program
Write-Host "`nSending: BUILD.SCHEMA"
$writer.WriteLine("BUILD.SCHEMA")
Start-Sleep -Milliseconds 10000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Wait for more output
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Logout
$writer.WriteLine("LOGTO")
Start-Sleep -Milliseconds 500

$client.Close()
Write-Host "`nSession closed"
