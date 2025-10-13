import asyncio
import time
from voice_handler import VoiceSystem

async def test_voice():
    voice_system = VoiceSystem()
    
    # Test TTS
    print("\n" + "="*50)
    print("Voice System Test")
    print("="*50 + "\n")
    
    print("1. Testing text-to-speech...")
    await voice_system.speak("Hello, I am HAL. I'm ready to assist you.")
    
    # Test STT with wake word
    print("\n2. Testing speech recognition with visualization...")
    print("- The volume bar shows your current audio level")
    print("- Say 'hal' to activate (watch for the status change)")
    print("- Speak your command when activated")
    print("- Press Ctrl+C to exit\n")
    
    async def handle_speech(text):
        print(f"\nRecognized: {text}")
        await voice_system.speak(f"I heard: {text}")
        time.sleep(1)  # Give time to read the transcription
        
    try:
        await voice_system.start_listening(handle_speech)
    except KeyboardInterrupt:
        print("\nStopping voice test...")
        voice_system.stop_listening()
        print("\nTest completed. Thank you!")

if __name__ == "__main__":
    asyncio.run(test_voice())
