"""Test HAProxy services"""
import requests
import json

print("=" * 60)
print("Testing HAProxy Services")
print("=" * 60)

# Test 1: Ollama
print("\n1. Testing Ollama (ollama.lcs.ai)...")
try:
    response = requests.post(
        'https://ollama.lcs.ai/api/generate',
        json={
            'model': 'gemma3:latest',
            'prompt': 'Say hello in 5 words',
            'stream': False
        },
        timeout=30,
        verify=False  # Skip SSL verification for self-signed certs
    )
    if response.status_code == 200:
        result = response.json()
        print(f"  Status: OK")
        print(f"  Response: {result.get('response', '')[:100]}")
    else:
        print(f"  Status: FAILED ({response.status_code})")
except Exception as e:
    print(f"  Status: ERROR - {e}")

# Test 2: Speech Service Root
print("\n2. Testing Speech Service (speech.lcs.ai)...")
try:
    response = requests.get('https://speech.lcs.ai/', timeout=10, verify=False)
    print(f"  Status: {response.status_code}")
    print(f"  Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    print(f"  Content (first 200 chars): {response.text[:200]}")
except Exception as e:
    print(f"  Status: ERROR - {e}")

# Test 3: Speech API endpoints
print("\n3. Testing Speech API Endpoints...")
endpoints = [
    '/api',
    '/health',
    '/transcribe',
    '/tts',
    '/docs',
    '/api/docs',
]

for endpoint in endpoints:
    try:
        url = f'https://speech.lcs.ai{endpoint}'
        response = requests.get(url, timeout=5, verify=False)
        if response.status_code == 200:
            print(f"  {endpoint}: OK (200)")
        elif response.status_code == 405:  # Method not allowed (might need POST)
            print(f"  {endpoint}: Exists (405 - try POST)")
        else:
            print(f"  {endpoint}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  {endpoint}: Not found or error")

print("\n" + "=" * 60)
print("Tests Complete")
print("=" * 60)
