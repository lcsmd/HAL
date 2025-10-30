      *#!/usr/bin/env python3
      *"""
      *CCD/CDA XML Parser for Epic Medical Records
      *Extracts key clinical data into structured format
      *Author: For Dr. Lawrence C. Sullivan
      *"""

      import xml.etree.ElementTree as ET
      import pandas as pd
      from datetime import datetime
      import json

      # HL7 CDA namespace
      NS = {
      'cda': 'urn:hl7-org:v3',
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      'sdtc': 'urn:hl7-org:sdtc'
      }

      class CCDParser:
      def __init__(self, xml_file):
      self.tree = ET.parse(xml_file)
      self.root = self.tree.getroot()

      def get_patient_demographics(self):
      """Extract patient demographic information"""
      patient_role = self.root.find('.//cda:recordTarget/cda:patientRole', NS)

      if patient_role is None:
      return None

      demographics = {}

      # Patient ID
      patient_id = patient_role.find('cda:id', NS)
      if patient_id is not None:
      demographics['patient_id'] = patient_id.get('extension')
      demographics['patient_id_root'] = patient_id.get('root')

      # Name
      name = patient_role.find('.//cda:patient/cda:name', NS)
      if name is not None:
      given = name.find('cda:given', NS)
      family = name.find('cda:family', NS)
      demographics['first_name'] = given.text if given is not None else ''
      demographics['last_name'] = family.text if family is not None else ''

      # Birth date
      birth_time = patient_role.find('.//cda:patient/cda:birthTime', NS)
      if birth_time is not None:
      demographics['birth_date'] = birth_time.get('value')

      # Gender
      gender = patient_role.find('.//cda:patient/cda:administrativeGenderCode', NS)
      if gender is not None:
      demographics['gender'] = gender.get('displayName')

      # Address
      addr = patient_role.find('cda:addr', NS)
      if addr is not None:
      street = addr.find('cda:streetAddressLine', NS)
      city = addr.find('cda:city', NS)
      state = addr.find('cda:state', NS)
      postal = addr.find('cda:postalCode', NS)

      demographics['address'] = {
      'street': street.text if street is not None else '',
      'city': city.text if city is not None else '',
      'state': state.text if state is not None else '',
      'zip': postal.text if postal is not None else ''
      }

      return demographics

      def get_medications(self):
      """Extract medication list"""
      medications = []

      # Find medications section
      med_section = self.root.find('.//cda:component/cda:structuredBody/cda:component/cda:section[cda:code[@code="10160-0"]]', NS)

      if med_section is None:
      return medications

      for entry in med_section.findall('.//cda:entry', NS):
         med = {}

         # Medication name
         manufactured_product = entry.find('.//cda:manufacturedProduct/cda:manufacturedMaterial', NS)
         if manufactured_product is not None:
         code = manufactured_product.find('cda:code', NS)
         if code is not None:
         med['name'] = code.get('displayName')
         med['rxnorm_code'] = code.get('code')

         # Dosage
         dose_quantity = entry.find('.//cda:doseQuantity', NS)
         if dose_quantity is not None:
         med['dose'] = dose_quantity.get('value')
         med['dose_unit'] = dose_quantity.get('unit')

         # Route
         route = entry.find('.//cda:routeCode', NS)
         if route is not None:
         med['route'] = route.get('displayName')

         # Frequency
         period = entry.find('.//cda:effectiveTime[@operator="A"]/cda:period', NS)
         if period is not None:
         med['frequency'] = f"Every {period.get('value')} {period.get('unit')}"

         # Status
         status_code = entry.find('.//cda:statusCode', NS)
         if status_code is not None:
         med['status'] = status_code.get('code')

         # Date
         effective_time = entry.find('.//cda:effectiveTime/cda:low', NS)
         if effective_time is not None:
         med['start_date'] = effective_time.get('value')

         medications.append(med)

         return medications

         def get_problems(self):
         """Extract problem/diagnosis list"""
         problems = []

         # Find problem section (code 11450-4)
         problem_section = self.root.find('.//cda:component/cda:structuredBody/cda:component/cda:section[cda:code[@code="11450-4"]]', NS)

         if problem_section is None:
         return problems

         for entry in problem_section.findall('.//cda:entry', NS):
            problem = {}

            # Problem name and code
            value = entry.find('.//cda:value', NS)
            if value is not None:
            problem['name'] = value.get('displayName')
            problem['icd_code'] = value.get('code')
            problem['code_system'] = value.get('codeSystem')

            # Status
            status = entry.find('.//cda:statusCode', NS)
            if status is not None:
            problem['status'] = status.get('code')

            # Date
            effective_time = entry.find('.//cda:effectiveTime/cda:low', NS)
            if effective_time is not None:
            problem['onset_date'] = effective_time.get('value')

            problems.append(problem)

            return problems

            def get_allergies(self):
            """Extract allergy list"""
            allergies = []

            # Find allergies section (code 48765-2)
            allergy_section = self.root.find('.//cda:component/cda:structuredBody/cda:component/cda:section[cda:code[@code="48765-2"]]', NS)

            if allergy_section is None:
            return allergies

            for entry in allergy_section.findall('.//cda:entry', NS):
               allergy = {}

               # Allergen
               participant = entry.find('.//cda:participant/cda:participantRole/cda:playingEntity', NS)
               if participant is not None:
               code = participant.find('cda:code', NS)
               if code is not None:
               allergy['allergen'] = code.get('displayName')
               allergy['rxnorm_code'] = code.get('code')

               # Reaction
               value = entry.find('.//cda:entryRelationship/cda:observation/cda:value', NS)
               if value is not None:
               allergy['reaction'] = value.get('displayName')

               # Severity
               severity = entry.find('.//cda:entryRelationship[@typeCode="SUBJ"]/cda:observation/cda:value', NS)
               if severity is not None:
               allergy['severity'] = severity.get('displayName')

               # Status
               status = entry.find('.//cda:statusCode', NS)
               if status is not None:
               allergy['status'] = status.get('code')

               allergies.append(allergy)

               return allergies

               def get_lab_results(self):
               """Extract laboratory results"""
               labs = []

               # Find results section (code 30954-2)
               results_section = self.root.find('.//cda:component/cda:structuredBody/cda:component/cda:section[cda:code[@code="30954-2"]]', NS)

               if results_section is None:
               return labs

               for organizer in results_section.findall('.//cda:organizer', NS):
                  # Get panel date
                  panel_date = organizer.find('.//cda:effectiveTime', NS)
                  panel_date_str = panel_date.get('value') if panel_date is not None else ''

                  for component in organizer.findall('.//cda:component', NS):
                     observation = component.find('cda:observation', NS)
                     if observation is None:
                     continue

                     lab = {}

                     # Test name
                     code = observation.find('cda:code', NS)
                     if code is not None:
                     lab['test_name'] = code.get('displayName')
                     lab['loinc_code'] = code.get('code')

                     # Result value
                     value = observation.find('cda:value', NS)
                     if value is not None:
                     lab['value'] = value.get('value')
                     lab['unit'] = value.get('unit')

                     # Reference range
                     ref_range = observation.find('.//cda:referenceRange/cda:observationRange/cda:value', NS)
                     if ref_range is not None:
                     lab['reference_range'] = ref_range.find('cda:low', NS).get('value') + '-' + ref_range.find('cda:high', NS).get('value')

                     # Interpretation
                     interp = observation.find('cda:interpretationCode', NS)
                     if interp is not None:
                     lab['interpretation'] = interp.get('code')

                     lab['date'] = panel_date_str

                     labs.append(lab)

                     return labs

                     def get_vital_signs(self):
                     """Extract vital signs"""
                     vitals = []

                     # Find vital signs section (code 8716-3)
                     vitals_section = self.root.find('.//cda:component/cda:structuredBody/cda:component/cda:section[cda:code[@code="8716-3"]]', NS)

                     if vitals_section is None:
                     return vitals

                     for organizer in vitals_section.findall('.//cda:organizer', NS):
                        # Get date
                        effective_time = organizer.find('cda:effectiveTime', NS)
                        date_str = effective_time.get('value') if effective_time is not None else ''

                        vital_set = {'date': date_str}

                        for component in organizer.findall('.//cda:component', NS):
                           observation = component.find('cda:observation', NS)
                           if observation is None:
                           continue

                           # Vital type
                           code = observation.find('cda:code', NS)
                           value = observation.find('cda:value', NS)

                           if code is not None and value is not None:
                           vital_name = code.get('displayName')
                           vital_value = value.get('value')
                           vital_unit = value.get('unit')

                           vital_set[vital_name] = f"{vital_value} {vital_unit}"

                           vitals.append(vital_set)

                           return vitals

                           def export_to_dataframes(self):
                           """Export all data to pandas DataFrames for analysis"""
                           return {
                           'demographics': pd.DataFrame([self.get_patient_demographics()]),
                           'medications': pd.DataFrame(self.get_medications()),
                           'problems': pd.DataFrame(self.get_problems()),
                           'allergies': pd.DataFrame(self.get_allergies()),
                           'labs': pd.DataFrame(self.get_lab_results()),
                           'vitals': pd.DataFrame(self.get_vital_signs())
                           }

                           def export_to_json(self, output_file):
                           """Export all data to JSON"""
                           data = {
                           'demographics': self.get_patient_demographics(),
                           'medications': self.get_medications(),
                           'problems': self.get_problems(),
                           'allergies': self.get_allergies(),
                           'labs': self.get_lab_results(),
                           'vitals': self.get_vital_signs()
                           }

                           with open(output_file, 'w') as f:
                           json.dump(data, f, indent=2)

                           print(f"Data exported to {output_file}")


                           # Example usage
                           if __name__ == "__main__":
                           # Parse CCD file
                           parser = CCDParser('your_ccd_file.xml')

                           # Get demographics
                           demographics = parser.get_patient_demographics()
                           print("Demographics:", demographics)

                           # Get medications
                           medications = parser.get_medications()
                           print(f"\nFound {len(medications)} medications")
                           for med in medications:
                              print(f"  - {med.get('name', 'Unknown')}: {med.get('dose', '')} {med.get('dose_unit', '')}")

                              # Get problems
                              problems = parser.get_problems()
                              print(f"\nFound {len(problems)} problems/diagnoses")
                              for prob in problems:
                                 print(f"  - {prob.get('name', 'Unknown')} (ICD: {prob.get('icd_code', 'N/A')})")

                                 # Export to DataFrames for analysis
                                 dfs = parser.export_to_dataframes()

                                 # Export to JSON
                                 parser.export_to_json('medical_records.json')

                                 # Save DataFrames to CSV
                                 for name, df in dfs.items():
                                    if not df.empty:
                                    df.to_csv(f'medical_records_{name}.csv', index=False)
                                    print(f"Saved {name} to CSV")
