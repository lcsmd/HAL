#!/usr/bin/env python3
"""
FHIR JSON Parser for Epic Medical Records
Processes FHIR Bundle resources into structured data
Author: For Dr. Lawrence C. Sullivan
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

class FHIRParser:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            self.data = json.load(f)
        
        # If it's a Bundle, extract entries
        if self.data.get('resourceType') == 'Bundle':
            self.resources = [entry['resource'] for entry in self.data.get('entry', [])]
        else:
            self.resources = [self.data]
        
        # Organize resources by type
        self.resources_by_type = {}
        for resource in self.resources:
            resource_type = resource.get('resourceType')
            if resource_type not in self.resources_by_type:
                self.resources_by_type[resource_type] = []
            self.resources_by_type[resource_type].append(resource)
    
    def get_patient_demographics(self) -> Dict:
        """Extract patient demographic information"""
        patients = self.resources_by_type.get('Patient', [])
        if not patients:
            return {}
        
        patient = patients[0]  # Usually just one patient
        demographics = {}
        
        # Patient ID
        demographics['patient_id'] = patient.get('id')
        
        # Name
        if 'name' in patient and patient['name']:
            name = patient['name'][0]
            demographics['first_name'] = ' '.join(name.get('given', []))
            demographics['last_name'] = name.get('family', '')
        
        # Birth date
        demographics['birth_date'] = patient.get('birthDate')
        
        # Gender
        demographics['gender'] = patient.get('gender')
        
        # Address
        if 'address' in patient and patient['address']:
            addr = patient['address'][0]
            demographics['address'] = {
                'line': ' '.join(addr.get('line', [])),
                'city': addr.get('city', ''),
                'state': addr.get('state', ''),
                'zip': addr.get('postalCode', ''),
                'country': addr.get('country', '')
            }
        
        # Telecom
        if 'telecom' in patient:
            for contact in patient['telecom']:
                system = contact.get('system')
                value = contact.get('value')
                if system == 'phone':
                    demographics['phone'] = value
                elif system == 'email':
                    demographics['email'] = value
        
        return demographics
    
    def get_medications(self) -> List[Dict]:
        """Extract medication information"""
        medications = []
        
        # Check both MedicationRequest and MedicationStatement
        med_requests = self.resources_by_type.get('MedicationRequest', [])
        med_statements = self.resources_by_type.get('MedicationStatement', [])
        
        all_meds = med_requests + med_statements
        
        for med_resource in all_meds:
            med = {}
            
            # Medication name
            if 'medicationCodeableConcept' in med_resource:
                coding = med_resource['medicationCodeableConcept'].get('coding', [])
                if coding:
                    med['name'] = coding[0].get('display')
                    med['rxnorm_code'] = coding[0].get('code')
                    med['system'] = coding[0].get('system')
            
            # Dosage
            if 'dosageInstruction' in med_resource:
                dosage = med_resource['dosageInstruction'][0]
                
                # Dose quantity
                if 'doseAndRate' in dosage:
                    dose_and_rate = dosage['doseAndRate'][0]
                    if 'doseQuantity' in dose_and_rate:
                        dose_qty = dose_and_rate['doseQuantity']
                        med['dose'] = dose_qty.get('value')
                        med['dose_unit'] = dose_qty.get('unit')
                
                # Route
                if 'route' in dosage:
                    route_coding = dosage['route'].get('coding', [])
                    if route_coding:
                        med['route'] = route_coding[0].get('display')
                
                # Timing/Frequency
                if 'timing' in dosage:
                    timing = dosage['timing']
                    if 'repeat' in timing:
                        repeat = timing['repeat']
                        med['frequency'] = repeat.get('frequency', '')
                        med['period'] = repeat.get('period', '')
                        med['period_unit'] = repeat.get('periodUnit', '')
                
                # Instructions
                med['instructions'] = dosage.get('text', '')
            
            # Status
            med['status'] = med_resource.get('status')
            
            # Dates
            if 'authoredOn' in med_resource:
                med['authored_date'] = med_resource['authoredOn']
            
            medications.append(med)
        
        return medications
    
    def get_conditions(self) -> List[Dict]:
        """Extract conditions/problems/diagnoses"""
        conditions = []
        
        condition_resources = self.resources_by_type.get('Condition', [])
        
        for cond_resource in condition_resources:
            condition = {}
            
            # Condition name and code
            if 'code' in cond_resource:
                coding = cond_resource['code'].get('coding', [])
                if coding:
                    condition['name'] = coding[0].get('display')
                    condition['code'] = coding[0].get('code')
                    condition['code_system'] = coding[0].get('system')
                    
                    # Identify if ICD-10, SNOMED, etc.
                    if 'icd' in condition['code_system'].lower():
                        condition['icd_code'] = condition['code']
                    elif 'snomed' in condition['code_system'].lower():
                        condition['snomed_code'] = condition['code']
            
            # Clinical status
            if 'clinicalStatus' in cond_resource:
                status_coding = cond_resource['clinicalStatus'].get('coding', [])
                if status_coding:
                    condition['clinical_status'] = status_coding[0].get('code')
            
            # Verification status
            if 'verificationStatus' in cond_resource:
                verif_coding = cond_resource['verificationStatus'].get('coding', [])
                if verif_coding:
                    condition['verification_status'] = verif_coding[0].get('code')
            
            # Category
            if 'category' in cond_resource:
                cat_coding = cond_resource['category'][0].get('coding', [])
                if cat_coding:
                    condition['category'] = cat_coding[0].get('display')
            
            # Onset date
            if 'onsetDateTime' in cond_resource:
                condition['onset_date'] = cond_resource['onsetDateTime']
            elif 'onsetPeriod' in cond_resource:
                condition['onset_date'] = cond_resource['onsetPeriod'].get('start')
            
            # Recorded date
            condition['recorded_date'] = cond_resource.get('recordedDate')
            
            conditions.append(condition)
        
        return conditions
    
    def get_allergies(self) -> List[Dict]:
        """Extract allergy information"""
        allergies = []
        
        allergy_resources = self.resources_by_type.get('AllergyIntolerance', [])
        
        for allergy_resource in allergy_resources:
            allergy = {}
            
            # Allergen
            if 'code' in allergy_resource:
                coding = allergy_resource['code'].get('coding', [])
                if coding:
                    allergy['allergen'] = coding[0].get('display')
                    allergy['code'] = coding[0].get('code')
                    allergy['system'] = coding[0].get('system')
            
            # Clinical status
            if 'clinicalStatus' in allergy_resource:
                status_coding = allergy_resource['clinicalStatus'].get('coding', [])
                if status_coding:
                    allergy['clinical_status'] = status_coding[0].get('code')
            
            # Verification status
            if 'verificationStatus' in allergy_resource:
                verif_coding = allergy_resource['verificationStatus'].get('coding', [])
                if verif_coding:
                    allergy['verification_status'] = verif_coding[0].get('code')
            
            # Type
            allergy['type'] = allergy_resource.get('type')
            
            # Category
            if 'category' in allergy_resource:
                allergy['category'] = ', '.join(allergy_resource['category'])
            
            # Criticality
            allergy['criticality'] = allergy_resource.get('criticality')
            
            # Reactions
            if 'reaction' in allergy_resource:
                reactions = []
                for reaction in allergy_resource['reaction']:
                    reaction_data = {}
                    
                    # Manifestation
                    if 'manifestation' in reaction:
                        manifestations = []
                        for manifestation in reaction['manifestation']:
                            coding = manifestation.get('coding', [])
                            if coding:
                                manifestations.append(coding[0].get('display'))
                        reaction_data['manifestation'] = ', '.join(manifestations)
                    
                    # Severity
                    reaction_data['severity'] = reaction.get('severity')
                    
                    reactions.append(reaction_data)
                
                allergy['reactions'] = reactions
            
            # Onset
            allergy['onset'] = allergy_resource.get('onsetDateTime')
            
            allergies.append(allergy)
        
        return allergies
    
    def get_observations(self, category: str = None) -> List[Dict]:
        """Extract observations (labs, vitals, etc.)"""
        observations = []
        
        observation_resources = self.resources_by_type.get('Observation', [])
        
        for obs_resource in observation_resources:
            # Filter by category if specified
            if category:
                obs_categories = obs_resource.get('category', [])
                category_match = False
                for cat in obs_categories:
                    coding = cat.get('coding', [])
                    if any(c.get('code') == category for c in coding):
                        category_match = True
                        break
                if not category_match:
                    continue
            
            observation = {}
            
            # Test/Observation name
            if 'code' in obs_resource:
                coding = obs_resource['code'].get('coding', [])
                if coding:
                    observation['name'] = coding[0].get('display')
                    observation['loinc_code'] = coding[0].get('code')
                    observation['system'] = coding[0].get('system')
            
            # Value
            if 'valueQuantity' in obs_resource:
                value_qty = obs_resource['valueQuantity']
                observation['value'] = value_qty.get('value')
                observation['unit'] = value_qty.get('unit')
            elif 'valueString' in obs_resource:
                observation['value'] = obs_resource['valueString']
            elif 'valueCodeableConcept' in obs_resource:
                coding = obs_resource['valueCodeableConcept'].get('coding', [])
                if coding:
                    observation['value'] = coding[0].get('display')
            
            # Reference range
            if 'referenceRange' in obs_resource:
                ref_range = obs_resource['referenceRange'][0]
                low = ref_range.get('low', {}).get('value')
                high = ref_range.get('high', {}).get('value')
                if low and high:
                    observation['reference_range'] = f"{low}-{high}"
                elif low:
                    observation['reference_range'] = f">={low}"
                elif high:
                    observation['reference_range'] = f"<={high}"
            
            # Interpretation
            if 'interpretation' in obs_resource:
                interp_coding = obs_resource['interpretation'][0].get('coding', [])
                if interp_coding:
                    observation['interpretation'] = interp_coding[0].get('code')
            
            # Status
            observation['status'] = obs_resource.get('status')
            
            # Date
            if 'effectiveDateTime' in obs_resource:
                observation['date'] = obs_resource['effectiveDateTime']
            elif 'effectivePeriod' in obs_resource:
                observation['date'] = obs_resource['effectivePeriod'].get('start')
            
            # Category
            if 'category' in obs_resource:
                categories = []
                for cat in obs_resource['category']:
                    coding = cat.get('coding', [])
                    if coding:
                        categories.append(coding[0].get('display'))
                observation['category'] = ', '.join(categories)
            
            observations.append(observation)
        
        return observations
    
    def get_lab_results(self) -> List[Dict]:
        """Extract laboratory results specifically"""
        return self.get_observations(category='laboratory')
    
    def get_vital_signs(self) -> List[Dict]:
        """Extract vital signs specifically"""
        return self.get_observations(category='vital-signs')
    
    def get_procedures(self) -> List[Dict]:
        """Extract procedure information"""
        procedures = []
        
        procedure_resources = self.resources_by_type.get('Procedure', [])
        
        for proc_resource in procedure_resources:
            procedure = {}
            
            # Procedure name
            if 'code' in proc_resource:
                coding = proc_resource['code'].get('coding', [])
                if coding:
                    procedure['name'] = coding[0].get('display')
                    procedure['code'] = coding[0].get('code')
                    procedure['system'] = coding[0].get('system')
            
            # Status
            procedure['status'] = proc_resource.get('status')
            
            # Date
            if 'performedDateTime' in proc_resource:
                procedure['date'] = proc_resource['performedDateTime']
            elif 'performedPeriod' in proc_resource:
                procedure['date'] = proc_resource['performedPeriod'].get('start')
            
            procedures.append(procedure)
        
        return procedures
    
    def get_immunizations(self) -> List[Dict]:
        """Extract immunization records"""
        immunizations = []
        
        immunization_resources = self.resources_by_type.get('Immunization', [])
        
        for imm_resource in immunization_resources:
            immunization = {}
            
            # Vaccine name
            if 'vaccineCode' in imm_resource:
                coding = imm_resource['vaccineCode'].get('coding', [])
                if coding:
                    immunization['vaccine'] = coding[0].get('display')
                    immunization['cvx_code'] = coding[0].get('code')
            
            # Status
            immunization['status'] = imm_resource.get('status')
            
            # Date
            immunization['date'] = imm_resource.get('occurrenceDateTime')
            
            # Dose quantity
            if 'doseQuantity' in imm_resource:
                dose = imm_resource['doseQuantity']
                immunization['dose'] = dose.get('value')
                immunization['dose_unit'] = dose.get('unit')
            
            # Route
            if 'route' in imm_resource:
                route_coding = imm_resource['route'].get('coding', [])
                if route_coding:
                    immunization['route'] = route_coding[0].get('display')
            
            immunizations.append(immunization)
        
        return immunizations
    
    def export_to_dataframes(self) -> Dict[str, pd.DataFrame]:
        """Export all data to pandas DataFrames"""
        return {
            'demographics': pd.DataFrame([self.get_patient_demographics()]),
            'medications': pd.DataFrame(self.get_medications()),
            'conditions': pd.DataFrame(self.get_conditions()),
            'allergies': pd.DataFrame(self.get_allergies()),
            'labs': pd.DataFrame(self.get_lab_results()),
            'vitals': pd.DataFrame(self.get_vital_signs()),
            'procedures': pd.DataFrame(self.get_procedures()),
            'immunizations': pd.DataFrame(self.get_immunizations())
        }
    
    def export_to_json(self, output_file: str):
        """Export all data to JSON"""
        data = {
            'demographics': self.get_patient_demographics(),
            'medications': self.get_medications(),
            'conditions': self.get_conditions(),
            'allergies': self.get_allergies(),
            'labs': self.get_lab_results(),
            'vitals': self.get_vital_signs(),
            'procedures': self.get_procedures(),
            'immunizations': self.get_immunizations()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data exported to {output_file}")
    
    def get_resource_summary(self) -> Dict[str, int]:
        """Get a summary of resource types and counts"""
        return {resource_type: len(resources) 
                for resource_type, resources in self.resources_by_type.items()}


# Example usage
if __name__ == "__main__":
    # Parse FHIR Bundle
    parser = FHIRParser('your_fhir_bundle.json')
    
    # Get resource summary
    print("Resource Summary:")
    for resource_type, count in parser.get_resource_summary().items():
        print(f"  {resource_type}: {count}")
    
    # Get patient demographics
    demographics = parser.get_patient_demographics()
    print("\nDemographics:", demographics)
    
    # Get conditions
    conditions = parser.get_conditions()
    print(f"\nFound {len(conditions)} conditions")
    for cond in conditions[:5]:  # Show first 5
        print(f"  - {cond.get('name', 'Unknown')} ({cond.get('clinical_status', 'Unknown status')})")
    
    # Get lab results
    labs = parser.get_lab_results()
    print(f"\nFound {len(labs)} lab results")
    for lab in labs[:5]:  # Show first 5
        print(f"  - {lab.get('name', 'Unknown')}: {lab.get('value', '')} {lab.get('unit', '')}")
    
    # Export to DataFrames
    dfs = parser.export_to_dataframes()
    
    # Export to JSON
    parser.export_to_json('fhir_medical_records.json')
    
    # Save DataFrames to CSV
    for name, df in dfs.items():
        if not df.empty:
            df.to_csv(f'fhir_{name}.csv', index=False)
            print(f"Saved {name} to CSV")
