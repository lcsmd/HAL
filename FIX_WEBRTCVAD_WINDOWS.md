# Fix webrtcvad Installation Error on Windows

## ❌ Problem
```
ERROR: Failed building wheel for webrtcvad
```

This happens because webrtcvad requires C++ compiler which most Windows PCs don't have.

---

## ✅ SOLUTION 1: Download Pre-built Wheel (EASIEST)

### Step 1: Download Pre-built Wheel

**Go to this website:**
```
https://www.lfd.uci.edu/~gohlke/pythonlibs/#webrtcvad
```

**Or use direct download:**

**For Python 3.13 (64-bit Windows):**
```
https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp313-cp313-win_amd64.whl
```

**For Python 3.12:**
```
https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp312-cp312-win_amd64.whl
```

**For Python 3.11:**
```
https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp311-cp311-win_amd64.whl
```

### Step 2: Install the Downloaded Wheel

**Open Command Prompt where you downloaded the file:**

```cmd
cd Downloads
pip install webrtcvad-2.0.10-cp313-cp313-win_amd64.whl
```

*(Change filename to match your Python version)*

### Step 3: Install Other Libraries

```cmd
pip install pyaudio openwakeword pygame websockets
```

---

## ✅ SOLUTION 2: PowerShell Auto-Download (RECOMMENDED)

**Run this in PowerShell:**

```powershell
# Detect Python version
$pyVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "Python version: $pyVersion" -ForegroundColor Cyan

# Download appropriate wheel
$url = switch ($pyVersion) {
    "3.13" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp313-cp313-win_amd64.whl" }
    "3.12" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp312-cp312-win_amd64.whl" }
    "3.11" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp311-cp311-win_amd64.whl" }
    "3.10" { "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp310-cp310-win_amd64.whl" }
    default { Write-Host "Python version not supported" -ForegroundColor Red; exit }
}

$filename = $url.Split('/')[-1]
Write-Host "Downloading $filename..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $url -OutFile $filename

Write-Host "Installing webrtcvad..." -ForegroundColor Yellow
pip install $filename

Write-Host "Installing other voice libraries..." -ForegroundColor Yellow
pip install pyaudio openwakeword pygame websockets

Write-Host "`nInstallation complete!" -ForegroundColor Green
Remove-Item $filename
```

---

## ✅ SOLUTION 3: Skip webrtcvad (Voice Works Without It)

**webrtcvad is optional** - the client can work without it!

**Just install these:**
```cmd
pip install pyaudio openwakeword pygame websockets
```

**What you lose:** Voice Activity Detection (silence detection)  
**What still works:** Wake word detection, recording, transcription, TTS

The client will use simpler silence detection instead.

---

## ✅ SOLUTION 4: Install Visual C++ Build Tools (SLOW)

**Only if you want to compile from source:**

### Step 1: Download Visual Studio Build Tools
```
https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
```

### Step 2: Install with C++ Workload
- Run installer
- Select "Desktop development with C++"
- Install (takes 15-20 minutes, 6+ GB)

### Step 3: Retry pip install
```cmd
pip install webrtcvad
```

**Note:** This is overkill just for webrtcvad. Use Solution 2 instead.

---

## 🎯 RECOMMENDED APPROACH

**Run this PowerShell script (Solution 2):**

```powershell
# Quick install script
$pyVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($pyVersion -eq "3.13") {
    $url = "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp313-cp313-win_amd64.whl"
} elseif ($pyVersion -eq "3.12") {
    $url = "https://download.lfd.uci.edu/pythonlibs/archived/webrtcvad-2.0.10-cp312-cp312-win_amd64.whl"
} else {
    Write-Host "For Python $pyVersion, download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#webrtcvad" -ForegroundColor Yellow
    Write-Host "Or skip webrtcvad - voice still works without it!" -ForegroundColor Green
    exit
}
$file = $url.Split('/')[-1]
Invoke-WebRequest -Uri $url -OutFile $file
pip install $file
pip install pyaudio openwakeword pygame websockets
Remove-Item $file
Write-Host "Done!" -ForegroundColor Green
```

---

## ✅ VERIFY INSTALLATION

**Test if webrtcvad installed:**

```cmd
python -c "import webrtcvad; print('webrtcvad OK')"
```

**Test all voice libraries:**

```cmd
python -c "import pyaudio, openwakeword, webrtcvad, pygame, websockets; print('All libraries OK')"
```

---

## 📋 Alternative: Run Without webrtcvad

**If you can't install it, just skip it:**

```cmd
pip install pyaudio openwakeword pygame websockets
```

**Then run the client** - it will detect webrtcvad is missing and use fallback silence detection.

You'll see a warning like:
```
webrtcvad not available, using basic silence detection
```

**This is fine!** Voice still works, just with simpler silence detection.

---

## 🎯 Summary

**Best Solution:** Use pre-built wheel (Solution 2 PowerShell script)  
**Fastest Solution:** Skip webrtcvad (Solution 3)  
**Most Complete:** Pre-built wheel gives you everything  

**Voice will work either way!**

---

**Status:** Multiple solutions provided  
**Recommended:** PowerShell auto-download script  
**Fallback:** Skip webrtcvad, voice still works
