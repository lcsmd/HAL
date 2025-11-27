# HAL System - Documentation Index

> **Personal AI Assistant with Medical, Financial, and Knowledge Management**

---

## 🎯 For AI Agents & Complete System Understanding

### **[HAL_SYSTEM_MASTER.md](HAL_SYSTEM_MASTER.md)** ← START HERE

**Complete system documentation in a single file** (846 lines, 31KB):
- Architecture decisions and rationale
- All code locations (75+ QM programs, 50+ Python scripts)
- Database structure (40+ files, schema system)
- Network infrastructure (4 servers, IP addresses, roles)
- Integration points (Epic, Gmail, AI services)
- Development history and lessons learned
- Security, deployment, and maintenance

**Purpose**: Single source of truth for AI agents to understand the entire HAL system.

---

## 🚀 Quick Start (For Users)

- **[START_HERE.md](START_HERE.md)** - Complete setup guide for Epic API integration
- **[README.md](README.md)** - System overview and basic usage
- **[CONFIGURATION.md](CONFIGURATION.md)** - Environment variable configuration

---

## 📚 Core Documentation

### System Architecture
- **[AI_INTEGRATION_SUMMARY.md](AI_INTEGRATION_SUMMARY.md)** - AI/LLM integration architecture (Ollama, OpenAI, Anthropic)
- **[MODEL_SYSTEM_README.md](MODEL_SYSTEM_README.md)** - Model selection and routing system
- **[README_SCHEMA_SYSTEM.md](README_SCHEMA_SYSTEM.md)** - Schema-driven file management system

### Medical Data
- **[README_EPIC_API.md](README_EPIC_API.md)** - Epic FHIR API integration guide
- **[NOTES/epic_api_quickstart.md](NOTES/epic_api_quickstart.md)** - 15-minute Epic setup
- **[NOTES/epic_api_setup_guide.md](NOTES/epic_api_setup_guide.md)** - Detailed Epic configuration
- **[NOTES/epic_export_guide.md](NOTES/epic_export_guide.md)** - Exporting data from Epic MyChart
- **[NOTES/medical_schema.md](NOTES/medical_schema.md)** - Medical entity schemas
- **[NOTES/medical_programs.md](NOTES/medical_programs.md)** - Medical data management programs

### Financial Data
- **[README_TRANSACTION_SYSTEM.md](README_TRANSACTION_SYSTEM.md)** - Transaction classification system
- **[TRANSACTION_SYSTEM_SUMMARY.md](TRANSACTION_SYSTEM_SUMMARY.md)** - Transaction features overview
- **[QUICKSTART_TRANSACTIONS.md](QUICKSTART_TRANSACTIONS.md)** - Quick start for transactions
- **[QUICKBOOKS_IMPORT_READY.md](QUICKBOOKS_IMPORT_READY.md)** - QuickBooks integration status
- **[README_AI_CLASSIFICATION.md](README_AI_CLASSIFICATION.md)** - AI-powered transaction classification
- **[README_AI_RULE_LEARNING.md](README_AI_RULE_LEARNING.md)** - Learning classification rules

### Security
- **[README_PASSWORD_MANAGER.md](README_PASSWORD_MANAGER.md)** - Password vault overview
- **[README_PASSWORD_QMBASIC.md](README_PASSWORD_QMBASIC.md)** - QM Basic password functions
- **[PASSWORD_MANAGER_SUMMARY.md](PASSWORD_MANAGER_SUMMARY.md)** - Password system features
- **[NOTES/password_manager_guide.md](NOTES/password_manager_guide.md)** - Detailed usage guide

---

## 🔧 Setup & Configuration

### Initial Setup
- **[QUICK_START_ENV.md](QUICK_START_ENV.md)** - Environment setup
- **[setup_environment.ps1](setup_environment.ps1)** - Automated environment configuration
- **[setup_environment.bat](setup_environment.bat)** - Batch file alternative

### Email Integration
- **[GMAIL_SETUP_INSTRUCTIONS.md](GMAIL_SETUP_INSTRUCTIONS.md)** - Gmail API setup
- **[PY/gmail_import.py](PY/gmail_import.py)** - Gmail import script

