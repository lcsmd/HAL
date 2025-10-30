#!/usr/bin/env python3
"""
Complete Example: Download and Analyze Your NYU Medical Data
Author: Dr. Lawrence C. Sullivan, M.D.

SETUP REQUIRED:
1. Register at https://fhir.epic.com/ (5 minutes)
2. Create a "Patient Standalone" app
3. Get your Client ID
4. Paste it below where it says "YOUR_CLIENT_ID_HERE"
5. Run this script: python complete_example.py

This script will:
- Connect to Epic via OAuth
- Download all your medical data
- Parse it into structured format
- Generate analysis and reports
- Create visualizations
"""

import os
import sys
from datetime import datetime

# ============================================================================
# CONFIGURATION - EDIT THIS SECTION
# ============================================================================

# Paste your Client ID from Epic Developer Portal here:
CLIENT_ID = "YOUR_CLIENT_ID_HERE"

# Or set as environment variable (more secure):
# CLIENT_ID = os.environ.get('EPIC_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')

# Output file names
OUTPUT_DIR = "my_medical_data"
RAW_DATA_FILE = "nyu_medical_data.json"
SUMMARY_REPORT = "health_summary_report.txt"
LAB_TRENDS_PLOT = "lab_trends.png"
TIMELINE_FILE = "medical_timeline.csv"

# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("=" * 80)
    print("NYU MEDICAL DATA DOWNLOADER AND ANALYZER")
    print("=" * 80)
    print()
    
    # Check if Client ID is set
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("ERROR: Please set your Client ID first!")
        print()
        print("Steps to get Client ID:")
        print("1. Go to https://fhir.epic.com/")
        print("2. Click 'Build Apps' → 'Create'")
        print("3. Fill in app details (see EPIC_API_GUIDE.md)")
        print("4. Copy your Client ID")
        print("5. Paste it in this script where it says 'YOUR_CLIENT_ID_HERE'")
        print()
        print("For detailed instructions, see: EPIC_API_GUIDE.md")
        sys.exit(1)
    
    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✓ Created output directory: {OUTPUT_DIR}/")
    
    # Import required modules
    print("\nLoading modules...")
    try:
        from epic_api_client import EpicFHIRClient
        from parse_fhir import FHIRParser
        from analyze_medical_data import MedicalDataAnalyzer
        print("✓ All modules loaded successfully")
    except ImportError as e:
        print(f"✗ Error importing modules: {e}")
        print("\nPlease install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # ========================================================================
    # STEP 1: CONNECT TO EPIC
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 1: CONNECTING TO EPIC FHIR API")
    print("=" * 80)
    
    try:
        client = EpicFHIRClient()
        print("\n⏳ Opening browser for NYU MyChart login...")
        print("   (A browser window will open for you to log in)")
        print()
        
        client.authorize(CLIENT_ID)
        
        print("\n✓ Successfully authenticated!")
        print(f"✓ Patient ID: {client.patient_id}")
    except Exception as e:
        print(f"\n✗ Error during authentication: {e}")
        print("\nTroubleshooting:")
        print("- Check that your Client ID is correct")
        print("- Ensure redirect URI is: http://localhost:8000/callback")
        print("- Make sure you're logging into NYU MyChart")
        print("\nSee EPIC_API_GUIDE.md for detailed troubleshooting")
        sys.exit(1)
    
    # ========================================================================
    # STEP 2: DOWNLOAD DATA
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 2: DOWNLOADING MEDICAL DATA")
    print("=" * 80)
    
    raw_data_path = os.path.join(OUTPUT_DIR, RAW_DATA_FILE)
    
    try:
        print("\n⏳ Downloading all medical records...")
        print("   This may take 1-3 minutes depending on data volume...")
        print()
        
        bundle = client.download_all_data(raw_data_path)
        
        print(f"\n✓ Downloaded {len(bundle['entry'])} resources")
        print(f"✓ Saved to: {raw_data_path}")
    except Exception as e:
        print(f"\n✗ Error downloading data: {e}")
        sys.exit(1)
    
    # ========================================================================
    # STEP 3: PARSE DATA
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 3: PARSING MEDICAL DATA")
    print("=" * 80)
    
    try:
        print("\n⏳ Parsing FHIR bundle...")
        parser = FHIRParser(raw_data_path)
        
        # Get resource summary
        summary = parser.get_resource_summary()
        print("\n✓ Parsed successfully!")
        print("\nData Summary:")
        for resource_type, count in sorted(summary.items()):
            print(f"  • {resource_type}: {count}")
        
        # Export to DataFrames
        print("\n⏳ Exporting to structured format...")
        dfs = parser.export_to_dataframes()
        
        # Save individual CSV files
        csv_count = 0
        for name, df in dfs.items():
            if not df.empty:
                csv_path = os.path.join(OUTPUT_DIR, f'{name}.csv')
                df.to_csv(csv_path, index=False)
                csv_count += 1
                print(f"  ✓ {name}.csv ({len(df)} records)")
        
        print(f"\n✓ Exported {csv_count} CSV files")
    except Exception as e:
        print(f"\n✗ Error parsing data: {e}")
        sys.exit(1)
    
    # ========================================================================
    # STEP 4: ANALYZE DATA
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 4: ANALYZING MEDICAL DATA")
    print("=" * 80)
    
    try:
        print("\n⏳ Running analysis...")
        analyzer = MedicalDataAnalyzer(dfs)
        
        # Lab trends analysis
        print("\n📊 Lab Trends Analysis:")
        lab_trends = analyzer.analyze_lab_trends(days_back=365)
        if lab_trends:
            print(f"  ✓ Analyzed {len(lab_trends)} lab tests")
            print("\n  Recent Lab Values:")
            for test, stats in list(lab_trends.items())[:5]:
                print(f"    • {test}:")
                print(f"      Latest: {stats['latest_value']:.2f} ({stats['latest_date'].strftime('%Y-%m-%d')})")
                print(f"      Trend: {stats['trend']}")
        else:
            print("  ⚠ No lab results found")
        
        # Medication analysis
        print("\n💊 Medication Analysis:")
        med_analysis = analyzer.analyze_medication_timeline()
        if med_analysis:
            print(f"  ✓ Total medications: {med_analysis['total_medications']}")
            print(f"  ✓ Unique medications: {med_analysis['unique_medications']}")
            if med_analysis['status_breakdown']:
                print("  Status breakdown:")
                for status, count in med_analysis['status_breakdown'].items():
                    print(f"    • {status}: {count}")
        else:
            print("  ⚠ No medications found")
        
        # Comorbidity analysis
        print("\n🏥 Comorbidity Analysis:")
        comorbidity = analyzer.identify_comorbidities()
        if comorbidity:
            print(f"  ✓ Active conditions: {comorbidity['total_conditions']}")
            print(f"  ✓ Chronic disease burden: {comorbidity['chronic_disease_burden']}")
            if comorbidity['chronic_conditions']:
                print("  Chronic conditions identified:")
                for condition in comorbidity['chronic_conditions'][:5]:
                    print(f"    • {condition}")
        else:
            print("  ⚠ No conditions found")
        
        # Vital signs
        print("\n❤️  Vital Signs Statistics:")
        vital_stats = analyzer.calculate_vital_statistics()
        if vital_stats:
            for vital, stats in list(vital_stats.items())[:5]:
                print(f"  • {vital}:")
                print(f"    Mean: {stats['mean']:.2f}, Latest: {stats['latest']:.2f}")
        else:
            print("  ⚠ No vital signs found")
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")
    
    # ========================================================================
    # STEP 5: GENERATE REPORTS
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 5: GENERATING REPORTS AND VISUALIZATIONS")
    print("=" * 80)
    
    try:
        # Generate summary report
        report_path = os.path.join(OUTPUT_DIR, SUMMARY_REPORT)
        print(f"\n⏳ Generating summary report...")
        analyzer.export_summary_report(report_path)
        print(f"  ✓ Summary report: {report_path}")
        
        # Generate lab trends plot
        if lab_trends:
            plot_path = os.path.join(OUTPUT_DIR, LAB_TRENDS_PLOT)
            print(f"\n⏳ Creating lab trends visualization...")
            
            # Get top lab tests for plotting
            top_tests = list(lab_trends.keys())[:6]
            analyzer.plot_lab_trends(
                test_names=top_tests,
                save_path=plot_path
            )
            print(f"  ✓ Lab trends plot: {plot_path}")
        
        # Generate timeline
        timeline_path = os.path.join(OUTPUT_DIR, TIMELINE_FILE)
        print(f"\n⏳ Creating medical timeline...")
        timeline = analyzer.generate_timeline(save_path=timeline_path)
        if timeline is not None and len(timeline) > 0:
            print(f"  ✓ Timeline: {timeline_path}")
            print(f"  ✓ Total events: {len(timeline)}")
        else:
            print("  ⚠ No timeline events found")
            
    except Exception as e:
        print(f"\n✗ Error generating reports: {e}")
    
    # ========================================================================
    # COMPLETION SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    
    print(f"\n📁 All files saved to: {OUTPUT_DIR}/")
    print("\nGenerated Files:")
    print(f"  • {RAW_DATA_FILE} - Complete FHIR data")
    print(f"  • demographics.csv - Patient information")
    print(f"  • medications.csv - Medication list")
    print(f"  • conditions.csv - Diagnoses")
    print(f"  • labs.csv - Laboratory results")
    print(f"  • vitals.csv - Vital signs")
    print(f"  • allergies.csv - Allergies")
    print(f"  • {SUMMARY_REPORT} - Analysis summary")
    if lab_trends:
        print(f"  • {LAB_TRENDS_PLOT} - Lab trends visualization")
    if timeline is not None and len(timeline) > 0:
        print(f"  • {TIMELINE_FILE} - Medical timeline")
    
    print("\n📊 Next Steps:")
    print("  • Open CSV files in Excel for detailed analysis")
    print(f"  • Read {SUMMARY_REPORT} for health summary")
    if lab_trends:
        print(f"  • View {LAB_TRENDS_PLOT} for visual trends")
    print("  • Use analyze_medical_data.py for custom analysis")
    
    print("\n💡 Tips:")
    print("  • Run this script regularly to track changes over time")
    print("  • Compare reports from different dates")
    print("  • See README.md for advanced analysis examples")
    
    print("\n" + "=" * 80)
    print(f"Session completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        print("\nFor support:")
        print("  • Check EPIC_API_GUIDE.md for troubleshooting")
        print("  • Contact: lcsmd@nyu.edu")
        sys.exit(1)
