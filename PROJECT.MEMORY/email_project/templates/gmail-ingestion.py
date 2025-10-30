#!/usr/bin/env python3
"""
Gmail Ingestion Module
Retrieves emails from Gmail and stores in OpenQM database
"""

import os
import base64
import pickle
import hashlib
import email
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

# Import our OpenQM interface (assuming it's in the same directory or installed)
try:
    from openqm_interface import OpenQMInterface, EmailRecord, AttachmentRecord
except ImportError:
    print("Error: openqm_interface module not found")
    exit(1)


class GmailIngestion:
    """Gmail email ingestion into OpenQM"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, config_dir: Path, base_dir: Path, qm_account='EMAILSYS'):
        self.config_dir = config_dir
        self.base_dir = base_dir
        self.attachments_dir = base_dir / 'attachments'
        self.html_objects_dir = base_dir / 'html_objects'
        self.bodies_dir = base_dir / 'bodies'
        
        # OpenQM interface
        self.qm = OpenQMInterface(account=qm_account)
        self.email_rec = EmailRecord(self.qm)
        self.attachment_rec = AttachmentRecord(self.qm)
        
        self.gmail_service = None
        
        # Disclaimer patterns
        self.disclaimer_patterns = [
            r'This email and any attachments.*?confidential',
            r'CONFIDENTIALITY NOTICE:.*?intended recipient',
            r'This message is intended only for.*?addressee',
        ]
        
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        token_file = self.config_dir / 'gmail_token.pickle'
        credentials_file = self.config_dir / 'gmail_credentials.json'
        
        if not credentials_file.exists():
            raise FileNotFoundError(f"Gmail credentials not found: {credentials_file}")
        
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), self.SCOPES)
                creds = flow.run_local_server(port=0)
                
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
                
        self.gmail_service = build('gmail', 'v1', credentials=creds)
        print("✓ Gmail authentication successful")
        
    def get_messages(self, max_results=100, query='', label_ids=None):
        """Retrieve message list from Gmail"""
        try:
            params = {
                'userId': 'me',
                'maxResults': max_results,
                'q': query
            }
            
            if label_ids:
                params['labelIds'] = label_ids
                
            results = self.gmail_service.users().messages().list(**params).execute()
            messages = results.get('messages', [])
            
            print(f"✓ Found {len(messages)} messages")
            return messages
            
        except HttpError as error:
            print(f"✗ Gmail API error: {error}")
            return []
            
    def get_message_detail(self, msg_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve full message details"""
        try:
            message = self.gmail_service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            return self._parse_message(message)
            
        except HttpError as error:
            print(f"✗ Error retrieving message {msg_id}: {error}")
            return None
            
    def _parse_message(self, message: Dict) -> Dict[str, Any]:
        """Parse Gmail message into structured format"""
        payload = message['payload']
        headers = {h['name']: h['value'] for h in payload['headers']}
        
        # Extract header fields
        parsed = {
            'gmail_id': message['id'],
            'thread_id': message.get('threadId', ''),
            'from': headers.get('From', ''),
            'to': self._parse_addresses(headers.get('To', '')),
            'cc': self._parse_addresses(headers.get('Cc', '')),
            'bcc': self._parse_addresses(headers.get('Bcc', '')),
            'subject': headers.get('Subject', 'No Subject'),
            'date': headers.get('Date', ''),
            'date_sent': self._parse_date(headers.get('Date', '')),
            'message_id': headers.get('Message-ID', ''),
            'in_reply_to': headers.get('In-Reply-To', ''),
            'references': headers.get('References', ''),
            'labels': message.get('labelIds', []),
            'snippet': message.get('snippet', '')
        }
        
        # Extract body and attachments
        body_data = self._extract_body_and_attachments(payload, message['id'])
        parsed.update(body_data)
        
        return parsed
        
    def _parse_addresses(self, address_string: str) -> List[str]:
        """Parse comma-separated email addresses"""
        if not address_string:
            return []
        return [addr.strip() for addr in address_string.split(',')]
        
    def _parse_date(self, date_string: str) -> str:
        """Convert email date to ISO format"""
        try:
            dt = parsedate_to_datetime(date_string)
            return dt.isoformat()
        except:
            return datetime.now().isoformat()
            
    def _extract_body_and_attachments(self, payload: Dict, msg_id: str) -> Dict:
        """Extract body content and attachments"""
        result = {
            'body_text': '',
            'body_html': '',
            'attachments': [],
            'format': 'text'
        }
        
        def process_part(part):
            mime_type = part.get('mimeType', '')
            filename = part.get('filename', '')
            
            if filename:  # Attachment
                attachment_data = self._process_attachment(part, msg_id, filename)
                if attachment_data:
                    result['attachments'].append(attachment_data)
                    
            elif mime_type == 'text/plain':
                body = self._decode_body(part.get('body', {}))
                if body:
                    result['body_text'] = body
                    
            elif mime_type == 'text/html':
                body = self._decode_body(part.get('body', {}))
                if body:
                    result['body_html'] = body
                    result['format'] = 'html'
                    
            # Recurse for multipart
            if 'parts' in part:
                for subpart in part['parts']:
                    process_part(subpart)
                    
        process_part(payload)
        
        return result
        
    def _decode_body(self, body_data: Dict) -> str:
        """Decode base64 email body"""
        if 'data' in body_data:
            try:
                decoded = base64.urlsafe_b64decode(body_data['data'])
                return decoded.decode('utf-8', errors='ignore')
            except:
                pass
        return ''
        
    def _process_attachment(self, part: Dict, msg_id: str, filename: str) -> Optional[str]:
        """Download and store attachment"""
        attachment_id = part['body'].get('attachmentId')
        if not attachment_id:
            return None
            
        try:
            attachment = self.gmail_service.users().messages().attachments().get(
                userId='me',
                messageId=msg_id,
                id=attachment_id
            ).execute()
            
            file_data = base64.urlsafe_b64decode(attachment['data'])
            file_hash = hashlib.sha256(file_data).hexdigest()
            
            # Store file
            file_path = self.attachments_dir / file_hash[:2] / file_hash
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not file_path.exists():
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                    
            # Store in OpenQM
            self.attachment_rec.create(file_hash, [filename])
            
            return file_hash
            
        except HttpError as error:
            print(f"✗ Error downloading attachment: {error}")
            return None
            
    def _extract_html_objects(self, html_content: str) -> tuple[str, List[str]]:
        """Extract embedded images from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        objects = []
        
        # Find all img tags with data URIs
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src.startswith('data:'):
                # Extract base64 data
                try:
                    header, encoded = src.split(',', 1)
                    img_data = base64.b64decode(encoded)
                    img_hash = hashlib.sha256(img_data).hexdigest()
                    
                    # Store image
                    img_path = self.html_objects_dir / img_hash[:2] / img_hash
                    img_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if not img_path.exists():
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                            
                    objects.append(img_hash)
                    
                    # Replace in HTML
                    img['src'] = f'/html-objects/{img_hash}'
                    
                except:
                    pass
                    
        return str(soup), objects
        
    def _detect_disclaimer(self, body: str) -> Optional[str]:
        """Detect and extract disclaimer text"""
        for pattern in self.disclaimer_patterns:
            match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(0)
        return None
        
    def _store_body(self, body_text: str, body_html: str) -> tuple[str, str]:
        """Store email body content"""
        body_id = ''
        html_id = ''
        
        if body_text:
            body_hash = hashlib.sha256(body_text.encode()).hexdigest()
            body_path = self.bodies_dir / f"{body_hash}.bod"
            
            if not body_path.exists():
                with open(body_path, 'w', encoding='utf-8') as f:
                    f.write(body_text)
                    
            body_id = body_hash
            
        if body_html:
            # Extract HTML objects
            clean_html, html_objects = self._extract_html_objects(body_html)
            
            html_hash = hashlib.sha256(clean_html.encode()).hexdigest()
            html_path = self.bodies_dir / f"{html_hash}.hbod"
            
            if not html_path.exists():
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(clean_html)
                    
            html_id = html_hash
            
        return body_id, html_id
        
    def ingest_message(self, msg_id: str) -> Optional[str]:
        """Process and store a single message"""
        # Get message details
        msg_data = self.get_message_detail(msg_id)
        if not msg_data:
            return None
            
        # Store body
        body_id, html_id = self._store_body(
            msg_data.get('body_text', ''),
            msg_data.get('body_html', '')
        )
        
        # Prepare email record
        email_data = {
            'from': msg_data['from'],
            'to': msg_data['to'],
            'cc': msg_data['cc'],
            'bcc': msg_data['bcc'],
            'subject': msg_data['subject'],
            'date_sent': msg_data['date_sent'],
            'body_id': body_id,
            'html_id': html_id,
            'format': msg_data['format'],
            'attachments': msg_data['attachments'],
            'thread_id': '',  # Will be assigned during thread reconstruction
            'categories': [],
            'priority': 5,
            'disclaimers': [],
            'spam_score': 0,
            'read': [],
            'confidential': False,
            'retention_policy': '',
            'rules': [],
            'forwarded_emails': []
        }
        
        # Store in OpenQM
        email_id = self.email_rec.create(email_data)
        
        if email_id:
            print(f"  ✓ Stored: {email_id} - {msg_data['subject'][:50]}")
            return email_id
        else:
            print(f"  ✗ Failed to store: {msg_data['subject'][:50]}")
            return None
            
    def ingest_batch(self, max_results=100, query=''):
        """Ingest a batch of emails"""
        print("="*60)
        print("Gmail Ingestion - Starting")
        print("="*60)
        
        self.authenticate()
        
        messages = self.get_messages(max_results=max_results, query=query)
        
        success_count = 0
        for i, msg in enumerate(messages, 1):
            print(f"\n[{i}/{len(messages)}] Processing {msg['id']}...")
            
            email_id = self.ingest_message(msg['id'])
            if email_id:
                success_count += 1
                
        print("\n" + "="*60)
        print(f"Ingestion Complete: {success_count}/{len(messages)} emails stored")
        print("="*60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gmail Email Ingestion')
    parser.add_argument('--base-dir', type=Path, 
                       default=Path.home() / 'email_management_system',
                       help='Base directory')
    parser.add_argument('--account', default='EMAILSYS', help='OpenQM account')
    parser.add_argument('--max', type=int, default=100, help='Max emails to ingest')
    parser.add_argument('--query', default='', help='Gmail search query')
    
    args = parser.parse_args()
    
    config_dir = args.base_dir / 'config'
    
    ingestion = GmailIngestion(
        config_dir=config_dir,
        base_dir=args.base_dir,
        qm_account=args.account
    )
    
    ingestion.ingest_batch(max_results=args.max, query=args.query)


if __name__ == '__main__':
    main()
