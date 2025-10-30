#!/usr/bin/env python3
"""
Create comprehensive schema for HAL system
Includes traditional data files and AI infrastructure
"""
import sys
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

def add_file(files_fno, name, abb, domain):
    """Add file definition"""
    rec = f"{abb}\xfe{name}\xfe{domain}\xfe\xfe\xfeauto\xfe\xfe0"
    qm.Write(files_fno, name, rec)
    print(f"  Added file: {name}")

def add_field(dff_fno, domain, filename, fieldname, m_s="s", assoc="", index="", required="n"):
    """Add field definition to DOM_FILE_FIELD"""
    key = f"{domain}:{filename}:{fieldname}"
    rec = f"{m_s}\xfe{assoc}\xfe{index}\xfe{required}"
    qm.Write(dff_fno, key, rec)

print("Connecting to QM...")
qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')

# Open files
files_fno = qm.Open("FILES")
dff_fno = qm.Open("DOM_FILE_FIELD")

print("\nCreating comprehensive HAL schema...")
print("="*60)

# ============================================
# PERSONAL DOMAIN (per)
# ============================================
print("\nPERSONAL DOMAIN (per)")
print("-"*60)

add_file(files_fno, "person", "per", "per")
add_field(dff_fno, "per", "person", "name_first", "s", "", "x", "y")
add_field(dff_fno, "per", "person", "name_last", "s", "", "x", "y")
add_field(dff_fno, "per", "person", "name_middle", "s", "", "", "n")
add_field(dff_fno, "per", "person", "phone_mobile", "s", "", "x", "n")
add_field(dff_fno, "per", "person", "phone_home", "s", "", "", "n")
add_field(dff_fno, "per", "person", "eadd", "s", "", "x", "n")
add_field(dff_fno, "per", "person", "address_street", "s", "", "", "n")
add_field(dff_fno, "per", "person", "city", "s", "", "x", "n")
add_field(dff_fno, "per", "person", "state", "s", "", "x", "n")
add_field(dff_fno, "per", "person", "zip", "s", "", "", "n")
add_field(dff_fno, "per", "person", "country", "s", "", "", "n")
add_field(dff_fno, "per", "person", "date", "s", "", "", "n")
add_field(dff_fno, "per", "person", "notes", "s", "", "", "n")
add_field(dff_fno, "per", "person", "tags", "m", "", "x", "n")
add_field(dff_fno, "per", "person", "active", "s", "", "x", "y")
add_field(dff_fno, "per", "person", "created_date", "s", "", "x", "y")
add_field(dff_fno, "per", "person", "updated_date", "s", "", "", "y")
print("  17 fields added")

# ============================================
# COMMUNICATION DOMAIN (com)
# ============================================
print("\nCOMMUNICATION DOMAIN (com)")
print("-"*60)

add_file(files_fno, "contact", "con", "com")
add_field(dff_fno, "com", "contact", "person_id", "s", "", "x", "y")
add_field(dff_fno, "com", "contact", "company_id", "s", "", "x", "n")
add_field(dff_fno, "com", "contact", "category", "s", "", "x", "n")
add_field(dff_fno, "com", "contact", "priority", "s", "", "x", "n")
add_field(dff_fno, "com", "contact", "notes", "s", "", "", "n")
add_field(dff_fno, "com", "contact", "tags", "m", "", "x", "n")
add_field(dff_fno, "com", "contact", "active", "s", "", "x", "y")
add_field(dff_fno, "com", "contact", "created_date", "s", "", "x", "y")
print("  8 fields added")

add_file(files_fno, "message", "msg", "com")
add_field(dff_fno, "com", "message", "person_id", "s", "", "x", "y")
add_field(dff_fno, "com", "message", "phone", "s", "", "x", "n")
add_field(dff_fno, "com", "message", "type", "s", "", "x", "y")
add_field(dff_fno, "com", "message", "direction", "s", "", "x", "y")
add_field(dff_fno, "com", "message", "subject", "s", "", "x", "n")
add_field(dff_fno, "com", "message", "body", "s", "", "", "y")
add_field(dff_fno, "com", "message", "date_sent", "s", "", "x", "y")
add_field(dff_fno, "com", "message", "status", "s", "", "x", "y")
add_field(dff_fno, "com", "message", "tags", "m", "", "x", "n")
print("  9 fields added")

# ============================================
# MEDICAL DOMAIN (med)
# ============================================
print("\nMEDICAL DOMAIN (med)")
print("-"*60)

