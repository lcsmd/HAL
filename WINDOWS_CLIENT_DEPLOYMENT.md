# Deploy HAL Client to a Different Windows PC

## 🎯 ON YOUR CLIENT PC (Not the server!)

**Open PowerShell on your client PC and run these commands:**

### Step 1: Create Directory
```powershell
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT"
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
```

### Step 2: Download Client Files from GitHub
```powershell
$baseUrl = "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client"

$files = @(
    "simple_gui.py",
    "test_client.py",
    "hal_voice_client_gui.py",
    "START_CLIENT.bat",
    "requirements.txt"
)

foreach ($file in $files) {
    Write-Host "Downloading $file..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri "$baseUrl/$file" -OutFile $file
    Write-Host "[OK] $file" -ForegroundColor Green
}

Write-Host "`nFiles downloaded!" -ForegroundColor Green
```

### Step 3: Install Python Libraries
```powershell
# Install websockets (required)
pip install websockets

# Install setuptools (fixes pkg_resources error)
pip install setuptools

# Install pygame (for sound)
pip install pygame

# Try to install voice libraries (optional, may need pre-built wheels)
pip install pyaudio openwakeword
```

### Step 4: Install webrtcvad (Special handling for Windows)

**Option A - Try pip first:**
```powershell
pip install webrtcvad
```

**If that fails, download pre-built wheel:**
```powershell
# For Python 3.13
Invoke-WebRequest -Uri "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp313-cp313-win_amd64.whl" -OutFile webrtcvad.whl
pip install webrtcvad.whl
Remove-Item webrtcvad.whl
```

**Or skip webrtcvad** - the client works without it!

### Step 5: Run the Simple GUI Client
```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python simple_gui.py
```

**Or run the test client:**
```powershell
python test_client.py
```

---

## ⚡ ONE-LINE QUICK INSTALL

**Copy/paste this entire command on your client PC:**

```powershell
New-Item -ItemType Directory -Force -Path "C:\HAL\VOICE_ASSISTANT_V2\CLIENT" | Out-Null; cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT; $baseUrl = "https://raw.githubusercontent.com/lcsmd/HAL/main/voice_assistant_v2/client"; @("simple_gui.py","test_client.py","hal_voice_client_gui.py","START_CLIENT.bat","requirements.txt") | ForEach-Object { Write-Host "Downloading $_..." -ForegroundColor Cyan; Invoke-WebRequest -Uri "$baseUrl/$_" -OutFile $_ }; Write-Host "`nInstalling libraries..." -ForegroundColor Yellow; pip install websockets pygame setuptools; Write-Host "`nDone! Run: python simple_gui.py" -ForegroundColor Green
```

**Then run:**
```powershell
python simple_gui.py
```

---

## 🎯 What You Need on Client PC:

**Required:**
- Python 3.x installed
- websockets library
- setuptools library

**Optional (for voice):**
- pygame
- pyaudio
- openwakeword
- webrtcvad

**The client works with just websockets and setuptools!**

---

## ✅ Verify Setup on Client PC

**After downloading and installing, test:**

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT

# Check files exist
dir

# Check libraries
python -c "import websockets; print('websockets OK')"

# Test connection
python test_client.py
```

**Should see:** "The current time is [time]"

---

## 🚀 Run Client

```powershell
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python simple_gui.py
```

**Type messages and press ENTER - HAL responds!**

---

## 📋 Summary

**On your CLIENT PC (not server):**
1. Open PowerShell
2. Run the one-line install command above
3. Run: `python simple_gui.py`
4. Start chatting with HAL!

**Server:** 10.1.34.103:8768  
**Client:** Your Windows PC  
**Connection:** Over network via WebSockets
