# HAL Code Reorganization - SAFE Migration Steps

## CRITICAL SAFETY RULE

**NEVER DELETE ANY EXISTING DIRECTORIES!**

We will only:
1. Create NEW QM directory files if they don't exist
2. Copy programs to new locations (originals stay in place)
3. Rename during copy (originals unchanged)

## Step 1: Check What Already Exists

From PowerShell in C:\QMSYS\HAL:

```powershell
Get-ChildItem -Directory | Where-Object {$_.Name -match "\.BP$|\.PY$"} | Select-Object Name
```

This shows all existing .BP and .PY directories. **DO NOT DELETE ANY OF THEM!**

## Step 2: Start QM Session

```
cd C:\QMSYS\HAL
qm
```

At QM prompt:
```
:LOGTO HAL
```

## Step 3: Create QM Directory Files (Only if They Don't Exist)

```
:BASIC ONCE.BP CREATE.DOMAIN.DIRS
:RUN ONCE.BP CREATE.DOMAIN.DIRS
```

This program will:
- Check if FIN.BP, MED.BP, SEC.BP, COM.BP, UTIL.BP exist
- Create them ONLY if they don't already exist
- Skip any that already exist

## Step 4: Verify New Directories

```
:LISTF
```

Look for the new directory files in the list.

## Step 5: Run Migration (Copies Programs, Doesn't Delete)

```
:BASIC ONCE.BP MIGRATE.REORGANIZE
:RUN ONCE.BP MIGRATE.REORGANIZE
```

Type **YES** when prompted.

This program will:
- **COPY** programs from BP to domain directories
- **RENAME** during copy (add FIN., MED., SEC. prefixes)
- **LEAVE ORIGINALS** in BP untouched
- Generate a report of what was copied

## Step 6: Review Migration Report

```
notepad C:\QMSYS\HAL\MIGRATION.REPORT.txt
```

## Step 7: Compile New Programs

```
:BASIC FIN.BP *
:BASIC MED.BP *
:BASIC SEC.BP *
:BASIC UTIL.BP *
```

## Step 8: Catalog New Programs

```
:CATALOG FIN.BP *
:CATALOG MED.BP *
:CATALOG SEC.BP *
:CATALOG UTIL.BP *
```

## Step 9: Test Everything

Test the new programs to make sure they work correctly.

## Step 10: ONLY After Verification - Archive Old Programs

**ONLY after you've verified everything works**, you can optionally move (not delete) old programs to an archive:

```
:CREATE.FILE BP.ARCHIVE DIRECTORY
```

Then manually move old programs from BP to BP.ARCHIVE for safekeeping.

**NEVER delete the originals until you're 100% certain the new structure works!**

## What This Approach Does

✅ Creates new directories safely
✅ Copies programs (originals stay in place)
✅ Renames during copy
✅ Leaves all original code untouched
✅ Allows testing before any cleanup
✅ Provides rollback capability

## What This Approach Does NOT Do

❌ Delete any directories
❌ Delete any programs
❌ Modify original code
❌ Risk data loss

This is the SAFE way to reorganize!
