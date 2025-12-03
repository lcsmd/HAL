# HAL Client - Complete Setup from GitHub
# Run this on YOUR CLIENT PC (not the server)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "HAL Voice Client - Complete Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create directory
Write-Host "[1/4] Creating directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT" | Out-Null
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT\models" | Out-Null
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT

# Step 2: Download client files from GitHub
Write-Host "[2/4] Downloading client files from GitHub..." -ForegroundColor Yellow
$baseUrl = "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client"

$files = @(
    "simple_gui.py",
    "hal_voice_client_gui.py", 
    "hal_voice_client.py",
    "test_client.py",
    "START_CLIENT.bat",
    "requirements.txt",
    "voice_client.config"
)

foreach ($file in $files) {
    Write-Host "  Downloading $file..." -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri "$baseUrl/$file" -OutFile $file -ErrorAction Stop
        Write-Host "  [OK] $file" -ForegroundColor Green
    } catch {
        Write-Host "  [SKIP] $file (not found)" -ForegroundColor Yellow
    }
}

# Step 3: Download wake word model
Write-Host "[3/4] Downloading wake word model..." -ForegroundColor Yellow
$modelUrl = "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1/hey_jarvis_v0.1.onnx"
Write-Host "  Downloading hey_jarvis_v0.1.onnx..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $modelUrl -OutFile "models\hey_jarvis_v0.1.onnx"
Write-Host "  [OK] Wake word model downloaded" -ForegroundColor Green

# Step 4: Install Python libraries
Write-Host "[4/4] Installing voice libraries..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Cyan

pip install websockets pygame setuptools pyaudio openwakeword webrtcvad

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Client installed at: C:\HAL\VOICE_ASSISTANT_V2\CLIENT" -ForegroundColor White
Write-Host ""
Write-Host "To run voice mode:" -ForegroundColor Yellow
Write-Host "  cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT" -ForegroundColor White
Write-Host "  python hal_voice_client_gui.py" -ForegroundColor White
Write-Host ""
Write-Host "To run text mode:" -ForegroundColor Yellow
Write-Host "  python simple_gui.py" -ForegroundColor White
Write-Host ""
Write-Host "Say 'Hey Jarvis' to activate voice!" -ForegroundColor Cyan
Write-Host ""
