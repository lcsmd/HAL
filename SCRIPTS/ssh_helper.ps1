# Helper script to SSH to ubu6
param(
    [string]$Command = "hostname"
)

$password = "apgar-66"
$username = "lawr"
$host = "ubu6"
$port = "2222"

# Try using plink if available (PuTTY)
if (Get-Command plink -ErrorAction SilentlyContinue) {
    echo $password | plink -ssh -P $port -l $username -pw $password $host $Command
} else {
    Write-Host "Note: SSH with password may require manual entry"
    ssh -p $port "$username@$host" $Command
}
