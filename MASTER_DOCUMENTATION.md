# HAL AI Assistant - Master Documentation Index

**Complete documentation for the HAL AI Assistant system**

---

## 🚀 Quick Start

**New User?** Start here:
1. [WEB_VOICE_CLIENT_README.md](WEB_VOICE_CLIENT_README.md) - Overview of web voice client
2. [WEB_VOICE_CLIENT_QUICK_START.md](WEB_VOICE_CLIENT_QUICK_START.md) - User guide (if available)
3. Access HAL: **https://hal.lcs.ai**

**Developer?** Start here:
1. [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md) - System architecture
2. [TODO.md](TODO.md) - Current tasks and priorities
3. [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) - Common errors and solutions

---

## 📚 Documentation Categories

### 🎤 Web Voice Client (Current Focus)

**Main Documentation:**
- [WEB_VOICE_CLIENT_README.md](WEB_VOICE_CLIENT_README.md) - Master overview and quick links
- [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md) - Complete technical architecture
- [TODO.md](TODO.md) - Task list, priorities, known issues, timeline
- [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) - Error reference with solutions

**Status:** In Development - WebSocket connection being debugged

**Key Features:**
- Zero-installation browser interface
- Server-side wake word detection
- Cross-platform (any device with browser)
- Real SSL certificate (*.lcs.ai)

---

### 🖥️ Legacy Python Clients

**Windows Client:**
- [WINDOWS_CLIENT_DEPLOYMENT.md](WINDOWS_CLIENT_DEPLOYMENT.md) - Deployment guide
- [WINDOWS_CLIENT_QUICK_DEPLOY.md](WINDOWS_CLIENT_QUICK_DEPLOY.md) - Quick deployment
- [START_HAL_CLIENT_WINDOWS.md](START_HAL_CLIENT_WINDOWS.md) - Startup instructions
- [CLIENT_SETUP_FINAL.md](CLIENT_SETUP_FINAL.md) - Final setup instructions
- [CLIENT_VOICE_STATUS.md](CLIENT_VOICE_STATUS.md) - Voice status documentation
- [CLIENT_COMPLETE_SETUP.ps1](CLIENT_COMPLETE_SETUP.ps1) - Automated setup script

**Voice Mode:**
- [VOICE_MODE_READY.md](VOICE_MODE_READY.md) - Voice mode status
- [VOICE_MODE_SETUP.md](VOICE_MODE_SETUP.md) - Voice mode configuration
- [VOICE_SYSTEM_SETUP_COMPLETE.md](VOICE_SYSTEM_SETUP_COMPLETE.md) - Setup completion
- [FIX_WEBRTCVAD_WINDOWS.md](FIX_WEBRTCVAD_WINDOWS.md) - webrtcvad troubleshooting
- [FIX_WHISPER_CONNECTION.md](FIX_WHISPER_CONNECTION.md) - Whisper connectivity issues

**Client Updates:**
- [HOW_TO_UPDATE_CLIENT.md](HOW_TO_UPDATE_CLIENT.md) - Update procedure
- [UPDATE_CLIENT.bat](UPDATE_CLIENT.bat) - Update script
- [PULL_CLIENT_ONLY.md](PULL_CLIENT_ONLY.md) - Pull client files from GitHub

**Mac Deployment:**
- [mac_deployment_package/](mac_deployment_package/) - Mac client files

**Status:** Deprecated - Replaced by web client

---

### 🔧 System Setup & Configuration

**Auto-Start Configuration:**
- [AUTO_START_DEPLOYMENT_COMPLETE.md](AUTO_START_DEPLOYMENT_COMPLETE.md) - Auto-start deployment
- [QM_PHANTOM_AUTO_START.md](QM_PHANTOM_AUTO_START.md) - QM phantom auto-start
- [Q_POINTERS_SETUP.md](Q_POINTERS_SETUP.md) - Q-pointer configuration
- [SERVICES_AUTO_START_GUIDE.md](SERVICES_AUTO_START_GUIDE.md) - Services auto-start guide

**Local Catalog:**
- [CATALOG_LOCAL_INFO.md](CATALOG_LOCAL_INFO.md) - Local catalog information

