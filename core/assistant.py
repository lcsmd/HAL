import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import speech_recognition as sr
import pyttsx3
from email_handler import EmailInterface
from task_handler import TaskInterface
from memory_handler import MemorySystem
from model_router import ModelRouter
from voice_handler import VoiceSystem

@dataclass
class AssistantConfig:
    name: str
    voice_id: str
    personality_traits: Dict[str, float]
    default_model: str

class AIAssistant:
    def __init__(self, config: AssistantConfig):
        self.config = config
        self.memory = MemorySystem()
        self.model_router = ModelRouter()
        self.voice_system = VoiceSystem()
        self.email_interface = EmailInterface()
        self.task_interface = TaskInterface()
        
    async def process_input(self, input_text: str, input_type: str = "text") -> str:
        # Store input in memory
        self.memory.store_interaction("user_input", input_text)
        
        # Route to appropriate model
        task_type = self.model_router.classify_task(input_text)
        model = self.model_router.select_model(task_type)
        
        # Process with selected model
        response = await model.generate_response(
            input_text,
            context=self.memory.get_relevant_context(input_text)
        )
        
        # Store response in memory
        self.memory.store_interaction("assistant_response", response)
        
        return response
    
    async def handle_voice_input(self) -> str:
        voice_input = await self.voice_system.listen()
        return await self.process_input(voice_input, "voice")
    
    async def respond_with_voice(self, text: str):
        await self.voice_system.speak(text)
    
    def learn_new_skill(self, skill_name: str, skill_data: Dict):
        self.memory.store_skill(skill_name, skill_data)
        self.model_router.update_skill_models(skill_name)
    
    def update_personality(self, trait: str, value: float):
        self.config.personality_traits[trait] = value
        self.memory.store_personality_update(trait, value)
    
    async def process_email(self, email_id: str):
        email_content = await self.email_interface.get_email(email_id)
        return await self.process_input(f"Process email: {email_content}")
    
    async def handle_task(self, task_id: str):
        task_details = await self.task_interface.get_task(task_id)
        return await self.process_input(f"Handle task: {task_details}")
