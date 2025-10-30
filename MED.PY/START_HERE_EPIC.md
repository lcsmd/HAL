# 🏥 START HERE - Epic Medical Records Toolkit
## Complete Guide for Dr. Lawrence C. Sullivan

**Created:** October 22, 2024  
**Purpose:** Download and analyze your medical records from NYU Langone Health

---

## 🎯 WHAT THIS TOOLKIT DOES

This toolkit allows you to:

1. **Download** your complete medical records from Epic (NYU)
2. **Parse** the data into analyzable formats (CSV, JSON, pandas)
3. **Analyze** trends, patterns, and insights
4. **Visualize** lab results, medications, and timelines
5. **Generate** comprehensive health reports

All using Python scripts designed specifically for bioinformatics research.

---

## 📦 WHAT YOU HAVE

### **11 Files Total:**

#### **🔧 Core Tools (Use These):**
1. **complete_example.py** ⭐ - ONE-CLICK SOLUTION - Run this first!
2. **parse_ccd.py** - Parse XML files from MyChart
3. **parse_fhir.py** - Parse FHIR JSON files  
4. **analyze_medical_data.py** - Advanced analytics
5. **epic_api_client.py** - Direct API connection

#### **📖 Documentation (Read These):**
6. **EPIC_API_GUIDE.md** ⭐ - Complete API setup guide
7. **API_QUICK_REFERENCE.md** ⭐ - One-page cheat sheet
8. **QUICK_START.md** - 5-minute getting started
9. **README.md** - Full documentation
10. **FILE_INDEX.md** - File descriptions

#### **⚙️ Setup:**
11. **requirements.txt** - Python packages

---

## 🚀 THREE WAYS TO GET YOUR DATA

### **METHOD 1: API ACCESS (BEST for automation)**
✅ Real-time data  
✅ Automated updates  
✅ Complete data access  
⏱️ Setup: 10 minutes  

**Steps:**
1. Read **EPIC_API_GUIDE.md** (detailed instructions)
2. Or read **API_QUICK_REFERENCE.md** (one-page version)
3. Register at https://fhir.epic.com/ (5 min)
4. Get Client ID
5. Run **complete_example.py** with your Client ID

```python
# Edit complete_example.py:
CLIENT_ID = "paste-your-client-id-here"

# Then run:
python complete_example.py
```

### **METHOD 2: MYCHART DOWNLOAD (FASTEST)**
✅ No registration  
✅ Works immediately  
⏱️ Setup: 2 minutes  

**Steps:**
1. Go to mychartnyu.org
2. Medical Records → Download
3. Choose CCD/CDA format (XML)
4. Save file

```python
from parse_ccd import CCDParser

parser = CCDParser('your_downloaded_file.xml')
dfs = parser.export_to_dataframes()

# Export to CSV
for name, df in dfs.items():
    df.to_csv(f'{name}.csv', index=False)
```

### **METHOD 3: FORMAL REQUEST (MOST COMPLETE)**
✅ FHIR format (best structure)  
✅ Complete historical data  
⏱️ Setup: 2-5 days  

**Steps:**
1. Call NYU Health Information Management: (212) 263-6485
2. Request "FHIR-formatted electronic medical records"
3. Cite 21st Century Cures Act (your right!)
4. Receive within 2-5 business days

```python
from parse_fhir import FHIRParser

parser = FHIRParser('your_fhir_file.json')
dfs = parser.export_to_dataframes()
```

---

## ⚡ QUICK START (Choose Your Path)

### **PATH A: I Want API Access (10 minutes)**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Register at Epic (follow EPIC_API_GUIDE.md)
#    - Go to https://fhir.epic.com/
#    - Create "Patient Standalone" app
#    - Get Client ID

# 3. Edit complete_example.py
#    - Paste your Client ID

# 4. Run
python complete_example.py
```

**Output:**
- All data in `my_medical_data/` folder
- CSV files for Excel
- Health summary report
- Lab trends visualization
- Medical timeline

---

### **PATH B: I Have a MyChart Download (5 minutes)**

```bash
# 1. Install dependencies
pip install pandas lxml matplotlib

# 2. Download from MyChart (mychartnyu.org)

# 3. Run parser
python -c "
from parse_ccd import CCDParser
parser = CCDParser('your_file.xml')
dfs = parser.export_to_dataframes()
for name, df in dfs.items():
    df.to_csv(f'{name}.csv', index=False)
