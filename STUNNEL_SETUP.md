# Stunnel Setup for OpenQM AI Integration

## Installation

1. **Download stunnel for Windows:**
   - Visit: https://www.stunnel.org/downloads.html
   - Download the latest Windows installer (e.g., `stunnel-5.71-win64-installer.exe`)

2. **Install stunnel:**
   - Run the installer
   - Default installation path: `C:\Program Files (x86)\stunnel\`
   - Install as a Windows service (recommended)

3. **Configure stunnel:**
   - Copy `C:\QMSYS\HAL\stunnel.conf` to `C:\Program Files (x86)\stunnel\config\stunnel.conf`
   - Or update the existing config file with the OpenAI and Anthropic tunnels

4. **Start stunnel service:**
   ```powershell
   # Start the service
   Start-Service stunnel
   
   # Set to start automatically
   Set-Service -Name stunnel -StartupType Automatic
   ```

5. **Verify it's running:**
   ```powershell
   # Check if ports are listening
   netstat -an | findstr "8443"
   netstat -an | findstr "8444"
   ```

## Configuration Details

The `stunnel.conf` file creates two tunnels:

- **OpenAI**: localhost:8443 → api.openai.com:443
- **Anthropic**: localhost:8444 → api.anthropic.com:443

## Testing

After stunnel is running, compile and test:

```
:basic hal.bp ask.ai.b
:catalog hal.bp ask.ai.b local
:ask.b gpt-4o what is egpa
:ask.b claude-3-5-sonnet-20241022 what is egpa
```

## Benefits over Python approach

✅ **Faster** - No Python startup overhead (~100-200ms saved)
✅ **Connection pooling** - Reuses connections for better performance
✅ **Native** - Pure UniBasic with !CALLHTTP
✅ **Reliable** - Dedicated SSL/TLS proxy
✅ **Lightweight** - Runs as Windows service

## Troubleshooting

If connections fail:
1. Check stunnel service is running: `Get-Service stunnel`
2. Check logs: `C:\QMSYS\HAL\stunnel.log`
3. Verify ports are listening: `netstat -an | findstr "8443 8444"`
4. Test with curl: `curl http://localhost:8443/v1/models -H "Authorization: Bearer YOUR_KEY"`
