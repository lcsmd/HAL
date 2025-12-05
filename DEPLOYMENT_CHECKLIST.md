# HAL Web Voice Client - Deployment Checklist

**Issue:** WebSocket connection unstable - browser connects then immediately disconnects  
**Fix Date:** 2025-12-04  
**Target Deployment:** Immediate

---

## Pre-Deployment Review

### ✅ Changes Made

**Code Changes:**
- [x] Fixed HAProxy WebSocket routing in `haproxy.cfg`
- [x] Fixed Python import path in `PY/voice_gateway_web.py`
- [x] Created startup scripts (`.sh` and `.bat`)
- [x] Created comprehensive documentation

**Documentation Created:**
- [x] WEB_VOICE_CLIENT_TESTING.md - Testing & troubleshooting guide
- [x] WEB_VOICE_CLIENT_FIX_SUMMARY.md - Detailed fix documentation
- [x] WEB_VOICE_QUICK_REFERENCE.md - Quick reference card
- [x] DEPLOYMENT_CHECKLIST.md - This file

**Risk Assessment:**
- **Risk Level:** LOW
- **Impact:** Configuration changes only, no code logic changes
- **Rollback Time:** < 2 minutes
- **Expected Downtime:** < 1 minute (HAProxy reload)

---

## Deployment Steps

### Step 1: Commit Changes to Git ✅

```bash
cd /Users/lawr/Projects/hal

# Review changes
git status
git diff haproxy.cfg
git diff PY/voice_gateway_web.py

# Add all changes
git add haproxy.cfg
git add PY/voice_gateway_web.py
git add start_web_voice_servers.sh start_web_voice_servers.bat stop_web_voice_servers.sh
git add WEB_VOICE_CLIENT_*.md
git add DEPLOYMENT_CHECKLIST.md

# Commit
git commit -m "fix: resolve WebSocket connection issues for web voice client

- Fix HAProxy WebSocket routing (split ACLs, proper use-server directive)
- Fix Python import path in voice_gateway_web.py
- Add startup scripts for easy server management
- Add comprehensive testing and troubleshooting documentation

Fixes #1 (WebSocket connection loop)
Resolves TODO.md priority items 1, 2, 3"

# Push to remote
git push origin main
```

**Status:** ⏳ Pending

---

### Step 2: Backup Current Configuration ✅

**On HAProxy Server (ubu6 / 10.1.50.100):**

```bash
ssh lawr@10.1.50.100 -p 2222

# Backup current HAProxy config
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup.$(date +%Y%m%d_%H%M%S)

# Verify backup exists
ls -lh /etc/haproxy/haproxy.cfg.backup.*

# Note the backup filename for rollback
```

**On Windows Server (10.1.34.103):**

```bash
# Backup current code (if not already in git)
cd C:\qmsys\hal
git status
# If there are uncommitted changes, commit or stash them
```

**Status:** ⏳ Pending

---

### Step 3: Deploy HAProxy Configuration ✅

**On HAProxy Server:**

```bash
ssh lawr@10.1.50.100 -p 2222

# Pull latest code (if repo is accessible from HAProxy server)
cd /path/to/hal
git pull

# Or: Copy manually
# scp haproxy.cfg lawr@10.1.50.100:/tmp/haproxy.cfg

# Copy to HAProxy config location
sudo cp /path/to/hal/haproxy.cfg /etc/haproxy/haproxy.cfg
# Or: sudo cp /tmp/haproxy.cfg /etc/haproxy/haproxy.cfg

# Verify configuration syntax
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Expected output: "Configuration file is valid"
```

**If syntax check FAILS:**
```bash
# DO NOT PROCEED - Restore backup
sudo cp /etc/haproxy/haproxy.cfg.backup.XXXXXX /etc/haproxy/haproxy.cfg
# Investigate syntax errors
```

**If syntax check PASSES:**
```bash
# Reload HAProxy (graceful, no downtime)
sudo systemctl reload haproxy

# Check status
sudo systemctl status haproxy

# Should show: "active (running)"

# Monitor logs for errors
sudo tail -f /var/log/haproxy.log
# Watch for 1 minute, press Ctrl+C

# If no errors, proceed to next step
```

