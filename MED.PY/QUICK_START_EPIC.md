# QUICK START GUIDE
## Getting Your Epic Medical Records Analyzed in 5 Minutes

**Author:** Dr. Lawrence C. Sullivan  
**Date:** October 2024

---

## Step 1: Download Your Data from MyChart (2 minutes)

1. Go to **mychartnyu.org**
2. Log in
3. Click **"Medical Records"** → **"Download"**
4. Choose **CCD/CDA format** (XML file)
5. Save file as `my_records.xml`

---

## Step 2: Setup (2 minutes)

```bash
# Install Python packages
pip install pandas numpy lxml matplotlib seaborn scipy

# Or use the requirements file
pip install -r requirements.txt
```

---

## Step 3: Parse Your Data (30 seconds)

```python
# For CCD/XML files:
from parse_ccd import CCDParser

parser = CCDParser('my_records.xml')

# View your data
demographics = parser.get_patient_demographics()
print(demographics)

medications = parser.get_medications()
for med in medications:
    print(f"{med['name']}: {med.get('dose', '')}")

# Export to CSV for Excel
dfs = parser.export_to_dataframes()
for name, df in dfs.items():
    df.to_csv(f'{name}.csv', index=False)

print("Done! Check the CSV files")
```

---

## Step 4: Analyze (Optional - 30 seconds)

```python
from analyze_medical_data import MedicalDataAnalyzer

# Load your parsed data
analyzer = MedicalDataAnalyzer(dfs)

# Analyze lab trends
lab_trends = analyzer.analyze_lab_trends(days_back=365)
for test, stats in list(lab_trends.items())[:5]:
    print(f"{test}: {stats['latest_value']} (trend: {stats['trend']})")

# Generate report
analyzer.export_summary_report('my_health_summary.txt')

# Plot labs
analyzer.plot_lab_trends(save_path='my_lab_trends.png')
```

---

## What You Get:

### CSV Files (for Excel):
- `demographics.csv` - Your personal info
- `medications.csv` - All medications
- `problems.csv` - Diagnoses/conditions
- `allergies.csv` - Allergies
- `labs.csv` - Lab results
- `vitals.csv` - Vital signs

### Analysis Outputs:
- `my_health_summary.txt` - Comprehensive text report
- `my_lab_trends.png` - Visual trends of lab values
- `medical_timeline.csv` - Timeline of all medical events

---

## Troubleshooting:

**"Module not found"**
```bash
pip install --break-system-packages pandas lxml
```

**"File not found"**
```python
# Make sure you're in the right directory
import os
print(os.getcwd())  # Shows current directory
os.chdir('/path/to/your/files')  # Change if needed
```

**"Cannot parse XML"**
```python
# Check if file is valid XML
with open('my_records.xml', 'r') as f:
    print(f.read(500))  # Print first 500 characters
```

---

## For FHIR JSON Files:

If you have FHIR JSON instead of CCD XML:

```python
from parse_fhir import FHIRParser

parser = FHIRParser('my_fhir_bundle.json')

# Everything else is the same!
dfs = parser.export_to_dataframes()
```

---

## Need Help?

1. Check **README.md** for detailed documentation
2. See example scripts in the files
3. Contact: lcsmd@nyu.edu

---

## Next Steps:

### For Research:
- See `analyze_medical_data.py` for advanced analytics
- Check out correlation analysis examples
- Time series forecasting of lab values

### For Clinical Use:
- Generate periodic health reports
- Track medication changes
- Monitor chronic condition trends

### For Bioinformatics:
- Connect to drug databases (ChEMBL, DrugBank)
- NLP on clinical notes with scispaCy
- ML models for risk prediction

---

**Remember:** Your medical data is protected health information (PHI). Keep it secure!

```bash
# Secure your files
chmod 600 *.xml *.json *.csv
```
