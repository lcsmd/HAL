"""Test the TNG activation sound"""
import wave
import os

sound_file = r"C:\qmsys\hal\VOICE\SOUNDS\ack.wav"

print("="*60)
print("Testing TNG Activation Sound")
print("="*60)
print()

# Check file exists
if os.path.exists(sound_file):
    print(f"[OK] Sound file found: {sound_file}")
    
    # Get file info
    file_size = os.path.getsize(sound_file)
    print(f"     Size: {file_size:,} bytes")
    
    # Read WAV properties
    with wave.open(sound_file, 'r') as wav:
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        framerate = wav.getframerate()
        n_frames = wav.getnframes()
        duration = n_frames / framerate
        
        print(f"     Format: {channels} channel(s), {sample_width*8}-bit")
        print(f"     Sample rate: {framerate} Hz")
        print(f"     Duration: {duration:.2f} seconds")
        print()
        
        if channels == 1 and framerate == 16000:
            print("[OK] Format is correct for voice interface!")
        else:
            print("[WARNING] Expected mono 16kHz")
    
    print()
    print("="*60)
    print("Sound file ready to use!")
    print("="*60)
    print()
    print("This Star Trek TNG activation sound will play when:")
    print("  - Wake word is detected")
    print("  - Client sends wake_word_detected message")
    print("  - Voice Gateway sends 'ack' response")
    print()
    print("To hear it, start the Mac client and say 'Hey Computer'")
    print("or run: python clients/mac_voice_client.py")
    
else:
    print(f"[ERROR] Sound file not found: {sound_file}")
    
print()