print('Done! Check the CSV files')
"
```

---

### **PATH C: I'm Exploring First (2 minutes)**

```bash
# 1. Read documentation
cat QUICK_START.md          # Basic overview
cat EPIC_API_GUIDE.md       # API details
cat API_QUICK_REFERENCE.md  # One-page reference

# 2. Look at example code
cat complete_example.py     # Complete working example
cat parse_ccd.py           # CCD parser
cat parse_fhir.py          # FHIR parser
```

---

## 📊 WHAT YOU'LL GET

### **Raw Data:**
- `nyu_medical_data.json` - Complete FHIR bundle

### **Structured Data (CSV for Excel):**
- `demographics.csv` - Your personal information
- `medications.csv` - All medications (current & past)
- `conditions.csv` - Diagnoses with ICD codes
- `labs.csv` - Laboratory results with values & dates
- `vitals.csv` - Vital signs (BP, HR, temp, weight)
- `allergies.csv` - Allergies and reactions
- `procedures.csv` - Medical procedures
- `immunizations.csv` - Vaccine history

### **Analysis Reports:**
- `health_summary_report.txt` - Comprehensive text summary
- `lab_trends.png` - Visual chart of lab values over time
- `medical_timeline.csv` - Complete timeline of medical events

---

## 💻 SYSTEM REQUIREMENTS

### **Minimum:**
- Python 3.8+
- 4GB RAM
- 500MB disk space

### **Recommended:**
- Python 3.10+
- 8GB RAM
- 2GB disk space (for large datasets)

### **Installation:**
```bash
# Check Python version
python3 --version

# Install packages
pip install -r requirements.txt

# Or minimal install:
pip install pandas lxml matplotlib numpy
```

---

## 🎓 FOR YOUR BIOINFORMATICS WORK

### **Integration Possibilities:**

**Drug Databases:**
```python
# Connect to ChEMBL, DrugBank
from bioservices import ChEMBL
chembl = ChEMBL()
```

**NLP on Clinical Notes:**
```python
# Process with scispaCy
import spacy
nlp = spacy.load("en_core_sci_sm")
```

**Machine Learning:**
```python
# Feature extraction for ML models
from sklearn.ensemble import RandomForestClassifier
# Use parsed data as features
```

**Genomics Integration:**
```python
# Combine with genomic data
# Pharmacogenomics analysis
# Phenotype extraction
```

---

## 🔒 SECURITY & PRIVACY

**IMPORTANT:** Your medical data is Protected Health Information (PHI)

### **Best Practices:**

1. **Secure Storage:**
```bash
# Set restrictive permissions
chmod 600 *.json *.xml *.csv
chmod 700 *.py
```

2. **Encryption:**
```bash
# Encrypt sensitive files
openssl enc -aes-256-cbc -salt -in data.json -out data.json.enc
```

3. **Environment Variables:**
```bash
# Don't hardcode credentials
export EPIC_CLIENT_ID="your-client-id"
```

4. **Git Ignore:**
```bash
# Don't commit data to git
echo "*.json" >> .gitignore
echo "*.csv" >> .gitignore
echo "*.xml" >> .gitignore
```

---

## 📞 SUPPORT & RESOURCES

### **For This Toolkit:**
- **Questions:** lcsmd@nyu.edu
- **Phone:** 212-255-0712

### **Epic/API Issues:**
- **Developer Portal:** https://fhir.epic.com/
- **Community Forum:** https://fhir.epic.com/Community

### **NYU Langone:**
- **MyChart:** mychartnyu.org
- **MyChart Support:** (844) 698-6972
- **Health Info Mgmt:** (212) 263-6485

### **Technical Help:**
- **Python Issues:** Check README.md troubleshooting section
- **Data Format Questions:** See FILE_INDEX.md

---

## 🐛 COMMON ISSUES & SOLUTIONS

### **Issue: Module not found**
```bash
# Solution:
pip install -r requirements.txt
```

### **Issue: Can't parse file**
```bash
# Solution: Check file format
head -20 your_file.xml  # Should show XML structure
```

### **Issue: API authentication fails**
- Check Client ID is correct
- Verify redirect URI: `http://localhost:8000/callback`
- See EPIC_API_GUIDE.md troubleshooting section

### **Issue: No data in parsed output**
- Verify MyChart download completed
- Check file isn't empty
- Try re-downloading from MyChart

---

## 📚 RECOMMENDED READING ORDER

### **If you're new:**
1. ⭐ **START_HERE.md** (this file) - Overview
2. ⭐ **QUICK_START.md** - Basic usage
3. **README.md** - Full documentation

