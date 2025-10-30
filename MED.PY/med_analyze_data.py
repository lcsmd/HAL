#!/usr/bin/env python3
"""
Medical Data Analysis for Bioinformatics Research
Advanced analytics and visualization for parsed EHR data
Author: For Dr. Lawrence C. Sullivan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class MedicalDataAnalyzer:
    def __init__(self, data_dfs: dict):
        """
        Initialize with dictionary of DataFrames
        data_dfs should contain: demographics, medications, conditions, labs, vitals, etc.
        """
        self.data = data_dfs
        self.setup_visualizations()
    
    def setup_visualizations(self):
        """Setup visualization parameters"""
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def analyze_lab_trends(self, test_name: str = None, days_back: int = 365):
        """Analyze trends in lab results over time"""
        if 'labs' not in self.data or self.data['labs'].empty:
            print("No lab data available")
            return None
        
        labs_df = self.data['labs'].copy()
        
        # Convert date strings to datetime
        if 'date' in labs_df.columns:
            labs_df['date'] = pd.to_datetime(labs_df['date'], errors='coerce')
            labs_df = labs_df.dropna(subset=['date'])
            labs_df = labs_df.sort_values('date')
            
            # Filter by date range
            cutoff_date = datetime.now() - timedelta(days=days_back)
            labs_df = labs_df[labs_df['date'] >= cutoff_date]
        
        # Filter by specific test if provided
        if test_name:
            labs_df = labs_df[labs_df['test_name'].str.contains(test_name, case=False, na=False)]
        
        # Convert values to numeric
        labs_df['value_numeric'] = pd.to_numeric(labs_df['value'], errors='coerce')
        
        # Group by test name
        test_groups = labs_df.groupby('test_name')
        
        results = {}
        for test, group in test_groups:
            if group['value_numeric'].notna().sum() < 2:
                continue
            
            results[test] = {
                'count': len(group),
                'mean': group['value_numeric'].mean(),
                'std': group['value_numeric'].std(),
                'min': group['value_numeric'].min(),
                'max': group['value_numeric'].max(),
                'latest_value': group.iloc[-1]['value_numeric'],
                'latest_date': group.iloc[-1]['date'],
                'trend': self._calculate_trend(group['date'], group['value_numeric'])
            }
        
        return results
    
    def _calculate_trend(self, dates, values):
        """Calculate trend (increasing/decreasing/stable)"""
        if len(values) < 2:
            return 'insufficient_data'
        
        # Convert dates to numeric (days since first measurement)
        dates_numeric = [(d - dates.iloc[0]).days for d in dates]
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(dates_numeric, values)
        
        if p_value > 0.05:
            return 'stable'
        elif slope > 0:
            return 'increasing'
        else:
            return 'decreasing'
    
    def plot_lab_trends(self, test_names: list = None, save_path: str = None):
        """Visualize lab trends over time"""
        if 'labs' not in self.data or self.data['labs'].empty:
            print("No lab data available")
            return
        
        labs_df = self.data['labs'].copy()
        labs_df['date'] = pd.to_datetime(labs_df['date'], errors='coerce')
        labs_df = labs_df.dropna(subset=['date'])
        labs_df['value_numeric'] = pd.to_numeric(labs_df['value'], errors='coerce')
        labs_df = labs_df.dropna(subset=['value_numeric'])
        
        if test_names:
            labs_df = labs_df[labs_df['test_name'].isin(test_names)]
        else:
            # Get most common tests
            test_counts = labs_df['test_name'].value_counts()
            test_names = test_counts.head(6).index.tolist()
            labs_df = labs_df[labs_df['test_name'].isin(test_names)]
        
        # Create subplot for each test
        n_tests = len(test_names)
        fig, axes = plt.subplots(n_tests, 1, figsize=(12, 4*n_tests))
        
        if n_tests == 1:
            axes = [axes]
        
        for idx, test in enumerate(test_names):
            test_data = labs_df[labs_df['test_name'] == test].sort_values('date')
            
            ax = axes[idx]
            ax.plot(test_data['date'], test_data['value_numeric'], marker='o', linestyle='-', linewidth=2, markersize=6)
            ax.set_title(f'{test} Over Time', fontsize=12, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Value')
            ax.grid(True, alpha=0.3)
            
            # Add reference range if available
            if 'reference_range' in test_data.columns and test_data['reference_range'].notna().any():
                ref_range = test_data['reference_range'].iloc[0]
                if '-' in str(ref_range):
                    try:
                        low, high = map(float, str(ref_range).split('-'))
                        ax.axhspan(low, high, alpha=0.2, color='green', label='Reference Range')
                        ax.legend()
                    except:
                        pass
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        else:
            plt.show()
    
    def analyze_medication_timeline(self):
        """Analyze medication start/stop patterns"""
        if 'medications' not in self.data or self.data['medications'].empty:
            print("No medication data available")
            return None
        
        meds_df = self.data['medications'].copy()
        
        # Convert dates
        date_cols = ['start_date', 'authored_date']
        for col in date_cols:
            if col in meds_df.columns:
                meds_df[col] = pd.to_datetime(meds_df[col], errors='coerce')
        
        # Count by status
        status_counts = meds_df['status'].value_counts()
        
        # Count by medication class (would need drug classification database)
        med_counts = meds_df['name'].value_counts()
        
        return {
            'total_medications': len(meds_df),
            'status_breakdown': status_counts.to_dict(),
            'top_medications': med_counts.head(10).to_dict(),
            'unique_medications': len(med_counts)
        }
    
    def identify_comorbidities(self):
        """Identify comorbidity patterns"""
        if 'conditions' not in self.data or self.data['conditions'].empty:
            print("No condition data available")
            return None
        
        conditions_df = self.data['conditions'].copy()
        
        # Filter active conditions
        if 'clinical_status' in conditions_df.columns:
            active_conditions = conditions_df[conditions_df['clinical_status'] == 'active']
        else:
            active_conditions = conditions_df
        
        # Count conditions
        condition_counts = active_conditions['name'].value_counts()
        
        # Identify common comorbidity clusters (simplified)
        # In practice, you'd use ICD-10 hierarchies or clinical groupings
        chronic_keywords = ['diabetes', 'hypertension', 'hyperlipidemia', 'asthma', 'copd', 'depression', 'anxiety']
        chronic_conditions = []
        
        for keyword in chronic_keywords:
            matching = active_conditions[active_conditions['name'].str.contains(keyword, case=False, na=False)]
            if not matching.empty:
                chronic_conditions.extend(matching['name'].tolist())
        
        return {
            'total_conditions': len(active_conditions),
            'condition_counts': condition_counts.to_dict(),
            'chronic_conditions': chronic_conditions,
            'chronic_disease_burden': len(chronic_conditions)
        }
    
    def calculate_vital_statistics(self):
        """Calculate statistics on vital signs"""
        if 'vitals' not in self.data or self.data['vitals'].empty:
            print("No vital signs data available")
            return None
        
        vitals_df = self.data['vitals'].copy()
        
        # Convert date
        if 'date' in vitals_df.columns:
            vitals_df['date'] = pd.to_datetime(vitals_df['date'], errors='coerce')
            vitals_df = vitals_df.sort_values('date')
        
        stats = {}
        
        # Parse vital sign values
        vital_types = ['Blood Pressure', 'Heart Rate', 'Temperature', 'Weight', 'Height', 'BMI', 'Oxygen Saturation']
        
        for vital_type in vital_types:
            matching_cols = [col for col in vitals_df.columns if vital_type.lower() in col.lower()]
            
            if matching_cols:
                col = matching_cols[0]
                values = []
                
                for val in vitals_df[col].dropna():
                    # Extract numeric value
                    try:
                        if '/' in str(val):  # Blood pressure
                            systolic = float(str(val).split('/')[0].strip().split()[0])
                            values.append(systolic)
                        else:
                            numeric = float(''.join(filter(lambda x: x.isdigit() or x == '.', str(val))))
                            values.append(numeric)
                    except:
                        continue
                
                if values:
                    stats[vital_type] = {
                        'count': len(values),
                        'mean': np.mean(values),
                        'std': np.std(values),
                        'min': np.min(values),
                        'max': np.max(values),
                        'latest': values[-1]
                    }
        
        return stats
    
    def generate_timeline(self, save_path: str = None):
        """Generate a comprehensive medical timeline"""
        events = []
        
        # Add conditions
        if 'conditions' in self.data and not self.data['conditions'].empty:
            cond_df = self.data['conditions'].copy()
            if 'onset_date' in cond_df.columns:
                cond_df['onset_date'] = pd.to_datetime(cond_df['onset_date'], errors='coerce')
                for _, row in cond_df.iterrows():
                    if pd.notna(row['onset_date']):
                        events.append({
                            'date': row['onset_date'],
                            'type': 'Diagnosis',
                            'description': row.get('name', 'Unknown'),
                            'category': 'Condition'
                        })
        
        # Add medications
        if 'medications' in self.data and not self.data['medications'].empty:
            med_df = self.data['medications'].copy()
            date_col = 'start_date' if 'start_date' in med_df.columns else 'authored_date'
            if date_col in med_df.columns:
                med_df[date_col] = pd.to_datetime(med_df[date_col], errors='coerce')
                for _, row in med_df.iterrows():
                    if pd.notna(row[date_col]):
                        events.append({
                            'date': row[date_col],
                            'type': 'Medication Start',
                            'description': row.get('name', 'Unknown'),
                            'category': 'Medication'
                        })
        
        # Add procedures
        if 'procedures' in self.data and not self.data['procedures'].empty:
            proc_df = self.data['procedures'].copy()
            if 'date' in proc_df.columns:
                proc_df['date'] = pd.to_datetime(proc_df['date'], errors='coerce')
                for _, row in proc_df.iterrows():
                    if pd.notna(row['date']):
                        events.append({
                            'date': row['date'],
                            'type': 'Procedure',
                            'description': row.get('name', 'Unknown'),
                            'category': 'Procedure'
                        })
        
        # Create timeline DataFrame
        if events:
            timeline_df = pd.DataFrame(events)
            timeline_df = timeline_df.sort_values('date')
            
            if save_path:
                timeline_df.to_csv(save_path, index=False)
                print(f"Timeline saved to {save_path}")
            
            return timeline_df
        else:
            print("No timeline events found")
            return None
    
    def export_summary_report(self, output_file: str = 'medical_summary.txt'):
        """Generate a comprehensive text summary report"""
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("MEDICAL RECORD SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            # Demographics
            if 'demographics' in self.data and not self.data['demographics'].empty:
                f.write("PATIENT DEMOGRAPHICS\n")
                f.write("-" * 40 + "\n")
                demo = self.data['demographics'].iloc[0]
                for key, value in demo.items():
                    if pd.notna(value):
                        f.write(f"{key}: {value}\n")
                f.write("\n")
            
            # Conditions
            if 'conditions' in self.data and not self.data['conditions'].empty:
                f.write("ACTIVE CONDITIONS\n")
                f.write("-" * 40 + "\n")
                for _, cond in self.data['conditions'].iterrows():
                    f.write(f"• {cond.get('name', 'Unknown')}")
                    if 'icd_code' in cond and pd.notna(cond['icd_code']):
                        f.write(f" (ICD: {cond['icd_code']})")
                    f.write("\n")
                f.write("\n")
            
            # Medications
            if 'medications' in self.data and not self.data['medications'].empty:
                f.write("CURRENT MEDICATIONS\n")
                f.write("-" * 40 + "\n")
                for _, med in self.data['medications'].iterrows():
                    f.write(f"• {med.get('name', 'Unknown')}")
                    if 'dose' in med and pd.notna(med['dose']):
                        f.write(f" - {med['dose']} {med.get('dose_unit', '')}")
                    f.write("\n")
                f.write("\n")
            
            # Allergies
            if 'allergies' in self.data and not self.data['allergies'].empty:
                f.write("ALLERGIES\n")
                f.write("-" * 40 + "\n")
                for _, allergy in self.data['allergies'].iterrows():
                    f.write(f"• {allergy.get('allergen', 'Unknown')}")
                    if 'reaction' in allergy and pd.notna(allergy['reaction']):
                        f.write(f" - Reaction: {allergy['reaction']}")
                    f.write("\n")
                f.write("\n")
            
            # Lab trends
            lab_trends = self.analyze_lab_trends()
            if lab_trends:
                f.write("RECENT LAB RESULTS\n")
                f.write("-" * 40 + "\n")
                for test, stats in list(lab_trends.items())[:10]:
                    f.write(f"• {test}\n")
                    f.write(f"  Latest: {stats['latest_value']:.2f} ({stats['latest_date'].strftime('%Y-%m-%d')})\n")
                    f.write(f"  Trend: {stats['trend']}\n")
                f.write("\n")
        
        print(f"Summary report saved to {output_file}")


# Example usage
if __name__ == "__main__":
    # Load parsed data (example with FHIR)
    from parse_fhir import FHIRParser
    
    parser = FHIRParser('your_fhir_bundle.json')
    data_dfs = parser.export_to_dataframes()
    
    # Create analyzer
    analyzer = MedicalDataAnalyzer(data_dfs)
    
    # Run analyses
    print("Analyzing lab trends...")
    lab_trends = analyzer.analyze_lab_trends(days_back=180)
    if lab_trends:
        for test, stats in list(lab_trends.items())[:5]:
            print(f"\n{test}:")
            print(f"  Count: {stats['count']}")
            print(f"  Mean: {stats['mean']:.2f}")
            print(f"  Latest: {stats['latest_value']:.2f} ({stats['latest_date'].strftime('%Y-%m-%d')})")
            print(f"  Trend: {stats['trend']}")
    
    print("\n" + "="*50)
    print("Analyzing medications...")
    med_analysis = analyzer.analyze_medication_timeline()
    if med_analysis:
        print(f"Total medications: {med_analysis['total_medications']}")
        print(f"Unique medications: {med_analysis['unique_medications']}")
        print("Status breakdown:", med_analysis['status_breakdown'])
    
    print("\n" + "="*50)
    print("Identifying comorbidities...")
    comorbidity_analysis = analyzer.identify_comorbidities()
    if comorbidity_analysis:
        print(f"Total conditions: {comorbidity_analysis['total_conditions']}")
        print(f"Chronic disease burden: {comorbidity_analysis['chronic_disease_burden']}")
    
    print("\n" + "="*50)
    print("Calculating vital statistics...")
    vital_stats = analyzer.calculate_vital_statistics()
    if vital_stats:
        for vital, stats in vital_stats.items():
            print(f"\n{vital}:")
            print(f"  Mean: {stats['mean']:.2f}")
            print(f"  Latest: {stats['latest']:.2f}")
    
    # Generate visualizations
    print("\n" + "="*50)
    print("Generating lab trend plots...")
    analyzer.plot_lab_trends(save_path='lab_trends.png')
    
    # Generate timeline
    print("\n" + "="*50)
    print("Generating medical timeline...")
    timeline = analyzer.generate_timeline(save_path='medical_timeline.csv')
    
    # Export summary report
    print("\n" + "="*50)
    print("Generating summary report...")
    analyzer.export_summary_report()
