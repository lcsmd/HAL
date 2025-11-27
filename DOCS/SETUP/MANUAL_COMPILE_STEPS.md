# Manual Steps to Complete Voice Listener Compilation

## Current Status
All code fixes are complete in **BP/VOICE.LISTENER** (6045 bytes, updated 2:18 AM):
- ✅ Removed ON/OFF ERROR (not supported in QM)
- ✅ Added SKT$BLOCKING flag to WRITE.SOCKET for reliable data transmission
- ✅ Uses JPARSE for JSON parsing
- ✅ Source file is ready to compile

## Problem
Cannot automate telnet login to QM - connection resets after sending username

## Manual Steps Required

### 1. Log into QM via telnet
```
telnet localhost 4243
Username: LAWR
Password: apgar-66
Account: HAL
```

### 2. Compile and catalog
```
BASIC BP VOICE.LISTENER
CATALOG BP VOICE.LISTENER
```

### 3. Verify compilation
- Check that **BP.OUT\VOICE.LISTENER** exists
- Should be a compiled object file

### 4. Start PHANTOM
```
PHANTOM VOICE.LISTENER
```

### 5. Test directly
```
cd C:\qmsys\hal
python test_qm_direct_newline.py
```

**Expected output:**
```
[OK] Connected!
[OK] Message sent
[OK] Received response with intent: MEDICATION
```

### 6. Test full system (Voice Gateway + QM Listener)
```
python tests\test_text_input.py
```

**Expected output:**
```
Response: I detected a medication query: What medications am I taking?
Intent: MEDICATION
```

## Key Changes Made

### VOICE.LISTENER (BP/VOICE.LISTENER)
1. **Line 39**: Changed `WRITE.SOCKET(CLIENT.SKT, RESPONSE.JSON, 0, 0)` 
   to `WRITE.SOCKET(CLIENT.SKT, RESPONSE.JSON, SKT$BLOCKING, 5000)`
   - This ensures data is flushed before socket closes
   - Prevents connection abort errors

2. **Removed lines 38-42**: ON ERROR / OFF ERROR not supported in QM
   - Removed error handler
   - Simplified to direct READ.SOCKET call

3. **Uses JPARSE**: Proper JSON parsing (from BP/%Dx12)
   - JPARSE(MESSAGE.JSON) for parsing
   - JSON.OBJ{"transcription"} for field extraction
   - Fallback to SIMPLE.PARSE if JPARSE fails

## Troubleshooting

### If BASIC fails
- Check BP/VOICE.LISTENER exists
- Run: `LIST BP VOICE.LISTENER` to view source
- Check BP.OUT\VOICE.LISTENER.LIS for errors

### If PHANTOM doesn't start
- Check user limit: `LIST.READU` (max 6 users)
- Logout old phantoms: `qm -k <uid>`
- Check COMO log: `$COMO/PH*` files for errors

### If test fails with connection abort
- Verify SKT$BLOCKING is in WRITE.SOCKET call
- Check BP.OUT\VOICE.LISTENER timestamp matches compilation time
- Restart phantom to load new code

## Files Modified
- `BP/VOICE.LISTENER` - Main listener (195 lines)
- `PY/voice_gateway.py` - Voice Gateway (reads full JSON responses)
- `compile_qm_direct.py` - Compilation script (telnet issues)
- `test_qm_direct_newline.py` - Direct test script

## Next Steps After 100% Working
1. Start Voice Gateway: `python PY/voice_gateway.py`
2. Test with real audio through clients
3. Start Faster-Whisper service on ubuai.q.lcs.ai:9000
4. Test end-to-end voice input