### **For API access:**
1. ⭐ **API_QUICK_REFERENCE.md** - One-page guide
2. ⭐ **EPIC_API_GUIDE.md** - Complete setup
3. **complete_example.py** - Working code

### **For analysis:**
1. **README.md** - Analysis examples
2. **analyze_medical_data.py** - Advanced features
3. **FILE_INDEX.md** - Reference

---

## 🎯 YOUR ACTION PLAN

### **Option 1: Get Started in 5 Minutes (MyChart)**
```
☐ Go to mychartnyu.org
☐ Download CCD/XML file
☐ Run: pip install pandas lxml
☐ Run: python parse_ccd.py your_file.xml
☐ Check CSV files in Excel
```

### **Option 2: Set Up API (10 Minutes)**
```
☐ Read API_QUICK_REFERENCE.md
☐ Register at https://fhir.epic.com/
☐ Create patient app
☐ Get Client ID
☐ Edit complete_example.py
☐ Run: python complete_example.py
```

### **Option 3: Request FHIR Data (Best Quality)**
```
☐ Call (212) 263-6485
☐ Request FHIR format
☐ Wait 2-5 days
☐ Run: python parse_fhir.py your_file.json
☐ Advanced analysis with all tools
```

---

## 🌟 QUICK WINS

### **Want to see your lab trends?**
```python
from parse_ccd import CCDParser
from analyze_medical_data import MedicalDataAnalyzer

parser = CCDParser('your_file.xml')
dfs = parser.export_to_dataframes()

analyzer = MedicalDataAnalyzer(dfs)
analyzer.plot_lab_trends(save_path='my_trends.png')
```

### **Want a health summary?**
```python
analyzer.export_summary_report('summary.txt')
# Open summary.txt to read
```

### **Want to find a specific medication?**
```python
meds = dfs['medications']
metformin = meds[meds['name'].str.contains('Metformin', case=False)]
print(metformin)
```

### **Want to track A1C over time?**
```python
labs = dfs['labs']
a1c = labs[labs['test_name'].str.contains('A1c', case=False)]
print(a1c[['date', 'value', 'unit']])
```

---

## ✅ SUCCESS CHECKLIST

After setup, you should be able to:

```
☐ Parse your medical records
☐ Export to CSV files
☐ View data in Excel
☐ Generate health summary report
☐ Create lab trend visualizations
☐ Track medications over time
☐ Identify active conditions
☐ See medical timeline
```

---

## 🚀 NEXT LEVEL

Once comfortable with basics:

1. **Automate downloads:** Schedule daily API pulls
2. **Build dashboards:** Real-time health monitoring
3. **ML models:** Predictive analytics on your data
4. **Research integration:** Connect to bioinformatics pipelines
5. **Cohort analysis:** Compare with population data

See README.md "Advanced Analysis" section for examples.

---

## 📝 REMEMBER

- ⭐ **complete_example.py** - Easiest way to get everything
- ⭐ **EPIC_API_GUIDE.md** - Complete API setup
- ⭐ **API_QUICK_REFERENCE.md** - One-page cheat sheet
- Your medical data is PHI - keep it secure!
- This is YOUR data - you have the right to access it

---

## 💡 PRO TIPS

1. **Run complete_example.py first** - It does everything automatically
2. **Save your Client ID** - You'll use it repeatedly
3. **Export to CSV** - Easier to explore in Excel first
4. **Read the summary report** - Good overview of your health
5. **Check lab trends plot** - Visual insights are powerful

---

## 🎉 YOU'RE READY!

Choose your path:
- **Fast:** Download from MyChart (2 min)
- **Best:** API setup (10 min)  
- **Complete:** Request FHIR (2-5 days)

Then run the appropriate parser and start analyzing your health data!

**Questions?** Email lcsmd@nyu.edu

---

**Created for:** Dr. Lawrence C. Sullivan, M.D.  
**NYS License:** 193973  
**Contact:** lcsmd@nyu.edu | 212-255-0712  
**Date:** October 22, 2024

---

## 🔗 QUICK LINKS

- Epic Developer: https://fhir.epic.com/
- NYU MyChart: https://mychartnyu.org/
- NYU Health Records: (212) 263-6485
- MyChart Support: (844) 698-6972

---

**Remember:** This toolkit respects your privacy and security. All processing is done locally on your computer. No data is sent anywhere except to Epic (when using API).

**Good luck with your bioinformatics research!** 🔬
