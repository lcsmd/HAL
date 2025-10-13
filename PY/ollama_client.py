import requests
from typing import Dict, Any, List
from config import config

class OllamaClient:
    def __init__(self):
        self.base_url = f"http://{config.ollama_server.host}:{config.ollama_server.port}"
    
    def generate(self, prompt: str, model: str = "llama2") -> str:
        """Generate text using Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
    
    def get_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
        except Exception as e:
            print(f"Error getting models: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if Ollama server is available"""
        try:
            response = requests.get(f"{self.base_url}/api/version")
            return response.status_code == 200
        except:
            return False
