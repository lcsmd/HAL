import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio
from dotenv import load_dotenv
from memory_handler import MemorySystem
from model_router import ModelRouter
from voice_handler import VoiceSystem
from email_handler import EmailInterface
from task_handler import TaskInterface

load_dotenv()

@dataclass
class AssistantConfig:
    name: str
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
        self.is_running = False
    
    async def start(self):
        """Start the assistant and begin listening for voice input"""
        self.is_running = True
        await self.voice_system.start_listening(self._handle_voice_input)
    
    async def stop(self):
        """Stop the assistant"""
        self.is_running = False
        self.voice_system.stop_listening()
    
    async def _handle_voice_input(self, text: str):
        """Handle voice input from the user"""
        # Store the voice input in memory
        self.memory.store_interaction("user_input", text)
        
        # Process the input
        response = await self.process_input(text)
        
        # Respond with voice
        await self.voice_system.speak(response)
    
    async def process_input(self, input_text: str, input_type: str = "text") -> str:
        """Process user input and generate a response"""
        # Get relevant context from memory
        context = self.memory.get_relevant_context(input_text)
        
        # Route to appropriate model
        task_type = self.model_router.classify_task(input_text)
        model = self.model_router.select_model(task_type)
        
        # Generate response
        response = await model.generate_response(
            input_text,
            context=context
        )
        
        # Store response in memory
        self.memory.store_interaction("assistant_response", response)
        
        return response
    
    def learn_new_skill(self, skill_name: str, skill_data: Dict):
        """Add a new skill to the assistant's capabilities"""
        self.memory.store_skill(skill_name, skill_data)
        self.model_router.update_skill_models(skill_name)
    
    def update_personality(self, trait: str, value: float):
        """Update a personality trait"""
        self.config.personality_traits[trait] = value
        self.memory.store_personality_update(trait, value)
    
    async def process_email(self, email_id: str):
        """Process an email"""
        email_content = await self.email_interface.get_email(email_id)
        return await self.process_input(f"Process email: {email_content}")
    
    async def handle_task(self, task_id: str):
        """Handle a task"""
        task_details = await self.task_interface.get_task(task_id)
        return await self.process_input(f"Handle task: {task_details}")

if __name__ == "__main__":
    # Initialize the assistant
    config = AssistantConfig(
        name="HAL",
        personality_traits={
            "helpful": 0.9,
            "precise": 0.8,
            "formal": 0.7
        },
        default_model="gpt-3.5-turbo"
    )
    
    assistant = AIAssistant(config)
    
    try:
        # Start the assistant
        asyncio.run(assistant.start())
    except KeyboardInterrupt:
        # Handle graceful shutdown
        asyncio.run(assistant.stop())
        print("\nAssistant stopped.")
