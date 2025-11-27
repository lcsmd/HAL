# HAL Documentation Guide

**All HAL documentation is organized in the DOCS/ directory**

---

## 📂 Documentation Structure

```
DOCS/
├── SYSTEM/           - Core system documentation
├── ARCHITECTURE/     - Architectural decisions
├── FEATURES/         - Feature-specific docs
│   ├── MEDICAL/
│   ├── FINANCIAL/
│   ├── PASSWORD/
│   ├── VOICE/
│   └── SCHEMA/
├── DEPLOYMENT/       - Deployment guides
├── SETUP/            - Setup and quick starts
├── STATUS/           - Status reports
├── DEVELOPMENT/      - Development docs
└── REFERENCE/        - Reference materials
```

---

## 🎯 Start Here

### For Complete System Understanding

**Read**: [DOCS/SYSTEM/HAL_SYSTEM_MASTER.md](DOCS/SYSTEM/HAL_SYSTEM_MASTER.md)

This master document contains:
- Complete architecture overview
- All code locations and database structure
- Network infrastructure
- Development history
- Everything an AI agent or developer needs to know

### For Maintaining Documentation

**Read**: [DOCS/SYSTEM/DOCUMENTATION_MAINTENANCE.md](DOCS/SYSTEM/DOCUMENTATION_MAINTENANCE.md)

Critical instructions for:
- Keeping docs updated
- GitHub workflow
- What to update when
- AI agent responsibilities

---

## 📖 Quick Access

### System Documentation
- [System Master](DOCS/SYSTEM/HAL_SYSTEM_MASTER.md) - Complete system guide
- [Documentation Index](DOCS/SYSTEM/INDEX.md) - All documentation listed
- [Configuration](DOCS/SYSTEM/CONFIGURATION.md) - Environment setup

### Feature Documentation
- [Medical/Epic API](DOCS/FEATURES/MEDICAL/) - Healthcare integration
- [Financial/Transactions](DOCS/FEATURES/FINANCIAL/) - Transaction management
- [Password Manager](DOCS/FEATURES/PASSWORD/) - Password vault
- [Voice Interface](DOCS/FEATURES/VOICE/) - Voice interaction
- [Schema System](DOCS/FEATURES/SCHEMA/) - Database schema

### Quick Starts
- [Epic API Setup](DOCS/SETUP/START_HERE.md) - Epic integration
- [Environment Setup](DOCS/SETUP/QUICK_START_ENV.md) - Initial configuration
- [Transaction System](DOCS/FEATURES/FINANCIAL/QUICKSTART_TRANSACTIONS.md) - Financial setup

### Deployment
- [Mac Client](DOCS/DEPLOYMENT/MAC_DEPLOYMENT_READY.md) - Mac deployment package
- [Deployment Guide](DOCS/DEPLOYMENT/DEPLOY_INSTRUCTIONS.md) - General deployment

---

## 🔍 Finding Documentation

### By Topic

**Medical**: `DOCS/FEATURES/MEDICAL/`  
**Financial**: `DOCS/FEATURES/FINANCIAL/`  
**Voice**: `DOCS/FEATURES/VOICE/`  
**Deployment**: `DOCS/DEPLOYMENT/`  
**Architecture**: `DOCS/ARCHITECTURE/`

### By Purpose

**Getting Started**: `DOCS/SETUP/`  
**Understanding System**: `DOCS/SYSTEM/HAL_SYSTEM_MASTER.md`  
**Developing Features**: `DOCS/DEVELOPMENT/`  
**Status Reports**: `DOCS/STATUS/`

---

## 📝 Adding New Documentation

1. Determine category (SYSTEM, FEATURES, etc.)
2. Place in appropriate subdirectory
3. Update [DOCS/SYSTEM/INDEX.md](DOCS/SYSTEM/INDEX.md)
4. Update this file (DOCS.md) if major addition
5. Commit with message: `docs: add [description]`

---

## 🔗 External Resources

- **GitHub**: https://github.com/lcsmd/hal
- **Mac Deployment Package**: `C:\qmsys\hal\mac_deployment_package\`
- **OpenQM Help**: `C:\qmsys\hal\QM_HELP\`

---

**Location**: `C:\qmsys\hal\DOCS.md` (root directory)  
**Purpose**: Navigation guide for DOCS/ directory  
**Last Updated**: 2025-11-27
