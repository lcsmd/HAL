#!/usr/bin/env python3
"""
HAL System Test Script
Tests all components of the HAL system: client, AI server, and OpenQM
"""

import os
import sys
import json
import time
import base64
import asyncio
import websockets
import requests
from datetime import datetime
import sounddevice as sd
import numpy as np

# Configuration
QM_HOST = os.getenv("QM_HOST", "mv1.q.lcs.ai")
QM_PORT = int(os.getenv("QM_PORT", "4243"))
AI_SERVER = os.getenv("HAL_SERVER_URL", "ws://ollama.lcs.ai:8765").replace("ws://", "http://")

class HALTester:
    def __init__(self):
        self.qm_base_url = f"http://{QM_HOST}:{QM_PORT}"
        self.ai_server_url = AI_SERVER
        self.test_results = []
        
    def log_result(self, test_name, success, message=""):
        """Log test result"""
        result = "✓" if success else "✗"
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        print(f"{result} {test_name}: {message}")
        
    async def test_qm_health(self):
        """Test OpenQM health endpoint"""
        try:
            response = requests.get(f"{self.qm_base_url}/hal/health")
            success = response.status_code == 200
            msg = "OpenQM is healthy" if success else f"OpenQM health check failed: {response.status_code}"
            self.log_result("OpenQM Health", success, msg)
        except Exception as e:
            self.log_result("OpenQM Health", False, f"Error: {str(e)}")
            
    async def test_ai_server_health(self):
        """Test AI server health"""
        try:
            response = requests.get(f"{self.ai_server_url}/health")
            success = response.status_code == 200
            msg = "AI server is healthy" if success else f"AI server health check failed: {response.status_code}"
            self.log_result("AI Server Health", success, msg)
        except Exception as e:
            self.log_result("AI Server Health", False, f"Error: {str(e)}")
            
    async def test_task_creation(self):
        """Test task creation through OpenQM"""
        try:
            data = {
                "text": "Create a task to test the system",
                "timestamp": time.time()
            }
            response = requests.post(f"{self.qm_base_url}/hal/process", json=data)
            success = response.status_code == 200
            msg = "Task creation successful" if success else f"Task creation failed: {response.status_code}"
            self.log_result("Task Creation", success, msg)
        except Exception as e:
            self.log_result("Task Creation", False, f"Error: {str(e)}")
            
    async def test_schedule_creation(self):
        """Test schedule creation through OpenQM"""
        try:
            data = {
                "text": f"Schedule a test meeting tomorrow at 10 AM",
                "timestamp": time.time()
            }
            response = requests.post(f"{self.qm_base_url}/hal/process", json=data)
            success = response.status_code == 200
            msg = "Schedule creation successful" if success else f"Schedule creation failed: {response.status_code}"
            self.log_result("Schedule Creation", success, msg)
        except Exception as e:
            self.log_result("Schedule Creation", False, f"Error: {str(e)}")
            
    async def test_audio_processing(self):
        """Test audio processing through AI server"""
        try:
            # Generate a test audio signal
            sample_rate = 16000
            duration = 2  # seconds
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
            audio = (audio * 32767).astype(np.int16)
            
            # Convert to base64
            audio_bytes = audio.tobytes()
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Send to AI server
            async with websockets.connect(self.ai_server_url.replace("http://", "ws://")) as websocket:
                await websocket.send(json.dumps({
                    "type": "audio",
                    "data": audio_b64
                }))
                
                response = await websocket.recv()
                response_data = json.loads(response)
                
                success = "data" in response_data
                msg = "Audio processing successful" if success else "Audio processing failed"
                self.log_result("Audio Processing", success, msg)
        except Exception as e:
            self.log_result("Audio Processing", False, f"Error: {str(e)}")
            
    def print_summary(self):
        """Print test summary"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["success"])
        failed = total - passed
        
        print("\nTest Summary")
        print("============")
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if failed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"- {result['test']}: {result['message']}")
                    
    async def run_all_tests(self):
        """Run all tests"""
        print("Starting HAL System Tests")
        print("========================")
        
        await self.test_qm_health()
        await self.test_ai_server_health()
        await self.test_task_creation()
        await self.test_schedule_creation()
        await self.test_audio_processing()
        
        self.print_summary()

if __name__ == "__main__":
    tester = HALTester()
    asyncio.run(tester.run_all_tests())
