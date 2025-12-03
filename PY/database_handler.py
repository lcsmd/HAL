#!/usr/bin/env python3
"""
Database Handler - Queries QM database using natural language
"""

import re
from typing import Dict
import sys
sys.path.insert(0, '.')
from qm_execute import execute_qm_command

def handle_database_query(query: str, config: Dict, session_id: str, context: list = None) -> Dict:
    """Handle database queries"""
    
    print(f"[DB Handler] Query: {query}")
    
    try:
        # Parse database intent
        db_query = parse_database_query(query)
        
        if not db_query:
            return {
                'text': "I couldn't understand that database query.",
                'status': 'error'
            }
        
        # Execute QM query
        result = execute_database_query(db_query, config)
        
        return {
            'text': result['message'],
            'data': result.get('data'),
            'query_type': result.get('query_type'),
            'status': 'success' if result.get('success') else 'error'
        }
        
    except Exception as e:
        print(f"[DB Handler] Error: {e}")
        return {
            'text': f"Database error: {e}",
            'status': 'error'
        }

def parse_database_query(query: str) -> Dict:
    """Parse natural language database query"""
    query_lower = query.lower()
    
    # Patient/person lookup
    if re.search(r'\b(find|search|lookup|get|show)\b.*\b(patient|person)\b', query_lower):
        # Extract name
        name_match = re.search(r'(patient|person)\s+(?:named?\s+)?([a-z\s]+)', query_lower)
        if name_match:
            name = name_match.group(2).strip()
            return {
                'type': 'patient_lookup',
                'name': name,
                'file': 'PERSON'
            }
    
    # Medication lookup
    elif re.search(r'\bmedication|medicine|drug|prescription\b', query_lower):
        return {
            'type': 'medication_query',
            'file': 'MEDICATION'
        }
    
    # Appointment lookup
    elif re.search(r'\bappointment|schedule|visit\b', query_lower):
        # Check if looking for specific date
        date_match = re.search(r'(today|tomorrow|monday|tuesday|wednesday|thursday|friday)', query_lower)
        return {
            'type': 'appointment_query',
            'date': date_match.group(1) if date_match else 'today',
            'file': 'APPOINTMENT'
        }
    
    # Count queries
    elif re.search(r'\bhow many|count|total\b', query_lower):
        # Determine what to count
        if 'patient' in query_lower:
            file_name = 'PERSON'
        elif 'appointment' in query_lower:
            file_name = 'APPOINTMENT'
        elif 'medication' in query_lower:
            file_name = 'MEDICATION'
        else:
            file_name = None
        
        return {
            'type': 'count',
            'file': file_name
        }
    
    # List queries
    elif re.search(r'\blist|show all|get all\b', query_lower):
        if 'patient' in query_lower:
            return {
                'type': 'list',
                'file': 'PERSON',
                'limit': 10
            }
        elif 'appointment' in query_lower:
            return {
                'type': 'list',
                'file': 'APPOINTMENT',
                'limit': 10
            }
    
    return None

def execute_database_query(db_query: Dict, config: Dict) -> Dict:
    """Execute database query via QM"""
    
    query_type = db_query['type']
    account = config.get('default_account', 'HAL')
    
    try:
        if query_type == 'patient_lookup':
            name = db_query['name']
            # Execute QM command to find patient
            qm_command = f'LIST {db_query["file"]} WITH NAME = "{name.upper()}"'
            result = execute_qm_command(qm_command, account)
            
            if result.get('success'):
                output = result.get('output', '')
                if output and len(output) > 10:
                    return {
                        'success': True,
                        'message': f"Found patient: {output[:200]}",
                        'data': output,
                        'query_type': 'patient_lookup'
                    }
                else:
                    return {
                        'success': True,
                        'message': f"No patient found with name: {name}",
                        'query_type': 'patient_lookup'
                    }
        
        elif query_type == 'count':
            file_name = db_query.get('file')
            if not file_name:
                return {
                    'success': False,
                    'message': "Couldn't determine what to count."
                }
            
            qm_command = f'COUNT {file_name}'
            result = execute_qm_command(qm_command, account)
            
            if result.get('success'):
                output = result.get('output', '0').strip()
                return {
                    'success': True,
                    'message': f"There are {output} records in {file_name}.",
                    'data': output,
                    'query_type': 'count'
                }
        
        elif query_type == 'list':
            file_name = db_query['file']
            limit = db_query.get('limit', 10)
            
            qm_command = f'SELECT {file_name}'
            result = execute_qm_command(qm_command, account)
            
            if result.get('success'):
                output = result.get('output', '')
                lines = output.split('\n')[:limit]
                summary = '\n'.join(lines)
                return {
                    'success': True,
                    'message': f"Here are the first {limit} records:\n{summary}",
                    'data': output,
                    'query_type': 'list'
                }
        
        elif query_type == 'appointment_query':
            date = db_query.get('date', 'today')
            qm_command = f'LIST APPOINTMENT WITH DATE = "{date.upper()}"'
            result = execute_qm_command(qm_command, account)
            
            if result.get('success'):
                output = result.get('output', '')
                if output and len(output) > 10:
                    return {
                        'success': True,
                        'message': f"Appointments for {date}:\n{output[:300]}",
                        'data': output,
                        'query_type': 'appointment'
                    }
                else:
                    return {
                        'success': True,
                        'message': f"No appointments found for {date}.",
                        'query_type': 'appointment'
                    }
        
        return {
            'success': False,
            'message': f"Query type not implemented: {query_type}"
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"Database query failed: {e}"
        }

def execute_qm_command(command: str, account: str) -> Dict:
    """Execute a QM command (placeholder - implement actual QM execution)"""
    # TODO: Implement actual QM command execution
    # For now, return mock data
    print(f"[DB] Would execute: {command} on account {account}")
    return {
        'success': True,
        'output': 'Mock database response',
        'command': command
    }
