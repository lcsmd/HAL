#!/usr/bin/env python3
"""
Test Wake Word Detection
Debug script to verify OpenWakeWord is working
"""
import sys
import struct
import time

try:
    import pyaudio
    import openwakeword
    from openwakeword.model import Model
    import numpy as np
except ImportError as e:
    print(f"Error: Missing dependencies - {e}")
    print("Install with:")
    print("  pip install pyaudio openwakeword numpy")
    sys.exit(1)

# Configuration
WAKE_WORD_MODEL = 'hey_jarvis'
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80ms at 16kHz

def test_microphone():
    """Test if microphone is accessible"""
    print("\n" + "="*60)
    print("1. Testing Microphone Access")
    print("="*60)
    
    p = pyaudio.PyAudio()
    
    # List all input devices
    print("\nAvailable input devices:")
    input_devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            input_devices.append((i, info['name']))
            print(f"  [{i}] {info['name']} (channels: {info['maxInputChannels']})")
    
    if not input_devices:
        print("✗ No input devices found!")
        p.terminate()
        return None
    
    # Try to select best microphone
    mic_index = input_devices[0][0]
    for idx, name in input_devices:
        if any(keyword in name.lower() for keyword in ['brio', 'usb', 'microphone']):
            mic_index = idx
            break
    
    print(f"\n✓ Selected: {p.get_device_info_by_index(mic_index)['name']}")
    p.terminate()
    return mic_index

def test_wake_word_model():
    """Test if wake word model loads"""
    print("\n" + "="*60)
    print("2. Testing Wake Word Model")
    print("="*60)
    
    try:
        print(f"Loading model: {WAKE_WORD_MODEL}...")
        model = Model(wakeword_models=[WAKE_WORD_MODEL], inference_framework='onnx')
        
        model_names = list(model.models.keys())
        if not model_names:
            print("✗ No models loaded!")
            return None
        
        wake_word_name = model_names[0]
        print(f"✓ Model loaded: {wake_word_name}")
        return model, wake_word_name
        
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        return None

def test_audio_stream(mic_index):
    """Test if we can read audio from microphone"""
    print("\n" + "="*60)
    print("3. Testing Audio Stream")
    print("="*60)
    
    try:
        p = pyaudio.PyAudio()
        stream = p.open(
            rate=SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=mic_index,
            frames_per_buffer=CHUNK_SIZE
        )
        
        print("Reading 5 audio chunks...")
        for i in range(5):
            audio_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            print(f"  Chunk {i+1}: {len(audio_data)} bytes")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        print("✓ Audio stream working")
        return True
        
    except Exception as e:
        print(f"✗ Audio stream failed: {e}")
        return False

def test_wake_word_detection(model, wake_word_name, mic_index):
    """Test actual wake word detection"""
    print("\n" + "="*60)
    print("4. Testing Wake Word Detection")
    print("="*60)
    
    try:
        p = pyaudio.PyAudio()
        stream = p.open(
            rate=SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=mic_index,
            frames_per_buffer=CHUNK_SIZE
        )
        
        print(f"\nListening for wake word: '{wake_word_name}'")
        print("Say: 'Hey Jarvis' or 'Computer'")
        print("Press Ctrl+C to stop")
        print("\nScores (threshold: 0.5):")
        
        try:
            chunk_count = 0
            while True:
                # Read audio chunk
                audio_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                audio_array = struct.unpack_from("h" * CHUNK_SIZE, audio_data)
                
                # Convert to float32 normalized to [-1, 1]
                audio_float = np.array(audio_array, dtype=np.float32) / 32768.0
                
                # Get predictions
                predictions = model.predict(audio_float)
                score = predictions[wake_word_name]
                
                # Print score periodically
                chunk_count += 1
                if chunk_count % 10 == 0:  # Every ~800ms
                    print(f"  Score: {score:.3f} {'🔊 WAKE WORD!' if score > 0.5 else ''}")
                
                # Check if wake word detected
                if score > 0.5:
                    print(f"\n✓ WAKE WORD DETECTED! (score: {score:.3f})")
                    print("Waiting 2 seconds before continuing...\n")
                    time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\nStopped by user")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        return True
        
    except Exception as e:
        print(f"✗ Wake word detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*60)
    print("HAL Wake Word Detection Test")
    print("="*60)
    
    # Test 1: Microphone
    mic_index = test_microphone()
    if mic_index is None:
        return 1
    
    # Test 2: Model
    result = test_wake_word_model()
    if result is None:
        return 1
    model, wake_word_name = result
    
    # Test 3: Audio stream
    if not test_audio_stream(mic_index):
        return 1
    
    # Test 4: Wake word detection
    if not test_wake_word_detection(model, wake_word_name, mic_index):
        return 1
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
    return 0

if __name__ == '__main__':
    sys.exit(main())
