"""Test direct connection to Faster-Whisper on ubuai:9000"""
import requests
import base64

print("Testing Faster-Whisper on ubuai:9000...")
print("")

# Test 1: Check if service is accessible
print("1. Testing connectivity...")
try:
    response = requests.get('http://ubuai:9000/health', timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("   [ERROR] Cannot connect to ubuai:9000")
    print("   Is Faster-Whisper running?")
except Exception as e:
    print(f"   [ERROR] {e}")

print("")

# Test 2: Try transcription endpoint
print("2. Testing /transcribe endpoint...")
try:
    # Create dummy audio data
    dummy_audio = b"test audio data"
    audio_b64 = base64.b64encode(dummy_audio).decode()
    
    response = requests.post(
        'http://ubuai:9000/transcribe',
        json={
            'audio': audio_b64,
            'language': 'en',
            'task': 'transcribe'
        },
        timeout=10
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
    
except requests.exceptions.ConnectionError:
    print("   [ERROR] Cannot connect to ubuai:9000")
except Exception as e:
    print(f"   [ERROR] {e}")

print("")
print("=" * 60)
print("If Faster-Whisper isn't running, you need to start it on ubuai")
print("SSH to ubuai and start the Faster-Whisper service")
print("=" * 60)
