# Medical Schema Documentation

## Overview

The HAL system now includes comprehensive medical/healthcare data management with 7 new files that integrate with the existing PERSON file.

## Medical Files

### 1. MEDICAL_HISTORY (mhx)
Tracks medical conditions, diagnoses, and health history.
- Links to PERSON, DOCTOR, HEALTHCARE_FACILITY
- Supports ICD-10 codes
- Tracks condition status (active/resolved/chronic/managed)
- Stores treatment plans and prognosis
- Multivalued fields for complications and related conditions

### 2. MEDICATION (med)
Manages current and historical medications.
- Links to PERSON, DOCTOR (prescriber), PHARMACY
- Includes NDC codes for drug identification
- Tracks dosage, frequency, route of administration
- Monitors refills, side effects, and drug interactions
- Cost tracking with insurance coverage flag

### 3. ALLERGY (alg)
Records allergies and sensitivities.
- Links to PERSON and verifying DOCTOR
- Categorizes by allergen type (food/drug/environmental/insect/other)
- Severity levels (mild/moderate/severe/life-threatening)
- Tracks reactions, symptoms, and cross-reactions
- EpiPen requirement flag

### 4. DOCTOR (dtr)
Healthcare provider directory.
- Stores physician credentials (NPI, license, certifications)
- Specialty and sub-specialty tracking
- Practice information and contact details
- Insurance plans accepted
- Languages spoken (multivalued)

### 5. MEDICAL_TEST (tst)
Laboratory and diagnostic test results.
- Links to PERSON, ordering DOCTOR, FACILITY
- Supports CPT and LOINC codes
- Tracks test status, results, and reference ranges
- Abnormal and critical result flags
- Follow-up tracking
- Cost and insurance coverage

### 6. HEALTHCARE_FACILITY (hcf)
Healthcare facilities and locations.
- Hospitals, clinics, labs, imaging centers, pharmacies
- NPI identification
- Specialties offered (multivalued)
- Hours of operation, parking, accessibility
- Insurance plans accepted

### 7. APPOINTMENT (apt)
Medical appointment scheduling and tracking.
- Links to PERSON, DOCTOR, FACILITY
- Appointment date/time with duration
- Status tracking (scheduled/confirmed/completed/cancelled/no-show)
- Check-in/check-out times and wait time tracking
- Visit summary with diagnosis codes
- Prescriptions and tests ordered during visit
- Follow-up scheduling

## Data Relationships

```
PERSON (per)
  ├─→ MEDICAL_HISTORY (mhx)
  │     └─→ DOCTOR (dtr)
  │     └─→ HEALTHCARE_FACILITY (hcf)
  ├─→ MEDICATION (med)
  │     └─→ DOCTOR (dtr) [prescriber]
  │     └─→ MEDICAL_HISTORY (mhx) [condition]
  ├─→ ALLERGY (alg)
  │     └─→ DOCTOR (dtr) [verified by]
  ├─→ MEDICAL_TEST (tst)
  │     └─→ DOCTOR (dtr) [ordered by]
  │     └─→ HEALTHCARE_FACILITY (hcf)
  │     └─→ MEDICAL_HISTORY (mhx) [related condition]
  └─→ APPOINTMENT (apt)
        └─→ DOCTOR (dtr)
        └─→ HEALTHCARE_FACILITY (hcf)
        └─→ MEDICATION (med) [prescriptions]
        └─→ MEDICAL_TEST (tst) [tests ordered]
```

## Field Formatting

All medical files follow the intelligent formatting rules:
- **Date fields**: D4- conversion, 10R format (YYYY-MM-DD)
- **Currency fields** (COST, COPAY): MD2 conversion, 12R format
- **Y/N flags**: 1L format
- **Names**: 30L format
- **Status fields**: 12L format
- **Codes** (ICD, CPT, NDC, NPI): 15L format

## Usage Examples

### Query all active medications for a person
```
LIST MEDICATION WITH PERSON_ID = "P001" AND STATUS = "active"
```

### Find all appointments for a specific doctor
```
LIST APPOINTMENT WITH DOCTOR_ID = "D123" AND APPOINTMENT_DATE >= "2025-10-01"
```

### View medical history with conditions
```
LIST MEDICAL_HISTORY WITH PERSON_ID = "P001" AND STATUS = "active"
```

### Check for drug allergies before prescribing
```
LIST ALLERGY WITH PERSON_ID = "P001" AND ALLERGEN_TYPE = "drug"
```

## Privacy and Security Considerations

Medical data requires special handling:
1. **HIPAA Compliance**: Ensure proper access controls
2. **Encryption**: Consider encrypting sensitive fields
3. **Audit Logging**: Track all access to medical records
4. **Data Retention**: Follow regulatory requirements
5. **Patient Consent**: Track consent for data sharing

## Next Steps

1. Implement access control and audit logging
2. Create medical data entry programs
3. Build reporting and analytics queries
4. Integrate with external medical systems (HL7/FHIR)
5. Add medication interaction checking
6. Implement appointment reminder system
