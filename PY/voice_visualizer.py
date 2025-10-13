import sys
import threading
import time
import numpy as np
from typing import List, Optional
from tqdm import tqdm

class VoiceVisualizer:
    def __init__(self, width: int = 50):
        self.width = width
        self.volume_history: List[float] = []
        self.is_active = False
        self.is_listening = False
        self.wake_word_detected = False
        self._lock = threading.Lock()
        self.max_history = 100
        self.visualization_thread: Optional[threading.Thread] = None
        
    def start(self):
        """Start the visualization thread"""
        self.is_active = True
        self.visualization_thread = threading.Thread(target=self._visualization_loop)
        self.visualization_thread.daemon = True
        self.visualization_thread.start()
    
    def stop(self):
        """Stop the visualization"""
        self.is_active = False
        if self.visualization_thread:
            self.visualization_thread.join()
    
    def update_volume(self, audio_chunk: np.ndarray):
        """Update the volume level from audio chunk"""
        with self._lock:
            volume = float(np.abs(audio_chunk).mean())
            self.volume_history.append(volume)
            if len(self.volume_history) > self.max_history:
                self.volume_history.pop(0)
    
    def set_listening_state(self, is_listening: bool):
        """Update the listening state"""
        self.is_listening = is_listening
    
    def set_wake_word_state(self, detected: bool):
        """Update the wake word detection state"""
        self.wake_word_detected = detected
    
    def _get_volume_bar(self) -> str:
        """Generate the volume visualization bar"""
        if not self.volume_history:
            return "█" * 0 + "░" * self.width
        
        with self._lock:
            current_volume = self.volume_history[-1]
            max_volume = max(self.volume_history)
            normalized_volume = min(1.0, current_volume / (max_volume + 1e-6))
            filled = int(normalized_volume * self.width)
            return "█" * filled + "░" * (self.width - filled)
    
    def _get_status_indicator(self) -> str:
        """Generate the status indicator"""
        if self.wake_word_detected:
            return "🎯 HAL ACTIVATED"
        elif self.is_listening:
            return "👂 Listening for wake word..."
        else:
            return "⏸️  Paused"
    
    def _visualization_loop(self):
        """Main visualization loop"""
        with tqdm(total=0, bar_format='{desc}', file=sys.stdout) as pbar:
            while self.is_active:
                volume_bar = self._get_volume_bar()
                status = self._get_status_indicator()
                
                # Create the visualization
                visualization = f"\r{status}\n"
                visualization += f"Volume: |{volume_bar}|"
                
                # Update the progress bar description
                pbar.set_description_str(visualization)
                pbar.refresh()
                
                time.sleep(0.05)  # Update rate
    
    def clear(self):
        """Clear the visualization"""
        sys.stdout.write("\033[K")  # Clear line
        sys.stdout.flush()
