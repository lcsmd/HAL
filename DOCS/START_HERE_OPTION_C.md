# HAL Voice System - Option C Implementation

**Start here for Option C (Hybrid Architecture) deployment**

---

## 📚 Documentation Index

All documentation for Option C has been organized in the DOCS directory:

### **1. Quick Overview**
📄 **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** ← **START HERE**
- Which component runs on which machine
- 3-machine architecture diagram
- Port summary
- Quick troubleshooting

---

### **2. Quick Start (5 minutes)**
📄 **[QUICK_START_OPTION_C.md](QUICK_START_OPTION_C.md)**
- 3-step deployment
- Prerequisites check
- Quick tests
- Fast troubleshooting

---

### **3. Mac Client Setup**
📄 **[../clients/MAC_QUICK_START.md](../clients/MAC_QUICK_START.md)**
- Complete macOS setup
- Homebrew dependencies
- Microphone permissions
- Mac-specific troubleshooting

---

### **4. Complete Deployment Guide**
📄 **[DEPLOYMENT_GUIDE_OPTION_C.md](DEPLOYMENT_GUIDE_OPTION_C.md)**
- Detailed step-by-step deployment
- Component testing procedures
- Monitoring and logs
- Advanced configuration
- Complete troubleshooting matrix

---

### **5. Implementation Summary**
📄 **[OPTION_C_IMPLEMENTATION_COMPLETE.md](OPTION_C_IMPLEMENTATION_COMPLETE.md)**
- Complete architecture overview
- All deliverables
- Performance benchmarks
- Requirements checklist
- Code metrics

---

## 🖥️ Component Directories

### UBUAI Server
📁 **[../ubuai_server/](../ubuai_server/)**
- `main.py` - FastAPI server (runs on Linux GPU server)
- `requirements.txt` - Python dependencies
- `.env.example` - Configuration template
- `README.md` - API documentation

### Voice Client
📁 **[../clients/](../clients/)**
- `hal_voice_client_full.py` - Voice client (runs on YOUR MAC)
- `requirements.txt` - Python dependencies
- `MAC_QUICK_START.md` - Mac setup guide
- `README.md` - Usage documentation
- `setup_sounds.sh` - Sound setup script

### QM Listener
📁 **[../BP/](../BP/)**
- `VOICE.LISTENER` - QM Basic program (runs on Windows QM server)

---

## 🚀 Quick Start Path

**For fastest deployment, follow this order**:

1. Read: **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** (2 min)
2. Read: **[QUICK_START_OPTION_C.md](QUICK_START_OPTION_C.md)** (3 min)
3. Deploy QM Listener (2 min)
4. Deploy UBUAI Server (2 min)
5. Setup Mac Client: **[../clients/MAC_QUICK_START.md](../clients/MAC_QUICK_START.md)** (5 min)
6. Test end-to-end (1 min)

**Total time: ~15 minutes**

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────┐
│  YOUR MAC (macOS)                        │
│  Voice Client                            │
│  - Wake word detection                   │
│  - Audio capture/playback                │
└──────────────┬──────────────────────────┘
               │ WebSocket
               ▼
┌─────────────────────────────────────────┐
│  UBUAI Server (Linux - 10.1.10.20)      │
│  FastAPI Server                          │
│  - GPU transcription (Faster-Whisper)   │
│  - TTS (ElevenLabs)                      │
└──────────────┬──────────────────────────┘
               │ TCP
               ▼
┌─────────────────────────────────────────┐
│  QM Server (Windows - 10.1.34.103)      │
│  QM Voice Listener                       │
│  - Intent routing                        │
│  - Handlers                              │
└─────────────────────────────────────────┘
```

---

## ✅ What Was Built

- ✅ UBUAI FastAPI server with GPU transcription and TTS
- ✅ QM Voice Listener with improved async TCP handling
- ✅ Mac voice client with wake word, VAD, and interruption
- ✅ Audio feedback with TNG activation sound
- ✅ 10-second passive listening window
- ✅ Complete documentation for all components

---

## 🆘 Need Help?

**Component doesn't work?**
- See troubleshooting in **[DEPLOYMENT_GUIDE_OPTION_C.md](DEPLOYMENT_GUIDE_OPTION_C.md)**

**Mac-specific issues?**
- See **[../clients/MAC_QUICK_START.md](../clients/MAC_QUICK_START.md)**

**Want detailed architecture?**
- See **[OPTION_C_IMPLEMENTATION_COMPLETE.md](OPTION_C_IMPLEMENTATION_COMPLETE.md)**

---

**Ready to deploy? Start with [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)!**
