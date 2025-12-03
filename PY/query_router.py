#!/usr/bin/env python3
"""
Query Router - Routes queries to appropriate handlers
Handles: Home Assistant, Database, LLM (Ollama/OpenAI/Claude)
"""

import re
import os
import json
from typing import Dict, Tuple

# Handler modules
from home_assistant_handler import handle_home_assistant
from database_handler import handle_database_query
from llm_handler import handle_llm_query

class QueryRouter:
    def __init__(self, config_path=None):
        """Initialize router with configuration"""
        self.config = self.load_config(config_path)
        
        # Intent patterns
        self.home_assistant_patterns = [
            r'\b(turn on|turn off|switch|toggle|dim|brighten|set)\b.*\b(light|lights|lamp|switch|plug)\b',
            r'\b(open|close|lock|unlock)\b.*\b(door|window|garage|blinds|curtain)\b',
            r'\b(set|adjust|change)\b.*\b(temperature|thermostat|climate|heat|cool)\b',
            r'\b(play|pause|stop|volume|skip)\b.*\b(music|media|tv|speaker)\b',
            r'\b(arm|disarm)\b.*\b(alarm|security)\b',
            r'\bscene\b',
            r'\bautomation\b',
        ]
        
        self.database_patterns = [
            r'\b(find|search|lookup|get|show|list|retrieve)\b.*\b(patient|customer|record|person|appointment)\b',
            r'\b(what|who|when|where)\b.*(is|are|was|were).*(in|on|from).*\b(database|system|records?)\b',
            r'\bquery\b',
            r'\b(medication|allergy|vital|diagnosis|immunization|transaction|order)\b',
            r'\b(how many|count|total)\b',
        ]
        
    def load_config(self, config_path):
        """Load configuration from file or use defaults"""
        default_config = {
            'llm': {
                'provider': 'ollama',  # ollama, openai, claude
                'ollama': {
                    'url': 'http://10.1.10.20:11434',
                    'model': 'llama3.2:latest'
                },
                'openai': {
                    'api_key': os.getenv('OPENAI_API_KEY', ''),
                    'model': 'gpt-4'
                },
                'claude': {
                    'api_key': os.getenv('ANTHROPIC_API_KEY', ''),
                    'model': 'claude-3-sonnet-20240229'
                }
            },
            'home_assistant': {
                'url': os.getenv('HA_URL', 'http://homeassistant.local:8123'),
                'token': os.getenv('HA_TOKEN', ''),
                'enabled': True
            },
            'database': {
                'enabled': True,
                'default_account': 'HAL'
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge configs
                default_config.update(user_config)
        
        return default_config
    
    def detect_intent(self, query: str) -> Tuple[str, float]:
        """
        Detect query intent
        Returns: (intent_type, confidence)
        intent_type: 'home_assistant', 'database', 'llm', 'builtin'
        """
        query_lower = query.lower()
        
        # Check for built-in queries (time, date, hello) - HIGHEST PRIORITY
        if re.search(r'\b(what|current|tell me)\s+(time|date)\b', query_lower):
            return ('builtin', 0.95)
        if re.search(r'\b(hello|hi|hey)\b', query_lower) and len(query_lower) < 20:
            return ('builtin', 0.95)
        
        # Check Home Assistant patterns
        for pattern in self.home_assistant_patterns:
            if re.search(pattern, query_lower):
                return ('home_assistant', 0.9)
        
        # Check Database patterns
        for pattern in self.database_patterns:
            if re.search(pattern, query_lower):
                return ('database', 0.85)
        
        # Default to LLM for general queries
        return ('llm', 0.7)
    
    def route_query(self, query: str, session_id: str = 'unknown', context: list = None) -> Dict:
        """
        Route query to appropriate handler
        Returns: {'text': response, 'intent': intent_type, 'status': success/error}
        """
        try:
            # Detect intent
            intent, confidence = self.detect_intent(query)
            
            print(f"[Router] Intent: {intent} (confidence: {confidence})")
            print(f"[Router] Query: {query[:50]}...")
            
            # Route to handler
            if intent == 'builtin':
                # Use AI.SERVER for built-in queries (time, date, hello)
                import socket
                import json
                response = self._query_ai_server(query, session_id)
                
            elif intent == 'home_assistant' and self.config['home_assistant']['enabled']:
                response = handle_home_assistant(
                    query, 
                    self.config['home_assistant'], 
                    session_id
                )
                
            elif intent == 'database' and self.config['database']['enabled']:
                response = handle_database_query(
                    query, 
                    self.config['database'], 
                    session_id,
                    context
                )
                
            else:  # LLM
                response = handle_llm_query(
                    query, 
                    self.config['llm'], 
                    session_id,
                    context
                )
            
            # Add metadata
            if isinstance(response, dict):
                response['intent'] = intent
                response['confidence'] = confidence
            else:
                response = {
                    'text': str(response),
                    'intent': intent,
                    'confidence': confidence,
                    'status': 'success'
                }
            
            return response
            
        except Exception as e:
            print(f"[Router] Error: {e}")
            import traceback
            traceback.print_exc()
            return {
                'text': f"I encountered an error processing your request: {e}",
                'intent': 'error',
                'status': 'error'
            }
    
    def _query_ai_server(self, query: str, session_id: str) -> Dict:
        """Query AI.SERVER directly for built-in responses"""
        import socket
        import json
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect(('localhost', 8745))
            
            message = {'type': 'text_input', 'text': query, 'session_id': session_id}
            s.sendall(json.dumps(message).encode() + b'\n')
            
            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                if b'}' in chunk:
                    break
            
            s.close()
            
            if response_data:
                result = json.loads(response_data.decode())
                return {
                    'text': result.get('text', 'No response'),
                    'status': result.get('status', 'success'),
                    'intent': 'builtin'
                }
        except Exception as e:
            print(f"[Router] AI.SERVER error: {e}")
            return {'text': f'Error: {e}', 'status': 'error', 'intent': 'builtin'}

# Singleton instance
_router = None

def get_router(config_path=None):
    """Get or create router instance"""
    global _router
    if _router is None:
        _router = QueryRouter(config_path)
    return _router

def route_query(query: str, session_id: str = 'unknown', context: list = None, config_path=None) -> Dict:
    """Convenience function to route a query"""
    router = get_router(config_path)
    return router.route_query(query, session_id, context)
