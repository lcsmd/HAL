#!/usr/bin/env python3
"""
OpenQM Database Interface
Python wrapper for OpenQM MultiValue database operations
"""

import subprocess
import json
import tempfile
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class OpenQMInterface:
    """Interface to OpenQM MultiValue database"""
    
    # Field delimiters for MultiValue structure
    FM = chr(254)  # Field Mark
    VM = chr(253)  # Value Mark
    SM = chr(252)  # Subvalue Mark
    
    def __init__(self, account='EMAILSYS'):
        self.account = account
        self.temp_dir = Path(tempfile.gettempdir())
        
    def _escape_qm(self, text: str) -> str:
        """Escape text for QMBasic"""
        if not text:
            return ''
        return (text.replace("'", "''")
                    .replace('\n', ' ')
                    .replace('\r', ''))
    
    def _execute_qm_script(self, script: str) -> tuple[int, str, str]:
        """Execute QMBasic script"""
        script_file = self.temp_dir / f'qm_script_{os.getpid()}.bas'
        
        try:
            with open(script_file, 'w') as f:
                f.write(script)
                
            result = subprocess.run(
                ['qm', '-A', self.account, '-K', str(script_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode, result.stdout, result.stderr
            
        finally:
            if script_file.exists():
                script_file.unlink()
    
    def write_record(self, file_name: str, record_id: str, data: Dict[str, Any]) -> bool:
        """
        Write a record to OpenQM file
        
        Args:
            file_name: OpenQM file name
            record_id: Record identifier
            data: Dictionary with field numbers as keys
            
        Returns:
            True if successful
        """
        script = f"""
OPEN '{file_name}' TO FILE.VAR ELSE
    PRINT 'ERROR: Cannot open file {file_name}'
    STOP
END

RECORD = ''
"""
        
        # Build record fields
        for field_num, value in sorted(data.items()):
            if isinstance(value, list):
                # MultiValue field
                escaped_values = [self._escape_qm(str(v)) for v in value]
                mv_string = self.VM.join(escaped_values)
                script += f"RECORD<{field_num}> = '{mv_string}'\n"
            else:
                # Single value
                escaped = self._escape_qm(str(value))
                script += f"RECORD<{field_num}> = '{escaped}'\n"
        
        script += f"""
WRITE RECORD TO FILE.VAR, '{self._escape_qm(record_id)}'
PRINT 'SUCCESS'
"""
        
        rc, stdout, stderr = self._execute_qm_script(script)
        return rc == 0 and 'SUCCESS' in stdout
    
    def read_record(self, file_name: str, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Read a record from OpenQM file
        
        Args:
            file_name: OpenQM file name
            record_id: Record identifier
            
        Returns:
            Dictionary with field data or None if not found
        """
        script = f"""
OPEN '{file_name}' TO FILE.VAR ELSE
    PRINT 'ERROR: Cannot open file'
    STOP
END

READ RECORD FROM FILE.VAR, '{self._escape_qm(record_id)}' ELSE
    PRINT 'NOT_FOUND'
    STOP
END

* Output record as delimited string
PRINT 'DATA:'
FOR I = 1 TO DCOUNT(RECORD, @FM)
    FIELD.VAL = RECORD<I>
    IF I > 1 THEN PRINT @FM:
    PRINT FIELD.VAL:
NEXT I
"""
        
        rc, stdout, stderr = self._execute_qm_script(script)
        
        if 'NOT_FOUND' in stdout:
            return None
            
        if rc != 0 or 'ERROR' in stdout:
            return None
        
        # Parse output
        if 'DATA:' in stdout:
            data_str = stdout.split('DATA:')[1].strip()
            fields = data_str.split(self.FM)
            
            result = {}
            for idx, field in enumerate(fields, 1):
                if self.VM in field:
                    # MultiValue field
                    result[idx] = field.split(self.VM)
                else:
                    result[idx] = field
                    
            return result
            
        return None
    
    def delete_record(self, file_name: str, record_id: str) -> bool:
        """Delete a record from OpenQM file"""
        script = f"""
OPEN '{file_name}' TO FILE.VAR ELSE
    PRINT 'ERROR: Cannot open file'
    STOP
END

DELETE FILE.VAR, '{self._escape_qm(record_id)}'
PRINT 'SUCCESS'
"""
        
        rc, stdout, stderr = self._execute_qm_script(script)
        return rc == 0 and 'SUCCESS' in stdout
    
    def select_records(self, file_name: str, criteria: str = '') -> List[str]:
        """
        Select record IDs from file
        
        Args:
            file_name: OpenQM file name
            criteria: Selection criteria (e.g., "WITH FIELD.1 = 'value'")
            
        Returns:
            List of record IDs
        """
        script = f"""
OPEN '{file_name}' TO FILE.VAR ELSE
    PRINT 'ERROR: Cannot open file'
    STOP
END

SELECT FILE.VAR {criteria}

IDS = ''
LOOP
    READNEXT ID ELSE EXIT
    IF IDS NE '' THEN IDS := @FM
    IDS := ID
REPEAT

PRINT 'IDS:':IDS
"""
        
        rc, stdout, stderr = self._execute_qm_script(script)
        
        if 'IDS:' in stdout:
            ids_str = stdout.split('IDS:')[1].strip()
            if ids_str:
                return ids_str.split(self.FM)
                
        return []
    
    def get_next_id(self, counter_name: str) -> int:
        """Get next sequential ID from counter"""
        script = f"""
OPEN 'SYSTEM.CONFIG' TO CONFIG.FILE ELSE
    PRINT 'ERROR: Cannot open SYSTEM.CONFIG'
    STOP
END

READ COUNTERS FROM CONFIG.FILE, 'COUNTERS' ELSE
    COUNTERS = ''
    FOR I = 1 TO 10
        COUNTERS<I> = 0
    NEXT I
END

* Counter mapping
COUNTER.MAP = ''
COUNTER.MAP<1> = 'EMAIL.COUNT'
COUNTER.MAP<2> = 'THREAD.COUNT'
COUNTER.MAP<3> = 'ATTACHMENT.COUNT'
COUNTER.MAP<4> = 'CONTACT.COUNT'
COUNTER.MAP<5> = 'GROUP.COUNT'
COUNTER.MAP<6> = 'DOMAIN.COUNT'
COUNTER.MAP<7> = 'RULE.COUNT'
COUNTER.MAP<8> = 'CATEGORY.COUNT'

LOCATE '{counter_name}' IN COUNTER.MAP<1> SETTING POS THEN
    COUNTERS<POS> += 1
    NEXT.ID = COUNTERS<POS>
    WRITE COUNTERS TO CONFIG.FILE, 'COUNTERS'
    PRINT 'ID:':NEXT.ID
END ELSE
    PRINT 'ERROR: Invalid counter name'
END
"""
        
        rc, stdout, stderr = self._execute_qm_script(script)
        
        if 'ID:' in stdout:
            try:
                return int(stdout.split('ID:')[1].strip())
            except ValueError:
                pass
                
        return -1


class EmailRecord:
    """Email record structure"""
    
    def __init__(self, qm: OpenQMInterface):
        self.qm = qm
        self.file_name = 'EMAILS'
        
    def create(self, email_data: Dict[str, Any]) -> str:
        """Create new email record"""
        email_id = f"E{self.qm.get_next_id('EMAIL.COUNT'):010d}"
        
        record = {
            1: email_data.get('from', ''),
            2: email_data.get('to', []),
            3: email_data.get('cc', []),
            4: email_data.get('bcc', []),
            5: email_data.get('attachments', []),
            6: email_data.get('format', 'text'),
            7: email_data.get('date_sent', ''),
            8: email_data.get('subject', ''),
            9: email_data.get('body_id', ''),
            10: email_data.get('html_id', ''),
            11: email_data.get('thread_id', ''),
            12: email_data.get('categories', []),
            13: email_data.get('priority', 5),
            14: email_data.get('disclaimers', []),
            15: email_data.get('spam_score', 0),
            16: email_data.get('read', []),
            17: email_data.get('confidential', False),
            18: email_data.get('retention_policy', ''),
            19: email_data.get('rules', []),
            20: email_data.get('forwarded_emails', [])
        }
        
        if self.qm.write_record(self.file_name, email_id, record):
            return email_id
        return None
    
    def get(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve email record"""
        record = self.qm.read_record(self.file_name, email_id)
        
        if record:
            return {
                'id': email_id,
                'from': record.get(1, ''),
                'to': record.get(2, []) if isinstance(record.get(2), list) else [record.get(2, '')],
                'cc': record.get(3, []) if isinstance(record.get(3), list) else [],
                'bcc': record.get(4, []) if isinstance(record.get(4), list) else [],
                'attachments': record.get(5, []) if isinstance(record.get(5), list) else [],
                'format': record.get(6, 'text'),
                'date_sent': record.get(7, ''),
                'subject': record.get(8, ''),
                'body_id': record.get(9, ''),
                'html_id': record.get(10, ''),
                'thread_id': record.get(11, ''),
                'categories': record.get(12, []) if isinstance(record.get(12), list) else [],
                'priority': int(record.get(13, 5)),
                'disclaimers': record.get(14, []) if isinstance(record.get(14), list) else [],
                'spam_score': float(record.get(15, 0)),
                'read': record.get(16, []) if isinstance(record.get(16), list) else [],
                'confidential': record.get(17, 'False') == 'True',
                'retention_policy': record.get(18, ''),
                'rules': record.get(19, []) if isinstance(record.get(19), list) else [],
                'forwarded_emails': record.get(20, []) if isinstance(record.get(20), list) else []
            }
            
        return None


class AttachmentRecord:
    """Attachment record structure"""
    
    def __init__(self, qm: OpenQMInterface):
        self.qm = qm
        self.file_name = 'ATTACHMENTS'
        
    def create(self, file_hash: str, file_names: List[str]) -> str:
        """Create attachment record"""
        record = {
            1: file_hash,
            2: file_names
        }
        
        if self.qm.write_record(self.file_name, file_hash, record):
            return file_hash
        return None


class ThreadRecord:
    """Thread record structure"""
    
    def __init__(self, qm: OpenQMInterface):
        self.qm = qm
        self.file_name = 'THREADS'
        
    def create(self, thread_data: Dict[str, Any]) -> str:
        """Create thread record"""
        thread_id = f"T{self.qm.get_next_id('THREAD.COUNT'):010d}"
        
        record = {
            1: thread_data.get('emails', []),
            2: thread_data.get('date_started', ''),
            3: thread_data.get('last_date', ''),
            4: thread_data.get('categories', []),
            5: thread_data.get('priority', 5),
            6: thread_data.get('rules', [])
        }
        
        if self.qm.write_record(self.file_name, thread_id, record):
            return thread_id
        return None


# Example usage
if __name__ == '__main__':
    # Initialize interface
    qm = OpenQMInterface(account='EMAILSYS')
    
    # Create email record
    email_rec = EmailRecord(qm)
    
    test_email = {
        'from': 'sender@example.com',
        'to': ['recipient@example.com'],
        'subject': 'Test Email',
        'date_sent': '2025-04-12 10:30:00',
        'body_id': 'B0000000001',
        'format': 'html',
        'categories': ['Work', 'Important']
    }
    
    email_id = email_rec.create(test_email)
    if email_id:
        print(f"Created email: {email_id}")
        
        # Retrieve it
        retrieved = email_rec.get(email_id)
        print(f"Retrieved: {retrieved}")
