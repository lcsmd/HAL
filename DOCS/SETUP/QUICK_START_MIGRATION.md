# HAL Code Reorganization - Quick Start

## Step 1: Check What Needs to be Deleted

First, check if the .PY directories are empty:

```powershell
Get-ChildItem FIN.PY, MED.PY, SEC.PY, COM.PY, UTIL.PY
```

**If they are EMPTY**, you can delete them along with the .BP directories:

```powershell
Remove-Item FIN.BP, FIN.PY, MED.BP, MED.PY, SEC.BP, SEC.PY, COM.BP, COM.PY, UTIL.BP, UTIL.PY -Recurse -Force
```

**If they contain files**, DO NOT DELETE THEM! Only delete the .BP directories:

```powershell
Remove-Item FIN.BP, MED.BP, SEC.BP, COM.BP, UTIL.BP -Recurse -Force
```

### DO NOT DELETE THESE EXISTING DIRECTORIES:
- ❌ BP (core system programs - KEEP THIS!)
- ❌ PY (core Python programs - KEEP THIS!)
- ❌ TRANS.BP (transaction programs - KEEP THIS!)
- ❌ EPIC.BP (Epic medical programs - KEEP THIS!)
- ❌ ONCE.BP (migration programs - already created correctly)
- ❌ ONCE.PY (migration scripts - already created correctly)
- ❌ Any other existing .BP directories

## Step 2: Run QM Commands

Start QM:
```
cd C:\QMSYS\HAL
qm
```

At QM prompt:
```
:LOGTO HAL
:BASIC ONCE.BP CREATE.DOMAIN.DIRS
:RUN ONCE.BP CREATE.DOMAIN.DIRS
```

This creates the QM directory files properly.

## Step 3: Run Migration

```
:BASIC ONCE.BP MIGRATE.REORGANIZE
:RUN ONCE.BP MIGRATE.REORGANIZE
```

Type **YES** when prompted to confirm.

## Step 4: Review Results

Check the migration report:
```
notepad C:\QMSYS\HAL\MIGRATION.REPORT.txt
```

## That's it!

The programs are now organized in domain directories with proper naming conventions.
