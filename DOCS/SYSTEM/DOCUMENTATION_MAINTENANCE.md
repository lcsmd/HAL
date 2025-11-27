# HAL Documentation Maintenance Guide

**For AI Agents and Human Maintainers**

---

## 🎯 Purpose

This document provides **critical instructions** for keeping HAL system documentation current. All AI agents working on this project **MUST** read and follow these instructions.

---

## ⚠️ CRITICAL RULES

### Rule 1: Master Document is Source of Truth

**File**: `HAL_SYSTEM_MASTER.md`

**Purpose**: Single source of truth for system architecture

**When to update**: ANY architectural change, code reorganization, or infrastructure modification

**Penalty for not updating**: Future AI agents will have outdated information and may make conflicting changes

### Rule 2: Update GitHub BEFORE Major Changes

**Repository**: `https://github.com/lcsmd/hal`  
**Owner**: `lcsmd`

**WORKFLOW**:
```
1. Pull latest from GitHub
2. Review current documentation
3. Make code changes
4. Update documentation
5. Commit documentation first
6. Commit code changes
7. Push to GitHub
8. THEN make major infrastructure changes
```

**Why**: Ensures backup exists before risky changes

### Rule 3: Update Documentation IMMEDIATELY

**Do not**:
- Make changes without documenting
- Plan to "document later"
- Assume documentation will be updated by someone else
- Skip documentation for "small changes"

**Do**:
- Update relevant docs in same session as code changes
- Add entries to development history
- Update affected file inventories
- Check related documentation for consistency

---

## 📋 GitHub Repository Information

### Repository Details

**URL**: `https://github.com/lcsmd/hal`  
**Owner**: `lcsmd`  
**Primary Branch**: `main`  
**Visibility**: Private (assume unless told otherwise)

### Clone Repository

```bash
# First time setup
cd C:\qmsys
git clone https://github.com/lcsmd/hal.git

# Or if already exists
cd C:\qmsys\hal
git pull origin main
```

### Authentication

**Credentials**: See `CREDENTIALS.txt`  
**SSH Key**: Preferred method (if configured)  
**HTTPS**: Fallback method

### Git Configuration

```bash
git config user.name "HAL Development"
git config user.email "dev@hal.local"
```

---

## 🔄 Update Workflow for AI Agents

### Before Starting Any Work

```bash
# 1. Navigate to repository
cd C:\qmsys\hal

# 2. Check current status
git status

# 3. Pull latest changes
git pull origin main

# 4. Review recent commits
git log --oneline -10

# 5. Read HAL_SYSTEM_MASTER.md (if changed)
# Check "Last Updated" date
```

### During Development

**For Every Code Change**:

1. **Identify affected documentation**
   - Master file? (architectural changes)
   - Domain-specific docs? (medical, financial, etc.)
   - Code organization? (new files, moved files)
   - Network changes? (IPs, ports, servers)
   - Integration changes? (new APIs, services)

2. **Update immediately in same session**
   - Edit relevant markdown files
   - Update file inventories
   - Update architecture diagrams (text-based)
   - Add to development history

3. **Verify consistency**
   - Check cross-references
   - Update related documents
   - Ensure no contradictions

### After Making Changes

```bash
# 1. Review all changes
git status
git diff

# 2. Stage documentation first
git add HAL_SYSTEM_MASTER.md
git add DOCUMENTATION_MAINTENANCE.md
git add [other docs changed]

# 3. Commit documentation
git commit -m "docs: update architecture for [change description]

- Updated HAL_SYSTEM_MASTER.md with [specific change]
- Updated [other files] to reflect [changes]
- Reason: [why this change was made]

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"

# 4. Stage code changes
git add BP/
git add PY/
git add [other code]

# 5. Commit code
git commit -m "feat: [feature description]

- Added [specific changes]
- Modified [files changed]
- Related to: [issue/requirement]

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"

# 6. Push to GitHub
git push origin main
```

### Before Major Changes

**"Major Changes" defined as**:
- Infrastructure modifications (server changes, network reconfiguration)
- Database schema changes affecting multiple files
- Architectural refactoring
- Integration with new external systems
- Deployment of new services

**Required workflow**:

```bash
# 1. Ensure everything is committed and pushed
git status  # Should be clean
git push origin main

# 2. Create backup branch
git checkout -b backup-before-[change-name]-$(date +%Y%m%d)
git push origin backup-before-[change-name]-$(date +%Y%m%d)

# 3. Return to main
git checkout main

# 4. Now proceed with major changes

# 5. If changes fail, can revert:
# git checkout backup-before-[change-name]-[date]
# git checkout -b main-recovery
# git push origin main-recovery --force
```

---

## 📝 What to Update When

### When Adding New Code

**Update**:
1. `HAL_SYSTEM_MASTER.md` - Code Organization section
2. File count in relevant section (BP/ or PY/)
3. Add to appropriate category
4. Update System Metrics section
5. Add to Development History

**Example**:
```markdown
### QM Basic Programs (BP/ Directory)

**Count**: 76+ programs  ← INCREMENT THIS

**Categories**:

1. **Core System** (11 programs)  ← INCREMENT IF RELEVANT
   - `WEBSOCKET.LISTENER` - Main phantom process
   - `NEW.PROGRAM` - Brief description  ← ADD YOUR PROGRAM
```

### When Adding New Database File

**Update**:
1. `HAL_SYSTEM_MASTER.md` - Database Structure section
2. Increment total file count
3. Add to appropriate domain table
4. Update Schema System section if schema added
5. Add entry to Development History

**Example**:
```markdown
### Database Structure

**Total Files**: 41+ data files  ← INCREMENT

### Domain: Medical (10 files)  ← INCREMENT IF NEW DOMAIN FILE

| File | Description | Key Field | Record Count |
|------|-------------|-----------|--------------|
| NEW_FILE | Description | ID.FIELD | Variable |  ← ADD ROW
```

### When Changing Architecture

**Update**:
1. `HAL_SYSTEM_MASTER.md` - Architectural Decisions section
2. Add new decision with full rationale
3. Update architecture diagrams
4. Update affected sections (Network, Integration Points, etc.)
5. Add major entry to Development History
6. Update Timeline

**Template for new decision**:
```markdown
### Decision X: [Decision Title]

**Made**: [Date]  
**Rationale**:
- [Why this decision was made]
- [Problems it solves]
- [Benefits gained]

**Alternatives Considered**:
- [Option A] (rejected: [reason])
- [Option B] (rejected: [reason])

**Impact**: 
- [How this affects the system]
- [What changed]
- [Who is affected]

**Files Affected**:
- `file1` - [what changed]
- `file2` - [what changed]
```

### When Adding Integration

**Update**:
1. `HAL_SYSTEM_MASTER.md` - Integration Points section
2. Add to External Systems table
3. Document API endpoints
4. Add authentication details
5. Document data flow
6. Update Network Infrastructure if new ports
7. Update Development History

**Template**:
```markdown
**X. [System Name] ([Protocol])**
- **Purpose**: [What it does]
- **Protocol**: [HTTP/WebSocket/etc.]
- **Endpoint**: [URL]
- **Data Flow**: [Source → Processing → Destination]
- **Frequency**: [How often]
- **Code**: [File locations]
```

### When Modifying Network

**Update**:
1. `HAL_SYSTEM_MASTER.md` - Network Infrastructure section
2. Update server topology diagram (ASCII art)
3. Update Server Details table
4. Update Port Allocation table
5. Update `mac_deployment_package/NETWORK_INFO.md`
6. Update `network_config.sh` if IPs changed
7. Update `CREDENTIALS.txt` if access changed

### When Adding Documentation

**Update**:
1. `HAL_SYSTEM_MASTER.md` - Documentation Index section
2. Add to appropriate category
3. Brief description of purpose
4. Target audience
5. Update `INDEX.md` main documentation index

---

## 🔍 Documentation Review Checklist

### Before Committing

**Run this checklist**:

- [ ] Updated `HAL_SYSTEM_MASTER.md` "Last Updated" date
- [ ] Added entry to Development History section
- [ ] Updated file counts (code, database, docs)
- [ ] Updated relevant domain-specific docs
- [ ] Checked for broken internal links
- [ ] Updated architecture diagrams if changed
- [ ] Updated System Metrics section
- [ ] Verified no contradictions with other docs
- [ ] Reviewed git diff for accuracy
- [ ] Commit messages are clear and descriptive