**Status:** ⏳ Pending

---

### Step 4: Deploy Code to Windows Server ✅

**On Windows Server (10.1.34.103):**

```bash
# Stop existing servers
cd C:\qmsys\hal

# If using Git Bash or WSL:
./stop_web_voice_servers.sh

# Or manually:
taskkill /F /IM python.exe

# Pull latest code
git pull origin main

# Verify changes applied
git log --oneline -3

# Make scripts executable (Git Bash/WSL only)
chmod +x start_web_voice_servers.sh stop_web_voice_servers.sh

# Review updated files
git diff HEAD~1 PY/voice_gateway_web.py
```

**Status:** ⏳ Pending

---

### Step 5: Start Updated Services ✅

**On Windows Server:**

```bash
cd C:\qmsys\hal

# Option 1: Using batch file (Windows)
start_web_voice_servers.bat

# Option 2: Using shell script (Git Bash/WSL)
./start_web_voice_servers.sh

# Wait 5 seconds for services to start
```

**Verify services are running:**
```bash
# Check ports are listening
netstat -an | findstr "8080 8768"

# Should see:
#   TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING
#   TCP    0.0.0.0:8768           0.0.0.0:0              LISTENING

# Check logs for errors
tail -f logs/voice_gateway.log
tail -f logs/http_server.log

# Look for:
#   [VoiceGatewayWeb] Starting on ws://0.0.0.0:8768
#   No error messages or stack traces
```

**Status:** ⏳ Pending

---

### Step 6: Test WebSocket Connection ✅

**From your local machine:**

**Test 1: Basic connectivity**
```bash
# Test HTTP server
curl -I http://10.1.34.103:8080

# Expected: HTTP/1.0 200 OK

# Test through HAProxy
curl -I https://hal.lcs.ai

# Expected: HTTP/2 200
```

**Test 2: WebSocket connection**

Open browser to: **https://hal.lcs.ai**

Watch the status indicator:
- Should show "Connecting..." (< 1 second)
- Then "Connected!" (within 3 seconds)
- Should NOT show "Disconnected"

Open browser console (F12 → Console):
- Should see: `[OK] Connected to HAL`
- Should NOT see: WebSocket connection errors

**Test 3: Text input**

In the HAL web client:
1. Type: `hello`
2. Press Enter or click Send
3. Should see your message appear on the right (blue bubble)
4. Within 3 seconds, HAL's response should appear on left (white bubble)

**Test 4: Multiple messages**

Send 5 messages in a row:
- `hello`
- `what time is it`
- `tell me a joke`
- `what is 2+2`
- `goodbye`

All should get responses with no errors.

**Test 5: Connection stability**

Leave the page open for 5 minutes. Connection should stay "Connected!" the entire time.

**Status:** ⏳ Pending

---

### Step 7: Monitor for Issues ✅

**Monitor logs for 10 minutes:**

**HAProxy logs:**
```bash
ssh lawr@10.1.50.100 -p 2222
sudo tail -f /var/log/haproxy.log

# Look for:
#   - Requests going to "hal2_backend/hal2_ws" (WebSocket)
#   - Requests going to "hal2_backend/hal2_http" (HTTP)
#   - No error 502, 503, 504
```

**Voice Gateway logs:**
```bash
# On Windows Server
tail -f C:\qmsys\hal\logs\voice_gateway.log

# Look for:
#   - "Client connected: [session-id]"
#   - "_handle_message" entries
#   - NO exception stack traces
```

**Browser console:**
```
# Keep browser DevTools open
# Watch Console tab for errors
# Watch Network tab → WS for WebSocket status
```

**Status:** ⏳ Pending

---

## Rollback Procedure

**If issues are detected, immediately rollback:**

### Rollback HAProxy (< 1 minute)

