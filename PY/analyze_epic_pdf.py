#!/usr/bin/env python3
"""
Analyze Epic PDF export to determine data extraction feasibility
"""
import sys
import os

try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False
    print("PyPDF2 not installed. Install with: pip install PyPDF2")

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
    print("pdfplumber not installed. Install with: pip install pdfplumber")

def analyze_with_pypdf2(pdf_path):
    """Analyze PDF using PyPDF2"""
    print("\n" + "="*60)
    print("Analysis with PyPDF2")
    print("="*60)
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        print(f"\nTotal pages: {len(reader.pages)}")
        
        # Check metadata
        if reader.metadata:
            print("\nPDF Metadata:")
            for key, value in reader.metadata.items():
                print(f"  {key}: {value}")
        
        # Extract text from first few pages
        print("\n" + "-"*60)
        print("Sample content from first 3 pages:")
        print("-"*60)
        
        for i in range(min(3, len(reader.pages))):
            page = reader.pages[i]
            text = page.extract_text()
            print(f"\n--- Page {i+1} ---")
            # Show first 1000 characters
            print(text[:1000] if text else "[No text extracted]")
            if len(text) > 1000:
                print(f"\n... ({len(text)} total characters)")

def analyze_with_pdfplumber(pdf_path):
    """Analyze PDF using pdfplumber (better for tables)"""
    print("\n" + "="*60)
    print("Analysis with pdfplumber")
    print("="*60)
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"\nTotal pages: {len(pdf.pages)}")
        
        # Check first few pages
        for i in range(min(3, len(pdf.pages))):
            page = pdf.pages[i]
            
            print(f"\n--- Page {i+1} ---")
            
            # Extract text
            text = page.extract_text()
            if text:
                print("\nText content (first 800 chars):")
                print(text[:800])
                if len(text) > 800:
                    print(f"\n... ({len(text)} total characters)")
            
            # Check for tables
            tables = page.extract_tables()
            if tables:
                print(f"\nFound {len(tables)} table(s) on this page")
                for j, table in enumerate(tables[:2]):  # Show first 2 tables
                    print(f"\nTable {j+1} (first 5 rows):")
                    for row in table[:5]:
                        print(row)

def detect_epic_format(pdf_path):
    """Detect Epic export format and provide recommendations"""
    print("\n" + "="*60)
    print("Epic Format Detection & Recommendations")
    print("="*60)
    
    # Try to read first page
    text_sample = ""
    
    if HAS_PDFPLUMBER:
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) > 0:
                text_sample = pdf.pages[0].extract_text() or ""
    elif HAS_PYPDF:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if len(reader.pages) > 0:
                text_sample = reader.pages[0].extract_text() or ""
    
    # Analyze content
    print("\nDetected sections:")
    sections = []
    
    if "medication" in text_sample.lower():
        sections.append("Medications")
    if "allerg" in text_sample.lower():
        sections.append("Allergies")
    if "immunization" in text_sample.lower() or "vaccine" in text_sample.lower():
        sections.append("Immunizations")
    if "problem" in text_sample.lower() or "diagnosis" in text_sample.lower():
        sections.append("Problems/Diagnoses")
    if "vital" in text_sample.lower():
        sections.append("Vital Signs")
    if "lab" in text_sample.lower() or "result" in text_sample.lower():
        sections.append("Lab Results")
    
    for section in sections:
        print(f"  ✓ {section}")
    
    print("\n" + "-"*60)
    print("RECOMMENDATIONS:")
    print("-"*60)
    
    print("\n1. PDF Format (Current):")
    print("   ✗ Requires OCR or complex parsing")
    print("   ✗ Tables may not extract cleanly")
    print("   ✗ Data validation difficult")
    print("   ✓ Human-readable")
    print("   ✓ Can be processed with pdfplumber/PyPDF2")
    
    print("\n2. FHIR JSON (RECOMMENDED):")
    print("   ✓ Machine-readable structured data")
    print("   ✓ Standard healthcare format")
    print("   ✓ Easy to parse and validate")
    print("   ✓ Already have parser (epic_parser.py)")
    print("   ✓ Preserves data relationships")
    print("   → Request from Epic: 'Export as FHIR JSON'")
    
    print("\n3. CCD-C XML:")
    print("   ✓ Structured clinical document")
    print("   ✓ Standard format (C-CDA)")
    print("   ~ Requires XML parsing")
    print("   → Request from Epic: 'Download Continuity of Care Document'")
    
    print("\n4. CSV Export:")
    print("   ✓ Easy to parse")
    print("   ✓ Can import to Excel for review")
    print("   ✗ May require separate files per data type")
    print("   ✗ Loses data relationships")
    print("   → Request from Epic: 'Export to CSV' or 'Download as Spreadsheet'")
    
    print("\n" + "="*60)
    print("BEST OPTION:")
    print("="*60)
    print("\nRequest from Epic MyChart:")
    print("  1. Log into MyChart")
    print("  2. Go to 'Menu' → 'Medical Record'")
    print("  3. Select 'Share My Record' or 'Download'")
    print("  4. Choose format: 'FHIR' or 'JSON' (if available)")
    print("  5. If FHIR not available, choose 'CCD' or 'XML'")
    print("  6. Last resort: Request individual CSV exports")
    
    print("\nAlternatively:")
    print("  - Contact Epic support to request FHIR API access")
    print("  - Use Epic's 'MyChart' mobile app (may have export options)")
    print("  - Ask your healthcare provider for structured data export")

def main():
    pdf_path = r"c:\QMSYS\HAL\UPLOADS\LAWRENCE C SULLIVAN-12-11-1966-Requested Record.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return 1
    
    print("Epic PDF Medical Record Analyzer")
    print("="*60)
    print(f"File: {pdf_path}")
    print(f"Size: {os.path.getsize(pdf_path):,} bytes")
    
    if not HAS_PYPDF and not HAS_PDFPLUMBER:
        print("\nError: No PDF library available")
        print("Install with: pip install PyPDF2 pdfplumber")
        return 1
    
    # Analyze with available tools
    if HAS_PDFPLUMBER:
        try:
            analyze_with_pdfplumber(pdf_path)
        except Exception as e:
            print(f"\nError with pdfplumber: {e}")
    
    if HAS_PYPDF:
        try:
            analyze_with_pypdf2(pdf_path)
        except Exception as e:
            print(f"\nError with PyPDF2: {e}")
    
    # Provide recommendations
    detect_epic_format(pdf_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
