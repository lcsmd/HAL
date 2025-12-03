# HAL Personal AI Assistant - System Master Documentation

**Version**: 2.0  
**Last Updated**: 2025-11-27  
**Purpose**: Complete system understanding for AI agents and developers

---

## 🎯 Purpose of This Document

This is the **single source of truth** for understanding the HAL Personal AI Assistant system. Read this document to understand:
- Architectural decisions and rationale
- All code locations and database structures
- Network topology and server roles
- Development history and design patterns
- Integration points and data flows

**Target Audience**: AI agents, developers, maintainers, auditors

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architectural Decisions](#architectural-decisions)
3. [Network Infrastructure](#network-infrastructure)
4. [Code Organization](#code-organization)
5. [Database Structure](#database-structure)
6. [Documentation Index](#documentation-index)
7. [Development History](#development-history)
8. [Integration Points](#integration-points)

---

## 🏗️ System Overview

### What is HAL?

HAL is a **personal AI assistant** combining:
- **OpenQM MultiValue Database** - Core data storage
- **GPU-Accelerated AI Services** - LLM and voice processing
- **Voice Interface** - Real-time speech interaction
- **Multi-Modal Data Management** - Medical, financial, personal data

### Core Philosophy

1. **Data Sovereignty** - All personal data stored locally (no cloud)
2. **Multi-Value Database** - OpenQM for flexible schema-less storage
3. **AI-Enhanced** - GPU acceleration for real-time responses
4. **Voice-First** - Natural conversation interface
5. **Modular Architecture** - Clear separation of concerns

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Python (Mac/Windows clients) | User interface |
| **Communication** | WebSocket (native QM) | Real-time bidirectional |
| **Business Logic** | OpenQM Basic | Database operations, routing |
| **Database** | OpenQM MultiValue | Data persistence |
| **AI/ML** | Ollama (LLM), Faster-Whisper (STT) | GPU-accelerated inference |
| **Infrastructure** | Windows Server, Linux GPU server | Compute resources |

---

## 🧠 Architectural Decisions

### Decision 1: OpenQM as Primary Database

**Made**: Project inception (2024)  
**Rationale**:
- MultiValue architecture allows flexible schema evolution
- Native support for multi-valued attributes (medications, allergies as lists)
- No ORM overhead - direct database operations
- 40+ years of proven stability
- Built-in BASIC language for business logic
- Cross-platform (Windows primary, Linux possible)

**Alternatives Considered**:
- PostgreSQL (rejected: rigid schema, ORM complexity)
- MongoDB (rejected: less mature, document model not ideal)
- SQLite (rejected: limited concurrency, no server)

**Impact**: All data operations use QM Basic, schemas defined in SCHEMA/ directory

---

### Decision 2: Phantom Process for WebSocket Listener

**Made**: November 2025  
**Rationale**:
- Native QM sockets eliminate Python gateway layer
- Direct database access (no IPC overhead)
- Simplified deployment (one process instead of two)
- Automatic restart capability
- Lower latency (<50ms saved)

**Previous Architecture**: 
```
Mac → Python Voice Gateway → QM Listener → Database
```

**Current Architecture**:
```
Mac → QM WebSocket Phantom → Database
```

**Impact**: 
- BP/WEBSOCKET.LISTENER runs as phantom process
- Python PY/voice_gateway.py is deprecated (kept for reference)
- Port 8768 handled directly by QM
- Simplified deployment and maintenance

**Files Affected**:
- `BP/WEBSOCKET.LISTENER` - Main phantom process
- `HAL.SPLITTER.LOG` - Phantom process logs
- Deployment scripts updated

---

### Decision 3: GPU Server for AI Workloads

**Made**: Mid-2025  
**Rationale**:
- Voice transcription requires <200ms latency for natural feel
- LLM inference 20-50x faster on GPU
- Centralized AI compute reduces client requirements
- Multiple clients can share GPU resources
- Cost-effective (one GPU server vs. multiple client GPUs)

**Server**: ubuai (10.1.10.20) - Ubuntu Linux with NVIDIA GPU

**Services**:
- Faster-Whisper (port 9000) - STT
- Ollama (port 11434) - LLM inference

**Impact**: Real-time voice interaction possible, sub-2-second end-to-end responses

---

### Decision 4: Schema-Driven File Management

**Made**: October 2025  
**Rationale**:
- Consistent field definitions across files
- Self-documenting data structures
- Automated dictionary generation
- Migration support
- Domain-driven design

**Implementation**: 
- CSV schemas in `SCHEMA/` directory
- Programs in `BP/SCHEMA.*` for management
- Include files in `EQU/*.h` for field references

**Impact**: 84 include files, 40+ entity types, consistent data access

---

### Decision 5: Hybrid Python + QM Basic Architecture

**Made**: Project inception  
**Rationale**:
- Python for external integrations (Epic API, Gmail, AI services)
- QM Basic for database operations and business logic
- Best tool for each job
- Python has rich ecosystem for APIs
- QM Basic excels at data manipulation

**Integration Method**: 
- Python scripts call QM via command-line: `qm.exe -aHAL "COMMAND"`
- QM calls Python via EXECUTE: `EXECUTE "python script.py"`
- Shared data through files or HTTP APIs

**Impact**: 
- 75+ QM Basic programs in BP/
- 50+ Python scripts in PY/
- Clear separation of concerns

---

### Decision 6: Voice-First Interface Design

**Made**: September 2025  
**Rationale**:
- Hands-free operation critical for accessibility
- Natural conversation more intuitive than GUI
- Voice context improves with conversation history
- Medical queries benefit from verbal interaction

**Implementation**:
- Wake word detection (client-side)
- Streaming audio to GPU server
- Intent detection in QM
- Context-aware responses
- Follow-up window (10 seconds)

**Impact**: 
- Voice interface 88% operational
- Multiple client types supported
- Low latency requirements drove GPU decision

---

### Decision 7: Multi-Domain Data Model

**Made**: Project inception, refined October 2025  
**Rationale**:
- Personal assistant needs diverse data types
- Medical, financial, personal domains are distinct
- Domain-driven design improves maintainability
- Each domain has specialized handlers

**Domains Implemented**:
1. **Medical** - Medications, allergies, immunizations, appointments, doctors, facilities
2. **Financial** - Transactions, payees, categories, reimbursements
3. **Personal** - Contacts, places, photos, documents, conversations
4. **Knowledge** - Tasks, notes, memories, skills
5. **System** - Schema, logs, configuration, models

**Impact**: 
- 40+ OpenQM files
- Domain-specific BP programs (MEDICATION.*, TRANSACTION.*, etc.)
- Specialized intent handlers

---

### Decision 8: Epic FHIR API Integration

**Made**: October 2025  
**Rationale**:
- Standardized healthcare data exchange
- USCDI v3 compliance
- Direct patient access (no provider intermediary)
- OAuth 2.0 security
- Real-time sync capability

**Implementation**:
- Python OAuth flow (PY/epic_api_setup.py)
- FHIR bundle parsing (PY/epic_parser.py)
- Scheduled sync (PY/epic_scheduler.py)
- Maps to QM medical files

**Impact**: 
- Complete medical history import
- Automated daily sync
- 9 medical entity types
- HIPAA-compliant storage

---

## 🌐 Network Infrastructure

### Server Topology

```
┌──────────────────────────────────────────────────────────────┐
│                      HAL Network                             │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│ QM Server           │  10.1.34.103 (Windows)
│ Role: Database      │  - OpenQM Database
│ User: lawr          │  - WebSocket Listener (port 8768)
│                     │  - Business Logic
└─────────────────────┘

┌─────────────────────┐
│ AI Server (ubuai)   │  10.1.10.20 (Ubuntu Linux)
│ Role: GPU Compute   │  - Faster-Whisper STT (port 9000)
│ User: lawr          │  - Ollama LLM (port 11434)
│ GPU: NVIDIA/AMD     │  - GPU-accelerated inference
└─────────────────────┘

┌─────────────────────┐
│ HAProxy             │  10.1.50.100 (Linux)
│ Role: Load Balancer │  - SSH (port 2222)
│ User: lawr          │  - Optional SSL termination
└─────────────────────┘

┌─────────────────────┐
│ Proxmox             │  10.1.33.1 (Proxmox VE)
│ Role: Hypervisor    │  - VM host
│ User: root          │  - Infrastructure management
└─────────────────────┘

┌─────────────────────┐
│ Mac Clients         │  Various IPs
│ Role: UI            │  - Voice/text interface
│                     │  - User interaction
└─────────────────────┘
```

### Network Details

**Subnet**: 10.1.0.0/16 (private network)

**Firewall Rules Required**:
- QM Server: Allow inbound TCP 8768 (WebSocket)
- AI Server: Allow inbound TCP 9000 (Whisper), 11434 (Ollama)
- HAProxy: Allow inbound TCP 2222 (SSH)

**Credentials**: See `C:\qmsys\hal\mac_deployment_package\CREDENTIALS.txt`

### Port Allocation

| Service | Server | Port | Protocol | Purpose |
|---------|--------|------|----------|---------|
| WebSocket Listener | 10.1.34.103 | 8768 | WS | Client connections |
| Faster-Whisper | 10.1.10.20 | 9000 | HTTP | Speech-to-Text |
| Ollama | 10.1.10.20 | 11434 | HTTP | LLM inference |
| HAProxy SSH | 10.1.50.100 | 2222 | SSH | Admin access |
| Proxmox Web | 10.1.33.1 | 8006 | HTTPS | VM management |

---

## 📂 Code Organization

### Directory Structure

```
C:\qmsys\hal\
├── BP/                          - QM Basic programs (75+ files)
│   ├── WEBSOCKET.LISTENER       - Phantom process (port 8768)
│   ├── VOICE.*.b                - Voice interface handlers
│   ├── MEDICATION.*.b           - Medical data programs
│   ├── TRANSACTION.*.b          - Financial programs
│   ├── SCHEMA.*.b               - Schema management
│   ├── PASSWORD.*.b             - Password vault
│   └── IMPORT.*.b               - Data import utilities
│
├── BP.OUT/                      - Compiled QM programs
│
├── EQU/                         - Include files (84 files)
│   ├── *.h                      - Field definitions
│   ├── *.equ                    - Legacy equates
│   └── COMMON.h                 - Shared constants
│
├── PY/                          - Python scripts (50+ files)
│   ├── epic_api_*.py            - Epic FHIR integration
│   ├── voice_gateway.py         - Deprecated (use phantom)
│   ├── hal_agent.py             - AI agent
│   ├── password_*.py            - Password management
│   └── ai_*.py                  - AI integration
│
├── SCHEMA/                      - CSV schema definitions
│   ├── domains.csv              - Domain registry
│   ├── files.csv                - File definitions
│   ├── fields.csv               - Field catalog
│   └── *.csv                    - Entity schemas
│
├── mac_deployment_package/      - Mac client deployment
│   ├── hal_text_client.py       - Text interface client
│   ├── hal_voice_client.py      - Voice interface client
│   ├── NETWORK_INFO.md          - Network documentation
│   ├── AI_SERVICES.md           - AI services guide
│   └── *.sh                     - Setup scripts
│
├── clients/                     - Client applications
│   └── Various client implementations
│
├── config/                      - Configuration files
│   └── epic_api_config.json     - Epic API settings
│
├── UPLOADS/                     - Data import staging
├── logs/                        - Application logs
└── tests/                       - Test scripts
```

### QM Basic Programs (BP/ Directory)

**Count**: 75+ programs

**Categories**:

1. **Core System** (10 programs)
   - `WEBSOCKET.LISTENER` - Main phantom process
   - `OPEN.FILES` - File handle management
   - `BUILD.SCHEMA` - Schema generation
   - `DATA.FILTER` - Query filtering

2. **Medical Domain** (15 programs)
   - `MEDICATION.MENU` - Medication management
   - `MEDICAL.MENU` - Medical data hub
   - `IMPORT.EPIC` - Epic FHIR import
   - `VOICE.HANDLE.MEDICATION` - Voice handler

3. **Financial Domain** (12 programs)
   - `IMPORT.QUICKEN` - QuickBooks import
   - `STANDARDIZE.PAYEES` - Payee normalization
   - `TAG.REIMBURSABLE` - Expense categorization
   - `REPORT.REIMBURSABLE` - Reporting

4. **Schema Management** (8 programs)
   - `SCHEMA.MANAGER` - Main menu
   - `SCHEMA.ADD.DOMAIN` - Domain creation
   - `SCHEMA.ADD.FILE` - File creation
   - `SCHEMA.VALIDATE` - Schema validation

5. **Password Management** (7 programs)
   - `PASSWORD.MENU` - Main menu
   - `PASSWORD.ADD` - Add credential
   - `PASSWORD.VIEW` - View credential
   - `PASSWORD.MASTER.SETUP` - Master password

6. **Data Import** (8 programs)
   - Various import utilities

7. **Voice Interface** (10 programs)
   - Multiple VOICE.LISTENER versions (legacy)
   - Intent handlers

**Compilation**: 
```qm
LOGTO HAL
BASIC BP program.name
CATALOG BP program.name
```

### Python Scripts (PY/ Directory)

**Count**: 50+ scripts

**Categories**:

1. **Epic API Integration** (5 scripts)
   - `epic_api_setup.py` - OAuth flow
   - `epic_api_sync.py` - Data synchronization
   - `epic_parser.py` - FHIR parsing
   - `epic_scheduler.py` - Scheduled sync
   - `test_epic_setup.py` - Testing

2. **AI Integration** (6 scripts)
   - `ai_classifier.py` - Transaction classification
   - `ai_rule_learner.py` - Rule learning
   - `hal_agent.py` - AI agent
   - `voice_gateway.py` - Deprecated gateway
   - `qm_executor.py` - QM execution wrapper

3. **Password Management** (4 scripts)
   - `password_manager.py` - Manager CLI
   - `password_crypto.py` - Encryption
   - `import_passwords.py` - Import utility

4. **Schema Management** (15+ scripts)
   - `create_all_schema.py` - Schema generation
   - `run_setup_*.py` - Setup automation
   - Various builders

5. **Gmail Integration** (1 script)
   - `gmail_import.py` - Email import

6. **Photo Analysis** (1 script)
   - `photo_analyzer.py` - Image AI

**Execution**: 
```bash
cd C:\qmsys\hal
python PY\script_name.py
```

### Include Files (EQU/ Directory)

**Count**: 84 files

**Purpose**: Field definitions for QM Basic programs

**Naming Convention**:
- `ENTITY.h` - Full field definitions (uppercase)
- `entity.equ` - Legacy equates (lowercase)

**Usage**:
```qm
PROGRAM EXAMPLE
   $INCLUDE EQU MEDICATION.h
   
   * Now can use: MED.NAME, MED.DOSAGE, etc.
   READ MED.REC FROM MEDICATION.FILE, MED.ID ELSE STOP
   PRINT MED.REC<MED.NAME>
END
```

**Generation**: Created by `BUILD.SCHEMA` from SCHEMA/ CSV files

---

## 🗄️ Database Structure

### OpenQM Account

**Account Name**: `HAL`  
**Location**: `C:\qmsys\hal\`  
**Access**: `LOGTO HAL` from QM prompt

### File Organization

**Total Files**: 40+ data files

**File Types**:
1. **Data Files** - Primary storage (e.g., MEDICATION)
2. **Dictionary Files** - Field definitions (e.g., MEDICATION.DIC)
3. **Index Files** - Performance indexes (auto-generated)

### Domain: Medical (9 files)

| File | Description | Key Field | Record Count |
|------|-------------|-----------|--------------|
| MEDICATION | Prescriptions | MED.ID | Variable |
| ALLERGY | Allergic reactions | ALG.ID | Variable |
| IMMUNIZATION | Vaccinations | IMM.ID | Variable |
| MEDICAL_HISTORY | Diagnoses | MHX.ID | Variable |
| MEDICAL_TEST | Lab results | TST.ID | Variable |
| VITAL_SIGNS | BP, weight, etc. | VIT.ID | Variable |
| APPOINTMENT | Doctor visits | APT.ID | Variable |
| DOCTOR | Healthcare providers | DOC.ID | Variable |
| HEALTHCARE_FACILITY | Hospitals, clinics | HCF.ID | Variable |

**Schema Location**: 
- CSV: `SCHEMA/medical_*.csv`
- Include: `EQU/MEDICATION.h`, `EQU/ALLERGY.h`, etc.

### Domain: Financial (5 files)

| File | Description | Key Field | Record Count |
|------|-------------|-----------|--------------|
| TRANSACTION | Bank transactions | TRN.ID | Variable |
| PAYEE | Vendors, merchants | PYE.ID | Variable |
| CATEGORY | Expense categories | CAT.ID | Variable |
| REIMBURSEMENT | Reimbursable expenses | RMB.ID | Variable |
| TAG | Transaction tags | TAG.ID | Variable |

**Schema Location**: 
- CSV: `SCHEMA/financial_*.csv`
- Include: `EQU/TRANSACTION.h`, `EQU/PAYEE.h`, etc.

### Domain: Personal (8 files)

| File | Description | Key Field |
|------|-------------|-----------|
| PERSON | People, contacts | PER.ID |
| PLACE | Locations | PLA.ID |
| PHOTO | Images | PHO.ID |
| PHOTO_GROUP | Image collections | PHG.ID |
| DOCUMENT | Documents | DOC.ID |
| EMAIL | Email messages | EML.ID |
| CONVERSATION | Chat history | CON.ID |
| SESSION | User sessions | SES.ID |

### Domain: Knowledge (7 files)

| File | Description | Key Field |
|------|-------------|-----------|
| MEMORY | AI memory | MEM.ID |
| TASK | To-do items | TSK.ID |
| EVENT | Calendar events | EVT.ID |
| SKILL | Learned capabilities | SKL.ID |
| RULE | Business rules | RUL.ID |
| PROMPT | AI prompts | PRM.ID |
| MODEL | AI model configs | MOD.ID |

### Domain: System (11 files)

| File | Description | Key Field |
|------|-------------|-----------|
| SCHEMA | Schema definitions | SCH.ID |
| DOMAINS | Domain registry | DOM.ID |
| FIELDS | Field catalog | FLD.ID |
| FILES | File metadata | FIL.ID |
| DOM_FILE_FIELD | Relationships | - |
| PASSWORD_VAULT | Encrypted passwords | PWD.ID |
| MASTER_PASSWORD | Master pwd hash | MASTER |
| LOG | System logs | LOG.ID |
| IMPORT_LOG | Import history | IMP.ID |
| INTEGRATION | External systems | INT.ID |
| COMMAND.QUEUE | Command queue | CMD.ID |

### Schema System

**Purpose**: Self-documenting, consistent data structures

**Components**:
1. **domains.csv** - Domain definitions
2. **files.csv** - File definitions per domain
3. **fields.csv** - Field catalog
4. **Entity CSVs** - Specific entity schemas

**Location**: `C:\qmsys\hal\SCHEMA/`

**Management Programs**:
- `SCHEMA.MANAGER` - Main menu
- `SCHEMA.ADD.DOMAIN` - Add domain
- `SCHEMA.ADD.FILE` - Add file
- `SCHEMA.ADD.FIELD` - Add field
- `SCHEMA.VALIDATE` - Validation
- `BUILD.SCHEMA` - Generate includes

**Workflow**:
1. Edit CSV in SCHEMA/
2. Run `BUILD.SCHEMA` to generate .h files
3. Run `BUILD.DICT` to update dictionaries
4. Compile programs that use new fields

### Database Access Patterns

**Direct Access** (from QM Basic):
```qm
OPEN 'MEDICATION' TO MEDICATION.FILE ELSE STOP
READ MED.REC FROM MEDICATION.FILE, MED.ID ELSE STOP
PRINT MED.REC<MED.NAME>
```

**Via Python** (command-line):
```bash
qm.exe -aHAL "LIST MEDICATION WITH NAME = 'Metformin'"
```

**Via WebSocket** (from Mac client):
```python
# Client sends JSON
{"type": "query", "intent": "MEDICATION", "text": "List my medications"}

# QM phantom processes and returns JSON
{"type": "response", "intent": "MEDICATION", "data": [...]}
```

---

## 📚 Documentation Index

### Core Documentation (in C:\qmsys\hal\)

| File | Purpose | Primary Audience |
|------|---------|------------------|
| **HAL_SYSTEM_MASTER.md** | This file - Complete system overview | AI agents, developers |
| **README.md** | Project introduction | Users, newcomers |
| **INDEX.md** | Documentation index | All users |
| **START_HERE.md** | Quick start for Epic API | Users |
| **CONFIGURATION.md** | Environment variable setup | Administrators |

### Architectural Documentation

| File | Purpose |
|------|---------|
| **AI_INTEGRATION_SUMMARY.md** | LLM integration architecture |
| **MODEL_SYSTEM_README.md** | Model selection system |
| **VOICE_SYSTEM_FINAL_STATUS.md** | Voice interface status |
| **README_SCHEMA_SYSTEM.md** | Schema system design |

### Feature Documentation

| File | Purpose |
|------|---------|
| **README_EPIC_API.md** | Epic FHIR API integration |
| **README_TRANSACTION_SYSTEM.md** | Financial transaction system |
| **README_PASSWORD_MANAGER.md** | Password vault |
| **README_AI_CLASSIFICATION.md** | AI-powered classification |
| **README_AI_RULE_LEARNING.md** | Rule learning system |

### Deployment Documentation

| File | Purpose |
|------|---------|
| **mac_deployment_package/README.md** | Mac client deployment |
| **mac_deployment_package/NETWORK_INFO.md** | Network topology |
| **mac_deployment_package/AI_SERVICES.md** | GPU AI services |
| **mac_deployment_package/PHANTOM_PROCESS_INFO.md** | QM phantom process |
| **mac_deployment_package/QUICKSTART.md** | 5-minute setup |

### Development Documentation

| File | Purpose |
|------|---------|
| **NAMING_CONVENTIONS.md** | Code style guide |
| **ORGANIZATION_FINAL.md** | Project organization |
| **MIGRATION.REPORT.txt** | Migration history |

### Status Documents

| File | Purpose |
|------|---------|
| **FINAL_SUMMARY.md** | Project summary |
| **DEPLOYMENT_COMPLETE.md** | Deployment status |
| **CLEANUP_SUMMARY.md** | Cleanup history |

### User Guides (NOTES/)

| File | Purpose |
|------|---------|
| **NOTES/epic_api_quickstart.md** | Epic API 15-min guide |
| **NOTES/medical_schema.md** | Medical data structure |
| **NOTES/password_manager_guide.md** | Password usage guide |

---

## 📜 Development History

### Timeline

**Phase 1: Foundation (2024 Q1-Q2)**
- Selected OpenQM as database
- Established QM Basic + Python hybrid architecture
- Created initial medical data structures
- Implemented password vault

**Phase 2: Medical Integration (2024 Q3)**
- Epic FHIR API integration
- USCDI v3 compliance
- Automated daily sync
- 9 medical entity types

**Phase 3: Financial System (2024 Q4)**
- Transaction import (QuickBooks)
- AI-powered classification
- Payee standardization
- Reimbursement tracking

**Phase 4: Schema System (2025 October)**
- CSV-based schema definitions
- Automated include file generation
- Schema validation
- 84 include files created
- Domain-driven organization

**Phase 5: Voice Interface (2025 September-November)**
- Initial Python gateway approach
- Switched to QM phantom process
- GPU server integration (Faster-Whisper, Ollama)
- Mac client development
- 88% operational status

**Phase 6: Current (2025 November)**
- Mac deployment package creation
- Comprehensive documentation
- System consolidation
- Performance optimization

### Key Milestones

1. **First working query** - QM Basic program querying OpenQM
2. **Epic API authorization** - OAuth flow working
3. **First voice query** - End-to-end voice interaction
4. **Schema system deployment** - Self-documenting structure
5. **Mac client deployment** - Remote access working
6. **Phantom process migration** - Eliminated Python gateway

### Lessons Learned

1. **MultiValue Advantage**: Flexible schema evolution invaluable for personal data
2. **Python-QM Hybrid**: Best of both worlds (ecosystem vs. database access)
3. **GPU Necessity**: Real-time voice requires GPU acceleration
4. **Schema First**: CSV schemas prevent drift, improve maintainability
5. **Phantom Process**: Eliminating middleware reduces complexity and latency
6. **Documentation Critical**: Comprehensive docs enable AI agent assistance

---

## 🔌 Integration Points

### External Systems

**1. Epic MyChart (FHIR API)**
- **Purpose**: Medical record synchronization
- **Protocol**: HTTPS REST + OAuth 2.0
- **Endpoint**: `https://apporchard.epic.com/`
- **Data Flow**: Epic → Python → QM database
- **Frequency**: Daily automated sync
- **Code**: `PY/epic_api_*.py`, `BP/IMPORT.EPIC`

**2. QuickBooks (CSV Export)**
- **Purpose**: Transaction import
- **Protocol**: File-based (CSV)
- **Data Flow**: QuickBooks → CSV → Python parser → QM
- **Frequency**: Manual import
- **Code**: `PY/ai_classifier.py`, `BP/IMPORT.QUICKEN`

**3. Gmail (API)**
- **Purpose**: Email archive
- **Protocol**: HTTPS REST + OAuth 2.0
- **Data Flow**: Gmail → Python → QM EMAIL file
- **Frequency**: Manual/scheduled
- **Code**: `PY/gmail_import.py`

**4. Ollama (LLM API)**
- **Purpose**: AI language model inference
- **Protocol**: HTTP REST
- **Endpoint**: `http://10.1.10.20:11434/api/generate`
- **Data Flow**: QM → Ollama → QM (response)
- **Frequency**: On-demand per query
- **Code**: QM Basic EXECUTE commands calling curl

**5. Faster-Whisper (STT API)**
- **Purpose**: Speech-to-text transcription
- **Protocol**: HTTP REST
- **Endpoint**: `http://10.1.10.20:9000/transcribe`
- **Data Flow**: Mac client → QM phantom → Whisper → QM
- **Frequency**: Real-time during voice interaction
- **Code**: QM phantom WEBSOCKET.LISTENER

### Internal Integration Points

**1. QM ↔ Python**
- **Method A**: Command-line execution
  ```bash
  qm.exe -aHAL "LIST MEDICATION"
  ```
- **Method B**: Python calls QM
  ```python
  os.system('qm.exe -aHAL "COMMAND"')
  ```
- **Method C**: QM calls Python
  ```qm
  EXECUTE "python PY\script.py" CAPTURING OUTPUT
  ```

**2. Mac Client ↔ QM Server**
- **Protocol**: WebSocket (ws://)
- **Port**: 8768
- **Format**: JSON messages
- **Example**:
  ```json
  Request:  {"type": "text_input", "text": "List medications"}
  Response: {"type": "response", "intent": "MEDICATION", "data": [...]}
  ```

**3. QM ↔ GPU Server**
- **Whisper**: HTTP POST with base64 audio
- **Ollama**: HTTP POST with JSON prompt
- **No persistent connection**: Request/response pattern

---

## 🔐 Security & Access Control

### Authentication Layers

**1. Network Level**
- Private network (10.1.0.0/16)
- Firewall rules (ports 8768, 9000, 11434, 2222)
- SSH key authentication (optional)

**2. Application Level**
- Master password for password vault
- OpenQM account permissions
- No authentication on WebSocket (trusted network assumption)

**3. Data Encryption**
- Password vault: AES-256 encryption
- Epic tokens: Stored encrypted in config/epic_tokens.json
- Network: No TLS (local network only)

### Credentials

**Location**: `mac_deployment_package/CREDENTIALS.txt`  
**Warning**: Plaintext passwords - keep secure

**Servers**:
- QM Server (10.1.34.103): lawr / apgar-66
- AI Server (10.1.10.20): lawr / apgar-66
- HAProxy (10.1.50.100): lawr / apgar-66 (SSH port 2222)
- Proxmox (10.1.33.1): root / apgar-66

### Recommendations

1. Change default passwords if internet-accessible
2. Enable SSH key authentication (run `setup_ssh_keys.sh`)
3. Consider VPN for remote access
4. Implement TLS/SSL for WebSocket (wss://)
5. Add authentication to WebSocket listener
6. Regular security audits

---

## 📝 Documentation Maintenance (CRITICAL)

### ⚠️ For AI Agents: READ THIS FIRST

**This documentation MUST be kept updated as the system evolves.**

### Maintenance Document

**File**: `DOCUMENTATION_MAINTENANCE.md`  
**Purpose**: Complete instructions for maintaining this master file and all related documentation

**YOU MUST READ**: [DOCUMENTATION_MAINTENANCE.md](DOCUMENTATION_MAINTENANCE.md)

This file contains:
- ✅ Instructions for updating this master file
- ✅ GitHub repository workflow
- ✅ What to update when making changes
- ✅ Commit message standards
- ✅ Documentation review checklist
- ✅ Emergency procedures

### GitHub Repository

**Repository**: `https://github.com/lcsmd/hal`  
**Owner**: `lcsmd`  
**Branch**: `main`

**CRITICAL WORKFLOW**:
```bash
# Before major changes
git pull origin main
git checkout -b backup-before-[change]-$(date +%Y%m%d)
git push origin backup-before-[change]-$(date +%Y%m%d)
git checkout main

# Make changes, update docs, commit
git add HAL_SYSTEM_MASTER.md [other docs]
git commit -m "docs: update for [change]"
git add [code files]
git commit -m "feat: [change]"
git push origin main

# THEN proceed with major infrastructure changes
```

### Update Rules for AI Agents

**ALWAYS**:
1. ✅ Read this file before making changes
2. ✅ Update this file immediately after architectural changes
3. ✅ Commit documentation before code
4. ✅ Push to GitHub before major changes
5. ✅ Update "Last Updated" date (below)
6. ✅ Add entry to Development History
7. ✅ Update file counts if changed
8. ✅ Check for contradictions with other docs

**NEVER**:
1. ❌ Skip documentation updates
2. ❌ Make major changes without GitHub backup
3. ❌ Leave this file outdated
4. ❌ Create contradictions
5. ❌ Delete content without moving it

### When to Update This File

**Update immediately when**:
- Adding/removing code files
- Changing architecture
- Modifying database structure
- Changing network infrastructure
- Adding integrations
- Making deployment changes
- Learning important lessons

**See**: `DOCUMENTATION_MAINTENANCE.md` for complete instructions

---

## 🚀 Getting Started (For AI Agents)

### To Understand the System

**Read in this order**:
1. **This file** (HAL_SYSTEM_MASTER.md) - Architecture overview
2. **NETWORK_INFO.md** - Infrastructure details
3. **AI_SERVICES.md** - GPU AI services
4. **README_SCHEMA_SYSTEM.md** - Data structure
5. **PHANTOM_PROCESS_INFO.md** - QM process model

### To Make Code Changes

**Understand**:
1. What domain? (Medical, Financial, Personal, etc.)
2. QM Basic or Python? (Database vs. Integration)
3. Schema changes needed? (Check SCHEMA/)
4. Include files affected? (Recompile after)

**Workflow**:
1. Edit appropriate file (BP/*.b or PY/*.py)
2. If schema change: Update SCHEMA/*.csv, run BUILD.SCHEMA
3. If QM Basic: BASIC BP program, CATALOG BP program
4. If Python: Test with `python PY\script.py`
5. Update documentation (this file if architectural)

### To Deploy Changes

**QM Server**:
```qm
LOGTO HAL
BASIC BP PROGRAM.NAME
CATALOG BP PROGRAM.NAME
```

**Python**:
```bash
# Test locally
python PY\script.py

# Deploy to production
# Copy to C:\qmsys\hal\PY\
```

**Mac Client**:
```bash
# Update mac_deployment_package/
# Users re-download and run setup_mac.sh
```

---

## 📊 System Metrics

### Current State (2025-11-27)

**Code**:
- QM Basic Programs: 75+
- Python Scripts: 50+
- Include Files: 84
- Lines of Code: ~50,000 (estimated)

**Data**:
- OpenQM Files: 40+
- Schema Definitions: 40+ entities
- Documentation Files: 97 markdown files

**Infrastructure**:
- Servers: 4 (QM, AI, HAProxy, Proxmox)
- Network Ports: 6 services
- Storage: ~10 GB (database + code)

**Performance**:
- Voice Query Latency: 1.2-2.4 seconds
- Text Query Latency: 1.1-2.1 seconds
- GPU Speedup: 20-50x over CPU
- WebSocket Phantom: <50ms overhead

**Completeness**:
- Voice Interface: 88% operational
- Medical Integration: 100% (Epic API working)
- Financial System: 100% (Import/classification working)
- Password Manager: 100% (Vault operational)
- Mac Client: 100% (Deployment package ready)

---

## 🎯 Future Roadmap

### Near Term (Next 3 Months)

1. **Voice Interface to 100%**
   - Fix phantom process QM READ.SOCKET timing
   - Add voice feedback (TTS)
   - Improve wake word accuracy

2. **Mobile Clients**
   - iOS voice client
   - Android voice client

3. **Additional Integrations**
   - Home Assistant
   - Calendar sync (Google/Apple)
   - More financial sources

### Medium Term (3-6 Months)

1. **AI Enhancements**
   - Context-aware responses
   - Long-term memory
   - Proactive suggestions

2. **Data Analysis**
   - Health trend analysis
   - Financial insights
   - Automated reporting

3. **Multi-User Support**
   - User accounts
   - Permission system
   - Shared data

### Long Term (6-12 Months)

1. **Cloud Backup**
   - Encrypted cloud sync
   - Disaster recovery

2. **Advanced AI**
   - Custom model fine-tuning
   - Multi-modal (vision + voice)
   - Predictive capabilities

3. **Platform Expansion**
   - Web interface
   - API for third-party apps
   - Plugin system

---

## 📞 Contact & Support

### For AI Agents

**When you need to**:
- Understand architecture: Re-read this file
- Make code changes: Check [Code Organization](#code-organization)
- Add features: Review [Architectural Decisions](#architectural-decisions)
- Debug issues: Check logs in `C:\qmsys\hal\logs\`
- Deploy: Follow [Getting Started](#getting-started-for-ai-agents)

### Documentation Updates

**When to update this file**:
- Major architectural changes
- New integration added
- Infrastructure changes
- New code modules added
- Database schema evolution

**How to update**:
1. Edit `C:\qmsys\hal\HAL_SYSTEM_MASTER.md`
2. Update "Last Updated" date
3. Add entry to [Development History](#development-history)
4. Commit with message: "docs: update system master documentation"

---

## ✅ Summary

### What You Now Know

After reading this document, you understand:

✅ **Architecture**: QM database + Python integrations + GPU AI  
✅ **Network**: 4 servers, private network, specific roles  
✅ **Code**: 75+ QM programs, 50+ Python scripts, organized by domain  
✅ **Database**: 40+ files, schema-driven, multi-domain model  
✅ **Voice**: Phantom process, GPU STT/LLM, Mac client  
✅ **Medical**: Epic FHIR integration, USCDI v3 compliant  
✅ **Financial**: Transaction import, AI classification  
✅ **Deployment**: Mac package ready, comprehensive docs  

### Key Takeaways

1. **OpenQM is central** - All data operations go through QM
2. **Python for integrations** - External APIs, AI services
3. **GPU for real-time** - Voice requires GPU acceleration
4. **Schema-driven** - CSV schemas generate includes
5. **Phantom process** - QM handles WebSocket directly
6. **Multi-domain** - Medical, financial, personal, knowledge, system
7. **Voice-first** - Natural conversation is primary UI
8. **Local-first** - All personal data on premises

### Next Steps

**To work on HAL**:
1. Read specific domain docs (medical, financial, etc.)
2. Review code in relevant directory (BP/ or PY/)
3. Check schema in SCHEMA/
4. Test changes locally
5. Update documentation
6. Deploy carefully

---

**End of HAL System Master Documentation**

*This document is the single source of truth for HAL architecture.*  
*Keep it updated as the system evolves.*

---

**File Location**: `C:\qmsys\hal\HAL_SYSTEM_MASTER.md`  
**Version**: 2.0  
**Maintained By**: Project maintainers and AI agents  
**Last Review**: 2025-11-27

---

## 🔄 For Future AI Agents

**Before you make ANY changes to this system**:

1. ✅ Read this entire file (`HAL_SYSTEM_MASTER.md`)
2. ✅ Read `DOCUMENTATION_MAINTENANCE.md` for update procedures
3. ✅ **Read `DOCS/SYNTAX.MD`** for OpenQM syntax rules and common errors
4. ✅ Pull latest from GitHub: `git pull origin main`
5. ✅ Understand current architecture and decisions
6. ✅ Create backup branch before major changes
7. ✅ Update docs in same session as code changes
8. ✅ Push to GitHub before risky operations

**Before writing QM BASIC or QM TCL code**:

1. ✅ **MUST READ**: `DOCS/SYNTAX.MD` - Contains all OpenQM syntax rules
2. ✅ Check Section 15 for previously encountered syntax errors
3. ✅ Follow QM-specific conventions (not UniVerse)
4. ✅ If you encounter a NEW syntax error:
   - Add entry to `DOCS/SYNTAX.MD` Section 15 immediately
   - Include date, description, wrong/correct examples
   - Commit the update so future agents learn from it

**Repository**: https://github.com/lcsmd/hal (owner: lcsmd)

**Your responsibility**: 
- Keep this documentation accurate and current
- Learn from previous syntax errors in SYNTAX.MD
- Update SYNTAX.MD when you discover new errors
- Never repeat errors listed in SYNTAX.MD Section 15

**Failure to maintain docs**: Future AI agents will make conflicting changes based on outdated information.

**Failure to read SYNTAX.MD**: You will repeat syntax errors that have already been solved.
