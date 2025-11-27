# HAL Code Organization Proposal

## Current Issues

1. **Flat structure** - All programs in single BP/ and PY/ directories
2. **No domain grouping** - Medical, financial, security programs mixed together
3. **Name collision risk** - SETUP, MENU, etc. could conflict across domains
4. **Hard to navigate** - 46 QMBasic + 44 Python programs in flat directories
5. **No distinction** - Core vs. domain-specific vs. utility vs. one-time programs

## Organizational Options

### Option 1: Domain-Prefixed Programs (Flat Structure)
**Keep flat directories, prefix program names with domain**

```
BP/
  sys.BUILD.SCHEMA
  sys.BUILD.INDEX
  sys.OPEN.FILES
  fin.IMPORT.QUICKEN
  fin.STANDARDIZE.PAYEES
  fin.TAG.REIMBURSABLE
  fin.REPORT.REIMBURSABLE
  med.IMPORT.EPIC
  med.MEDICAL.MENU
  med.MEDICATION.MENU
  sec.PASSWORD.MENU
  sec.PASSWORD.ADD
  sec.PASSWORD.VIEW
```

**Pros:**
- Simple to implement
- All programs in one place
- Easy to catalog
- Clear domain ownership

**Cons:**
- Still cluttered with 90+ programs
- Longer program names
- No physical separation

### Option 2: Domain Directories (Deep Structure)
**Organize by domain with .BP and .PY suffixes**

```
FIN.BP/          # Financial QMBasic programs
  IMPORT.QUICKEN
  STANDARDIZE.PAYEES
  TAG.REIMBURSABLE
  REPORT.REIMBURSABLE
  MANAGE.RULES

FIN.PY/          # Financial Python programs
  ai_rule_learner.py
  ai_classifier.py

MED.BP/          # Medical QMBasic programs
  IMPORT.EPIC
  MEDICAL.MENU
  MEDICATION.MENU
  APPOINTMENT.REMINDER

MED.PY/          # Medical Python programs
  epic_api_sync.py
  epic_parser.py
  epic_scheduler.py
  analyze_epic_pdf.py

SEC.BP/          # Security QMBasic programs
  PASSWORD.MENU
  PASSWORD.ADD
  PASSWORD.VIEW
  PASSWORD.SEARCH
  PASSWORD.DELETE
  PASSWORD.LOGIN
  PASSWORD.MASTER.SETUP

SEC.PY/          # Security Python programs
  password_manager.py
  password_crypto.py
  crypto_wrapper.py
  import_passwords.py

SYS.BP/          # System/Core QMBasic programs
  BUILD.SCHEMA
  BUILD.INDEX
  BUILD.DICT
  OPEN.FILES
  SCHEMA.MANAGER
  SCHEMA.ADD.DOMAIN
  SCHEMA.ADD.FILE
  SCHEMA.ADD.FIELD

SYS.PY/          # System/Core Python programs
  compile_schema.py
  create_all_schema.py
  hal_service.py
  hal_agent.py
  hal_chat.py

UTIL.BP/         # Utility programs (one-time, testing)
  TEST.DICT
  TEST.OPEN.FILES
  TEST.PATH
  CRUD.TEMPLATE
  STR

UTIL.PY/         # Utility Python scripts
  verify_setup.py
  verify_bp_type.py
  test_system.py
```

**Pros:**
- Clear domain separation
- Prevents name collisions
- Easy to find related programs
- Scalable as system grows
- Can set permissions per domain

**Cons:**
- More directories to manage
- Need to catalog from multiple locations
- Slightly more complex structure

### Option 3: Hybrid Approach (RECOMMENDED)
**Domain directories for domain-specific, flat for core/utilities**

