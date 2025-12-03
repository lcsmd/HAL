# Automated SSH Key Setup Script
$pubKey = Get-Content $env:USERPROFILE\.ssh\id_rsa.pub
$password = "apgar-66"
$server = "lawr@10.1.10.20"

# Create command to add key
$remoteCmd = "mkdir -p ~/.ssh && echo '$pubKey' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"

# Use Process with StandardInput to send password
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "ssh"
$psi.Arguments = "-o StrictHostKeyChecking=no $server `"$remoteCmd`""
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi
$process.Start() | Out-Null

# Wait a moment for password prompt
Start-Sleep -Milliseconds 500

# Send password
$process.StandardInput.WriteLine($password)
$process.StandardInput.Close()

# Wait for completion
$output = $process.StandardOutput.ReadToEnd()
$error = $process.StandardError.ReadToEnd()
$process.WaitForExit(10000)

Write-Host "Output: $output"
Write-Host "Error: $error"
Write-Host "Exit Code: $($process.ExitCode)"