### Monthly Review (Human or AI)

- [ ] Review all "Last Updated" dates
- [ ] Check System Metrics against actual counts
- [ ] Verify IP addresses still accurate
- [ ] Update credentials if changed
- [ ] Review Development History completeness
- [ ] Check for outdated information
- [ ] Update Future Roadmap section
- [ ] Clean up deprecated documents

---

## 📊 Automated Checks (Optional)

### Script to Verify Documentation

Create `scripts/check_docs.py`:

```python
#!/usr/bin/env python3
"""
Check documentation consistency
Run before committing major changes
"""

import os
from datetime import datetime

def check_master_updated():
    """Verify HAL_SYSTEM_MASTER.md was updated recently"""
    master = "HAL_SYSTEM_MASTER.md"
    if not os.path.exists(master):
        print("❌ HAL_SYSTEM_MASTER.md not found!")
        return False
    
    # Check last modified date
    mod_time = os.path.getmtime(master)
    age_days = (datetime.now().timestamp() - mod_time) / 86400
    
    if age_days > 30:
        print(f"⚠️  HAL_SYSTEM_MASTER.md not updated in {age_days:.0f} days")
        return False
    
    print(f"✅ HAL_SYSTEM_MASTER.md updated {age_days:.0f} days ago")
    return True

def count_files():
    """Count actual files vs. documented counts"""
    bp_count = len([f for f in os.listdir("BP") if f.endswith(".b")])
    py_count = len([f for f in os.listdir("PY") if f.endswith(".py")])
    
    print(f"📊 Actual counts:")
    print(f"   BP programs: {bp_count}")
    print(f"   Python scripts: {py_count}")
    
    # Could parse HAL_SYSTEM_MASTER.md and compare
    # Left as exercise

if __name__ == "__main__":
    check_master_updated()
    count_files()
```

Usage:
```bash
python scripts/check_docs.py
```

---

## 🤖 Instructions for AI Agents

### You Are Responsible For

1. **Reading** `HAL_SYSTEM_MASTER.md` before making any changes
2. **Understanding** current architecture before proposing changes
3. **Updating** documentation immediately after code changes
4. **Committing** documentation separately from code
5. **Pushing** to GitHub before major changes
6. **Verifying** consistency across all related docs

### You Must Never

1. ❌ Skip documentation updates
2. ❌ Make major changes without GitHub backup
3. ❌ Commit code without updating docs
4. ❌ Change architecture without documenting rationale
5. ❌ Leave "Last Updated" dates stale
6. ❌ Create contradictions between documents
7. ❌ Delete documentation without moving content

### When in Doubt

1. **Ask the user** before making undocumented changes
2. **Reference** existing patterns in documentation
3. **Err on the side** of over-documentation
4. **Create a backup branch** before risky changes
5. **Document your uncertainty** in commit messages

### Your Workflow Template

```
1. git pull origin main
2. Read HAL_SYSTEM_MASTER.md development history
3. Make code changes
4. Update HAL_SYSTEM_MASTER.md immediately
5. Update related docs (domain-specific, network, etc.)
6. git add [docs]
7. git commit -m "docs: [changes]"
8. git add [code]
9. git commit -m "feat/fix: [changes]"
10. git push origin main
11. Verify push succeeded
```

---

## 📁 Files You Must Keep Updated

### Critical Files (Update for ANY architectural change)

1. **HAL_SYSTEM_MASTER.md** - Master architecture document
2. **DOCUMENTATION_MAINTENANCE.md** - This file
3. **README.md** - If user-facing changes
4. **INDEX.md** - If adding new documentation

### Domain-Specific Files (Update when domain changes)

**Medical**:
- `README_EPIC_API.md`
- `NOTES/medical_schema.md`
- `NOTES/medical_programs.md`

**Financial**:
- `README_TRANSACTION_SYSTEM.md`
- `README_AI_CLASSIFICATION.md`
- `QUICKSTART_TRANSACTIONS.md`

**Network**:
- `mac_deployment_package/NETWORK_INFO.md`
- `mac_deployment_package/AI_SERVICES.md`
- `CONFIGURATION.md`

