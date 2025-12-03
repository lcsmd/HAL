#!/usr/bin/env python3
"""Test the qm_client_sync module directly"""
import sys
sys.path.insert(0, '.')
from qm_client_sync import query_qm

# Test queries
queries = [
    "what time is it",
    "hello",
    "tell me a joke",
    "what is 2+2"
]

for query in queries:
    print(f"\n=== Testing: {query} ===")
    response = query_qm(query, 'test-session')
    print(f"Response type: {type(response)}")
    print(f"Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
    print(f"Full response: {response}")
    print(f"Text field: {response.get('text', 'NO TEXT FIELD!')}")
    if 'response_text' in response:
        print(f"response_text field: {response.get('response_text')}")
