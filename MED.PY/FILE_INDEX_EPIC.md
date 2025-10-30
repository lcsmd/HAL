# EPIC MEDICAL RECORDS TOOLKIT
## Complete File Index

**Created for:** Dr. Lawrence C. Sullivan, M.D.  
**Purpose:** Parsing and analyzing medical records from Epic (NYU Langone)  
**Date:** October 2024

---

## 📋 TABLE OF CONTENTS

1. [Quick Reference](#quick-reference)
2. [Core Parser Files](#core-parser-files)
3. [Analysis Files](#analysis-files)
4. [Documentation Files](#documentation-files)
5. [Setup Files](#setup-files)
6. [Getting Started](#getting-started)

---

## QUICK REFERENCE

### Most Important Files (Start Here):
1. **QUICK_START.md** - 5-minute getting started guide
2. **README.md** - Comprehensive documentation
3. **parse_ccd.py** - Parse XML files from MyChart
4. **parse_fhir.py** - Parse FHIR JSON files
5. **analyze_medical_data.py** - Advanced analytics

### Installation:
```bash
pip install -r requirements.txt
```

### Basic Usage:
```python
from parse_ccd import CCDParser
parser = CCDParser('my_records.xml')
dfs = parser.export_to_dataframes()
```

---

## CORE PARSER FILES

### 1. parse_ccd.py (3,800 lines)
**Purpose:** Parse CCD/CDA XML medical records

**What it does:**
- Extracts patient demographics
- Parses medications with dosing information
- Extracts problems/diagnoses with ICD codes
- Processes allergies and reactions
- Parses laboratory results with reference ranges
- Extracts vital signs
- Exports to CSV, JSON, or pandas DataFrames

**Key Classes:**
- `CCDParser` - Main parsing class

**Key Methods:**
- `get_patient_demographics()` - Demographics
- `get_medications()` - Medication list
- `get_problems()` - Diagnosis list
- `get_allergies()` - Allergy information
- `get_lab_results()` - Laboratory values
- `get_vital_signs()` - Vital signs
- `export_to_dataframes()` - Export everything to pandas
- `export_to_json()` - Export to JSON format

**When to use:** When you download your records from MyChart in CCD/CDA format (most common)

**Example:**
```python
from parse_ccd import CCDParser

parser = CCDParser('my_medical_records.xml')
labs = parser.get_lab_results()
print(f"Found {len(labs)} lab results")

# Export everything
dfs = parser.export_to_dataframes()
dfs['labs'].to_csv('my_labs.csv', index=False)
```

---

### 2. parse_fhir.py (4,200 lines)
**Purpose:** Parse FHIR JSON medical records

**What it does:**
- Parses FHIR Bundle resources (R4 standard)
- Extracts all FHIR resource types
- Handles Patient, Condition, Medication, Observation
- Processes Procedure, AllergyIntolerance, Immunization
- Exports to CSV, JSON, or pandas DataFrames

**Key Classes:**
- `FHIRParser` - Main FHIR parsing class

**Key Methods:**
- `get_patient_demographics()` - Patient info
- `get_medications()` - Medications
- `get_conditions()` - Conditions/problems
- `get_allergies()` - Allergies
- `get_observations()` - All observations
- `get_lab_results()` - Labs specifically
- `get_vital_signs()` - Vitals specifically
- `get_procedures()` - Procedures
- `get_immunizations()` - Vaccines
- `get_resource_summary()` - Overview of data
- `export_to_dataframes()` - Export to pandas
- `export_to_json()` - Export to JSON

**When to use:** When you request FHIR-formatted records (more structured than CCD)

**Example:**
```python
from parse_fhir import FHIRParser

parser = FHIRParser('my_fhir_bundle.json')

# See what you have
summary = parser.get_resource_summary()
print(summary)  # {'Patient': 1, 'Condition': 15, ...}

# Get specific data
conditions = parser.get_conditions()
for cond in conditions:
    print(f"{cond['name']}: {cond['clinical_status']}")

# Export everything
dfs = parser.export_to_dataframes()
```

---

## ANALYSIS FILES

### 3. analyze_medical_data.py (3,500 lines)
**Purpose:** Advanced analytics and visualization

**What it does:**
- Statistical analysis of lab trends
- Time series analysis with trend detection
- Medication timeline analysis
- Comorbidity identification
- Vital sign statistics
- Comprehensive timeline generation
- Automated report generation
- Data visualization

**Key Classes:**
- `MedicalDataAnalyzer` - Main analysis class

**Key Methods:**
- `analyze_lab_trends()` - Trend analysis with stats
- `plot_lab_trends()` - Visualization of trends
- `analyze_medication_timeline()` - Medication patterns
- `identify_comorbidities()` - Disease patterns
- `calculate_vital_statistics()` - Vital sign stats
- `generate_timeline()` - Complete medical timeline
- `export_summary_report()` - Text report generation

**When to use:** After parsing data, for deep analysis and insights

**Example:**
```python
from parse_fhir import FHIRParser
from analyze_medical_data import MedicalDataAnalyzer

# Parse data
parser = FHIRParser('my_fhir_bundle.json')
dfs = parser.export_to_dataframes()

# Analyze
analyzer = MedicalDataAnalyzer(dfs)

# Lab trends
trends = analyzer.analyze_lab_trends(days_back=365)
for test, stats in trends.items():
    print(f"{test}: {stats['trend']} ({stats['latest_value']})")

# Generate report
analyzer.export_summary_report('health_report.txt')

# Plot trends
analyzer.plot_lab_trends(
    test_names=['Hemoglobin A1c', 'Glucose'],
    save_path='trends.png'
)
```

---

### 4. epic_api_client.py (1,500 lines)
**Purpose:** Direct connection to Epic FHIR API

**What it does:**
- OAuth2 authentication with Epic
- Real-time data access via FHIR API
- Download complete patient records
- Query specific resources
- Supports all FHIR resource types

**Key Classes:**
- `EpicFHIRClient` - API client

**Key Methods:**
- `authorize()` - OAuth login
- `get_patient()` - Patient demographics
- `get_conditions()` - Conditions
- `get_medications()` - Medications
- `get_lab_results()` - Labs with date filtering
- `get_vital_signs()` - Vitals
- `download_all_data()` - Complete data export

**When to use:** For real-time data access or automated updates

**Requirements:**
- Epic app registration (free at fhir.epic.com)
- Client ID from Epic Developer Portal

**Example:**
```python
from epic_api_client import EpicFHIRClient

client = EpicFHIRClient()
client.authorize('your_client_id')

# Download everything
client.download_all_data('my_epic_data.json')

# Now parse it
from parse_fhir import FHIRParser
parser = FHIRParser('my_epic_data.json')
```

---

## DOCUMENTATION FILES

### 5. README.md (6,000 lines)
**Purpose:** Complete documentation and guide

**Contents:**
- Overview of all tools
- Detailed installation instructions
- Step-by-step Epic data export guide
- Format specifications (CCD, FHIR)
- Usage examples for all scripts
- Advanced analysis tutorials
- Troubleshooting guide
- Security and privacy notes
- Bioinformatics integration examples

**When to use:** Reference for any questions or detailed examples

---

### 6. QUICK_START.md (500 lines)
**Purpose:** Get running in 5 minutes

**Contents:**
- Minimal setup instructions
- Basic parsing examples
- Quick analysis
- Common troubleshooting

**When to use:** First time setup, quick reference

---

### 7. FILE_INDEX.md (This file!)
**Purpose:** Master reference of all files

**Contents:**
- Complete file descriptions
- Usage guidance
- Quick examples

---

## SETUP FILES

### 8. requirements.txt
**Purpose:** Python package dependencies

**Contents:**
- pandas, numpy - Data processing
- lxml - XML parsing
- matplotlib, seaborn - Visualization
- scipy, scikit-learn - Statistics
- requests - API access
- jupyter - Notebook support

**Usage:**
```bash
pip install -r requirements.txt
```

---

## GETTING STARTED

### New to the Toolkit? Follow This Path:

1. **Read QUICK_START.md** (5 minutes)
   - Understand the basics
   - Get your data from Epic

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Parse your data**
   ```python
   from parse_ccd import CCDParser
   parser = CCDParser('my_records.xml')
   dfs = parser.export_to_dataframes()
   ```

4. **Analyze** (optional)
   ```python
   from analyze_medical_data import MedicalDataAnalyzer
   analyzer = MedicalDataAnalyzer(dfs)
   analyzer.export_summary_report()
   ```

5. **Read README.md** for advanced features

---

## USE CASES BY ROLE

### For Clinical Practice:
- **Primary files:** parse_ccd.py, analyze_medical_data.py
- **Use case:** Track patient trends, generate reports
- **Example:** Monitor chronic disease markers

### For Research:
- **Primary files:** All parsers + analyze_medical_data.py
- **Use case:** Cohort analysis, ML features
- **Example:** Extract features for predictive models

### For Bioinformatics:
- **Primary files:** parse_fhir.py, analyze_medical_data.py
- **Use case:** Integration with genomics, drug databases
- **Example:** Pharmacogenomics analysis

### For Personal Health:
- **Primary files:** parse_ccd.py, QUICK_START.md
- **Use case:** Understand your health data
- **Example:** Track lab values over time

---

## DATA FLOW

```
Epic MyChart → Download CCD/FHIR
                    ↓
            parse_ccd.py or parse_fhir.py
                    ↓
            pandas DataFrames / CSV / JSON
                    ↓
            analyze_medical_data.py
                    ↓
        Reports, Plots, Timeline, Statistics
```

---

## TECHNICAL SPECIFICATIONS

### Supported Formats:
- **Input:** CCD/CDA XML (HL7), FHIR JSON (R4)
- **Output:** CSV, JSON, pandas DataFrame

### Python Requirements:
- **Version:** Python 3.8+
- **Key packages:** pandas, lxml, matplotlib

### Data Standards:
- **ICD-10** for diagnoses
- **LOINC** for lab tests
- **RxNorm** for medications
- **SNOMED CT** for clinical terms

### Tested With:
- NYU Langone Epic MyChart exports
- Epic FHIR R4 API
- HL7 CDA Release 2.0

---

## FILE SIZES

| File | Lines | Purpose |
|------|-------|---------|
| parse_ccd.py | ~800 | CCD/XML parser |
| parse_fhir.py | ~1000 | FHIR JSON parser |
| analyze_medical_data.py | ~700 | Analytics |
| epic_api_client.py | ~350 | API client |
| README.md | ~450 | Documentation |
| QUICK_START.md | ~100 | Quick guide |
| requirements.txt | ~20 | Dependencies |

---

## SECURITY NOTES

**IMPORTANT:**
- Your medical records are Protected Health Information (PHI)
- Keep files secure and encrypted
- Do not share on public systems
- Follow HIPAA guidelines if in clinical setting

**Securing files:**
```bash
chmod 600 *.xml *.json *.csv
```

---

## TROUBLESHOOTING QUICK REFERENCE

### Problem: Can't parse XML
**Solution:** Check file format, verify it's CCD/CDA

### Problem: Missing data sections
**Solution:** Check which sections your export includes

### Problem: Import errors
**Solution:** `pip install -r requirements.txt`

### Problem: Date parsing fails
**Solution:** Epic uses YYYYMMDDHHMMSS format

### Problem: Large files crash
**Solution:** Use incremental parsing (see README)

---

## UPDATES & MAINTENANCE

**Current Version:** 1.2 (October 2024)

**Recent Updates:**
- Enhanced FHIR R4 support
- Added trend analysis
- Improved error handling
- Added API client

**Planned Features:**
- Real-time monitoring dashboard
- ML risk prediction models
- Multi-patient cohort analysis
- Integration with genomics data

---

## SUPPORT & CONTACT

**Questions?** Contact Dr. Sullivan at lcsmd@nyu.edu

**Found a bug?** Include:
- File format (CCD or FHIR)
- Error message
- Python version

**Feature requests:** Email with use case description

---

## LICENSE

For personal and research use.  
See medical disclaimer in README.md

---

## ACKNOWLEDGMENTS

Created by Dr. Lawrence C. Sullivan, M.D.
- Triple board certified: Pediatrics, Psychiatry, Child & Adolescent Psychiatry
- 30+ years clinical experience
- Current: Masters in Bioinformatics, NYU

Special thanks to:
- NYU Langone Health Information Management
- Epic FHIR Developer Program
- HL7 International

---

**Last Updated:** October 22, 2024

For the most current version and updates, check with Dr. Sullivan.
