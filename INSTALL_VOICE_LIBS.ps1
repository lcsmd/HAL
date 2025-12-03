# HAL Voice Libraries Installer for Windows
# Handles webrtcvad pre-built wheel automatically

$ErrorActionPreference = "Continue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "HAL Voice Libraries Installer" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Detect Python version
Write-Host "Detecting Python version..." -ForegroundColor Yellow
$pyVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$pyFull = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
Write-Host "[OK] Python $pyFull detected" -ForegroundColor Green
Write-Host ""

# Install PyAudio
Write-Host "[1/5] Installing PyAudio..." -ForegroundColor Yellow
pip install pyaudio
Write-Host ""

# Install pygame
Write-Host "[2/5] Installing pygame..." -ForegroundColor Yellow
pip install pygame
Write-Host ""

# Install websockets
Write-Host "[3/5] Installing websockets..." -ForegroundColor Yellow
pip install websockets
Write-Host ""

# Install openwakeword
Write-Host "[4/5] Installing openwakeword..." -ForegroundColor Yellow
pip install openwakeword
Write-Host ""

# Install webrtcvad (pre-built wheel)
Write-Host "[5/5] Installing webrtcvad..." -ForegroundColor Yellow

$whlUrl = switch ($pyVersion) {
    "3.13" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp313-cp313-win_amd64.whl" }
    "3.12" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp312-cp312-win_amd64.whl" }
    "3.11" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp311-cp311-win_amd64.whl" }
    "3.10" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp310-cp310-win_amd64.whl" }
    default { 
        Write-Host "[SKIP] No pre-built wheel for Python $pyVersion" -ForegroundColor Yellow
        Write-Host "       Voice will work without webrtcvad (using fallback)" -ForegroundColor Cyan
        $null
    }
}

if ($whlUrl) {
    $whlFile = $whlUrl.Split('/')[-1]
    
    try {
        Write-Host "  Downloading $whlFile..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $whlUrl -OutFile $whlFile -ErrorAction Stop
        
        Write-Host "  Installing from wheel..." -ForegroundColor Cyan
        pip install $whlFile
        
        Remove-Item $whlFile -ErrorAction SilentlyContinue
        Write-Host "[OK] webrtcvad installed" -ForegroundColor Green
    } catch {
        Write-Host "[WARN] Could not download wheel: $_" -ForegroundColor Yellow
        Write-Host "       Trying pip install (may fail)..." -ForegroundColor Yellow
        pip install webrtcvad 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[SKIP] webrtcvad installation failed" -ForegroundColor Yellow
            Write-Host "       Voice will work without it (using fallback)" -ForegroundColor Cyan
        }
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Test imports
Write-Host "Testing installed libraries..." -ForegroundColor Yellow
Write-Host ""

$testScript = @"
import sys
try:
    import pyaudio
    print('  [OK] pyaudio')
except ImportError:
    print('  [ERROR] pyaudio - not installed')
    
try:
    import openwakeword
    print('  [OK] openwakeword')
except ImportError:
    print('  [ERROR] openwakeword - not installed')

try:
    import webrtcvad
    print('  [OK] webrtcvad')
except ImportError:
    print('  [WARN] webrtcvad - not installed (voice will use fallback)')

try:
    import pygame
    print('  [OK] pygame')
except ImportError:
    print('  [ERROR] pygame - not installed')

try:
    import websockets
    print('  [OK] websockets')
except ImportError:
    print('  [ERROR] websockets - not installed')
"@

python -c $testScript

Write-Host ""
Write-Host "You can now run the HAL voice client!" -ForegroundColor Green
Write-Host ""
Write-Host "Run: cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT" -ForegroundColor White
Write-Host "     python hal_voice_client_gui.py" -ForegroundColor White
Write-Host ""