### Migration & Upgrades
- **[QUICK_START_MIGRATION.md](QUICK_START_MIGRATION.md)** - Migration guide
- **[SAFE_MIGRATION_STEPS.md](SAFE_MIGRATION_STEPS.md)** - Safe migration procedures
- **[FINAL_MIGRATION_STEPS.md](FINAL_MIGRATION_STEPS.md)** - Final migration steps
- **[FORMAT_CONVERSION_COMPLETE.md](FORMAT_CONVERSION_COMPLETE.md)** - Format conversion status

---

## 📖 Technical Documentation

### Schema System
- **[DOCS/SCHEMA_ARCHITECTURE.md](DOCS/SCHEMA_ARCHITECTURE.md)** - Schema architecture overview
- **[DOCS/SCHEMA_QUICK_START.md](DOCS/SCHEMA_QUICK_START.md)** - Quick start guide
- **[SCHEMA/](SCHEMA/)** - Directory containing all CSV schemas

### Data Import
- **[UPLOADS/QUICKBOOKS_IMPORT_GUIDE.md](UPLOADS/QUICKBOOKS_IMPORT_GUIDE.md)** - QuickBooks CSV import
- **[UPLOADS/CSV_IMPORT_GUIDE.md](UPLOADS/CSV_IMPORT_GUIDE.md)** - Generic CSV import
- **[UPLOADS/QM_INTERNAL_FORMATS.md](UPLOADS/QM_INTERNAL_FORMATS.md)** - QM data formats
- **[UPLOADS/DUPLICATE_PREVENTION_SUMMARY.md](UPLOADS/DUPLICATE_PREVENTION_SUMMARY.md)** - Duplicate detection

### Organization & Standards
- **[NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md)** - File and entity naming rules
- **[NAMING_FINAL.md](NAMING_FINAL.md)** - Finalized naming standards
- **[NAMING_SUMMARY.md](NAMING_SUMMARY.md)** - Naming summary
- **[ORGANIZATION_FINAL.md](ORGANIZATION_FINAL.md)** - Final organization structure
- **[ORGANIZATION_PROPOSAL.md](ORGANIZATION_PROPOSAL.md)** - Original proposal
- **[ORGANIZATION_REVISED.md](ORGANIZATION_REVISED.md)** - Revised proposal

---

## 🛠️ Development

### QM Basic Programs
- **[BP/](BP/)** - Main program directory (54 programs)
  - Schema management (SCHEMA.*)
  - Password vault (PASSWORD.*)
  - Data import (IMPORT.*)
  - Medical menus (MEDICAL.*, MEDICATION.*)
  - Transaction processing (STANDARDIZE.*, TAG.*)

### Python Scripts
- **[PY/](PY/)** - Python scripts directory (50+ scripts)
  - Epic API: `epic_api_*.py`
  - Password management: `password_*.py`
  - AI classification: `ai_*.py`
  - Photo analysis: `photo_analyzer.py`
  - HAL agent: `hal_agent.py`, `hal_service.py`

### Include Files
- **[EQU/](EQU/)** - QM Basic include files (84 headers)
  - File equates: `*.h` files
  - Domain definitions
  - Common variables

---

## 📊 Data Files

### Medical Entities (9 types)
- **MEDICATION** - Prescriptions and medications
- **ALLERGY** - Allergic reactions and sensitivities
- **IMMUNIZATION** - Vaccination records
- **MEDICAL_HISTORY** - Diagnoses and conditions
- **MEDICAL_TEST** - Lab results and diagnostics
- **VITAL_SIGNS** - Blood pressure, weight, temperature, etc.
- **DOCTOR** - Healthcare providers
- **HEALTHCARE_FACILITY** - Hospitals and clinics
- **PHARMACY** - Pharmacy locations

### Financial Entities
- **TRANSACTION** - Bank transactions
- **PAYEE** - Vendors and merchants
- **CATEGORY** - Transaction categories
- **REIMBURSEMENT** - Reimbursable expenses
- **TAG** - Transaction tags

### Personal Data
- **PERSON** - People and contacts
- **PLACE** - Locations
- **PHOTO** - Image files
- **PHOTO_GROUP** - Image collections
- **DOCUMENT** - Documents
- **EMAIL** - Email messages
- **CONVERSATION** - Chat history