```bash
ssh lawr@10.1.50.100 -p 2222

# Find backup file
ls -ltr /etc/haproxy/haproxy.cfg.backup.*

# Restore latest backup
sudo cp /etc/haproxy/haproxy.cfg.backup.YYYYMMDD_HHMMSS /etc/haproxy/haproxy.cfg

# Reload
sudo systemctl reload haproxy

# Verify
sudo systemctl status haproxy
```

### Rollback Code (< 2 minutes)

```bash
# On Windows Server
cd C:\qmsys\hal

# Stop servers
./stop_web_voice_servers.sh

# Revert git changes
git log --oneline -5
git revert <commit-hash>
# Or
git reset --hard HEAD~1

# Restart with old code
./start_web_voice_servers.sh
```

---

## Post-Deployment Verification

### ✅ Checklist

Once deployed, verify all these items:

**Infrastructure:**
- [ ] HAProxy config updated successfully
- [ ] HAProxy reloaded without errors
- [ ] HAProxy status is "active (running)"
- [ ] No errors in HAProxy logs

**Services:**
- [ ] HTTP server running (port 8080)
- [ ] Voice Gateway running (port 8768)
- [ ] Both ports show "LISTENING" in netstat
- [ ] No errors in service logs

**Connectivity:**
- [ ] Can access https://hal.lcs.ai
- [ ] Page loads without SSL errors
- [ ] No errors in browser console
- [ ] Status shows "Connected!" (not "Disconnected")

**Functionality:**
- [ ] Text input works (can type and send messages)
- [ ] Responses appear within 5 seconds
- [ ] Can send 10+ messages without issues
- [ ] Connection stays stable for 10+ minutes

**Performance:**
- [ ] Response time < 5 seconds
- [ ] No lag in UI
- [ ] WebSocket messages are small (<10KB typically)

---

## Success Metrics

**The deployment is successful when:**

1. ✅ All checklist items above are verified
2. ✅ No errors in any logs for 1 hour
3. ✅ At least 3 test conversations completed successfully
4. ✅ Connection remains stable for 1+ hour
5. ✅ Response times meet targets (< 5 seconds)

---

## Next Steps After Successful Deployment

Once the fix is verified working:

1. **Update TODO.md**
   - Mark issue #1 (WebSocket connection) as ✅ COMPLETE
   - Mark issue #2 (Wake word) as next priority
   - Mark issue #3 (Text input) as ✅ COMPLETE

2. **Update ERRORS_ENCOUNTERED.md**
   - Add entry for this WebSocket issue
   - Document the solution for future reference

3. **Announce success**
   - Update team/stakeholders
   - Document in project log

4. **Plan next enhancements:**
   - Visual feedback improvements
   - Error handling refinements
   - Voice wake word detection
   - TTS audio responses

---

## Troubleshooting Guide

**If issues occur during deployment:**

See: **WEB_VOICE_CLIENT_TESTING.md** for comprehensive troubleshooting.

**Quick fixes for common issues:**

**Issue: HAProxy config syntax error**
- Restore backup and review changes carefully
- Check for typos in ACL names
- Verify backend server IPs are correct

**Issue: Services won't start**
- Check if ports are already in use: `netstat -an | findstr "8080 8768"`
- Kill existing processes: `taskkill /F /IM python.exe`
- Check Python version: `python --version` (need 3.7+)

**Issue: Import errors in Python**
- Install dependencies: `pip install websockets aiohttp`
- Check sys.path is correctly set
- Verify query_router.py exists in PY/

**Issue: Still getting disconnects**
- Check HAProxy logs to see where requests are routed
- Test direct connection (bypass HAProxy): `ws://10.1.34.103:8768`
- Verify both ACLs are matching in HAProxy config

---

## Contact Info

**For deployment issues:**
- Check: WEB_VOICE_CLIENT_TESTING.md
- Review: HAL_SYSTEM_MASTER.md
- Logs: logs/voice_gateway.log, /var/log/haproxy.log

---

**Deployment Checklist Last Updated:** 2025-12-04  
**Status:** Ready for deployment  
**Estimated Time:** 15-30 minutes total