**Remote Deployment:**
- [DEPLOY_REMOTE_CLIENTS.md](DEPLOY_REMOTE_CLIENTS.md) - Remote client deployment

**QM Integration:**
- [RUN_IN_QM.txt](RUN_IN_QM.txt) - Running commands in QM
- [START_QM_LISTENER.txt](START_QM_LISTENER.txt) - QM listener startup

---

### 🏗️ Architecture & Technical

**System Architecture:**
- [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md) - Web client architecture (CURRENT)
- [ROUTER_SETUP.md](ROUTER_SETUP.md) - Query router setup

**Data Structures:**
- [DICT_ATTRIBUTE_REFERENCE.md](DICT_ATTRIBUTE_REFERENCE.md) - Dictionary attributes
- [DOCS.md](DOCS.md) - Documentation system

**Compilation & Build:**
- [COMPILE_AND_TEST_DOCS.md](COMPILE_AND_TEST_DOCS.md) - Compilation and testing
- [COMPILATION_REPORT.md](COMPILATION_REPORT.md) - Compilation report

---

### 📖 Project Documentation

**Main Documentation:**
- [README.md](README.md) - Project README
- [READ_ME_FIRST.txt](READ_ME_FIRST.txt) - First-time setup guide

**GitHub Setup:**
- [QUICK_GITHUB_SETUP.md](QUICK_GITHUB_SETUP.md) - Quick GitHub setup
- [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md) - Push to GitHub guide

**Migration & Backup:**
- [BACKUP_SUMMARY.md](BACKUP_SUMMARY.md) - Backup summary
- [FIXING_LARGE_FILES.md](FIXING_LARGE_FILES.md) - Fixing large files in Git

---

### 🛠️ Development & Deployment

**Development Workflow:**
- [TODO.md](TODO.md) - Current tasks and priorities ⭐
- [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) - Error reference ⭐

**Scripts & Setup:**
- [SETUP_SCRIPT_README.md](SETUP_SCRIPT_README.md) - Setup script documentation
- [QUICK_DEPLOY.txt](QUICK_DEPLOY.txt) - Quick deployment steps

**Testing:**
- [test_*.py](.) - Various test scripts in root directory

---

### 🐛 Troubleshooting & Fixes

**Error Reference:**
- [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) - Comprehensive error reference ⭐

**Specific Issues:**
- [FIX_WEBRTCVAD_WINDOWS.md](FIX_WEBRTCVAD_WINDOWS.md) - webrtcvad installation issues
- [FIX_WHISPER_CONNECTION.md](FIX_WHISPER_CONNECTION.md) - Whisper connectivity
- [CLIENT_FIX_INSTRUCTIONS.md](CLIENT_FIX_INSTRUCTIONS.md) - Client fixes
- [FIXING_LARGE_FILES.md](FIXING_LARGE_FILES.md) - Large files in Git

---

## 🗂️ File Organization

### Configuration Files
```
config/
└── router_config.json          # Query router configuration
```

### Python Backend
```
PY/
├── voice_gateway_web.py        # Web voice gateway (CURRENT)
├── voice_gateway_web_secure.py # SSL variant
├── voice_gateway_with_http.py  # Combined HTTP+WebSocket
├── query_router.py             # Query routing
├── llm_handler.py              # LLM integration
├── home_assistant_handler.py   # Home Assistant
├── database_handler.py         # Database queries
└── ai_server.py                # AI.SERVER
```

### Web Client
```
voice_assistant_v2/
└── web_client/
    ├── index.html              # Main UI
    ├── client.js               # Client logic
    ├── serve.py                # HTTP server
    ├── cert.pem               # SSL cert (for reference)
    └── key.pem                # SSL key (for reference)
```

### Legacy Clients
```
voice_assistant_v2/client/      # Python client files
clients/                        # Legacy client files
mac_deployment_package/         # Mac client
```

### Services
```
ubuai_services/                 # Ubuntu AI services
├── whisper_server.py
├── faster-whisper.service
├── ollama.service
└── install_services.sh
```

---

## 🎯 Current Focus