### System Files
- **SCHEMA** - Schema definitions
- **DOMAINS** - Domain registry
- **FIELDS** - Field definitions
- **FILES** - File metadata
- **MODEL** - AI model configurations
- **MEMORY** - AI memory storage
- **LOG** - System logs

---

## 🎯 Common Tasks

### Medical Data Management
```bash
# Setup Epic API (one-time)
python PY\epic_api_setup.py

# Sync medical data
python PY\epic_api_sync.py P001

# View medications
LIST MEDICATION

# View allergies
LIST ALLERGY
```

### Financial Data Management
```qm
# Import QuickBooks transactions
BASIC BP IMPORT.QUICKEN
CATALOG BP IMPORT.QUICKEN
IMPORT.QUICKEN

# Standardize payee names
STANDARDIZE.PAYEES

# Tag reimbursable expenses
TAG.REIMBURSABLE

# Generate reimbursement report
REPORT.REIMBURSABLE
```

### Password Management
```qm
# Access password menu
PASSWORD.MENU

# Add new password
PASSWORD.ADD

# Search passwords
PASSWORD.SEARCH

# View password entry
PASSWORD.VIEW
```

### Schema Management
```qm
# Schema manager menu
SCHEMA.MANAGER

# Add new domain
SCHEMA.ADD.DOMAIN

# Add new file
SCHEMA.ADD.FILE

# Validate schemas
SCHEMA.VALIDATE
```

### AI Integration
```qm
# Ask AI (default model)
ask.b what is EGPA

# Use specific model
ask.b gpt-4o explain quantum physics
ask.b claude-3.5-sonnet write a poem
ask.b deepseek-r1:32b solve this math problem
```

---

## 🔍 File Locations

### Configuration
- `config/` - Configuration files
- `config/epic_api_config.json` - Epic API settings
- `.env` - Environment variables (if using Python .env)

### Data Directories
- `SCHEMA/` - Schema CSV files
- `EQU/` - Include headers
- `UPLOADS/` - Downloaded/imported data
- `logs/` - Application logs

### Medical Directories
- `MEDICATION/` - Medication records
- `ALLERGY/` - Allergy records
- `IMMUNIZATION/` - Immunization records
- `MEDICAL_HISTORY/` - Medical history
- `VITAL_SIGNS/` - Vital signs

### Financial Directories
- `TRANSACTION/` - Transaction records
- `PAYEE/` - Payee information
- `REIMBURSEMENT/` - Reimbursement tracking

---

## 🆘 Troubleshooting

### Epic API Issues
- Check: `logs/epic_sync.log`
- Test: `python PY\test_epic_setup.py`
- Re-authorize: `python PY\epic_api_setup.py`

### Python Issues
- Verify installation: `python --version`
- Check environment: `echo %HAL_PYTHON_PATH%`
- Reinstall dependencies: `pip install -r PY\requirements.txt`

### QM Basic Issues
- Check compilation: `BASIC BP program.name`
- Catalog: `CATALOG BP program.name`
- View errors: Check compiler output

---

## 📝 Project Management

### Task Tracking
- **[TASKS/project_plan.md](TASKS/project_plan.md)** - Project roadmap
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Next development steps
- **[NOTES/progress.md](NOTES/progress.md)** - Development progress

### Change Logs
- **[CHANGELOG_ENV_CONFIG.md](CHANGELOG_ENV_CONFIG.md)** - Configuration changes
- **[FINAL_SUMMARY.md](FINAL_SUMMARY.md)** - Project summary

---

## 🌐 External Resources

### Epic API Resources
- [Epic App Orchard](https://apporchard.epic.com/) - Register your app
- [Epic FHIR Documentation](https://fhir.epic.com/) - API documentation

### OpenQM Resources
- **[QM_HELP/](QM_HELP/)** - OpenQM documentation (140+ files)
- OpenQM official documentation

---

## 📞 Support

For issues or questions:
1. Check relevant documentation above
2. Review logs in `logs/` directory
3. Run diagnostic scripts in `test_*.ps1`
4. Check git commit history for recent changes

---

**Last Updated**: 2025-10-30  
**System Version**: 2.0 (Schema System + Epic Integration)