```
BP/              # Core system programs (no domain prefix needed)
  BUILD.SCHEMA
  BUILD.INDEX
  BUILD.DICT
  OPEN.FILES
  SCHEMA.MANAGER
  SCHEMA.ADD.DOMAIN
  SCHEMA.ADD.FILE
  SCHEMA.ADD.FIELD
  SCHEMA.VALIDATE
  SCHEMA.SUMMARY

PY/              # Core system Python
  hal_service.py
  hal_agent.py
  hal_chat.py
  compile_schema.py
  create_all_schema.py

FIN.BP/          # Financial domain
  IMPORT.QUICKEN
  STANDARDIZE.PAYEES
  TAG.REIMBURSABLE
  REPORT.REIMBURSABLE
  MANAGE.RULES

FIN.PY/
  ai_rule_learner.py
  ai_classifier.py

MED.BP/          # Medical domain
  IMPORT.EPIC
  MEDICAL.MENU
  MEDICATION.MENU
  APPOINTMENT.REMINDER

MED.PY/
  epic_api_sync.py
  epic_parser.py
  epic_scheduler.py
  epic_api_setup.py
  analyze_epic_pdf.py
  combine_fhir_bundles.py

SEC.BP/          # Security domain
  PASSWORD.MENU
  PASSWORD.ADD
  PASSWORD.VIEW
  PASSWORD.SEARCH
  PASSWORD.DELETE
  PASSWORD.LOGIN
  PASSWORD.MASTER.SETUP

SEC.PY/
  password_manager.py
  password_crypto.py
  crypto_wrapper.py
  import_passwords.py

COM.BP/          # Communication domain
  (future: email, messaging programs)

COM.PY/
  gmail_import.py
  create_email_file.py
  setup_email_file.py

UTIL.BP/         # Utilities and one-time programs
  TEST.DICT
  TEST.OPEN.FILES
  TEST.PATH
  CRUD.TEMPLATE
  STR
  DATA.FILTER

UTIL.PY/         # Utility scripts
  verify_setup.py
  verify_bp_type.py
  verify_data_filter.py
  test_system.py
  check_voc.py
```

**Pros:**
- Best of both worlds
- Core programs easy to find (no prefix needed)
- Domain programs organized separately
- Prevents name collisions where it matters
- Utilities clearly separated
- Scalable and maintainable

**Cons:**
- Requires migration effort
- Need to update catalog references

## Recommended Structure: Hybrid Approach

### Directory Naming Convention

```
[DOMAIN].BP/     # QMBasic programs for domain
[DOMAIN].PY/     # Python programs for domain
BP/              # Core system QMBasic (no domain)
PY/              # Core system Python (no domain)
UTIL.BP/         # Utility QMBasic programs
UTIL.PY/         # Utility Python scripts
```

### Program Naming Convention

**Within domain directories:**
- No domain prefix needed (directory provides context)
- Use descriptive names: `IMPORT.QUICKEN`, `PASSWORD.MENU`
- Avoid generic names that might conflict

**Within core directories (BP/, PY/):**
- System-level programs only
- Prefix with function: `BUILD.SCHEMA`, `SCHEMA.MANAGER`
- Clear, unambiguous names

### Domain Abbreviations (from DOMAINS.CSV)

```
fin - Finance
med - Medical
sch - School
wor - Work
per - Personal
new - News
sys - System
sec - Security
com - Communication
doc - Documents
```

### Migration Plan

#### Phase 1: Create New Structure (No Breaking Changes)

```bash
# Create domain directories
mkdir FIN.BP FIN.PY
mkdir MED.BP MED.PY
mkdir SEC.BP SEC.PY
mkdir COM.BP COM.PY
mkdir UTIL.BP UTIL.PY
```

#### Phase 2: Copy Programs to New Locations

```bash
# Financial
copy BP\IMPORT.QUICKEN FIN.BP\
copy BP\STANDARDIZE.PAYEES FIN.BP\
copy BP\TAG.REIMBURSABLE FIN.BP\
copy BP\REPORT.REIMBURSABLE FIN.BP\
copy BP\MANAGE.RULES FIN.BP\

copy PY\ai_rule_learner.py FIN.PY\
copy PY\ai_classifier.py FIN.PY\

# Medical
copy BP\IMPORT.EPIC MED.BP\
copy BP\MEDICAL.MENU MED.BP\
copy BP\MEDICATION.MENU MED.BP\
copy BP\APPOINTMENT.REMINDER MED.BP\

copy PY\epic_api_sync.py MED.PY\
copy PY\epic_parser.py MED.PY\
copy PY\epic_scheduler.py MED.PY\
copy PY\epic_api_setup.py MED.PY\
copy PY\analyze_epic_pdf.py MED.PY\

# Security
copy BP\PASSWORD.* SEC.BP\

copy PY\password_manager.py SEC.PY\
copy PY\password_crypto.py SEC.PY\
copy PY\crypto_wrapper.py SEC.PY\
copy PY\import_passwords.py SEC.PY\

# Communication
copy PY\gmail_import.py COM.PY\
copy PY\create_email_file.py COM.PY\

# Utilities
copy BP\TEST.* UTIL.BP\
copy BP\CRUD.TEMPLATE UTIL.BP\
copy BP\STR UTIL.BP\
copy BP\DATA.FILTER UTIL.BP\

copy PY\verify_*.py UTIL.PY\
copy PY\test_system.py UTIL.PY\
```

