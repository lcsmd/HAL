import os
from typing import Dict, List, Any
from datetime import datetime
import json
from qm_interface import QMInterface

class MemorySystem:
    def __init__(self):
        self.qm = QMInterface()
        self.initialize_memory_structure()
    
    def initialize_memory_structure(self):
        """Initialize the required OpenQM files if they don't exist"""
        required_files = [
            "MEMORY.STORE",
            "USER.PROFILE",
            "CONVERSATION.HISTORY",
            "TASK.TRACKER",
            "EMAIL.STORE",
            "SKILL.REGISTRY",
            "MODEL.CONFIG"
        ]
        
        for file in required_files:
            self.qm.create_file_if_not_exists(file)
    
    def store_interaction(self, interaction_type: str, content: str):
        """Store an interaction in the conversation history"""
        record = {
            "type": interaction_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "context": self.get_current_context()
        }
        
        self.qm.write_record("CONVERSATION.HISTORY", record)
    
    def get_relevant_context(self, query: str, limit: int = 10) -> List[Dict]:
        """Retrieve relevant context based on the current query"""
        # Implement semantic search over conversation history
        return self.qm.search_records("CONVERSATION.HISTORY", query, limit)
    
    def store_skill(self, skill_name: str, skill_data: Dict):
        """Store a new skill in the skill registry"""
        record = {
            "name": skill_name,
            "data": skill_data,
            "learned_at": datetime.now().isoformat(),
            "last_used": None,
            "success_rate": 0.0
        }
        
        self.qm.write_record("SKILL.REGISTRY", record)
    
    def store_personality_update(self, trait: str, value: float):
        """Store personality trait updates"""
        record = {
            "trait": trait,
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        
        self.qm.write_record("USER.PROFILE", record)
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get the current context including active tasks, recent conversations, etc."""
        context = {
            "recent_conversations": self.qm.get_recent_records("CONVERSATION.HISTORY", 5),
            "active_tasks": self.qm.get_records("TASK.TRACKER", {"status": "active"}),
            "personality": self.qm.get_records("USER.PROFILE", {"type": "personality"})
        }
        return context
