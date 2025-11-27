# HAL Mac Client - One-Line Deployment

## Setup (On Windows QM Server)

### 1. Start the installer server:

```bash
cd C:\qmsys\hal\clients
python serve_installer.py
```

You'll see output like:
```
HAL Mac Installer Server
========================================
Serving at:
  http://192.168.1.100:8080/

On your Mac, run:
  curl -fsSL http://192.168.1.100:8080/install_hal_mac.sh | bash
```

## Deploy (On Mac)

### Option 1: Auto-detect server from URL
Copy the exact command shown by the server:

```bash
curl -fsSL http://192.168.1.100:8080/install_hal_mac.sh | bash
```

### Option 2: Specify server explicitly
```bash
curl -fsSL http://192.168.1.100:8080/install_hal_mac.sh | HAL_SERVER=192.168.1.100 bash
```

## What It Does

The one-line installer will:
1. ✓ Check Python 3 is installed
2. ✓ Install websockets dependency
3. ✓ Download HAL client to ~/.hal-client/
4. ✓ Create configuration with your server IP
5. ✓ Add 'hal' command to PATH
6. ✓ Test connection to HAL server

## After Installation

Restart your terminal, then:

```bash
# Interactive mode
hal

# Single query
hal --query "What medications am I taking?"
```

## Troubleshooting

### Windows Firewall
Allow port 8080 for installer server:
```powershell
New-NetFirewallRule -DisplayName "HAL Installer Server" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

### Mac can't connect to installer server
1. Check Windows firewall allows port 8080
2. Test from Mac: `curl http://192.168.1.100:8080/`
3. Make sure both machines on same network

### Installation fails
Download and run manually:
```bash
curl -O http://192.168.1.100:8080/install_hal_mac.sh
chmod +x install_hal_mac.sh
./install_hal_mac.sh
```

### Python not found on Mac
Install Python 3:
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

## Alternative: Use QM COMMAND.EXECUTOR

You can also use COMMAND.EXECUTOR to start the server:

```qm
In COM.DIR/INPUT.COMMANDS.txt:
PHANTOM python clients/serve_installer.py
```

Then run COMMAND.EXECUTOR.

## What Gets Installed

```
~/.hal-client/
├── hal_client.py     # Main client
├── .env              # Configuration
└── hal               # Launcher script
```

Plus PATH entry in your shell RC file (~/.zshrc or ~/.bashrc)

## Uninstall

```bash
rm -rf ~/.hal-client
# Remove PATH line from ~/.zshrc or ~/.bashrc
```

## Security Notes

- Installer server (port 8080) only needed during installation
- Stop it after Mac deployment completes (Ctrl+C)
- Voice Gateway (port 8768) stays running for voice queries
- No authentication currently - use VPN for remote access