add_file(files_fno, "medical_record", "mrc", "med")
add_field(dff_fno, "med", "medical_record", "person_id", "s", "", "x", "y")
add_field(dff_fno, "med", "medical_record", "date", "s", "", "x", "y")
add_field(dff_fno, "med", "medical_record", "type", "s", "", "x", "y")
add_field(dff_fno, "med", "medical_record", "title", "s", "", "x", "y")
add_field(dff_fno, "med", "medical_record", "description", "s", "", "", "n")
add_field(dff_fno, "med", "medical_record", "notes", "s", "", "", "n")
add_field(dff_fno, "med", "medical_record", "external_id", "s", "", "x", "n")
add_field(dff_fno, "med", "medical_record", "tags", "m", "", "x", "n")
add_field(dff_fno, "med", "medical_record", "created_date", "s", "", "x", "y")
print("  9 fields added")

# ============================================
# WORK DOMAIN (wor)
# ============================================
print("\nWORK DOMAIN (wor)")
print("-"*60)

add_file(files_fno, "project", "prj", "wor")
add_field(dff_fno, "wor", "project", "name", "s", "", "x", "y")
add_field(dff_fno, "wor", "project", "description", "s", "", "", "n")
add_field(dff_fno, "wor", "project", "status", "s", "", "x", "y")
add_field(dff_fno, "wor", "project", "priority", "s", "", "x", "n")
add_field(dff_fno, "wor", "project", "date_start", "s", "", "x", "n")
add_field(dff_fno, "wor", "project", "date_end", "s", "", "x", "n")
add_field(dff_fno, "wor", "project", "person_id", "s", "", "x", "n")
add_field(dff_fno, "wor", "project", "company_id", "s", "", "x", "n")
add_field(dff_fno, "wor", "project", "tags", "m", "", "x", "n")
add_field(dff_fno, "wor", "project", "active", "s", "", "x", "y")
add_field(dff_fno, "wor", "project", "created_date", "s", "", "x", "y")
print("  11 fields added")

add_file(files_fno, "task", "tsk", "wor")
add_field(dff_fno, "wor", "task", "title", "s", "", "x", "y")
add_field(dff_fno, "wor", "task", "description", "s", "", "", "n")
add_field(dff_fno, "wor", "task", "project_id", "s", "", "x", "n")
add_field(dff_fno, "wor", "task", "status", "s", "", "x", "y")
add_field(dff_fno, "wor", "task", "priority", "s", "", "x", "n")
add_field(dff_fno, "wor", "task", "date_due", "s", "", "x", "n")
add_field(dff_fno, "wor", "task", "date_completed", "s", "", "x", "n")
add_field(dff_fno, "wor", "task", "person_id", "s", "", "x", "n")
add_field(dff_fno, "wor", "task", "tags", "m", "", "x", "n")
add_field(dff_fno, "wor", "task", "created_date", "s", "", "x", "y")
print("  10 fields added")

# ============================================
# AI INFRASTRUCTURE DOMAIN (sys)
# ============================================
print("\nAI INFRASTRUCTURE DOMAIN (sys)")
print("-"*60)

add_file(files_fno, "prompt_template", "ptp", "sys")
add_field(dff_fno, "sys", "prompt_template", "name", "s", "", "x", "y")
add_field(dff_fno, "sys", "prompt_template", "description", "s", "", "", "n")
add_field(dff_fno, "sys", "prompt_template", "category", "s", "", "x", "y")
add_field(dff_fno, "sys", "prompt_template", "template_text", "s", "", "", "y")
add_field(dff_fno, "sys", "prompt_template", "parameters", "m", "", "", "n")
add_field(dff_fno, "sys", "prompt_template", "system_role", "s", "", "", "n")
add_field(dff_fno, "sys", "prompt_template", "temperature", "s", "", "", "n")
add_field(dff_fno, "sys", "prompt_template", "max_tokens", "s", "", "", "n")
add_field(dff_fno, "sys", "prompt_template", "tags", "m", "", "x", "n")
add_field(dff_fno, "sys", "prompt_template", "active", "s", "", "x", "y")
add_field(dff_fno, "sys", "prompt_template", "created_date", "s", "", "x", "y")
add_field(dff_fno, "sys", "prompt_template", "updated_date", "s", "", "", "y")
print("  12 fields added")

add_file(files_fno, "persona", "prs", "sys")
add_field(dff_fno, "sys", "persona", "name", "s", "", "x", "y")
add_field(dff_fno, "sys", "persona", "description", "s", "", "", "n")
add_field(dff_fno, "sys", "persona", "personality", "s", "", "", "y")
add_field(dff_fno, "sys", "persona", "voice_id", "s", "", "x", "n")
add_field(dff_fno, "sys", "persona", "tone", "s", "", "x", "n")
add_field(dff_fno, "sys", "persona", "expertise", "m", "", "x", "n")
add_field(dff_fno, "sys", "persona", "system_prompt", "s", "", "", "y")
add_field(dff_fno, "sys", "persona", "temperature", "s", "", "", "n")
add_field(dff_fno, "sys", "persona", "tags", "m", "", "x", "n")
add_field(dff_fno, "sys", "persona", "active", "s", "", "x", "y")
add_field(dff_fno, "sys", "persona", "created_date", "s", "", "x", "y")
print("  11 fields added")

