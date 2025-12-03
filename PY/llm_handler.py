#!/usr/bin/env python3
"""
LLM Handler - Routes queries to Ollama, OpenAI, or Claude
"""

import requests
import json
from typing import Dict

def handle_llm_query(query: str, config: Dict, session_id: str, context: list = None) -> Dict:
    """Send query to configured LLM provider"""
    
    provider = config.get('provider', 'ollama')
    
    print(f"[LLM Handler] Provider: {provider}, Query: {query[:50]}...")
    
    try:
        if provider == 'ollama':
            return query_ollama(query, config['ollama'], context)
        elif provider == 'openai':
            return query_openai(query, config['openai'], context)
        elif provider == 'claude':
            return query_claude(query, config['claude'], context)
        else:
            return {
                'text': f"Unknown LLM provider: {provider}",
                'status': 'error'
            }
    except Exception as e:
        print(f"[LLM Handler] Error: {e}")
        return {
            'text': f"LLM error: {e}",
            'status': 'error'
        }

def query_ollama(query: str, config: Dict, context: list = None) -> Dict:
    """Query Ollama LLM"""
    url = config.get('url', 'http://10.1.10.20:11434')
    model = config.get('model', 'llama3.2:latest')
    
    # Build prompt with context
    prompt = query
    if context and len(context) > 0:
        context_str = "\n".join([
            f"User: {item['utterance']}\nAssistant: {item['response']}"
            for item in context[-3:]  # Last 3 turns
        ])
        prompt = f"Previous conversation:\n{context_str}\n\nUser: {query}\nAssistant:"
    
    try:
        response = requests.post(
            f"{url}/api/generate",
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('response', '').strip()
            return {
                'text': answer,
                'model': model,
                'provider': 'ollama',
                'status': 'success'
            }
        else:
            return {
                'text': f"Ollama error: {response.status_code}",
                'status': 'error'
            }
            
    except requests.exceptions.Timeout:
        return {
            'text': "The AI model is taking too long to respond. Please try again.",
            'status': 'error'
        }
    except Exception as e:
        return {
            'text': f"Failed to connect to Ollama: {e}",
            'status': 'error'
        }

def query_openai(query: str, config: Dict, context: list = None) -> Dict:
    """Query OpenAI API"""
    api_key = config.get('api_key', '')
    model = config.get('model', 'gpt-4')
    
    if not api_key:
        return {
            'text': "OpenAI API key not configured",
            'status': 'error'
        }
    
    # Build messages with context
    messages = []
    if context and len(context) > 0:
        for item in context[-5:]:  # Last 5 turns
            messages.append({'role': 'user', 'content': item['utterance']})
            messages.append({'role': 'assistant', 'content': item['response']})
    
    messages.append({'role': 'user', 'content': query})
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            return {
                'text': answer,
                'model': model,
                'provider': 'openai',
                'status': 'success'
            }
        else:
            return {
                'text': f"OpenAI error: {response.status_code}",
                'status': 'error'
            }
            
    except Exception as e:
        return {
            'text': f"OpenAI connection error: {e}",
            'status': 'error'
        }

def query_claude(query: str, config: Dict, context: list = None) -> Dict:
    """Query Anthropic Claude API"""
    api_key = config.get('api_key', '')
    model = config.get('model', 'claude-3-sonnet-20240229')
    
    if not api_key:
        return {
            'text': "Claude API key not configured",
            'status': 'error'
        }
    
    # Build messages with context
    messages = []
    if context and len(context) > 0:
        for item in context[-5:]:
            messages.append({'role': 'user', 'content': item['utterance']})
            messages.append({'role': 'assistant', 'content': item['response']})
    
    messages.append({'role': 'user', 'content': query})
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'Content-Type': 'application/json'
            },
            json={
                'model': model,
                'messages': messages,
                'max_tokens': 500,
                'temperature': 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['content'][0]['text']
            return {
                'text': answer,
                'model': model,
                'provider': 'claude',
                'status': 'success'
            }
        else:
            return {
                'text': f"Claude error: {response.status_code}",
                'status': 'error'
            }
            
    except Exception as e:
        return {
            'text': f"Claude connection error: {e}",
            'status': 'error'
        }