### Active Development
**Web Voice Client** - Browser-based interface (https://hal.lcs.ai)

**Status:** In Development  
**Priority:** HIGH  
**Current Issue:** WebSocket connection instability

**See:** [TODO.md](TODO.md) for detailed task list

---

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Browser (Any Device)                                    │
│  - https://hal.lcs.ai                                   │
│  - Zero installation                                     │
│  - Voice + Text input                                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  HAProxy (ubu6)                                          │
│  - SSL termination (*.lcs.ai)                           │
│  - Routes HTTP → 10.1.34.103:8080                       │
│  - Routes WebSocket → 10.1.34.103:8768                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Windows Server (10.1.34.103)                           │
│  ├─ Port 8080: HTTP (static files)                      │
│  ├─ Port 8768: Voice Gateway (WebSocket + wake word)    │
│  └─ Port 8745: AI.SERVER (QM integration)               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Ubuntu Server (10.1.10.20)                             │
│  ├─ Port 8001: Whisper STT                              │
│  └─ Port 11434: Ollama LLM                              │
└─────────────────────────────────────────────────────────┘
```

**Detailed Architecture:** [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md)

---

## 📋 Documentation Standards

### File Naming Convention
- `[COMPONENT]_[TYPE].md` - Component-specific documentation
- `[ACTION]_[COMPONENT].md` - Action/procedure documentation
- `[TOPIC].md` - General topic documentation
- `MASTER_DOCUMENTATION.md` - This file (central index)

### Documentation Types
- **README** - Overview and introduction
- **ARCHITECTURE** - Technical design and structure
- **SETUP** - Installation and configuration
- **GUIDE** - Step-by-step procedures
- **REFERENCE** - Lookup information
- **TODO** - Task lists and roadmaps
- **ERRORS** - Error reference and solutions

### Required Sections
1. Overview/Purpose
2. Status (if applicable)
3. Content organized by topic
4. Links to related documentation
5. Last updated date

---

## 🔗 External Resources

### GitHub Repository
- **URL:** https://github.com/lcsmd/HAL
- **Branch:** main
- **Clone:** `git clone https://github.com/lcsmd/HAL.git`

### Key Dependencies
- **OpenWakeWord:** https://github.com/dscripka/openWakeWord
- **Faster-Whisper:** https://github.com/guillaumekln/faster-whisper
- **Ollama:** https://ollama.ai/
- **HAProxy:** https://www.haproxy.org/

### Useful Tools
- **WebSocket Testing:** wscat, Postman
- **Audio Testing:** Audacity, sox
- **Network Testing:** curl, wget, netcat

---

## 📞 Support & Contact

### Getting Help

1. **Check Documentation:**
   - Start with relevant section above
   - Check [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) for known issues
   - Review [TODO.md](TODO.md) for current status

2. **Debug Steps:**
   - Check server logs
   - Check browser console
   - Verify services are running
   - Test with simple examples

3. **Report Issues:**
   - Document steps to reproduce
   - Include error messages
   - Note environment details
   - Check if already in [TODO.md](TODO.md)

---

## 📊 Project Status

### Current Version
- **Web Client:** v1.0 (In Development)
- **Python Client:** v2.0 (Deprecated)
- **Core System:** v3.0 (Stable)

### Timeline
- **Started:** 2024
- **Web Client Development:** December 2025
- **Current Focus:** WebSocket debugging
- **Target:** Production release Q1 2026

### Key Milestones
- ✅ Python client working (deprecated)
- ✅ Web client UI completed
- ✅ Server-side processing implemented
- ✅ HAProxy configuration with SSL
- ⏳ WebSocket connection stability (in progress)
- ⏳ End-to-end voice testing
- ⏳ Production deployment
- ⏳ Authentication layer

---

## 🗺️ Documentation Roadmap

### Completed
- ✅ Web voice client architecture
- ✅ Error reference guide
- ✅ TODO list with priorities
- ✅ Master documentation index (this file)

### In Progress
- ⏳ User manual for web client
- ⏳ API documentation
- ⏳ Deployment guide

### Planned
- 📝 Video tutorials
- 📝 Architecture diagrams
- 📝 Performance optimization guide
- 📝 Security best practices
- 📝 Contribution guidelines

---

## 🔍 Quick Reference

### Essential Commands

**Start Services (Windows Server):**
```powershell
# HTTP Server
cd C:\qmsys\hal\voice_assistant_v2\web_client
python -m http.server 8080

# Voice Gateway
cd C:\qmsys\hal
python PY\voice_gateway_web.py

# AI.SERVER
python PY\ai_server.py
```

**Check Status:**
```powershell
# Check ports
netstat -ano | Select-String ":(8080|8768|8745)"

# Check processes
Get-Process python
```

**Git Operations:**
```bash
# Pull latest
git pull origin main

# Commit changes
git add -A
git commit -m "Description"
git push origin main
```

### Essential URLs
- **Web Client:** https://hal.lcs.ai
- **HAProxy Stats:** http://ubu6:8404/stats
- **GitHub Repo:** https://github.com/lcsmd/HAL

### Essential Ports
- **443** - HTTPS (HAProxy frontend)
- **8080** - HTTP static files
- **8768** - Voice Gateway (WebSocket)
- **8745** - AI.SERVER
- **8001** - Whisper STT (Ubuntu)
- **11434** - Ollama LLM (Ubuntu)

---

## 📝 Notes

### Development Philosophy
- **Zero Installation:** No client-side setup required
- **Server-Side Processing:** Leverage powerful server resources
- **Cross-Platform:** Works on any device with browser
- **Documentation First:** Comprehensive docs for maintainability
- **Error Prevention:** Learn from mistakes (see ERRORS_ENCOUNTERED.md)

### Best Practices
1. Always backup before major changes
2. Test incrementally (small changes)
3. Document as you go
4. Commit frequently with clear messages
5. Review TODO.md before starting work
6. Update documentation when changing code

### Deprecated Features
- Python desktop client (replaced by web client)
- Self-signed SSL certificates (replaced by wildcard cert)
- Client-side wake word detection (moved to server)
- Manual client deployment (replaced by URL access)

---

## 🔄 Document Maintenance

### Update Schedule
- **This File:** Update when adding new documentation
- **TODO.md:** Update daily during active development
- **ERRORS_ENCOUNTERED.md:** Update when encountering new errors
- **Architecture Docs:** Update when system changes

### Review Checklist
- [ ] Links work and point to correct files
- [ ] Status information is current
- [ ] New documentation is indexed
- [ ] Deprecated docs are marked
- [ ] External resources are valid

### Version History
- **v1.0** (2025-12-03) - Initial master documentation index

---

**Last Updated:** 2025-12-03 20:15 PST  
**Maintained By:** Droid (Factory AI)  
**Purpose:** Central hub for all HAL AI Assistant documentation

---

## 🎯 Start Here Based on Your Role

### 👤 End User
1. [WEB_VOICE_CLIENT_README.md](WEB_VOICE_CLIENT_README.md) - What is HAL and how to use it
2. Go to https://hal.lcs.ai and start using HAL

### 👨‍💻 Developer (New to Project)
1. [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md) - Understand the system
2. [TODO.md](TODO.md) - See what needs to be done
3. [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) - Learn from past mistakes
4. Clone repo and start coding

### 🔧 System Administrator
1. [SERVICES_AUTO_START_GUIDE.md](SERVICES_AUTO_START_GUIDE.md) - Service management
2. [WEB_VOICE_CLIENT_ARCHITECTURE.md](WEB_VOICE_CLIENT_ARCHITECTURE.md) - System architecture
3. Check server status and logs

### 🐛 Troubleshooting an Issue
1. [ERRORS_ENCOUNTERED.md](ERRORS_ENCOUNTERED.md) - Known errors and solutions
2. [TODO.md](TODO.md) - Check known issues section
3. Check relevant architecture documentation
4. Review server logs

### 📚 Writing Documentation
1. This file (MASTER_DOCUMENTATION.md) - Understand structure
2. Follow naming conventions
3. Add entry to appropriate section
4. Update "Last Updated" date
5. Commit with clear message

---

**Need help? Start with the relevant section above, then check the linked documentation.**
