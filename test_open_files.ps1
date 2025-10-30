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

# Compile OPEN.FILES
Write-Host "`nCompiling OPEN.FILES..."
$writer.WriteLine("BASIC BP OPEN.FILES")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Catalog OPEN.FILES
Write-Host "`nCataloging OPEN.FILES..."
$writer.WriteLine("CATALOG BP OPEN.FILES")
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

# Compile TEST.OPEN.FILES
Write-Host "`nCompiling TEST.OPEN.FILES..."
$writer.WriteLine("BASIC BP TEST.OPEN.FILES")
Start-Sleep -Milliseconds 2000
while ($stream.DataAvailable) {
    $line = $reader.ReadLine()
    Write-Host $line
}

# Catalog TEST.OPEN.FILES
Write-Host "`nCataloging TEST.OPEN.FILES..."
$writer.WriteLine("CATALOG BP TEST.OPEN.FILES")
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

# Run TEST.OPEN.FILES
Write-Host "`nRunning TEST.OPEN.FILES..."
$writer.WriteLine("TEST.OPEN.FILES")
Start-Sleep -Milliseconds 5000
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
