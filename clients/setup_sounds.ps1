# Setup HAL Voice Client Audio Feedback Sounds (Windows)
# Copies existing TNG activation sound and ack.wav from VOICE/SOUNDS

$ErrorActionPreference = "Stop"

Write-Host "Setting up HAL voice client audio feedback sounds..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "hal_voice_client_full.py")) {
    Write-Host "❌ Error: Run this script from the clients\ directory" -ForegroundColor Red
    exit 1
}

# Define paths
$VoiceSounds = "..\VOICE\SOUNDS"

# Function to copy sound file
function Copy-Sound {
    param($Source, $Dest, $Description)
    
    if (Test-Path $Source) {
        Copy-Item -Path $Source -Destination $Dest -Force
        Write-Host "✓ $Description" -ForegroundColor Green
    } else {
        Write-Host "⚠ Warning: $Source not found" -ForegroundColor Yellow
    }
}

# Copy TNG activation sound (MP3)
Copy-Sound "$VoiceSounds\TNG_activation.mp3" "activation.mp3" "Activation sound (TNG chirp)"

# Copy acknowledgement sound (WAV)
Copy-Sound "$VoiceSounds\ack.wav" "acknowledgement.wav" "Acknowledgement sound"

# Use ack.wav as error sound too (fallback)
if ((Test-Path "acknowledgement.wav") -and (-not (Test-Path "error.wav"))) {
    Copy-Item -Path "acknowledgement.wav" -Destination "error.wav" -Force
    Write-Host "✓ Error sound (using ack.wav as fallback)" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Audio feedback sounds setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Files created:"
Get-ChildItem "activation.mp3", "acknowledgement.wav", "error.wav" -ErrorAction SilentlyContinue | Format-Table Name, Length

Write-Host ""
Write-Host "You can now run: python hal_voice_client_full.py"
