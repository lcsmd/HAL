#!/usr/bin/env python3
"""
Epic MyChart Data Parser
Converts Epic exports (FHIR JSON, CCD XML, CSV) to QM-compatible format
"""
import sys
import os
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# Add SYSCOM to Python path for QMClient module
sys.path.insert(0, r'C:\QMSYS\SYSCOM')
import qmclient as qm

def parse_fhir_date(date_str):
    """Convert FHIR date to QM internal date (days since 1967-12-31)"""
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        base_date = datetime(1967, 12, 31)
        delta = dt - base_date
        return str(delta.days)
    except:
        return ""

def parse_fhir_medication(fhir_data, person_id):
    """Parse FHIR MedicationStatement resource"""
    medications = []
    
    if 'entry' in fhir_data:
        for entry in fhir_data['entry']:
            resource = entry.get('resource', {})
            if resource.get('resourceType') == 'MedicationStatement':
                med = {}
                med['PERSON_ID'] = person_id
                
                # Medication name
                medication = resource.get('medicationCodeableConcept', {})
                if 'text' in medication:
                    med['MEDICATION_NAME'] = medication['text']
                elif 'coding' in medication and len(medication['coding']) > 0:
                    med['MEDICATION_NAME'] = medication['coding'][0].get('display', '')
                
                # Dosage
                dosage = resource.get('dosage', [])
                if dosage and len(dosage) > 0:
                    dose_text = dosage[0].get('text', '')
                    med['DOSAGE'] = dose_text
                    
                    # Try to extract route
                    route = dosage[0].get('route', {})
                    if 'text' in route:
                        med['ROUTE'] = route['text']
                
                # Dates
                effective = resource.get('effectivePeriod', {})
                if 'start' in effective:
                    med['START_DATE'] = parse_fhir_date(effective['start'])
                if 'end' in effective:
                    med['END_DATE'] = parse_fhir_date(effective['end'])
                
                # Status
                status = resource.get('status', 'active')
                med['STATUS'] = status
                med['ACTIVE'] = 'Y' if status == 'active' else 'N'
                
                medications.append(med)
    
    return medications

def parse_fhir_allergy(fhir_data, person_id):
    """Parse FHIR AllergyIntolerance resource"""
    allergies = []
    
    if 'entry' in fhir_data:
        for entry in fhir_data['entry']:
            resource = entry.get('resource', {})
            if resource.get('resourceType') == 'AllergyIntolerance':
                allergy = {}
                allergy['PERSON_ID'] = person_id
                
                # Allergen
                code = resource.get('code', {})
                if 'text' in code:
                    allergy['ALLERGEN'] = code['text']
                elif 'coding' in code and len(code['coding']) > 0:
                    allergy['ALLERGEN'] = code['coding'][0].get('display', '')
                
                # Type
                category = resource.get('category', [])
                if category and len(category) > 0:
                    allergy['ALLERGEN_TYPE'] = category[0]
                
                # Severity
                criticality = resource.get('criticality', '')
                severity_map = {
                    'low': 'mild',
                    'high': 'severe',
                    'unable-to-assess': 'moderate'
                }
                allergy['SEVERITY'] = severity_map.get(criticality, 'moderate')
                
                # Reaction
                reactions = resource.get('reaction', [])
                if reactions and len(reactions) > 0:
                    manifestations = reactions[0].get('manifestation', [])
                    if manifestations and len(manifestations) > 0:
                        if 'text' in manifestations[0]:
                            allergy['REACTION'] = manifestations[0]['text']
                
                # Dates
                if 'onsetDateTime' in resource:
                    allergy['ONSET_DATE'] = parse_fhir_date(resource['onsetDateTime'])
                
                allergy['ACTIVE'] = 'Y'
                allergies.append(allergy)
    
    return allergies

def parse_fhir_immunization(fhir_data, person_id):
    """Parse FHIR Immunization resource"""
    immunizations = []
    
    if 'entry' in fhir_data:
        for entry in fhir_data['entry']:
            resource = entry.get('resource', {})
            if resource.get('resourceType') == 'Immunization':
                imm = {}
                imm['PERSON_ID'] = person_id
                
                # Vaccine name
                vaccine = resource.get('vaccineCode', {})
                if 'text' in vaccine:
                    imm['VACCINE_NAME'] = vaccine['text']
                elif 'coding' in vaccine and len(vaccine['coding']) > 0:
                    imm['VACCINE_NAME'] = vaccine['coding'][0].get('display', '')
                    # CVX code
                    for coding in vaccine['coding']:
                        if coding.get('system', '').endswith('cvx'):
                            imm['CVX_CODE'] = coding.get('code', '')
                
                # Date
                if 'occurrenceDateTime' in resource:
                    imm['ADMINISTRATION_DATE'] = parse_fhir_date(resource['occurrenceDateTime'])
                
                # Lot number
                if 'lotNumber' in resource:
                    imm['LOT_NUMBER'] = resource['lotNumber']
                
                # Route
                if 'route' in resource and 'text' in resource['route']:
                    imm['ROUTE'] = resource['route']['text']
                
                # Site
                if 'site' in resource and 'text' in resource['site']:
                    imm['SITE'] = resource['site']['text']
                
                imm['ACTIVE'] = 'Y'
                immunizations.append(imm)
    
    return immunizations

