# HAL System  OpenQM Assistant Project

## Current Phase
**Phase 2: Schema + EQU Foundation**

The OpenQM-based HAL Assistant is now transitioning from initialization to a schema-driven architecture.  
All data structures, files, and fields are defined via a single CSV source of truth:  
`C:\QMSYS\HAL\SCHEMA\schema.csv`

### Workflow Overview

1. **Schema Definition**
   - Add or modify entries in `SCHEMA\schema.csv`.
   - Each line defines one data file: its abbreviation, type, and field list.
   - Mark fields for secondary indexing with "Y" in the Indexed column.

2. **Build Phase**
   - Run program `BUILD.SCHEMA` in QM:
     ```
     > BASIC BP BUILD.SCHEMA
     > CATALOG BP BUILD.SCHEMA
     > BUILD.SCHEMA
     ```
   - This creates:
     - Dynamic/DIR files under the HAL account
     - Matching DICT entries for all fields
     - Sets DICT field 6 to S (single-valued) or M (multivalued) based on Type
     - Sets DICT field 8 to "X" for fields marked for indexing
     - EQU include files in `EQU\`
     - Updates `EQU\FILES.equ` master include

3. **Index Build Phase** (Optional, for performance)
   - Build secondary indexes for marked fields:
     ```
     > BUILD.INDEX <filename> ALL
     > BUILD.INDEX <filename> <fieldname>
     ```
   - Only build indexes when performance testing indicates benefit
   - Field 8 of DICT entries marked with "X" indicates index candidates

4. **Sync Phase**
   - Program `SYNC.SCHEMA` (pending) will reconcile schema changes and archive deletions to:
     `SCHEMA\schema_archive.csv`

4. **Runtime Access**
   - `OPEN.FILES` (to be implemented) opens all defined files into a `COMMON FILES()` block.
   - Each EQU file defines field-level equates, e.g.:
     ```
     EQU per.name TO per.r<NAME>
     EQU per.birthdate TO per.r<BIRTHDATE>
     ```

5. **Dependency Rule**
   > No data file may be referenced, populated, or queried until:
   > - It exists in `schema.csv`
   > - Its file and dictionary are built via `BUILD.SCHEMA`
   > - Its `.equ` file exists in the `EQU` directory

---

## Recent Progress
-  Created `SCHEMA`, `BP`, and `EQU` directories.
-  ✅ **BUILD.SCHEMA program completed and tested successfully!**
-  ✅ **BUILD.INDEX program created and compiled successfully!**
-  Fixed DELETE syntax errors (changed to OSDELETE for sequential files).
-  Fixed D-type dictionary structure (field 3=conversion, field 4=description).
-  Added secondary index support via DICT field 8 (set to "X" for indexed fields).
-  Compiled with 0 errors and executed successfully.
-  Generated all 18 EQU files with field-level equates.
-  Created master `FILES.EQU` with all $INCLUDE statements.
-  All data files and dictionaries created as DYNAMIC type.
-  All DICT entries created with correct D-type structure per OpenQM spec.
-  BUILD.INDEX supports building all indexes or specific fields.
-  Established source-of-truth model for schema definitions.
-  Defined rules for OpenQM integration, EQU conventions, and `COMMON FILES()` usage.
-  HAL Agent service now runs as Windows service (`HALAgent`).

---

## Next Steps
- [x] ~~Fix remaining syntax issues in `BUILD.SCHEMA`~~ ✅ **COMPLETED**
- [x] ~~Add proper CSV parser (`READSEQ` loop)~~ ✅ **COMPLETED**
- [x] ~~Auto-create `FILES.EQU` and test inclusion~~ ✅ **COMPLETED**
- [ ] Write `OPEN.FILES` program for dynamic file linking
- [ ] Implement `SYNC.SCHEMA` for schema change management
- [ ] Test schema propagation (DICT + EQU consistency)
- [ ] Create sample programs using the EQU includes
- [ ] Document usage patterns for developers

