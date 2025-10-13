import os
import sys
import subprocess
import platform
import time

def install_package(package_name):
    """Install a package using pip"""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✓ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing {package_name}: {e}")
        return False

def check_audio_setup():
    """Check and setup audio dependencies"""
    # First install sounddevice
    if not install_package("sounddevice==0.4.6"):
        return False
    
    # Now try to import and use it
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        print("\nAudio devices found:")
        input_devices = []
        output_devices = []
        
        for i, dev in enumerate(devices):
            device_info = f"  {i}: {dev['name']}"
            if dev['max_input_channels'] > 0:
                input_devices.append(device_info + " (Input)")
            if dev['max_output_channels'] > 0:
                output_devices.append(device_info + " (Output)")
        
        if input_devices:
            print("\nInput devices (microphones):")
            for dev in input_devices:
                print(dev)
        else:
            print("✗ No input devices found!")
            return False
            
        if output_devices:
            print("\nOutput devices (speakers):")
            for dev in output_devices:
                print(dev)
        else:
            print("✗ No output devices found!")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Error checking audio devices: {e}")
        return False

def main():
    """Main setup function"""
    print("\nChecking audio setup...")
    if not check_audio_setup():
        print("\nAudio setup failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n✓ All checks passed!")
    sys.exit(0)

if __name__ == "__main__":
    main()
