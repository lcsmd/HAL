# HAL Web Voice Client - Errors Encountered & Solutions

## Purpose

This document records all errors encountered during development to:
1. Avoid repeating the same mistakes
2. Provide troubleshooting reference
3. Document solutions that worked
4. Help future developers

---

## Error Categories

1. [Python/Library Issues](#python-library-issues)
2. [WebSocket Issues](#websocket-issues)
3. [HAProxy Configuration](#haproxy-configuration)
4. [SSL/Certificate Issues](#ssl-certificate-issues)
5. [Audio Processing](#audio-processing)
6. [Git/Version Control](#git-version-control)

---

## Python Library Issues

### Error: `webrtcvad` Won't Install on Windows

**Error Message:**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Cause:**
- `webrtcvad` requires C++ compiler
- Windows doesn't have compiler by default

**Solution:**
- Install Visual C++ Build Tools from Microsoft
- After installation, `pip install webrtcvad` works

**Prevention:**
- Document Windows prerequisites
- Provide pre-built wheel files for common Python versions

---

### Error: `openwakeword` Models Missing

**Error Message:**
```
FileNotFoundError: melspectrogram.onnx not found
FileNotFoundError: embedding_model.onnx not found
```

**Cause:**
- Models not included in pip package
- Must be downloaded separately

**Solution:**
```python
from openwakeword.utils import download_models
download_models()
```

**Prevention:**
- Document model download step
- Add to installation script
- Check for models on startup and download if missing

---

### Error: `AttributeError: module 'ssl' has no attribute 'wrap_socket'`

**Error Message:**
```
AttributeError: module 'ssl' has no attribute 'wrap_socket'
```

**Cause:**
- Python 3.13 deprecated `ssl.wrap_socket()`
- Must use `SSLContext.wrap_socket()` instead

**Wrong Code:**
```python
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile=cert_file,
    keyfile=key_file,
    server_side=True
)
```

**Correct Code:**
```python
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_file, key_file)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
```

**Prevention:**
- Use `SSLContext` for all SSL operations
- Test with latest Python versions

---

### Error: Port Already in Use

**Error Message:**
```
OSError: [Errno 98] Address already in use
```

**Cause:**
- Previous process still running on port
- Didn't stop old server before starting new one

**Solution:**
```powershell
# Stop all Python processes
Stop-Process -Name python -Force

# Wait for ports to be released
Start-Sleep -Seconds 2

# Start new server
python voice_gateway.py
```

**Prevention:**
- Always stop old processes before starting new
- Use unique ports for testing
- Implement graceful shutdown

---

## WebSocket Issues

### Error: WebSocket Connection Closes Immediately

**Symptoms:**
- Browser connects briefly then disconnects
- Connection state cycles: Connecting → Connected → Disconnected
- No error in browser console

**Cause:**
- WebSocket handshake completes but server closes connection
- May be due to protocol mismatch or server error

**Diagnosis:**
```javascript
ws.onclose = (event) => {
    console.log('Close code:', event.code);
    console.log('Close reason:', event.reason);
};
```

**Common Close Codes:**
- 1000: Normal closure
- 1006: Abnormal closure (no close frame received)
- 1011: Server error

**Solution:**
- Check server logs for errors
- Verify server is actually receiving connections
- Add keep-alive pings

**Prevention:**
- Implement ping/pong heartbeat
- Add detailed logging on both ends
- Handle connection errors gracefully

---

### Error: `TypeError: VoiceGateway.handle_client() missing 1 required positional argument: 'path'`

**Error Message:**
```
TypeError: VoiceGateway.handle_client() missing 1 required positional argument: 'path'
```

**Cause:**
- websockets library version changed API
- Older versions: `async def handle_client(websocket, path)`
- Newer versions: `async def handle_client(websocket)`

**Wrong Code:**
```python
async def handle_client(self, websocket, path):
    ...
```

**Correct Code:**
```python
async def handle_client(self, websocket):
    ...
```

**Prevention:**
- Check websockets documentation for version
- Use latest API conventions
- Pin library versions in requirements.txt

---

### Error: WebSocket Upgrade Not Detected by HAProxy

**Symptoms:**
- All requests go to HTTP backend (port 8080)
- WebSocket requests get 502 Bad Gateway
- HAProxy logs show wrong backend used

**Cause:**
- HAProxy ACL not detecting WebSocket upgrade headers
- Wrong header check or missing ACL

**Wrong Configuration:**
```haproxy
server hal2_http 10.1.34.103:8080 check
server hal2_ws 10.1.34.103:8768 check backup
```

**Issue:** `backup` means WebSocket only used if HTTP fails!

**Correct Configuration:**
```haproxy
# Detect WebSocket upgrade requests
acl is_websocket hdr(Connection) -i upgrade
acl is_websocket hdr(Upgrade) -i websocket

# Route WebSocket to port 8768, everything else to port 8080
use-server hal2_ws if is_websocket
server hal2_http 10.1.34.103:8080 check
server hal2_ws 10.1.34.103:8768 check
```

**Prevention:**
- Test WebSocket routing specifically
- Check HAProxy logs to verify correct backend used
- Don't use `backup` for WebSocket servers

---

## HAProxy Configuration

### Error: HAProxy Routes to Fallback Backend

**Symptoms:**
- Browser gets 502 Bad Gateway
- HAProxy logs show `fallback_backend` instead of `hal2_backend`
- All requests fail

**Cause:**
- ACL for domain not defined
- Domain doesn't match any ACL
- Falls through to default_backend

**Missing Configuration:**
```haproxy
# frontend https_in
# Missing: acl is_hal2 hdr(host) -i hal2.lcs.ai
# Missing: use_backend hal2_backend if is_hal2
```

**Solution:**
```haproxy
frontend https_in
    # Add ACL for hal2.lcs.ai
    acl is_hal2 hdr(host) -i hal2.lcs.ai
    
    # Add routing BEFORE default_backend
    use_backend hal2_backend if is_hal2
    
    default_backend fallback_backend
```

**Prevention:**
- Test each domain immediately after adding
- Check HAProxy logs to verify routing
- Use HAProxy stats page to monitor backends

---

### Error: Duplicate Backend Definition

**Error Message:**
```
ALERT: backend 'hal2_backend' has the same name as backend 'hal2_backend'
```

**Cause:**
- Added backend twice
- sed command didn't fully remove old section
- Manual editing error

**Solution:**
```bash
# Backup first!
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.backup

# Remove ALL instances of backend
sudo sed -i '/^backend hal2_backend$/,/^backend /{ /^backend hal2_backend$/!{ /^backend [a-z]/!d; } }' /etc/haproxy/haproxy.cfg

# Validate before adding new
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
```

**Prevention:**
- Always backup before editing
- Validate config after changes
- Use version control for configs
- Be careful with sed ranges

---

### Error: HAProxy Timeout Too Short

**Symptoms:**
- Long-running queries fail mid-execution
- WebSocket disconnects after 30 seconds
- 504 Gateway Timeout errors

**Cause:**
- Default timeout values too short for voice processing

**Wrong Configuration:**
```haproxy
timeout server 5000ms  # Only 5 seconds!
```

**Correct Configuration:**
```haproxy
backend hal2_backend
    timeout tunnel 3600s   # 1 hour for WebSocket
    timeout server 3600s   # 1 hour for long requests
```

**Prevention:**
- Set generous timeouts for voice/AI backends
- Monitor actual request durations
- Adjust timeouts based on usage

---

## SSL Certificate Issues

### Error: Self-Signed Certificate Warnings

**Symptoms:**
- Browser shows "Not Secure" warning
- Must click "Advanced" → "Proceed anyway"
- Microphone access blocked by browser

**Cause:**
- Self-signed certificates not trusted by browsers
- Browsers require trusted CA for microphone access

**Wrong Approach:**
- Generate self-signed cert with openssl
- Try to use on localhost or IP address

**Correct Approach:**
- Use HAProxy with real wildcard certificate
- Let HAProxy terminate SSL
- Backend servers use plain HTTP/WebSocket

**Solution:**
```haproxy
frontend https_in
    bind *:443 ssl crt /etc/haproxy/certs/wildcard.pem
```

**Prevention:**
- Always use real certificates for microphone access
- Use Let's Encrypt for public domains
- Use HAProxy or nginx for SSL termination

---

### Error: Certificate File Not Found

**Error Message:**
```
bind *:443 ssl crt /etc/haproxy/certs/wildcard.pem
[ALERT] cannot load SSL certificate from file
```

**Cause:**
- Certificate file doesn't exist
- Wrong path
- Permissions issue

**Solution:**
```bash
# Check file exists
ls -l /etc/haproxy/certs/wildcard.pem

# Fix permissions
sudo chmod 644 /etc/haproxy/certs/wildcard.pem

# Verify certificate is valid
openssl x509 -in /etc/haproxy/certs/wildcard.pem -text -noout
```

**Prevention:**
- Use absolute paths
- Set correct permissions (644 for cert, 600 for key)
- Validate certificate before using

---

## Audio Processing

### Error: `[Errno -9996] Invalid input device`

**Error Message:**
```
[Voice listening error: [Errno -9996] Invalid input device (no default output device)]
```

**Cause:**
- PyAudio can't find default input device
- Running on server without microphone
- Need to explicitly select input device

**Solution:**
```python
# Find available input devices
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        input_device = i
        break

# Use specific device
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    input_device_index=input_device,  # Add this!
    frames_per_buffer=1280
)
```

**Prevention:**
- Don't assume default device exists
- Explicitly enumerate and select devices
- Test on machines without microphone

---

### Error: Audio Format Mismatch

**Symptoms:**
- Wake word never detects
- Audio sounds distorted
- STT produces garbage text

**Cause:**
- Sample rate mismatch (e.g., sending 48kHz but expecting 16kHz)
- Wrong number of channels (stereo vs mono)
- Wrong bit depth (float vs int16)

**Correct Format:**
```javascript
// Browser side
const audioContext = new AudioContext({ sampleRate: 16000 });  // 16kHz
const stream = await navigator.mediaDevices.getUserMedia({ 
    audio: {
        channelCount: 1,        // Mono
        sampleRate: 16000,      // 16kHz
        echoCancellation: true,
        noiseSuppression: true
    }
});
```

```python
# Server side
RATE = 16000          # 16kHz
CHUNK = 1280          # 80ms at 16kHz
channels = 1          # Mono
format = int16        # 16-bit signed integer
```

**Prevention:**
- Document required audio format
- Validate audio format on server
- Test with different audio sources

---

## Git Version Control

### Error: `fatal: Unable to create '.git/index.lock': File exists`

**Error Message:**
```
fatal: Unable to create 'C:/QMSYS/HAL/.git/index.lock': File exists.
Another git process seems to be running in this repository
```

**Cause:**
- Previous git command crashed or was interrupted
- Lock file wasn't cleaned up
- Multiple git commands running simultaneously

**Solution:**
```powershell
Remove-Item ".git\index.lock" -Force -ErrorAction SilentlyContinue
```

**Prevention:**
- Wait for git commands to complete
- Don't run multiple git commands in parallel
- Implement proper error handling in scripts

---

### Error: Git Push Timeout

**Symptoms:**
- `git push` hangs for 60+ seconds
- Command times out without completing
- No error message, just timeout

**Cause:**
- Large number of files to push
- Slow network connection
- Git hooks taking too long

**Solution:**
```powershell
# Increase timeout
git push origin main --timeout=120

# Or push in smaller batches
git add specific_file.py
git commit -m "Small change"
git push
```

**Prevention:**
- Commit and push frequently (small batches)
- Use .gitignore to exclude large files
- Disable slow git hooks during development

---

## Best Practices Learned

### 1. WebSocket Development

**DO:**
- ✅ Implement ping/pong heartbeat
- ✅ Add detailed logging on both sides
- ✅ Handle all close codes gracefully
- ✅ Test reconnection logic
- ✅ Use proper timeouts

**DON'T:**
- ❌ Assume connection stays open forever
- ❌ Ignore close codes/reasons
- ❌ Use synchronous operations in async handlers
- ❌ Block the event loop with long operations

### 2. HAProxy Configuration

**DO:**
- ✅ Always backup before editing
- ✅ Validate config with `haproxy -c`
- ✅ Test each change immediately
- ✅ Use version control for configs
- ✅ Set appropriate timeouts for each backend

**DON'T:**
- ❌ Edit production config without backup
- ❌ Reload without validating first
- ❌ Use same timeout for all backends
- ❌ Forget to test ACL matching

### 3. Python Development

**DO:**
- ✅ Pin library versions in requirements.txt
- ✅ Test with latest Python version
- ✅ Handle exceptions gracefully
- ✅ Add logging everywhere
- ✅ Clean up resources properly

**DON'T:**
- ❌ Assume library APIs don't change
- ❌ Leave processes running when testing
- ❌ Ignore deprecation warnings
- ❌ Use blocking operations in async code

### 4. Audio Processing

**DO:**
- ✅ Document exact audio format required
- ✅ Validate format on both ends
- ✅ Test with different microphones
- ✅ Handle device enumeration properly
- ✅ Add visual feedback for audio levels

**DON'T:**
- ❌ Assume default device exists
- ❌ Mix sample rates
- ❌ Ignore audio quality issues
- ❌ Skip format conversion

### 5. SSL/HTTPS

**DO:**
- ✅ Use real certificates for microphone access
- ✅ Let reverse proxy handle SSL
- ✅ Keep certificate in secure location
- ✅ Monitor certificate expiration
- ✅ Test HTTPS before going live

**DON'T:**
- ❌ Use self-signed certs for production
- ❌ Expose private keys
- ❌ Forget to renew certificates
- ❌ Mix HTTP and HTTPS

---

## Debugging Techniques That Worked

### 1. HAProxy Debugging

```bash
# Watch logs in real-time
tail -f /var/log/haproxy.log | grep hal2

# Check which backend is being used
grep "hal2_backend" /var/log/haproxy.log | tail -20

# Test HAProxy config
haproxy -c -f /etc/haproxy/haproxy.cfg
```

### 2. WebSocket Debugging

```javascript
// Browser console
ws.onclose = (e) => {
    console.log('Close code:', e.code);
    console.log('Close reason:', e.reason);
    console.log('Was clean:', e.wasClean);
};

ws.onerror = (e) => {
    console.error('WebSocket error:', e);
};
```

### 3. Python Debugging

```python
# Add extensive logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Log all connections
print(f"[{datetime.now()}] Connection from {websocket.remote_address}")

# Log message flow
print(f"[{datetime.now()}] Received: {data.get('type')}")
print(f"[{datetime.now()}] Sending: {response.get('type')}")
```

### 4. Network Debugging

```powershell
# Check if ports are listening
netstat -ano | Select-String ":(8080|8768)"

# Check which process is using port
Get-Process -Id (Get-NetTCPConnection -LocalPort 8768).OwningProcess

# Test WebSocket connection
# Use wscat tool: npm install -g wscat
wscat -c wss://hal2.lcs.ai
```

---

## Common Mistakes to Avoid

1. **Not backing up configs before editing** - Always backup HAProxy config
2. **Running multiple instances** - Stop old processes before starting new
3. **Ignoring error messages** - Read and understand every error
4. **Not testing incrementally** - Test each small change immediately
5. **Assuming things work** - Verify every assumption with tests
6. **Mixing HTTP and HTTPS** - Use HTTPS everywhere for consistency
7. **Not checking logs** - Logs contain valuable debugging information
8. **Editing wrong file** - Verify you're editing the active config
9. **Not validating config** - Always validate before reloading
10. **Giving up too early** - Systematic debugging always finds the issue

---

**Last Updated:** 2025-12-03 19:55 PST
**Maintained By:** Droid
**Purpose:** Reference for future development and troubleshooting
