#!/usr/bin/env python3
"""
Gmail Import to HAL
Uses Gmail API to fetch emails and import to QM with data filtering
"""
import sys
import os
import pickle
import base64
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
sys.path.insert(0, r'c:\QMSYS\SYSCOM')
import qmclient as qm

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("ERROR: Gmail API libraries not installed")
    print("Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API"""
    creds = None
    token_file = 'config/gmail_token.pickle'
    creds_file = 'config/gmail_credentials.json'
    
    # Load existing token
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or get new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_file):
                print(f"ERROR: {creds_file} not found")
                print("\nTo set up Gmail API:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select existing")
                print("3. Enable Gmail API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download credentials.json")
                print(f"6. Save as {creds_file}")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token
        os.makedirs('config', exist_ok=True)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def get_email_body(payload):
    """Extract email body from message payload"""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                    break
            elif part['mimeType'] == 'text/html':
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
    else:
        if 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
    
    return body[:9999]  # Limit body length

def get_header(headers, name):
    """Get header value by name"""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return ""

def import_gmail_messages(service, qm_conn, max_results=100, days_back=30):
    """Import Gmail messages to QM"""
    
    print(f"\nFetching last {days_back} days of emails (max {max_results})...")
    
    # Calculate date filter
    after_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
    query = f'after:{after_date}'
    
    # Get message list
    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    print(f"Found {len(messages)} messages")
    
    if not messages:
        print("No messages found")
        return
    
    # Open EMAIL file
    email_fno = qm_conn.Open("EMAIL")
    
    # Stats
    imported = 0
    skipped = 0
    errors = 0
    
    print("\nImporting messages...")
    for i, msg in enumerate(messages, 1):
        try:
            # Get full message
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extract fields
            msg_id = message['id']
            thread_id = message['threadId']
            from_addr = get_header(headers, 'From')
            to_addrs = get_header(headers, 'To')
            cc_addrs = get_header(headers, 'Cc')
            bcc_addrs = get_header(headers, 'Bcc')
            subject = get_header(headers, 'Subject')
            date_str = get_header(headers, 'Date')
            
            # Parse date
            try:
                date_obj = parsedate_to_datetime(date_str)
                date_sent = date_obj.strftime('%Y-%m-%d')
            except:
                date_sent = datetime.now().strftime('%Y-%m-%d')
            
            # Get body
            body = get_email_body(message['payload'])
            
            # Build QM record
            # Fields: emailaccount, eadd_from, eadd_to, eadd_cc, eadd_bcc, subject, body, date_sent, date_rec
            rec = f"gmail\xfe{from_addr}\xfe{to_addrs}\xfe{cc_addrs}\xfe{bcc_addrs}\xfe{subject}\xfe{body}\xfe{date_sent}\xfe{date_sent}"
            
            # Use message ID as key
            key = f"GMAIL_{msg_id}"
            
            # Check if already imported
            try:
                existing = qm_conn.Read(email_fno, key)
                skipped += 1
                if i % 10 == 0:
                    print(f"  Progress: {i}/{len(messages)} ({imported} imported, {skipped} skipped)")
                continue
            except:
                pass  # Not found, continue with import
            
            # Write to EMAIL file
            qm_conn.Write(email_fno, key, rec)
            imported += 1
            
            if i % 10 == 0:
                print(f"  Progress: {i}/{len(messages)} ({imported} imported, {skipped} skipped)")
        
        except Exception as e:
            errors += 1
            print(f"  Error processing message {i}: {e}")
    
    print("\n" + "="*60)
    print("Import Complete!")
    print("="*60)
    print(f"Imported: {imported}")
    print(f"Skipped (duplicates): {skipped}")
    print(f"Errors: {errors}")
    print(f"Total processed: {len(messages)}")

def main():
    """Main import function"""
    print("="*60)
    print("Gmail Import to HAL")
    print("="*60)
    
    # Get parameters
    max_results = 500  # Max emails to fetch
    days_back = 30     # Days to look back
    
    if len(sys.argv) > 1:
        max_results = int(sys.argv[1])
    if len(sys.argv) > 2:
        days_back = int(sys.argv[2])
    
    # Authenticate with Gmail
    print("\nAuthenticating with Gmail...")
    service = authenticate_gmail()
    print("Authenticated!")
    
    # Connect to QM
    print("\nConnecting to QM...")
    qm.Connect('localhost', 4243, 'lawr', 'apgar-66', 'HAL')
    print("Connected!")
    
    # Check if EMAIL file exists
    try:
        result = qm.Execute("COUNT EMAIL")
        print(f"EMAIL file exists: {result[0]}")
    except:
        print("\nERROR: EMAIL file not found")
        print("Run: CREATE.FILE EMAIL DYNAMIC")
        print("Then: BUILD.DICT EMAIL")
        qm.Disconnect()
        return
    
    # Import messages
    import_gmail_messages(service, qm, max_results, days_back)
    
    # Show results
    print("\nVerifying import...")
    result = qm.Execute("COUNT EMAIL")
    print(f"Total emails in database: {result[0]}")
    
    result = qm.Execute("SELECT EMAIL WITH @ID LIKE 'GMAIL_...'")
    print(f"Gmail emails: {result[0]}")
    
    qm.Disconnect()
    print("\nDone!")

if __name__ == "__main__":
    main()