add_file(files_fno, "voice", "voi", "sys")
add_field(dff_fno, "sys", "voice", "name", "s", "", "x", "y")
add_field(dff_fno, "sys", "voice", "description", "s", "", "", "n")
add_field(dff_fno, "sys", "voice", "provider", "s", "", "x", "y")
add_field(dff_fno, "sys", "voice", "voice_id", "s", "", "x", "y")
add_field(dff_fno, "sys", "voice", "language", "s", "", "x", "y")
add_field(dff_fno, "sys", "voice", "gender", "s", "", "x", "n")
add_field(dff_fno, "sys", "voice", "accent", "s", "", "x", "n")
add_field(dff_fno, "sys", "voice", "sample_url", "s", "", "", "n")
add_field(dff_fno, "sys", "voice", "tags", "m", "", "x", "n")
add_field(dff_fno, "sys", "voice", "active", "s", "", "x", "y")
print("  10 fields added")

add_file(files_fno, "wake_word", "wak", "sys")
add_field(dff_fno, "sys", "wake_word", "word", "s", "", "x", "y")
add_field(dff_fno, "sys", "wake_word", "persona_id", "s", "", "x", "n")
add_field(dff_fno, "sys", "wake_word", "action", "s", "", "x", "y")
add_field(dff_fno, "sys", "wake_word", "priority", "s", "", "x", "n")
add_field(dff_fno, "sys", "wake_word", "active", "s", "", "x", "y")
add_field(dff_fno, "sys", "wake_word", "created_date", "s", "", "x", "y")
print("  6 fields added")

add_file(files_fno, "mood", "mod", "sys")
add_field(dff_fno, "sys", "mood", "name", "s", "", "x", "y")
add_field(dff_fno, "sys", "mood", "description", "s", "", "", "n")
add_field(dff_fno, "sys", "mood", "temperature", "s", "", "", "y")
add_field(dff_fno, "sys", "mood", "tone_modifiers", "m", "", "", "n")
add_field(dff_fno, "sys", "mood", "response_style", "s", "", "", "y")
add_field(dff_fno, "sys", "mood", "active", "s", "", "x", "y")
print("  6 fields added")

add_file(files_fno, "conversation", "cvs", "sys")
add_field(dff_fno, "sys", "conversation", "persona_id", "s", "", "x", "n")
add_field(dff_fno, "sys", "conversation", "mood_id", "s", "", "x", "n")
add_field(dff_fno, "sys", "conversation", "title", "s", "", "x", "n")
add_field(dff_fno, "sys", "conversation", "context", "s", "", "", "n")
add_field(dff_fno, "sys", "conversation", "date_start", "s", "", "x", "y")
add_field(dff_fno, "sys", "conversation", "date_end", "s", "", "x", "n")
add_field(dff_fno, "sys", "conversation", "message_count", "s", "", "", "n")
add_field(dff_fno, "sys", "conversation", "tags", "m", "", "x", "n")
print("  8 fields added")

add_file(files_fno, "conversation_message", "cvm", "sys")
add_field(dff_fno, "sys", "conversation_message", "conversation_id", "s", "", "x", "y")
add_field(dff_fno, "sys", "conversation_message", "role", "s", "", "x", "y")
add_field(dff_fno, "sys", "conversation_message", "content", "s", "", "", "y")
add_field(dff_fno, "sys", "conversation_message", "prompt_template_id", "s", "", "x", "n")
add_field(dff_fno, "sys", "conversation_message", "date", "s", "", "x", "y")
add_field(dff_fno, "sys", "conversation_message", "tokens", "s", "", "", "n")
print("  6 fields added")

add_file(files_fno, "memory", "mem", "sys")
add_field(dff_fno, "sys", "memory", "type", "s", "", "x", "y")
add_field(dff_fno, "sys", "memory", "content", "s", "", "", "y")
add_field(dff_fno, "sys", "memory", "context", "s", "", "", "n")
add_field(dff_fno, "sys", "memory", "person_id", "s", "", "x", "n")
add_field(dff_fno, "sys", "memory", "date", "s", "", "x", "y")
add_field(dff_fno, "sys", "memory", "importance", "s", "", "x", "n")
add_field(dff_fno, "sys", "memory", "tags", "m", "", "x", "n")
add_field(dff_fno, "sys", "memory", "active", "s", "", "x", "y")
print("  8 fields added")

print("\n" + "="*60)
print("Schema creation complete!")
print("="*60)

# Verify
result = qm.Execute("COUNT FILES")
print(f"\nFILES: {result[0]}")

result = qm.Execute("COUNT DOM_FILE_FIELD")
print(f"DOM_FILE_FIELD: {result[0]}")

qm.Disconnect()
print("\nDone!")
