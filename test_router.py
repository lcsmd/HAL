#!/usr/bin/env python3
"""Test the query router"""
import sys
sys.path.insert(0, 'PY')
from query_router import route_query

# Test queries
test_queries = [
    # Time/Date (built-in)
    "what time is it",
    "what's the date",
    
    # Home Assistant
    "turn on the living room lights",
    "set temperature to 72 degrees",
    "turn off all lights",
    
    # Database
    "find patient named John Smith",
    "how many appointments do we have",
    "list all patients",
    "show appointments for today",
    
    # General LLM queries
    "tell me a joke",
    "what is the capital of France",
    "explain quantum computing",
    "write a haiku about coffee"
]

print("=" * 60)
print("QUERY ROUTER TEST")
print("=" * 60)

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    response = route_query(query, 'test-session', None, 'config/router_config.json')
    
    print(f"Intent: {response.get('intent', 'unknown')}")
    print(f"Confidence: {response.get('confidence', 0)}")
    print(f"Status: {response.get('status', 'unknown')}")
    print(f"Response: {response.get('text', 'No response')[:200]}")
    
    if response.get('model'):
        print(f"Model: {response.get('model')}")
    if response.get('provider'):
        print(f"Provider: {response.get('provider')}")

print(f"\n{'='*60}")
print("Test complete!")
print(f"{'='*60}")
