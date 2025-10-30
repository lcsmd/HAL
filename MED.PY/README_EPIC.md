# Epic Medical Records Parser & Analyzer
## For Bioinformatics Research

Comprehensive toolkit for parsing, analyzing, and visualizing medical records exported from Epic EHR systems (NYU Langone Health).

**Author:** Dr. Lawrence C. Sullivan, M.D.  
**Purpose:** Bioinformatics research and personal health data analysis

---

## Table of Contents
1. [Overview](#overview)
2. [Getting Your Data from Epic](#getting-your-data-from-epic)
3. [Installation](#installation)
4. [Data Formats](#data-formats)
5. [Usage Examples](#usage-examples)
6. [Advanced Analysis](#advanced-analysis)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This toolkit provides three main components:

1. **CCD/CDA XML Parser** (`parse_ccd.py`) - Parses Continuity of Care Documents
2. **FHIR JSON Parser** (`parse_fhir.py`) - Parses FHIR Bundle resources  
3. **Medical Data Analyzer** (`analyze_medical_data.py`) - Advanced analytics and visualization

### Features
- Extract patient demographics
- Parse medications, conditions, allergies
- Analyze lab results and vital signs
- Trend analysis with statistical testing
- Generate timelines and summary reports
- Export to CSV, JSON, and pandas DataFrames

---

## Getting Your Data from Epic

### Method 1: MyChart (Fastest)

1. Go to **mychartnyu.org**
2. Log in with your NYU credentials
3. Navigate to **"Medical Records"** or **"Health Summary"**
4. Click **"Download"** or **"Export"**
5. Select format:
   - **CCD/CDA** (XML format) - Most common
   - **Blue Button** format
   - **PDF** (human-readable but not ideal for analysis)

### Method 2: Formal Request (Best for Research)

For machine-readable FHIR format (recommended for bioinformatics):

1. **Contact NYU Langone Health Information Management:**
   - Phone: (212) 263-6485
   - Specify you want electronic records in **FHIR JSON format**
   
2. **Submit HIPAA Right of Access Request:**
   - Under 21st Century Cures Act, you have the right to data in electronic format
   - Request: "FHIR-formatted medical records (JSON)"
   - Free or nominal fee (max $6.50 per law)

3. **Alternative formats to request:**
   - HL7 CDA (XML)
   - CSV/Excel for structured data
   - Bulk FHIR export

### Method 3: API Access (Advanced)

If you're building research tools:
- Epic supports **SMART on FHIR** apps
- Can connect via Epic's **MyChart API**
- Requires app registration

---

## Installation

### 1. Install Python (if needed)
```bash
# Check if Python is installed
python3 --version

# If not installed, install Python 3.10+
# macOS (with Homebrew):
brew install python

# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install python3 python3-pip

# Windows: Download from python.org
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv medical_env

# Activate it
# macOS/Linux:
source medical_env/bin/activate

# Windows:
medical_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Data Formats

### CCD/CDA XML Format

**Structure:**
```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <recordTarget>
    <patientRole>
      <!-- Patient demographics -->
    </patientRole>
  </recordTarget>
  <component>
    <structuredBody>
      <component>
        <section>
          <!-- Medications, Problems, Labs, etc. -->
        </section>
      </component>
    </structuredBody>
  </component>
</ClinicalDocument>
```

**Sections typically included:**
- 10160-0: Medications
- 11450-4: Problem List
- 48765-2: Allergies
- 30954-2: Lab Results
- 8716-3: Vital Signs

### FHIR JSON Format

**Structure:**
```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        ...
      }
    },
    {
      "resource": {
        "resourceType": "Condition",
        ...
      }
    }
  ]
}
```

**Resource types:**
- Patient, Condition, Medication, Observation
- Procedure, AllergyIntolerance, Immunization
- DiagnosticReport, Encounter

---

## Usage Examples

### Basic Parsing - CCD/CDA XML

```python
from parse_ccd import CCDParser

# Load and parse CCD file
parser = CCDParser('my_medical_records.xml')

# Get patient demographics
demographics = parser.get_patient_demographics()
print(f"Patient: {demographics['first_name']} {demographics['last_name']}")
print(f"DOB: {demographics['birth_date']}")

# Get medications
medications = parser.get_medications()
print(f"\nCurrent Medications ({len(medications)}):")
for med in medications:
    print(f"  • {med['name']}: {med.get('dose', '')} {med.get('dose_unit', '')}")

# Get problems/diagnoses
problems = parser.get_problems()
print(f"\nActive Problems ({len(problems)}):")
for prob in problems:
    print(f"  • {prob['name']} (ICD: {prob['icd_code']})")

# Get lab results
labs = parser.get_lab_results()
print(f"\nRecent Lab Results ({len(labs)}):")
for lab in labs[:5]:  # Show first 5
    print(f"  • {lab['test_name']}: {lab['value']} {lab['unit']}")

# Export everything to CSV files
dfs = parser.export_to_dataframes()
for name, df in dfs.items():
    if not df.empty:
        df.to_csv(f'{name}.csv', index=False)
        print(f"Saved {name}.csv")

# Export to JSON
parser.export_to_json('my_medical_data.json')
```

### Basic Parsing - FHIR JSON

```python
from parse_fhir import FHIRParser

# Load and parse FHIR bundle
parser = FHIRParser('my_fhir_bundle.json')

# See what resources are available
summary = parser.get_resource_summary()
print("Available Resources:")
for resource_type, count in summary.items():
    print(f"  {resource_type}: {count}")

# Get patient information
demographics = parser.get_patient_demographics()
print(f"\nPatient ID: {demographics['patient_id']}")

# Get conditions
conditions = parser.get_conditions()
print(f"\nConditions ({len(conditions)}):")
for cond in conditions:
    print(f"  • {cond['name']}")
    print(f"    Status: {cond['clinical_status']}")
    print(f"    Code: {cond.get('icd_code', cond.get('snomed_code', 'N/A'))}")

# Get lab results
labs = parser.get_lab_results()
print(f"\nLab Results ({len(labs)}):")
for lab in labs[:5]:
    print(f"  • {lab['name']}: {lab['value']} {lab['unit']}")
    if 'interpretation' in lab:
        print(f"    Interpretation: {lab['interpretation']}")

# Export to pandas DataFrames
dfs = parser.export_to_dataframes()

# Access specific DataFrame
meds_df = dfs['medications']
print(f"\nMedication Statistics:")
print(meds_df['status'].value_counts())
```

### Advanced Analysis

```python
from parse_fhir import FHIRParser
from analyze_medical_data import MedicalDataAnalyzer

# Parse your data
parser = FHIRParser('my_fhir_bundle.json')
data_dfs = parser.export_to_dataframes()

# Create analyzer
analyzer = MedicalDataAnalyzer(data_dfs)

# Analyze lab trends
lab_trends = analyzer.analyze_lab_trends(days_back=365)
print("Lab Trends:")
for test, stats in list(lab_trends.items())[:5]:
    print(f"\n{test}:")
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Std Dev: {stats['std']:.2f}")
    print(f"  Latest: {stats['latest_value']:.2f}")
    print(f"  Trend: {stats['trend']}")

# Plot specific lab values over time
analyzer.plot_lab_trends(
    test_names=['Hemoglobin', 'Glucose', 'Creatinine'],
    save_path='my_lab_trends.png'
)

# Analyze medications
med_analysis = analyzer.analyze_medication_timeline()
print(f"\nMedication Summary:")
print(f"  Total: {med_analysis['total_medications']}")
print(f"  Unique: {med_analysis['unique_medications']}")
print(f"  Status: {med_analysis['status_breakdown']}")

# Identify comorbidities
comorbidity = analyzer.identify_comorbidities()
print(f"\nComorbidity Analysis:")
print(f"  Active conditions: {comorbidity['total_conditions']}")
print(f"  Chronic disease burden: {comorbidity['chronic_disease_burden']}")

# Generate comprehensive timeline
timeline = analyzer.generate_timeline(save_path='medical_timeline.csv')
print(f"\nGenerated timeline with {len(timeline)} events")

# Export summary report
analyzer.export_summary_report('medical_summary.txt')
```

### Working with DataFrames for Custom Analysis

```python
import pandas as pd
from parse_fhir import FHIRParser

parser = FHIRParser('my_fhir_bundle.json')
dfs = parser.export_to_dataframes()

# Access labs DataFrame
labs_df = dfs['labs']

# Filter for specific test
glucose_tests = labs_df[labs_df['name'].str.contains('Glucose', case=False, na=False)]

# Convert to numeric and analyze
glucose_tests['value_numeric'] = pd.to_numeric(glucose_tests['value'], errors='coerce')
glucose_tests['date'] = pd.to_datetime(glucose_tests['date'])

# Calculate statistics
print("Glucose Statistics:")
print(f"  Mean: {glucose_tests['value_numeric'].mean():.2f}")
print(f"  Std: {glucose_tests['value_numeric'].std():.2f}")
print(f"  Min: {glucose_tests['value_numeric'].min():.2f}")
print(f"  Max: {glucose_tests['value_numeric'].max():.2f}")

# Group by month
glucose_tests['month'] = glucose_tests['date'].dt.to_period('M')
monthly_avg = glucose_tests.groupby('month')['value_numeric'].mean()
print("\nMonthly Average:")
print(monthly_avg)

# Identify abnormal values (example threshold)
abnormal = glucose_tests[glucose_tests['value_numeric'] > 100]
print(f"\nAbnormal results: {len(abnormal)}")
```

---

## Advanced Analysis

### Time Series Analysis

```python
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load your parsed data
from parse_fhir import FHIRParser
parser = FHIRParser('my_fhir_bundle.json')
dfs = parser.export_to_dataframes()

labs_df = dfs['labs']

# Focus on a specific test
test_name = 'Hemoglobin A1c'
test_data = labs_df[labs_df['name'] == test_name].copy()

# Convert to numeric
test_data['value_numeric'] = pd.to_numeric(test_data['value'], errors='coerce')
test_data['date'] = pd.to_datetime(test_data['date'])
test_data = test_data.sort_values('date')

# Calculate rate of change
test_data['days_since_first'] = (test_data['date'] - test_data['date'].min()).dt.days
slope, intercept, r_value, p_value, std_err = stats.linregress(
    test_data['days_since_first'], 
    test_data['value_numeric']
)

print(f"Trend Analysis for {test_name}:")
print(f"  Slope: {slope:.4f} units/day")
print(f"  R²: {r_value**2:.4f}")
print(f"  P-value: {p_value:.4f}")

if p_value < 0.05:
    if slope > 0:
        print(f"  Significant increasing trend")
    else:
        print(f"  Significant decreasing trend")
else:
    print(f"  No significant trend")

# Plot with trend line
plt.figure(figsize=(10, 6))
plt.scatter(test_data['date'], test_data['value_numeric'], s=100, alpha=0.6)
plt.plot(test_data['date'], intercept + slope * test_data['days_since_first'], 
         'r--', linewidth=2, label=f'Trend (slope={slope:.4f})')
plt.xlabel('Date')
plt.ylabel(f'{test_name} Value')
plt.title(f'{test_name} Over Time')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(f'{test_name}_trend.png', dpi=300, bbox_inches='tight')
```

### Correlation Analysis

```python
import seaborn as sns

# Analyze correlations between different lab values
labs_pivot = labs_df.pivot_table(
    index='date',
    columns='name',
    values='value',
    aggfunc='first'
)

# Convert all to numeric
labs_numeric = labs_pivot.apply(pd.to_numeric, errors='coerce')

# Calculate correlations
correlations = labs_numeric.corr()

# Plot heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlations, annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Lab Value Correlations')
plt.tight_layout()
plt.savefig('lab_correlations.png', dpi=300)
```

### Medication Adherence Analysis

```python
# Analyze medication patterns
meds_df = dfs['medications']

# Convert dates
meds_df['start_date'] = pd.to_datetime(meds_df['start_date'], errors='coerce')

# Calculate time on medication
meds_df['days_on_med'] = (pd.Timestamp.now() - meds_df['start_date']).dt.days

# Group by medication class (would need drug database for real classification)
print("Medication Duration Analysis:")
duration_stats = meds_df.groupby('name')['days_on_med'].agg(['count', 'mean', 'max'])
print(duration_stats.sort_values('mean', ascending=False).head(10))
```

---

## Troubleshooting

### Common Issues

**1. XML Parsing Errors**
```python
# Problem: Namespace issues
# Solution: Check if your XML uses different namespaces
import xml.etree.ElementTree as ET

tree = ET.parse('your_file.xml')
root = tree.getroot()

# Print the namespace
print("Root tag:", root.tag)
# Should be: {urn:hl7-org:v3}ClinicalDocument

# If different, update the NS dict in parse_ccd.py
```

**2. Date Format Issues**
```python
# Problem: Dates not parsing correctly
# Solution: Epic uses YYYYMMDDHHMMSS format

# Debug date parsing
date_string = "20240115143000"
parsed = pd.to_datetime(date_string, format='%Y%m%d%H%M%S')
print(parsed)  # 2024-01-15 14:30:00
```

**3. Missing Data**
```python
# Problem: Expected sections not found
# Solution: Check what sections your CCD actually contains

from parse_ccd import CCDParser
import xml.etree.ElementTree as ET

tree = ET.parse('your_file.xml')
root = tree.getroot()

NS = {'cda': 'urn:hl7-org:v3'}

# Find all section codes
sections = root.findall('.//cda:section/cda:code', NS)
print("Available sections:")
for section in sections:
    print(f"  Code: {section.get('code')}, Name: {section.get('displayName')}")
```

**4. FHIR Version Differences**
```python
# Different FHIR versions (DSTU2, STU3, R4) have different structures
# Check your FHIR version

import json
with open('your_fhir_bundle.json') as f:
    data = json.load(f)

# Check meta tag
if 'meta' in data:
    print("FHIR Version:", data['meta'].get('versionId'))

# Or check fhirVersion
if 'fhirVersion' in data:
    print("FHIR Version:", data['fhirVersion'])
```

**5. Large Files**
```python
# Problem: Memory issues with large XML files
# Solution: Use incremental parsing

import xml.etree.ElementTree as ET

# Parse incrementally
context = ET.iterparse('large_file.xml', events=('start', 'end'))
context = iter(context)
event, root = next(context)

for event, elem in context:
    if event == 'end' and 'entry' in elem.tag:
        # Process each entry
        process_entry(elem)
        # Clear from memory
        elem.clear()
```

### Getting Help

1. **Check Epic's Documentation:**
   - https://fhir.epic.com/
   - MyChart API documentation

2. **HL7 FHIR Spec:**
   - https://www.hl7.org/fhir/

3. **Contact NYU Langone IT:**
   - For format-specific questions about your export

---

## Next Steps for Bioinformatics Research

### 1. Connect to External Databases

```python
# Example: Enrich with drug databases
# pip install biopython bioservices

from bioservices import ChEMBL

chembl = ChEMBL()

# Look up drug information
drug_name = "Metformin"
results = chembl.get_molecule(drug_name)
```

### 2. Natural Language Processing on Clinical Notes

```python
# If you have clinical notes in your export
# pip install spacy scispacy

import spacy
import scispacy

# Load biomedical NLP model
nlp = spacy.load("en_core_sci_sm")

# Process clinical text
doc = nlp("Patient presents with type 2 diabetes and hypertension")

# Extract entities
for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")
```

### 3. Machine Learning Applications

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Example: Predict medication adherence
# Feature engineering from your parsed data

# This is a simplified example
features = labs_df.pivot_table(
    index='patient_id',
    columns='test_name',
    values='value',
    aggfunc='mean'
)

# Add more features from medications, conditions, etc.
# Then train your model
```

### 4. Integration with R

```python
# Export to R-compatible format
import pandas as pd

# Save as RDS
dfs['labs'].to_csv('labs_for_r.csv', index=False)

# Or use rpy2 for direct R integration
# pip install rpy2
```

---

## Security & Privacy

**IMPORTANT REMINDERS:**

1. **Your medical data is PHI (Protected Health Information)**
   - Keep files secure
   - Don't share raw files
   - Use encryption for storage

2. **For research use:**
   - De-identify data if sharing
   - Follow IRB protocols if applicable
   - Check HIPAA compliance

3. **File permissions:**
```bash
# Make files readable only by you
chmod 600 *.xml *.json *.csv
```

---

## License & Disclaimer

This toolkit is for personal use and research purposes.

**Medical Disclaimer:** This software is for informational purposes only and should not be used for medical diagnosis or treatment decisions. Always consult with qualified healthcare professionals.

**Created by:** Dr. Lawrence C. Sullivan, M.D.  
**Contact:** lcsmd@nyu.edu

---

## Updates & Maintenance

### Version History
- **v1.0** (2024): Initial release with CCD/FHIR parsers
- **v1.1** (2024): Added advanced analytics
- **v1.2** (2025): Enhanced FHIR R4 support

### Future Enhancements
- [ ] SMART on FHIR integration
- [ ] Real-time Epic API connection
- [ ] ML models for risk prediction
- [ ] Interactive dashboard
- [ ] Multi-patient cohort analysis

---

For questions or issues, contact Dr. Sullivan at lcsmd@nyu.edu
