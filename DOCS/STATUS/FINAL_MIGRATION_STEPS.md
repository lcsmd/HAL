# HAL Code Reorganization - Final Safe Steps

## Step 1: Clean Up Empty Windows Directories

Run the safe cleanup script:

```powershell
cd C:\QMSYS\HAL
.\cleanup_empty_dirs.ps1
```

This script will:
- Check each directory (FIN.BP, MED.BP, etc.)
- **Only delete if completely empty**
- **Keep any directory with files**
- Show you what it's doing

## Step 2: Start QM and Create Directory Files

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

This creates proper QM directory files.

## Step 3: Verify Directories Created

```
:LISTF
```

You should see: FIN.BP, MED.BP, SEC.BP, COM.BP, UTIL.BP

## Step 4: Run Migration Program

```
:BASIC ONCE.BP MIGRATE.REORGANIZE
:RUN ONCE.BP MIGRATE.REORGANIZE
```

Type **YES** when prompted.

This will:
- Copy programs from BP to domain directories
- Rename with domain prefixes (FIN., MED., SEC., etc.)
- Leave originals in BP unchanged
- Generate migration report

## Step 5: Review Migration Report

```
notepad C:\QMSYS\HAL\MIGRATION.REPORT.txt
```

## Step 6: Compile New Programs

```
:BASIC FIN.BP *
:BASIC MED.BP *
:BASIC SEC.BP *
:BASIC UTIL.BP *
```

## Step 7: Catalog New Programs

```
:CATALOG FIN.BP *
:CATALOG MED.BP *
:CATALOG SEC.BP *
:CATALOG UTIL.BP *
```

## Step 8: Test

Test the new programs:
```
:FIN.IMPORT.QUICKEN
:SEC.PASSWORD.MENU
:MED.IMPORT.EPIC
```

## Done!

Your code is now organized by domain with proper naming conventions.

Original programs remain in BP as backup until you're ready to archive them.
