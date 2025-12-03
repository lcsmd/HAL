# How to Update HAL Client

## 🔄 Quick Update Methods

### Method 1: Run Update Script (Easiest)

**On the HAL server (where C:\qmsys\hal exists):**

```cmd
cd C:\qmsys\hal
UPDATE_CLIENT.bat
```

This copies all updated files from server to `C:\HAL\VOICE_ASSISTANT_V2\CLIENT\`

---

### Method 2: Manual File Copy

**Copy this file from server to client:**

```
FROM: C:\qmsys\hal\voice_assistant_v2\client\hal_voice_client_gui.py
TO:   C:\HAL\VOICE_ASSISTANT_V2\CLIENT\hal_voice_client_gui.py
```

**Using Windows:**
1. Open two File Explorer windows
2. Navigate to source (left) and destination (right)
3. Drag and drop `hal_voice_client_gui.py`
4. Click "Replace" when prompted

---

### Method 3: Quick Edit (No Copy Needed)

**If you don't want to copy files, just edit directly:**

1. Open on client PC: `C:\HAL\VOICE_ASSISTANT_V2\CLIENT\hal_voice_client_gui.py`

2. Find line 52 (use Notepad's Edit → Find)

3. Change this line:
   ```python
   self.voice_server_url = os.getenv('VOICE_SERVER_URL', 'ws://10.1.10.20:8585')
   ```

4. To this:
   ```python
   self.voice_server_url = os.getenv('VOICE_SERVER_URL', 'ws://10.1.34.103:8768')
   ```

5. Save (Ctrl+S)

6. Done!

---

## 🎤 Install Voice Libraries

**On the client PC, run:**

```cmd
pip install pyaudio openwakeword webrtcvad pygame
```

This installs:
- `pyaudio` - Microphone recording
- `openwakeword` - Wake word detection ("Hey Jarvis")
- `webrtcvad` - Voice activity detection
- `pygame` - Audio playback for TTS

---

## ✅ Verify Update

**After updating, test the client:**

```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
python hal_voice_client_gui.py
```

**Should see:**
- Window opens
- "Connected" status at bottom
- No "Voice components not available" error (if libraries installed)
- Typing "what time is it" gets response

---

## 🔧 What Changed

### Before Update:
- ❌ Connected to: `ws://10.1.10.20:8585` (wrong server)
- ❌ No responses
- ❌ Voice didn't work

### After Update:
- ✅ Connects to: `ws://10.1.34.103:8768` (Voice Gateway)
- ✅ Text responses work
- ✅ Voice works (if libraries installed)

---

## 📦 Full Deployment to New Client PC

**If setting up client on a brand new PC:**

### Step 1: Install Python
Download from: https://python.org  
**Important:** Check "Add to PATH" during installation

### Step 2: Create Directory
```cmd
mkdir C:\HAL\VOICE_ASSISTANT_V2\CLIENT
```

### Step 3: Copy Files from Server

**Minimum files needed:**
```
hal_voice_client_gui.py  (main client)
START_CLIENT.bat         (launcher)
requirements.txt         (dependencies)
```

**Copy from:**
```
C:\qmsys\hal\voice_assistant_v2\client\*
```

**To:**
```
C:\HAL\VOICE_ASSISTANT_V2\CLIENT\
```

### Step 4: Install Dependencies
```cmd
cd C:\HAL\VOICE_ASSISTANT_V2\CLIENT
pip install websockets pygame pyaudio openwakeword webrtcvad
```

### Step 5: Run
```cmd
START_CLIENT.bat
```

---

## 🚀 Alternative: Use Standalone Client

**For simplest deployment to any PC:**

Copy these 3 files:
```
C:\qmsys\hal\DEPLOY\hal_client_standalone.py
C:\qmsys\hal\DEPLOY\START_HAL.bat
C:\qmsys\hal\DEPLOY\README.txt
```

Put anywhere on client PC and run `START_HAL.bat`

**Note:** Standalone client is text-only (no voice features).

---

## 📝 Summary

**To update existing client:**
1. Run `UPDATE_CLIENT.bat` on server
2. Or manually copy `hal_voice_client_gui.py` 
3. Install voice libraries: `pip install pyaudio openwakeword webrtcvad pygame`
4. Run client

**To deploy to new PC:**
1. Copy entire CLIENT folder
2. Install Python + dependencies
3. Run `START_CLIENT.bat`

---

**Questions? Check:**
- `CLIENT_FIX_INSTRUCTIONS.md` - Detailed troubleshooting
- `DEPLOY/CLIENT_QUICK_START.md` - Quick start guide
- `voice_assistant_v2/client/GUI_CLIENT.md` - GUI client documentation

**Status:** Ready to update! 🎉
