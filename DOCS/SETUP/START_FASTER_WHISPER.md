# Start Faster-Whisper on ubuai

Faster-Whisper is not currently running on ubuai:9000.

## To Start It:

### Step 1: SSH to ubuai
```bash
ssh lawr@ubuai
# Password: apgar-66
```

### Step 2: Check if Faster-Whisper is installed
```bash
# Check for faster-whisper
which faster-whisper
python3 -m pip list | grep faster-whisper

# Or check for whisper service
ps aux | grep whisper
systemctl status faster-whisper  # if it's a service
```

### Step 3: Start Faster-Whisper Server

**If it's a Python script:**
```bash
# Find the whisper server script
find ~ -name "*whisper*server*" -o -name "*speech*server*"

# Start it (example, adjust path):
python3 ~/faster-whisper/server.py --port 9000 --model large-v3
```

**If it's a systemd service:**
```bash
sudo systemctl start faster-whisper
sudo systemctl status faster-whisper
```

**If it's in a docker container:**
```bash
docker ps -a | grep whisper
docker start faster-whisper
```

### Step 4: Verify It's Running
```bash
# Check port
netstat -tulpn | grep 9000

# Test endpoint
curl http://localhost:9000/health
```

## Alternative: Use speech.lcs.ai Instead

If Faster-Whisper isn't set up on ubuai, we can figure out what speech.lcs.ai uses:

```bash
# From ubuai, check what's running
sudo netstat -tulpn | grep LISTEN

# Check HAProxy config to see what port speech.lcs.ai points to
sudo cat /etc/haproxy/haproxy.cfg | grep -A 10 speech
```

## For Now: Test Without STT

You can continue testing the voice interface with text input while we get STT working:

```python
# Send text directly instead of audio
python C:\qmsys\hal\tests\test_medication_query.py
```

---

**Let me know what you find on ubuai and I'll help configure it!**
