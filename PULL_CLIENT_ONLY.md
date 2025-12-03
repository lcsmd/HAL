# How to Pull ONLY Client Files from GitHub to Windows Client

## 🎯 Quick Method - Download Specific Files

### Option 1: Git Sparse Checkout (Recommended)

**On your Windows client PC, open Command Prompt:**

```cmd
cd C:\HAL
```

**If you DON'T have git installed yet:**

1. **First time setup - Clone only client folder:**
   ```cmd
   git clone --depth 1 --filter=blob:none --sparse https://github.com/lcsmd/HAL.git HAL_TEMP
   cd HAL_TEMP
   git sparse-checkout set voice_assistant_v2/client
   ```

2. **Copy files to your location:**
   ```cmd
   xcopy /E /I /Y voice_assistant_v2\client C:\HAL\VOICE_ASSISTANT_V2\CLIENT
   cd ..
   rmdir /S /Q HAL_TEMP
   ```

**If you ALREADY have the repo cloned:**

```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
git pull origin main voice_assistant_v2/client
```

---

### Option 2: Direct File Download (No Git Needed)

**Download these files directly from GitHub:**

1. **Open browser and go to:**
   ```
   https://github.com/lcsmd/HAL/tree/main/voice_assistant_v2/client
   ```

2. **Click on each file and download:**
   - Click file name → Click "Raw" button → Right-click → Save As
   
   **Required files:**
   - `hal_voice_client_gui.py`
   - `START_CLIENT.bat`
   - `requirements.txt`
   - `voice_client.config`

3. **Save to:**
   ```
   C:\HAL\VOICE_ASSISTANT_V2\CLIENT\
   ```

---

### Option 3: PowerShell Download Script (Easiest)

**On your Windows client, open PowerShell and run:**

```powershell
# Create directory if needed
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT"
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT

# Base URL for raw files
$baseUrl = "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client"

# Files to download
$files = @(
    "hal_voice_client_gui.py",
    "hal_voice_client.py",
    "voice_client.py",
    "START_CLIENT.bat",
    "requirements.txt",
    "voice_client.config",
    "GUI_CLIENT.md",
    "READY_TO_USE.md"
)

# Download each file
foreach ($file in $files) {
    Write-Host "Downloading $file..." -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri "$baseUrl/$file" -OutFile $file
        Write-Host "[OK] $file" -ForegroundColor Green
    } catch {
        Write-Host "[SKIP] $file not found" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Download complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Install voice libraries: pip install pyaudio openwakeword webrtcvad pygame"
Write-Host "2. Run client: START_CLIENT.bat"
```

---

### Option 4: One-Line PowerShell Download

**Copy and paste this entire command into PowerShell:**

```powershell
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT" | Out-Null; cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT; $baseUrl = "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client"; @("hal_voice_client_gui.py","START_CLIENT.bat","requirements.txt","voice_client.config") | ForEach-Object { Invoke-WebRequest -Uri "$baseUrl/$_" -OutFile $_ }; Write-Host "Download complete! Run: START_CLIENT.bat" -ForegroundColor Green
```

---

## ✅ After Downloading Files

**Install voice libraries:**

```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
pip install pyaudio openwakeword webrtcvad pygame
```

**Run the client:**

```cmd
START_CLIENT.bat
```

Or:

```cmd
python hal_voice_client_gui.py
```

---

## 🔄 To Update Later

**When files are updated on GitHub, just re-run the download command:**

**PowerShell one-liner (same as above):**
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT; $baseUrl = "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client"; @("hal_voice_client_gui.py","START_CLIENT.bat","requirements.txt","voice_client.config") | ForEach-Object { Invoke-WebRequest -Uri "$baseUrl/$_" -OutFile $_ }
```

This overwrites with latest versions from GitHub.

---

## 📋 Verify Files Are Correct

**After downloading, check the server URL in the client:**

```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
findstr "10.1.34.103" hal_voice_client_gui.py
```

**Should output:**
```
self.voice_server_url = os.getenv('VOICE_SERVER_URL', 'ws://10.1.34.103:8768')
```

If you see `10.1.10.20`, the file didn't update correctly. Try downloading again.

---

## 🎯 Complete Fresh Setup

**If starting from scratch on a new Windows client:**

```powershell
# 1. Create directory
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT"

# 2. Download files
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
$baseUrl = "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client"
@("hal_voice_client_gui.py","START_CLIENT.bat","requirements.txt") | ForEach-Object { Invoke-WebRequest -Uri "$baseUrl/$_" -OutFile $_ }

# 3. Install Python dependencies
pip install pyaudio openwakeword webrtcvad pygame websockets

# 4. Run
.\START_CLIENT.bat
```

---

## 📦 Files You Need (Minimum)

**Essential:**
- `hal_voice_client_gui.py` - Main client program
- `START_CLIENT.bat` - Launcher
- `requirements.txt` - Dependencies list

**Optional but recommended:**
- `voice_client.config` - Configuration file
- `GUI_CLIENT.md` - Documentation
- `READY_TO_USE.md` - Quick start guide

---

## ⚡ TL;DR - Fastest Way

**Run this in PowerShell on your Windows client:**

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client/hal_voice_client_gui.py" -OutFile hal_voice_client_gui.py
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client/START_CLIENT.bat" -OutFile START_CLIENT.bat
pip install pyaudio openwakeword webrtcvad pygame websockets
.\START_CLIENT.bat
```

**Done!** ✅

---

**GitHub Repository:** https://github.com/lcsmd/HAL  
**Client Path:** voice_assistant_v2/client/  
**Status:** Ready to download and use
