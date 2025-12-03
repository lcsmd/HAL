#!/usr/bin/env python3
"""
Home Assistant Handler - Controls smart home devices
"""

import requests
import re
from typing import Dict

def handle_home_assistant(query: str, config: Dict, session_id: str) -> Dict:
    """Handle Home Assistant commands"""
    
    url = config.get('url', 'http://homeassistant.local:8123')
    token = config.get('token', '')
    
    if not token:
        return {
            'text': "Home Assistant is not configured. Please set HA_TOKEN environment variable.",
            'status': 'error'
        }
    
    print(f"[HA Handler] Query: {query}")
    
    try:
        # Parse intent from query
        intent = parse_ha_intent(query)
        
        if not intent:
            return {
                'text': "I didn't understand that home automation command.",
                'status': 'error'
            }
        
        # Execute command
        result = execute_ha_command(url, token, intent)
        
        return {
            'text': result['message'],
            'action_taken': result.get('action', 'unknown'),
            'status': 'success' if result.get('success') else 'error'
        }
        
    except Exception as e:
        print(f"[HA Handler] Error: {e}")
        return {
            'text': f"Home Assistant error: {e}",
            'status': 'error'
        }

def parse_ha_intent(query: str) -> Dict:
    """Parse Home Assistant intent from natural language"""
    query_lower = query.lower()
    
    # Turn on/off
    if re.search(r'\bturn (on|off)\b', query_lower):
        action = 'turn_on' if 'turn on' in query_lower else 'turn_off'
        
        # Extract device/room
        device = None
        if 'light' in query_lower or 'lamp' in query_lower:
            device_type = 'light'
            # Try to extract specific light name
            words = query_lower.split()
            for i, word in enumerate(words):
                if word in ['light', 'lights', 'lamp']:
                    if i > 0 and words[i-1] not in ['the', 'turn', 'on', 'off']:
                        device = words[i-1]
                    elif i < len(words) - 1 and words[i+1] not in ['on', 'off', 'in']:
                        device = words[i+1]
        
        return {
            'action': action,
            'device_type': device_type,
            'device': device,
            'query': query
        }
    
    # Temperature/thermostat
    elif re.search(r'\bset.*temperature\b', query_lower):
        # Extract temperature
        temp_match = re.search(r'(\d+)\s*(degrees?|°)?', query_lower)
        if temp_match:
            temp = int(temp_match.group(1))
            return {
                'action': 'set_temperature',
                'device_type': 'climate',
                'value': temp,
                'query': query
            }
    
    # Scenes
    elif 'scene' in query_lower:
        scene_name = None
        # Extract scene name
        words = query_lower.split()
        for i, word in enumerate(words):
            if word == 'scene' and i < len(words) - 1:
                scene_name = words[i+1]
        
        return {
            'action': 'activate_scene',
            'scene': scene_name,
            'query': query
        }
    
    return None

def execute_ha_command(url: str, token: str, intent: Dict) -> Dict:
    """Execute Home Assistant API command"""
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    action = intent['action']
    
    try:
        if action in ['turn_on', 'turn_off']:
            # Call service
            service = 'turn_on' if action == 'turn_on' else 'turn_off'
            device_type = intent.get('device_type', 'light')
            device = intent.get('device')
            
            # Build entity_id
            if device:
                entity_id = f"{device_type}.{device}"
            else:
                entity_id = f"{device_type}.all"  # Or get all lights
            
            response = requests.post(
                f"{url}/api/services/{device_type}/{service}",
                headers=headers,
                json={'entity_id': entity_id},
                timeout=5
            )
            
            if response.status_code == 200:
                state = "on" if action == 'turn_on' else "off"
                return {
                    'success': True,
                    'message': f"Turned {state} the {device or device_type}.",
                    'action': f'{device_type}_{service}'
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to control {device or device_type}: {response.status_code}"
                }
        
        elif action == 'set_temperature':
            temp = intent['value']
            response = requests.post(
                f"{url}/api/services/climate/set_temperature",
                headers=headers,
                json={
                    'entity_id': 'climate.thermostat',
                    'temperature': temp
                },
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f"Set temperature to {temp} degrees.",
                    'action': 'climate_set_temperature'
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to set temperature: {response.status_code}"
                }
        
        elif action == 'activate_scene':
            scene = intent.get('scene', 'unknown')
            response = requests.post(
                f"{url}/api/services/scene/turn_on",
                headers=headers,
                json={'entity_id': f'scene.{scene}'},
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f"Activated {scene} scene.",
                    'action': 'scene_activated'
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to activate scene: {response.status_code}"
                }
        
        else:
            return {
                'success': False,
                'message': f"Unknown action: {action}"
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f"Home Assistant API error: {e}"
        }
