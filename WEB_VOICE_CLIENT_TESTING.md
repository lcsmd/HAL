# HAL Web Voice Client - Testing & Troubleshooting Guide

## Quick Start - Testing the Fix

### Step 1: Update HAProxy Configuration

**On HAProxy server (ubu6 / 10.1.50.100):**

```bash
# Backup current config
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup

# Copy the updated config from this repo
sudo cp haproxy.cfg /etc/haproxy/haproxy.cfg

# Verify configuration
sudo haproxy -c -f /etc/haproxy/haproxy.cfg

# Reload HAProxy (no downtime)
sudo systemctl reload haproxy

# Check status
sudo systemctl status haproxy
```

### Step 2: Start the Servers

**On Windows Server (10.1.34.103):**

```bash
# Option 1: Using the startup script (Linux/Mac/Git Bash)
./start_web_voice_servers.sh

# Option 2: Using Windows batch file
start_web_voice_servers.bat

# Option 3: Manual start
cd voice_assistant_v2/web_client
python -m http.server 8080 &

cd ../../PY
python voice_gateway_web.py &
```

### Step 3: Verify Servers Are Running

```bash
# Check if HTTP server is running
curl http://10.1.34.103:8080

# Check if Voice Gateway is running
netstat -an | grep 8768

# Or on Windows
netstat -an | findstr 8768
```

### Step 4: Test WebSocket Connection

**Option A: Using Browser Console**

1. Open https://hal.lcs.ai in your browser
2. Open Developer Tools (F12)
3. Go to Console tab
4. Look for connection messages:
   ```
   [OK] Connected to HAL
   ```

**Option B: Using wscat (command line)**

```bash
# Install wscat if needed
npm install -g wscat

# Test WebSocket connection
wscat -c wss://hal.lcs.ai

# You should see:
Connected (press CTRL+C to quit)

# Try sending a message:
{"type":"text_input","text":"hello"}

# You should get a response
```

### Step 5: Test Text Input

1. Open https://hal.lcs.ai
2. Wait for "Connected!" status
3. Type "hello" in the text box
4. Press Enter or click Send
5. You should see a response from HAL

### Step 6: Test Voice Input (Optional)

1. Click the microphone button (🎤)
2. Allow microphone access if prompted
3. Say "Hey Jarvis"
4. Speak your command
5. Wait for response

---

## Troubleshooting

### Issue: "Disconnected. Reconnecting..." Loop

**Symptoms:**
- Browser shows "Connecting..." → "Connected!" → "Disconnected" repeatedly
- No response to text input

**Diagnosis:**

1. **Check HAProxy logs:**
   ```bash
   sudo tail -f /var/log/haproxy.log
   ```
   Look for requests to `hal.lcs.ai` and which backend they're routed to.

2. **Check Voice Gateway logs:**
   ```bash
   tail -f logs/voice_gateway.log
   ```
   Look for "Client connected" messages.

3. **Check WebSocket handshake:**
   - Open browser DevTools → Network tab
   - Filter by "WS" (WebSocket)
   - Click on the WebSocket connection
   - Check Headers → Response Headers for "Upgrade: websocket"

**Solutions:**

A. **HAProxy not routing WebSocket correctly:**
   - Verify `use-server hal2_ws if is_websocket is_websocket_upgrade` line exists
   - Check ACLs are matching: `hdr(Connection) -i upgrade` and `hdr(Upgrade) -i websocket`
   - Reload HAProxy: `sudo systemctl reload haproxy`

B. **Voice Gateway not running:**
   - Check if process is running: `ps aux | grep voice_gateway_web`
   - Check port is listening: `netstat -an | grep 8768`
   - Restart: `python PY/voice_gateway_web.py`

C. **Firewall blocking port 8768:**
   - Windows: `netsh advfirewall firewall add rule name="HAL Voice Gateway" dir=in action=allow protocol=TCP localport=8768`
   - Linux: `sudo ufw allow 8768/tcp`

### Issue: "Connection error" in Browser

**Symptoms:**
- Status shows "Connection error"
- Console shows WebSocket error

**Solutions:**

1. **Check SSL certificate:**
   ```bash
   # Verify cert is valid for hal.lcs.ai
   openssl s_client -connect hal.lcs.ai:443 -servername hal.lcs.ai
   ```

2. **Check DNS resolution:**
   ```bash
   nslookup hal.lcs.ai
   # Should resolve to HAProxy server IP
   ```

3. **Test direct connection (bypass HAProxy):**
   - Temporarily change `serverUrl` in client.js:
     ```javascript
     this.serverUrl = 'ws://10.1.34.103:8768';
     ```
   - Open http://10.1.34.103:8080 (not HTTPS)
   - If this works, issue is with HAProxy

### Issue: Text Input Not Responding

**Symptoms:**
- Connection shows "Connected!"
- Typing and pressing Enter does nothing
- No error messages

**Diagnosis:**

1. **Check WebSocket is actually open:**
   - Open browser console
   - Type: `window.halClient.ws.readyState`
   - Should return `1` (OPEN)

2. **Check message is being sent:**
   - Add logging to client.js:
     ```javascript
     sendText() {
         const text = this.textInput.value.trim();
         console.log('[DEBUG] Sending:', text);
         // ... rest of code
     }
     ```

3. **Check server receives message:**
   - Look at voice_gateway.log for "[VoiceGatewayWeb] Client connected" and message handling

**Solutions:**

A. **WebSocket closed after initial connection:**
   - Check timeout settings in HAProxy (should be 3600s)
   - Check Voice Gateway isn't crashing (view logs)

