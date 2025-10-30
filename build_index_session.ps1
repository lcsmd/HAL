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

# Compile BUILD.SCHEMA
Write-Host "`nCompiling BUILD.SCHEMA..."
$writer.WriteLine("BASIC BP BUILD.SCHEMA")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Catalog BUILD.SCHEMA
Write-Host "`nCataloging BUILD.SCHEMA..."
$writer.WriteLine("CATALOG BP BUILD.SCHEMA")
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

# Compile BUILD.INDEX
Write-Host "`nCompiling BUILD.INDEX..."
$writer.WriteLine("BASIC BP BUILD.INDEX")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Catalog BUILD.INDEX
Write-Host "`nCataloging BUILD.INDEX..."
$writer.WriteLine("CATALOG BP BUILD.INDEX")
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

# Logout
$writer.WriteLine("LOGTO")
Start-Sleep -Milliseconds 500

$client.Close()
Write-Host "`nSession closed"