def import_to_qm(data_type, records, person_id):
    """Import parsed records into QM"""
    print(f"\nConnecting to QM...")
    status = qm.ConnectLocal("HAL")
    if not status:
        print(f"QM Connection Error: {qm.Error()}")
        return False
    
    print(f"Connected to HAL")
    
    # Open appropriate file
    file_map = {
        'medication': 'MEDICATION',
        'allergy': 'ALLERGY',
        'immunization': 'IMMUNIZATION'
    }
    
    file_name = file_map.get(data_type)
    if not file_name:
        print(f"Unknown data type: {data_type}")
        qm.Disconnect()
        return False
    
    fno = qm.Open(file_name)
    if fno == 0:
        print(f"Failed to open {file_name}: {qm.Error()}")
        qm.Disconnect()
        return False
    
    print(f"Opened {file_name} file")
    
    # Import records
    imported = 0
    for record in records:
        # Generate ID
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        rec_id = f"{data_type.upper()[:3]}{timestamp}"
        
        # Build QM record (field mark delimited)
        qm_record = ""
        for field_num, (field_name, field_value) in enumerate(record.items()):
            if field_value:
                # Use field mark (0xFE) to separate fields
                if qm_record:
                    qm_record += '\xfe'
                qm_record += str(field_value)
        
        # Write to QM
        try:
            qm.Write(fno, rec_id, qm_record)
            imported += 1
            print(f"  Imported {rec_id}")
        except Exception as e:
            print(f"  Error writing {rec_id}: {e}")
    
    print(f"\nImported {imported} {data_type} records")
    
    qm.Disconnect()
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python epic_parser.py <file_path> <person_id>")
        print("\nSupported formats:")
        print("  - FHIR JSON (MedicationStatement, AllergyIntolerance, Immunization)")
        print("  - CSV exports")
        print("  - CCD-C XML (future)")
        return 1
    
    file_path = sys.argv[1]
    person_id = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return 1
    
    print(f"Parsing Epic data from: {file_path}")
    print(f"Person ID: {person_id}")
    
    # Detect file type
    ext = Path(file_path).suffix.lower()
    
    if ext == '.json':
        # Parse FHIR JSON
        with open(file_path, 'r') as f:
            fhir_data = json.load(f)
        
        resource_type = fhir_data.get('resourceType', '')
        
        if resource_type == 'Bundle':
            # Check what's in the bundle
            if 'entry' in fhir_data and len(fhir_data['entry']) > 0:
                first_resource = fhir_data['entry'][0].get('resource', {})
                first_type = first_resource.get('resourceType', '')
                
                if first_type == 'MedicationStatement':
                    medications = parse_fhir_medication(fhir_data, person_id)
                    print(f"\nParsed {len(medications)} medications")
                    import_to_qm('medication', medications, person_id)
                
                elif first_type == 'AllergyIntolerance':
                    allergies = parse_fhir_allergy(fhir_data, person_id)
                    print(f"\nParsed {len(allergies)} allergies")
                    import_to_qm('allergy', allergies, person_id)
                
                elif first_type == 'Immunization':
                    immunizations = parse_fhir_immunization(fhir_data, person_id)
                    print(f"\nParsed {len(immunizations)} immunizations")
                    import_to_qm('immunization', immunizations, person_id)
        
        elif resource_type == 'MedicationStatement':
            medications = parse_fhir_medication({'entry': [{'resource': fhir_data}]}, person_id)
            import_to_qm('medication', medications, person_id)
        
        elif resource_type == 'AllergyIntolerance':
            allergies = parse_fhir_allergy({'entry': [{'resource': fhir_data}]}, person_id)
            import_to_qm('allergy', allergies, person_id)
        
        elif resource_type == 'Immunization':
            immunizations = parse_fhir_immunization({'entry': [{'resource': fhir_data}]}, person_id)
            import_to_qm('immunization', immunizations, person_id)
    
    elif ext == '.csv':
        print("CSV parsing not yet implemented")
        return 1
    
    elif ext == '.xml':
        print("XML/CCD parsing not yet implemented")
        return 1
    
    else:
        print(f"Unsupported file type: {ext}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
