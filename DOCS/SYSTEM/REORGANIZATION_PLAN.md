# HAL Documentation Reorganization Plan

**Date**: 2025-11-27  
**Purpose**: Move documentation from root HAL directory into organized DOCS structure

---

## 🎯 Problem

Currently **97+ markdown files** scattered in root `C:\qmsys\hal\` directory, causing:
- Clutter and confusion
- Difficult to find relevant docs
- Mixed with code and data files
- Hard to maintain organization

---

## 💡 Solution

Create organized OpenQM DOCS directory structure with logical categorization.

---

## 📂 Proposed DOCS Directory Structure

```
C:\qmsys\hal\DOCS\
│
├── SYSTEM\                     - Core system documentation
│   ├── HAL_SYSTEM_MASTER.md    - Master architecture doc (move here)
│   ├── DOCUMENTATION_MAINTENANCE.md
│   ├── README.md               - System overview
│   ├── INDEX.md                - Documentation index
│   ├── CONFIGURATION.md
│   └── CHANGELOG.md
│
├── ARCHITECTURE\               - Architectural documentation
│   ├── AI_INTEGRATION_SUMMARY.md
│   ├── MODEL_SYSTEM_README.md
│   ├── VOICE_INTERFACE_ARCHITECTURE.md
│   ├── SCHEMA_ARCHITECTURE.md
│   └── DEPLOYMENT_GUIDE.md
│
├── FEATURES\                   - Feature-specific documentation
│   ├── MEDICAL\
│   │   ├── README_EPIC_API.md
│   │   ├── MEDICAL_SCHEMA.md
│   │   ├── EPIC_API_QUICKSTART.md
│   │   └── EPIC_API_SETUP_GUIDE.md
│   ├── FINANCIAL\
│   │   ├── README_TRANSACTION_SYSTEM.md
│   │   ├── README_AI_CLASSIFICATION.md
│   │   ├── QUICKSTART_TRANSACTIONS.md
│   │   └── QUICKBOOKS_IMPORT_READY.md
│   ├── PASSWORD\
│   │   ├── README_PASSWORD_MANAGER.md
│   │   ├── PASSWORD_MANAGER_SUMMARY.md
│   │   └── PASSWORD_MANAGER_GUIDE.md
│   ├── VOICE\
│   │   ├── VOICE_SYSTEM_FINAL_STATUS.md
│   │   ├── VOICE_INTERFACE_SUMMARY.md
│   │   ├── START_VOICE_SYSTEM.md
│   │   └── QUICK_START_VOICE.md
│   └── SCHEMA\
│       ├── README_SCHEMA_SYSTEM.md
│       ├── SCHEMA_ARCHITECTURE.md
│       └── SCHEMA_QUICK_START.md
│
├── DEPLOYMENT\                 - Deployment documentation
│   ├── MAC_DEPLOYMENT_READY.md
│   ├── DEPLOYMENT_COMPLETE.md
│   ├── DEPLOYMENT_STATUS.md
│   └── DEPLOY_INSTRUCTIONS.md
│
├── SETUP\                      - Setup and quick start guides
│   ├── START_HERE.md
│   ├── QUICK_START_ENV.md
│   ├── QUICK_START_MIGRATION.md
│   └── SAFE_MIGRATION_STEPS.md
│
├── STATUS\                     - Status and progress reports
│   ├── FINAL_SUMMARY.md
│   ├── FINAL_STATUS.md
│   ├── CLEANUP_SUMMARY.md
│   └── MIGRATION_REPORT.txt
│
├── DEVELOPMENT\                - Development documentation
│   ├── NAMING_CONVENTIONS.md
│   ├── ORGANIZATION_FINAL.md
│   ├── CODING_STANDARDS.md
│   └── CHANGELOG_ENV_CONFIG.md
│
└── REFERENCE\                  - Reference materials
    ├── API_REFERENCE.md
    ├── COMMAND_REFERENCE.md
    └── TROUBLESHOOTING.md
```

---

## 🚀 Implementation Steps

### Step 1: Create DOCS Directory in QM (if not exists)

```qm
* In QM terminal
LOGTO HAL
CREATE.FILE DOCS DIRECTORY
```

Or verify exists:
```qm
LIST.FILES DOCS
```

### Step 2: Create Subdirectories

Since OpenQM DOCS is a directory-type file, we'll use filesystem subdirectories:

```bash
cd C:\qmsys\hal\DOCS
mkdir SYSTEM
mkdir ARCHITECTURE
mkdir FEATURES
mkdir FEATURES\MEDICAL
mkdir FEATURES\FINANCIAL
mkdir FEATURES\PASSWORD
mkdir FEATURES\VOICE
mkdir FEATURES\SCHEMA
mkdir DEPLOYMENT
mkdir SETUP
mkdir STATUS
mkdir DEVELOPMENT
mkdir REFERENCE
```

### Step 3: Move Files (Organized by Category)

**SYSTEM** (Core system docs):
```bash
move HAL_SYSTEM_MASTER.md DOCS\SYSTEM\
move DOCUMENTATION_MAINTENANCE.md DOCS\SYSTEM\
move INDEX.md DOCS\SYSTEM\
move CONFIGURATION.md DOCS\SYSTEM\
```

**ARCHITECTURE**:
```bash
move AI_INTEGRATION_SUMMARY.md DOCS\ARCHITECTURE\
move MODEL_SYSTEM_README.md DOCS\ARCHITECTURE\
move VOICE_INTERFACE_ARCHITECTURE.md DOCS\ARCHITECTURE\
```

**FEATURES\MEDICAL**:
```bash
move README_EPIC_API.md DOCS\FEATURES\MEDICAL\
move NOTES\medical_schema.md DOCS\FEATURES\MEDICAL\
move NOTES\epic_api_*.md DOCS\FEATURES\MEDICAL\
```

**FEATURES\FINANCIAL**:
```bash
move README_TRANSACTION_SYSTEM.md DOCS\FEATURES\FINANCIAL\
move README_AI_CLASSIFICATION.md DOCS\FEATURES\FINANCIAL\
move QUICKSTART_TRANSACTIONS.md DOCS\FEATURES\FINANCIAL\
```

(Continue for all categories...)

### Step 4: Update References

**Update these files**:
1. `DOCS\SYSTEM\HAL_SYSTEM_MASTER.md` - Update all relative paths
2. `DOCS\SYSTEM\INDEX.md` - Update all documentation links
3. `README.md` (keep in root) - Update links to DOCS/
4. `READ_ME_FIRST.txt` (keep in root) - Update paths

### Step 5: Create README in Each Subdirectory

Example `DOCS\FEATURES\MEDICAL\README.md`:
```markdown
# Medical Feature Documentation

