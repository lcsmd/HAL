#!/usr/bin/env python3
"""
Create DATA_FILTER file and schema for data quality rules
"""
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

print("Creating DATA_FILTER schema...")

# Add to FILES
files_fno = qm.Open("FILES")
rec = "dft\xfedata_filter\xfesys\xfe\xfe\xfeauto\xfe\xfe0"
qm.Write(files_fno, "data_filter", rec)
print("  Added to FILES")

# Add fields to DOM_FILE_FIELD
dff_fno = qm.Open("DOM_FILE_FIELD")

def add_field(fieldname, m_s="s", assoc="", index="", required="n"):
    key = f"sys:data_filter:{fieldname}"
    rec = f"{m_s}\xfe{assoc}\xfe{index}\xfe{required}"
    qm.Write(dff_fno, key, rec)

add_field("name", "s", "", "x", "y")
add_field("file_type", "s", "", "x", "y")
add_field("filter_type", "s", "", "x", "y")
add_field("criteria", "s", "", "", "y")
add_field("action", "s", "", "x", "y")
add_field("priority", "s", "", "x", "n")
add_field("active", "s", "", "x", "y")
add_field("description", "s", "", "", "n")
add_field("created_date", "s", "", "x", "y")

print("  Added 9 fields")

# Add some common field types for filters
fields_fno = qm.Open("FIELDS")

# action (filter action)
rec = "Action\xfe\xfe12L"
qm.Write(fields_fno, "action", rec)

# filter_type
rec = "Filter Type\xfe\xfe15L"
qm.Write(fields_fno, "filter_type", rec)

# criteria
rec = "Criteria\xfe\xfe50L"
qm.Write(fields_fno, "criteria", rec)

print("  Added field types")

print("\nCreating sample filter rules...")

# Create the file
result = qm.Execute("CREATE.FILE DATA_FILTER DYNAMIC")
print(result[0])

# Build dictionary
result = qm.Execute("BUILD.DICT DATA_FILTER")
print(result[0])

# Add sample filter rules
filter_fno = qm.Open("DATA_FILTER")

# Rule 1: Skip emails older than 1 year
rec = "Skip old emails\xfeemail\xfeage\xfedays:365\xfeSKIP\xfe10\xfeY\xfeRemove emails older than 1 year\xfe2025-10-23"
qm.Write(filter_fno, "FILTER001", rec)
print("  Added: Skip old emails")

# Rule 2: Dedupe persons by email
rec = "Dedupe by email\xfeperson\xfeduplicate\xfeemail\xfeMERGE\xfe20\xfeY\xfeMerge duplicate persons with same email\xfe2025-10-23"
qm.Write(filter_fno, "FILTER002", rec)
print("  Added: Dedupe persons by email")

# Rule 3: Validate email format
rec = "Validate email format\xfeperson\xfeinvalid\xfeemail_format\xfeSKIP\xfe30\xfeY\xfeSkip persons with invalid email\xfe2025-10-23"
qm.Write(filter_fno, "FILTER003", rec)
print("  Added: Validate email format")

# Rule 4: Required fields for person
rec = "Required person fields\xfeperson\xferequired\xfe1,2\xfeSKIP\xfe5\xfeY\xfeRequire first and last name\xfe2025-10-23"
qm.Write(filter_fno, "FILTER004", rec)
print("  Added: Required person fields")

print("\n" + "="*60)
print("DATA_FILTER system ready!")
print("="*60)

# Show the filters
result = qm.Execute("LIST DATA_FILTER NAME FILE_TYPE FILTER_TYPE ACTION ACTIVE")
print(result[0])

qm.Disconnect()
print("\nDone!")
