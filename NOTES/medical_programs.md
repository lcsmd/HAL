# Medical Data Management Programs

## Overview

Created comprehensive medical data management system with Epic integration, CRUD operations, and appointment reminders.

## Programs Created

### 1. MEDICAL.MENU
Main menu for medical data management system
- Access to all medical data modules
- Import/Export functionality
- User-friendly interface

### 2. MEDICATION.MENU
Complete medication management system
- **List**: View all or active medications
- **Add**: Create new medication records
- **Edit**: Update medication details
- **Discontinue**: Mark medications as discontinued
- **Delete**: Remove medication records
- **Search**: Find medications by name
- **Report**: Generate medication reports by person

### 3. IMPORT.EPIC
Epic MyChart data import utility
- **Formats supported**:
  - FHIR JSON (MedicationStatement, AllergyIntolerance, Immunization, Condition, Observation)
  - CSV exports
  - CCD-C XML (placeholder for future implementation)
- Auto-detects file format
- Routes to appropriate parser

### 4. APPOINTMENT.REMINDER
Automated appointment reminder system
- Checks upcoming appointments
- Generates reminder messages
- Marks reminders as sent
- Supports configurable reminder window
- **Integration points** (placeholders):
  - Email notifications
  - SMS notifications
  - Push notifications

### 5. epic_parser.py (Python)
Epic data parser with QMClient integration
- **FHIR JSON parsing**:
  - MedicationStatement → MEDICATION file
  - AllergyIntolerance → ALLERGY file
  - Immunization → IMMUNIZATION file
- Converts FHIR dates to QM internal format
- Direct QM database writes via QMClient
- Handles FHIR Bundles and individual resources

## Usage Examples

### Import Epic Data

**From QM:**
```
IMPORT.EPIC
```

**From Python (recommended for FHIR):**
```bash
python PY\epic_parser.py "path\to\epic_export.json" "PERSON_ID"
```

### Manage Medications

```
MEDICAL.MENU
# Select option 2 (Medications)
# Then choose desired operation
```

### Run Appointment Reminders

```
APPOINTMENT.REMINDER
# Enter days ahead (default 1)
```

### Schedule Daily Reminders

Create a Windows scheduled task:
```batch
cd C:\QMSYS\HAL
python PY\run_qm_program.py APPOINTMENT.REMINDER
```

## Data Flow

### Epic Import Flow
```
Epic MyChart Export (FHIR JSON)
    ↓
epic_parser.py
    ↓
Parse FHIR resources
    ↓
Convert to QM format
    ↓
QMClient.Write()
    ↓
QM Database (MEDICATION, ALLERGY, IMMUNIZATION, etc.)
```

### Appointment Reminder Flow
```
APPOINTMENT.REMINDER
    ↓
SELECT appointments for target date
    ↓
Read PERSON, DOCTOR details
    ↓
Format reminder message
    ↓
Mark reminder sent
    ↓
Send notification (email/SMS/push)
```

## File Structure

```
BP/
├── MEDICAL.MENU              - Main medical menu
├── MEDICATION.MENU           - Medication CRUD
├── IMPORT.EPIC               - Epic import (QMBasic)
└── APPOINTMENT.REMINDER      - Reminder system

PY/
└── epic_parser.py            - FHIR/CSV parser (Python)
```

## Next Steps

### Immediate
1. Create similar CRUD menus for other medical files:
   - ALLERGY.MENU
   - IMMUNIZATION.MENU
   - VITAL.SIGNS.MENU
   - MEDICAL.TEST.MENU
   - APPOINTMENT.MENU
   - DOCTOR.MENU
   - INSURANCE.MENU

2. Enhance epic_parser.py:
   - Add CSV parsing
   - Add CCD-C XML parsing
   - Support more FHIR resources (Condition, Observation, Procedure)
   - Batch import support

3. Implement notification systems:
   - Email integration (SMTP)
   - SMS integration (Twilio/AWS SNS)
   - Push notifications (Firebase/OneSignal)

### Future Enhancements
1. **Data Validation**:
   - Drug interaction checking
   - Allergy cross-checking before prescribing
   - Duplicate detection

2. **Reporting**:
   - Medication adherence reports
   - Immunization compliance
   - Vital signs trends
   - Appointment history

3. **Integration**:
   - HL7 message support
   - FHIR API server
   - Direct EHR integration
   - Pharmacy e-prescribing

4. **Analytics**:
   - Health trends analysis
   - Medication cost analysis
   - Provider performance metrics
   - Population health management

5. **Security**:
   - HIPAA compliance audit logging
   - Field-level encryption
   - Role-based access control
   - Data retention policies

## Epic Export Instructions

### From Epic MyChart:
1. Log into MyChart
2. Navigate to "Health Summary" or "Medical Records"
3. Select "Download" or "Export"
4. Choose format:
   - **FHIR JSON** (recommended) - Best for automated parsing
   - **CSV** - Good for manual review
   - **CCD-C XML** - Standard clinical document

### Supported Epic Exports:
- Medications list
- Allergies list
- Immunization records
- Problem list / Diagnoses
- Lab results
- Vital signs
- Appointment history

## Testing

### Test Data Import:
```python
# Create test FHIR file
python PY\epic_parser.py test_data\medications.json P001
```

### Test Medication Management:
```
# From QM
MEDICATION.MENU
# Add a test medication
# Edit it
# List active medications
```

### Test Reminders:
```
# Create future appointment first
APPOINTMENT.MENU
# Then run reminder
APPOINTMENT.REMINDER
```
