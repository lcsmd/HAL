# HAL Migration - Next Steps

## ✅ Completed

Empty Windows directories have been safely deleted.

## 🔄 Next: Run Migration in QM

You have two options:

### Option 1: Run Batch File (Automated)

```cmd
cd C:\QMSYS\HAL
run_migration.cmd
```

This will automatically:
1. Compile CREATE.DOMAIN.DIRS
2. Run CREATE.DOMAIN.DIRS (creates QM directory files)
3. Compile MIGRATE.REORGANIZE
4. Run MIGRATE.REORGANIZE (you'll need to type YES to confirm)

### Option 2: Run Manually in QM (Step-by-Step)

```
cd C:\QMSYS\HAL
qm
```

Then at QM prompt:

```
:LOGTO HAL
:BASIC ONCE.BP CREATE.DOMAIN.DIRS
:RUN ONCE.BP CREATE.DOMAIN.DIRS
:BASIC ONCE.BP MIGRATE.REORGANIZE
:RUN ONCE.BP MIGRATE.REORGANIZE
```

When prompted, type **YES** to confirm migration.

## 📋 What the Migration Does

1. **Creates QM directory files**: FIN.BP, MED.BP, SEC.BP, COM.BP, UTIL.BP
2. **Copies programs** from BP to domain directories
3. **Renames programs** with domain prefixes:
   - `IMPORT.QUICKEN` → `FIN.IMPORT.QUICKEN`
   - `PASSWORD.MENU` → `SEC.PASSWORD.MENU`
   - `IMPORT.EPIC` → `MED.IMPORT.EPIC`
   - etc.
4. **Leaves originals** in BP unchanged (safe!)
5. **Generates report**: MIGRATION.REPORT.txt

## 📊 After Migration

Review the report:
```
notepad C:\QMSYS\HAL\MIGRATION.REPORT.txt
```

Compile new programs:
```
:BASIC FIN.BP *
:BASIC MED.BP *
:BASIC SEC.BP *
:BASIC UTIL.BP *
```

Catalog new programs:
```
:CATALOG FIN.BP *
:CATALOG MED.BP *
:CATALOG SEC.BP *
:CATALOG UTIL.BP *
```

Test:
```
:FIN.IMPORT.QUICKEN
:SEC.PASSWORD.MENU
:MED.IMPORT.EPIC
```

## 🎉 Done!

Your code will be organized by domain with proper naming conventions!
