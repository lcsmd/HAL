#!/usr/bin/env python3
"""
Combine multiple FHIR JSON files into a single FHIR Bundle
"""
import json
import sys
import os
from pathlib import Path

def combine_fhir_files(input_files, output_file):
    """Combine multiple FHIR JSON files into a single Bundle"""
    
    combined_bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": []
    }
    
    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"Warning: File not found: {input_file}")
            continue
        
        print(f"Processing: {input_file}")
        
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Handle different input formats
        if data.get('resourceType') == 'Bundle':
            # It's already a bundle, extract entries
            if 'entry' in data:
                combined_bundle['entry'].extend(data['entry'])
                print(f"  Added {len(data['entry'])} entries from bundle")
        elif 'resourceType' in data:
            # It's a single resource, wrap it
            combined_bundle['entry'].append({'resource': data})
            print(f"  Added single resource: {data['resourceType']}")
        elif isinstance(data, list):
            # It's an array of resources
            for resource in data:
                if 'resourceType' in resource:
                    combined_bundle['entry'].append({'resource': resource})
            print(f"  Added {len(data)} resources from array")
    
    # Write combined bundle
    with open(output_file, 'w') as f:
        json.dump(combined_bundle, f, indent=2)
    
    print(f"\nCombined {len(combined_bundle['entry'])} total resources")
    print(f"Output written to: {output_file}")
    
    # Show summary
    resource_types = {}
    for entry in combined_bundle['entry']:
        resource = entry.get('resource', {})
        rtype = resource.get('resourceType', 'Unknown')
        resource_types[rtype] = resource_types.get(rtype, 0) + 1
    
    print("\nResource Summary:")
    for rtype, count in sorted(resource_types.items()):
        print(f"  {rtype}: {count}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python combine_fhir_bundles.py <file1.json> <file2.json> ... [-o output.json]")
        print("\nExample:")
        print("  python combine_fhir_bundles.py conditions.json medications.json allergies.json")
        print("  python combine_fhir_bundles.py *.json -o complete_record.json")
        return 1
    
    # Parse arguments
    input_files = []
    output_file = "combined_fhir_bundle.json"
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        else:
            input_files.append(sys.argv[i])
            i += 1
    
    if not input_files:
        print("Error: No input files specified")
        return 1
    
    print(f"Combining {len(input_files)} FHIR files...")
    print(f"Output: {output_file}\n")
    
    combine_fhir_files(input_files, output_file)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
