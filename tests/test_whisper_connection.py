"""
Test Faster-Whisper Server Connection
Verifies that the transcription server on ubuai is accessible
"""

import requests
import base64
import wave
import io
import numpy as np

WHISPER_URL = "http://ubuai.q.lcs.ai:9000/transcribe"

def generate_test_audio():
    """Generate a simple test audio file (1 second of silence)"""
    sample_rate = 16000
    duration = 1.0
    samples = int(sample_rate * duration)
    
    # Generate silence
    audio_data = np.zeros(samples, dtype=np.int16)
    
    # Create WAV in memory
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    return buffer.getvalue()

def test_whisper_connection():
    """Test connection to Faster-Whisper server"""
    print("Testing Faster-Whisper server connection...")
    print(f"URL: {WHISPER_URL}")
    
    try:
        # Generate test audio
        audio_bytes = generate_test_audio()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        
        # Send request
        print("Sending test transcription request...")
        response = requests.post(
            WHISPER_URL,
            json={
                'audio': audio_b64,
                'language': 'en',
                'task': 'transcribe'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Connection successful!")
            print(f"  Response: {result}")
            print(f"  Transcription: '{result.get('text', '')}'")
            return True
        else:
            print(f"✗ Server returned error: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Connection failed - cannot reach {WHISPER_URL}")
        print("  Is Faster-Whisper running on ubuai?")
        print("  Check network connectivity to ubuai.q.lcs.ai")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ Request timed out")
        print("  Server may be overloaded or not responding")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_ollama_connection():
    """Test connection to Ollama server"""
    print("\nTesting Ollama server connection...")
    
    OLLAMA_URL = "http://ubuai.q.lcs.ai:11434/api/tags"
    
    try:
        print(f"URL: {OLLAMA_URL}")
        response = requests.get(OLLAMA_URL, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            models = result.get('models', [])
            print(f"✓ Ollama connection successful!")
            print(f"  Available models: {len(models)}")
            for model in models[:5]:  # Show first 5
                print(f"    - {model.get('name')}")
            if len(models) > 5:
                print(f"    ... and {len(models) - 5} more")
            return True
        else:
            print(f"✗ Server returned error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Connection failed - cannot reach Ollama server")
        print("  Is Ollama running on ubuai?")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("HAL Voice Interface - Server Connection Tests")
    print("=" * 60)
    print()
    
    # Test Whisper
    whisper_ok = test_whisper_connection()
    
    # Test Ollama
    ollama_ok = test_ollama_connection()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Faster-Whisper: {'✓ OK' if whisper_ok else '✗ FAILED'}")
    print(f"  Ollama:         {'✓ OK' if ollama_ok else '✗ FAILED'}")
    print("=" * 60)
