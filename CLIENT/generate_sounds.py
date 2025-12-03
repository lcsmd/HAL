#!/usr/bin/env python3
"""
Generate audio feedback sounds for HAL voice client
Creates simple tone-based WAV files
"""
import wave
import struct
import math

def generate_tone(frequency, duration, sample_rate=44100, volume=0.3):
    """
    Generate a simple sine wave tone
    
    Args:
        frequency: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        volume: Volume (0.0 to 1.0)
    
    Returns:
        bytes: PCM audio data
    """
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        # Sine wave
        value = math.sin(2 * math.pi * frequency * i / sample_rate)
        
        # Apply envelope (fade in/out)
        envelope = 1.0
        fade_samples = int(sample_rate * 0.01)  # 10ms fade
        if i < fade_samples:
            envelope = i / fade_samples
        elif i > num_samples - fade_samples:
            envelope = (num_samples - i) / fade_samples
        
        # Convert to 16-bit PCM
        pcm_value = int(value * envelope * volume * 32767)
        samples.append(struct.pack('h', pcm_value))
    
    return b''.join(samples)

def generate_beep(frequencies, durations, filename, sample_rate=44100):
    """
    Generate a multi-tone beep
    
    Args:
        frequencies: List of frequencies in Hz
        durations: List of durations in seconds (same length as frequencies)
        filename: Output WAV filename
        sample_rate: Sample rate
    """
    # Generate audio for each tone
    audio_data = b''
    for freq, dur in zip(frequencies, durations):
        audio_data += generate_tone(freq, dur, sample_rate)
    
    # Write WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)
    
    print(f"✓ Generated: {filename}")

def main():
    """Generate all feedback sounds"""
    
    print("Generating HAL voice feedback sounds...\n")
    
    # Activation sound (TNG-inspired chirp)
    # Two quick rising tones
    generate_beep(
        frequencies=[800, 1200],
        durations=[0.08, 0.08],
        filename='activation.wav'
    )
    
    # Acknowledgement sound (processing chime)
    # Single gentle tone
    generate_beep(
        frequencies=[600],
        durations=[0.15],
        filename='acknowledgement.wav'
    )
    
    # Error sound (warning beep)
    # Two sharp descending tones
    generate_beep(
        frequencies=[800, 400],
        durations=[0.1, 0.15],
        filename='error.wav'
    )
    
    # Correction sound (optional - subtle beep for corrections)
    # Single short low tone
    generate_beep(
        frequencies=[400],
        durations=[0.1],
        filename='correction.wav'
    )
    
    print("\n✓ All sounds generated successfully!")
    print("\nYou can now run: python hal_voice_client_full.py")

if __name__ == '__main__':
    main()