B. **QueryRouter import failing:**
   - Check PY/query_router.py exists
   - Run test: `cd PY && python -c "from query_router import QueryRouter; print('OK')"`
   - If fails, check Python dependencies: `pip install -r requirements.txt`

C. **JSON parsing error:**
   - Check client is sending valid JSON
   - Check server logs for "Invalid JSON" errors

### Issue: Wake Word Not Detected

**Symptoms:**
- Microphone button works (turns red)
- Saying "Hey Jarvis" doesn't trigger anything
- No transcription appears

**Expected Behavior:**
The current implementation does NOT have wake word detection. Audio streaming will start when you click the microphone button, and transcription happens after you stop speaking (silence timeout).

**If you want wake word detection:**
You would need to add openwakeword library and implement detection in voice_gateway_web.py. This is currently out of scope.

**Workaround:**
1. Click microphone button
2. Speak your command directly (no need to say "Hey Jarvis")
3. Stop speaking and wait 1.5 seconds
4. Transcription will happen automatically

### Issue: No Response from HAL

**Symptoms:**
- Connection works
- Text is sent
- No response appears

**Diagnosis:**

1. **Check QueryRouter:**
   ```bash
   cd PY
   python -c "from query_router import QueryRouter; r = QueryRouter(); print(r.route_query('hello', 'test', []))"
   ```
   Should return a dict with "text" key.

2. **Check Ollama is running:**
   ```bash
   curl http://10.1.10.20:11434/api/version
   ```

3. **Check Voice Gateway can reach Ollama:**
   ```bash
   # From Windows Server
   curl http://10.1.10.20:11434/api/version
   ```

**Solutions:**

A. **Ollama not running:**
   - SSH to ubuai: `ssh lawr@10.1.10.20`
   - Check: `systemctl status ollama`
   - Start: `systemctl start ollama`

B. **QueryRouter failing:**
   - Check logs/voice_gateway.log for errors
   - Test query router independently
   - Check if model is loaded: `curl http://10.1.10.20:11434/api/tags`

C. **Network issue:**
   - Verify Windows Server can reach Ubuntu Server:
     ```bash
     ping 10.1.10.20
     curl http://10.1.10.20:11434/api/version
     ```

---

## Verification Checklist

Before declaring the system "working", verify all these:

- [ ] HAProxy config updated and reloaded
- [ ] HTTP server running on port 8080
- [ ] Voice Gateway running on port 8768
- [ ] Can access https://hal.lcs.ai in browser
- [ ] Status shows "Connected!" within 3 seconds
- [ ] Typing "hello" and pressing Enter gets a response
- [ ] Response appears within 5 seconds
- [ ] Clicking microphone button changes to red (listening)
- [ ] Speaking a command gets transcribed (optional for now)
- [ ] No errors in browser console
- [ ] No errors in voice_gateway.log
- [ ] HAProxy log shows requests going to hal2_backend

---

## Monitoring Commands

**Check server status:**
```bash
# On Windows Server
ps aux | grep "python.*8080\|voice_gateway"  # Linux/Mac
tasklist | findstr python                     # Windows

# Check ports
netstat -an | grep "8080\|8768"              # Linux/Mac
netstat -an | findstr "8080 8768"            # Windows
```

**View logs in real-time:**
```bash
# Voice Gateway
tail -f logs/voice_gateway.log

# HTTP Server
tail -f logs/http_server.log

# HAProxy
sudo tail -f /var/log/haproxy.log
```

**Test connectivity:**
```bash
# HTTP server
curl -I http://10.1.34.103:8080

# WebSocket (requires wscat)
wscat -c ws://10.1.34.103:8768

# Through HAProxy
curl -I https://hal.lcs.ai
```

---

## Performance Metrics

**Expected response times:**
- WebSocket connection: < 1 second
- Text query response: 1-3 seconds (depends on LLM)
- Voice transcription: 1-2 seconds
- Total voice query: 3-5 seconds

**If response times are slower:**
1. Check network latency to ubuai (ping 10.1.10.20)
2. Check Ollama is using GPU (check GPU utilization on ubuai)
3. Check model loaded: `curl http://10.1.10.20:11434/api/tags`
4. Consider using a smaller/faster model

---

## Next Steps After Fix

Once the WebSocket connection is stable:

1. **Add error handling improvements**
   - Better error messages to user
   - Retry logic with exponential backoff
   - Graceful degradation

2. **Add visual feedback**
   - Show when message is being sent
   - Show "HAL is thinking..." during processing
   - Animate the microphone during listening

3. **Optimize performance**
   - Cache common responses
   - Compress WebSocket messages
   - Use faster LLM model for simple queries

4. **Add features**
   - Text-to-speech responses
   - Multi-language support
   - User authentication
   - Conversation history persistence

---

## Getting Help

If issues persist:

1. **Gather diagnostic info:**
   ```bash
   # Save all logs
   cat logs/voice_gateway.log > diagnostics.txt
   sudo tail -100 /var/log/haproxy.log >> diagnostics.txt
   
   # Add system info
   python --version >> diagnostics.txt
   netstat -an | grep "8080\|8768" >> diagnostics.txt
   ```

2. **Check browser console:**
   - Open DevTools (F12)
   - Copy all errors from Console tab
   - Copy WebSocket messages from Network tab

3. **Test minimal setup:**
   - Stop HAProxy
   - Connect directly to WebSocket: `ws://10.1.34.103:8768`
   - If this works, issue is with HAProxy
   - If this fails, issue is with Voice Gateway

4. **Review documentation:**
   - HAL_SYSTEM_MASTER.md - System architecture
   - WEB_VOICE_CLIENT_ARCHITECTURE.md - Component details
   - ERRORS_ENCOUNTERED.md - Known issues and solutions

---

**Last Updated:** 2025-12-04
