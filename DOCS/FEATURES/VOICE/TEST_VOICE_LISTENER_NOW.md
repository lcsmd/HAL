# Test Voice Listener Now

Your VOICE_LISTENER (renamed from VOICE.LISTENER.MEDIUM) is running but crashing on messages.

## Quick Fix

I created `BP/VOICE.LISTENER.MINIMAL` which is even simpler and more stable.

## To Deploy:

```cmd
cd C:\qmsys\bin
qm HAL
```

Then:
```
LOGTO HAL
KILL.PHANTOM (find the current VOICE_LISTENER phantom and kill it)
COPY BP VOICE.LISTENER.MINIMAL BP VOICE.LISTENER OVERWRITING
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
PHANTOM BP VOICE.LISTENER
```

## Or Just Fix Current One:

The issue might be in the JSON parsing. Try stopping and restarting the current one:

```
KILL.PHANTOM (number)
PHANTOM BP VOICE.LISTENER
```

## Test After Restart:

```powershell
cd C:\qmsys\hal
python tests\test_text_input.py
```

Should see: "I detected a medication query..." instead of "Sorry, I'm having trouble..."

---

The minimal version:
- ✅ Simpler JSON parsing (less error-prone)
- ✅ Intent classification (MEDICATION, APPOINTMENT, HEALTH_DATA, GENERAL)
- ✅ Returns proper JSON responses
- ✅ More robust error handling