#### Phase 3: Compile and Catalog from New Locations

```
# Compile domain programs
BASIC FIN.BP IMPORT.QUICKEN
BASIC FIN.BP STANDARDIZE.PAYEES
...

# Catalog domain programs
CATALOG FIN.BP IMPORT.QUICKEN
CATALOG FIN.BP STANDARDIZE.PAYEES
...
```

#### Phase 4: Update Documentation

Update all README files to reference new locations.

#### Phase 5: Remove Old Copies (After Testing)

Once verified, remove programs from old BP/ and PY/ directories.

### Catalog Management

**Global Catalog:**
Programs cataloged from any directory are available system-wide.

```
:CATALOG FIN.BP IMPORT.QUICKEN
:IMPORT.QUICKEN              # Works from anywhere
```

**No conflicts** because program names are unique across domains.

### Benefits of This Approach

1. **Clear Organization** - Domain programs grouped together
2. **No Name Collisions** - `FIN.BP/SETUP` vs `MED.BP/SETUP` possible
3. **Easy Navigation** - Find all financial programs in FIN.BP/
4. **Scalable** - Add new domains easily
5. **Maintainable** - Clear ownership and responsibility
6. **Backward Compatible** - Cataloged programs work the same
7. **Separation of Concerns** - Core vs domain vs utility clearly separated

### Alternative: Domain Prefixes in Flat Structure

If you prefer simpler structure, use domain prefixes:

```
BP/
  fin.IMPORT.QUICKEN
  fin.STANDARDIZE.PAYEES
  med.IMPORT.EPIC
  med.MEDICAL.MENU
  sec.PASSWORD.MENU
  sys.BUILD.SCHEMA
```

**Pros:**
- Simpler directory structure
- All programs in one place
- Easy to see all programs at once

**Cons:**
- Longer program names
- Still cluttered
- Harder to navigate with 90+ programs

## Recommendation

**Use Hybrid Approach (Option 3)** because:

1. **Best organization** - Domain separation where it matters
2. **Prevents collisions** - Each domain can have MENU, SETUP, etc.
3. **Scalable** - Easy to add new domains
4. **Clear purpose** - Core vs domain vs utility obvious
5. **Professional** - Industry-standard organization pattern
6. **Maintainable** - Easy to find and update related programs

## Implementation Priority

### Immediate (Week 1)
1. Create domain directories
2. Copy financial programs (FIN.BP, FIN.PY)
3. Copy security programs (SEC.BP, SEC.PY)
4. Compile and catalog from new locations
5. Test functionality

### Short-term (Week 2-3)
1. Copy medical programs (MED.BP, MED.PY)
2. Copy communication programs (COM.PY)
3. Move utilities (UTIL.BP, UTIL.PY)
4. Update documentation

### Medium-term (Month 1)
1. Verify all programs work from new locations
2. Remove old copies from BP/ and PY/
3. Update all scripts and batch files
4. Create domain-specific README files

## Questions to Consider

1. **Should core programs stay in BP/ or move to SYS.BP/?**
   - Recommend: Keep in BP/ for simplicity
   - Core programs are used everywhere, no domain needed

2. **Should we use domain prefixes within domain directories?**
   - Recommend: No, directory provides context
   - `FIN.BP/IMPORT.QUICKEN` not `FIN.BP/fin.IMPORT.QUICKEN`

3. **What about programs that span multiple domains?**
   - Put in most relevant domain
   - Or create SHARED.BP/ for cross-domain programs

4. **Should TRANS.BP be renamed to FIN.BP?**
   - Yes, TRANS.BP contains old transaction programs
   - New programs already in FIN.BP
   - Can deprecate TRANS.BP after migration

5. **What about EPIC.BP?**
   - Rename to MED.BP or merge into MED.BP
   - EPIC is medical domain

## Summary

**Recommended approach: Hybrid with domain directories**

- Core programs: `BP/`, `PY/`
- Domain programs: `[DOMAIN].BP/`, `[DOMAIN].PY/`
- Utilities: `UTIL.BP/`, `UTIL.PY/`
- No domain prefixes in program names (directory provides context)
- Clear, scalable, professional organization

This provides the best balance of organization, maintainability, and ease of use.