**Voice**:
- `VOICE_SYSTEM_FINAL_STATUS.md`
- `mac_deployment_package/PHANTOM_PROCESS_INFO.md`

**Schema**:
- `README_SCHEMA_SYSTEM.md`
- `SCHEMA/*.csv` (if adding entities)

---

## 🔄 Version Control Best Practices

### Commit Message Format

```
<type>: <short description>

<detailed description>
<blank line>
- Bullet point changes
- More details
<blank line>
Reason: <why this change>
Related: <issues/tickets>
<blank line>
Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>
```

**Types**:
- `docs:` - Documentation only
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code restructuring
- `chore:` - Maintenance tasks
- `test:` - Testing changes

### When to Create Branches

**Always create branch for**:
- Major refactoring
- Experimental features
- Risky database changes
- Network infrastructure changes

**Can work on main for**:
- Bug fixes
- Documentation updates
- Minor feature additions
- Code cleanup

### Branch Naming

```
feature/[description]
fix/[bug-description]
refactor/[component]
experimental/[what-testing]
backup-before-[major-change]-[date]
```

---

## 📞 Escalation

### When to Ask User Before Proceeding

1. **Architectural changes** that affect multiple systems
2. **Breaking changes** that require migration
3. **Security implications** (credentials, encryption, access)
4. **Data loss risk** (database schema changes)
5. **Network changes** (IP changes, port changes)
6. **Cost implications** (new services, cloud resources)

### When You Can Proceed

1. **Bug fixes** that don't change architecture
2. **Documentation improvements**
3. **Code refactoring** that maintains same behavior
4. **Adding tests**
5. **Performance optimizations** (with benchmarks)

---

## ✅ Success Criteria

### Documentation is Maintained Successfully When

- ✅ Any team member/AI can read `HAL_SYSTEM_MASTER.md` and understand entire system
- ✅ No contradictions exist between documents
- ✅ All architectural decisions are documented with rationale
- ✅ File counts match reality (±1 acceptable)
- ✅ Network topology diagram reflects actual infrastructure
- ✅ Integration points are accurate and complete
- ✅ Development history shows clear timeline
- ✅ GitHub repository is up to date
- ✅ No "Last Updated" dates older than 60 days for active docs

---

## 🚨 Emergency Procedures

### If Documentation is Severely Outdated

1. **Stop** all development work
2. **Create** emergency branch: `git checkout -b docs-recovery`
3. **Audit** actual system state:
   - Count BP/ programs
   - Count PY/ scripts
   - Check EQU/ includes
   - Verify database files (LIST.FILES in QM)
   - Check actual IP addresses
   - Test all integration points
4. **Update** `HAL_SYSTEM_MASTER.md` with current reality
5. **Update** all related documentation
6. **Commit** with message: `docs: emergency audit and update - [date]`
7. **Push** to GitHub immediately
8. **Resume** normal development

### If Major Change Failed

1. **Don't panic** - you created backup branch
2. **Checkout** backup branch
3. **Review** what went wrong
4. **Document** the failure in Development History
5. **Fix** the issue or revert
6. **Push** corrected state to GitHub

---

## 📚 Summary

### For AI Agents: Remember These

1. **ALWAYS** read `HAL_SYSTEM_MASTER.md` first
2. **ALWAYS** update docs in same session as code changes
3. **ALWAYS** commit docs before code
4. **ALWAYS** push to GitHub before major changes
5. **NEVER** skip documentation
6. **NEVER** make contradictory changes
7. **NEVER** delete documentation without migrating content

### For Humans: Remember These

1. Review documentation quarterly
2. Update credentials if they change
3. Keep GitHub repository accessible to AI agents
4. Verify documentation after major AI agent sessions
5. Thank AI agents who maintain docs properly

---

**File**: `DOCUMENTATION_MAINTENANCE.md`  
**Purpose**: Instructions for maintaining HAL documentation  
**Audience**: AI agents (primary), human developers (secondary)  
**Criticality**: CRITICAL - System depends on accurate documentation  
**Last Updated**: 2025-11-27  

**This file itself must be kept updated as documentation practices evolve!**
