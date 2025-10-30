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

# List dictionary
Write-Host "`nListing PERSON dictionary..."
$writer.WriteLine("LIST DICT PERSON FIRST_NAME LAST_NAME EMAIL")
Start-Sleep -Milliseconds 3000
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