This directory contains documentation for HAL's medical data features.

## Files

- **README_EPIC_API.md** - Epic FHIR API integration guide
- **MEDICAL_SCHEMA.md** - Medical data structure
- **EPIC_API_QUICKSTART.md** - 15-minute quick start

## Related

- Code: `C:\qmsys\hal\BP\MEDICATION.*.b`, `BP\MEDICAL.*.b`
- Python: `C:\qmsys\hal\PY\epic_*.py`
- Schema: `C:\qmsys\hal\SCHEMA\medical_*.csv`
```

### Step 6: Update Root Directory

**Keep in root** (essential entry points):
- `README.md` - Main entry point
- `READ_ME_FIRST.txt` - Quick pointer
- `.github-reminder.txt` - Git workflow reminder

**Add new root file**:
- `DOCS.md` - Points to DOCS/ organization

---

## 📝 Files to Keep in Root

**Essential only**:
1. `README.md` - System introduction (links to DOCS/)
2. `READ_ME_FIRST.txt` - Quick start pointer
3. `.gitignore` - Git configuration
4. `.github-reminder.txt` - Git workflow
5. `DOCS.md` - Documentation navigation guide

**Everything else** → Move to DOCS/

---

## 🔄 Migration Commands

### PowerShell Script to Move Files

```powershell
# Create script: migrate_docs.ps1

$docs = @{
    "SYSTEM" = @(
        "HAL_SYSTEM_MASTER.md",
        "DOCUMENTATION_MAINTENANCE.md",
        "INDEX.md",
        "CONFIGURATION.md"
    )
    "ARCHITECTURE" = @(
        "AI_INTEGRATION_SUMMARY.md",
        "MODEL_SYSTEM_README.md"
    )
    # ... (continue for all categories)
}

foreach ($category in $docs.Keys) {
    foreach ($file in $docs[$category]) {
        if (Test-Path $file) {
            Move-Item $file "DOCS\$category\$file"
            Write-Host "Moved: $file -> DOCS\$category\"
        }
    }
}
```

---

## 📋 Updated Master File Location

**Old**: `C:\qmsys\hal\HAL_SYSTEM_MASTER.md`  
**New**: `C:\qmsys\hal\DOCS\SYSTEM\HAL_SYSTEM_MASTER.md`

**Update references in**:
- `README.md` → `[Master Doc](DOCS/SYSTEM/HAL_SYSTEM_MASTER.md)`
- `READ_ME_FIRST.txt` → `Location: C:\qmsys\hal\DOCS\SYSTEM\HAL_SYSTEM_MASTER.md`
- All internal documentation links

---

## ✅ Benefits of Reorganization

1. **Cleaner root directory** - Only essential files
2. **Logical organization** - Easy to find relevant docs
3. **Better maintenance** - Clear where to put new docs
4. **Scalability** - Can add new categories easily
5. **Professional structure** - Industry standard layout

---

## ⚠️ Risks and Mitigation

**Risk**: Broken links in documentation  
**Mitigation**: Use search/replace to update all references

**Risk**: Git history confusion  
**Mitigation**: Use `git mv` instead of move/delete

**Risk**: User confusion during transition  
**Mitigation**: Keep README.md in root pointing to new structure

---

## 🔍 Verification Checklist

After migration:

- [ ] All markdown files moved from root to DOCS/
- [ ] No broken links in documentation
- [ ] README.md updated with new paths
- [ ] READ_ME_FIRST.txt updated
- [ ] HAL_SYSTEM_MASTER.md updated
- [ ] INDEX.md updated with new structure
- [ ] Each DOCS subdirectory has README.md
- [ ] Git commit with descriptive message
- [ ] Pushed to GitHub
- [ ] Tested accessing docs from new locations

---

## 📅 Implementation Timeline

**Phase 1** (30 min): Create directory structure  
**Phase 2** (1 hour): Move files systematically  
**Phase 3** (1 hour): Update all references  
**Phase 4** (30 min): Create subdirectory READMEs  
**Phase 5** (30 min): Test and verify  
**Phase 6** (15 min): Commit and push to GitHub

**Total**: ~3.5 hours

---

## 🎯 Next Steps

1. User approval of structure
2. Create DOCS directory structure
3. Execute migration script
4. Update references
5. Test all documentation links
6. Commit to git with message: `docs: reorganize documentation into DOCS/ structure`
7. Push to GitHub

---

**Status**: PLANNED - Awaiting approval  
**File**: `DOCS_REORGANIZATION_PLAN.md`  
**Will be moved to**: `DOCS\SYSTEM\REORGANIZATION_PLAN.md` (after migration)
