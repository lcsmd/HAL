"""Generate placeholder audio feedback files for HAL Voice Interface"""
import numpy as np
import wave
import struct

SAMPLE_RATE = 16000

def generate_sine_wave(frequency, duration, amplitude=0.3):
    """Generate a sine wave"""
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples)
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

def generate_chirp(start_freq, end_freq, duration, amplitude=0.3):
    """Generate a frequency sweep (chirp)"""
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples)
    # Linear frequency sweep
    freq = np.linspace(start_freq, end_freq, samples)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    wave_data = amplitude * np.sin(phase)
    return wave_data

def save_wav(filename, audio_data):
    """Save audio data as WAV file"""
    # Normalize to 16-bit range
    audio_int16 = np.int16(audio_data * 32767)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_int16.tobytes())
    
    print(f"Created: {filename}")

def generate_all_sounds():
    """Generate all required audio feedback files"""
    
    # 1. Acknowledgment sound (ack.wav) - Rising two-tone chime
    print("Generating ack.wav...")
    tone1 = generate_sine_wave(800, 0.08, 0.3)
    silence = np.zeros(int(SAMPLE_RATE * 0.02))
    tone2 = generate_sine_wave(1000, 0.08, 0.3)
    ack = np.concatenate([tone1, silence, tone2])
    save_wav('ack.wav', ack)
    
    # 2. Processing sound (processing.wav) - Gentle pulsing tone
    print("Generating processing.wav...")
    # Create a pulsing effect with amplitude modulation
    duration = 0.5
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples)
    carrier = np.sin(2 * np.pi * 600 * t)
    modulator = 0.5 + 0.5 * np.sin(2 * np.pi * 3 * t)  # 3Hz pulse
    processing = 0.2 * carrier * modulator
    save_wav('processing.wav', processing)
    
    # 3. Error sound (error.wav) - Descending warning beep
    print("Generating error.wav...")
    error = generate_chirp(800, 400, 0.3, 0.4)
    save_wav('error.wav', error)
    
    # 4. Goodbye sound (goodbye.wav) - Descending three-tone
    print("Generating goodbye.wav...")
    tone1 = generate_sine_wave(1000, 0.1, 0.25)
    silence1 = np.zeros(int(SAMPLE_RATE * 0.05))
    tone2 = generate_sine_wave(800, 0.1, 0.25)
    silence2 = np.zeros(int(SAMPLE_RATE * 0.05))
    tone3 = generate_sine_wave(600, 0.15, 0.25)
    goodbye = np.concatenate([tone1, silence1, tone2, silence2, tone3])
    save_wav('goodbye.wav', goodbye)
    
    print("\n" + "="*60)
    print("All audio feedback files generated successfully!")
    print("="*60)
    print("\nFiles created:")
    print("  - ack.wav         (200ms rising chime)")
    print("  - processing.wav  (500ms pulsing tone)")
    print("  - error.wav       (300ms descending beep)")
    print("  - goodbye.wav     (450ms descending tones)")

if __name__ == "__main__":
    generate_all_sounds()
