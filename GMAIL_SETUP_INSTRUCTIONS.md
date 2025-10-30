# Gmail Import Setup Instructions

## Prerequisites

1. **Install Gmail API Python libraries:**
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Gmail API Setup

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name it "HAL Gmail Import"
4. Click "Create"

### Step 2: Enable Gmail API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and click "Enable"

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: HAL Gmail Import
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"
   - Scopes: Skip (click "Save and Continue")
   - Test users: Add your Gmail address
   - Click "Save and Continue"
4. Back to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: HAL Desktop
   - Click "Create"
5. Download the credentials JSON file
6. Save it as: `c:\QMSYS\HAL\config\gmail_credentials.json`

### Step 4: Run Import

```bash
cd c:\QMSYS\HAL
python PY\gmail_import.py
```

**First run:**
- Browser will open for authentication
- Sign in with your Gmail account
- Click "Allow" to grant access
- Token will be saved to `config/gmail_token.pickle`

**Subsequent runs:**
- Will use saved token (no browser needed)
- Token auto-refreshes when expired

## Usage

### Import last 30 days (max 500 emails):
```bash
python PY\gmail_import.py
```

### Import last 90 days (max 1000 emails):
```bash
python PY\gmail_import.py 1000 90
```

### Import all emails (max 5000):
```bash
python PY\gmail_import.py 5000 3650
```

## Parameters

```
python PY\gmail_import.py [max_results] [days_back]
```

- **max_results**: Maximum number of emails to fetch (default: 500)
- **days_back**: How many days to look back (default: 30)

## Features

✅ Fetches emails via Gmail API
✅ Extracts: from, to, cc, bcc, subject, body, date
✅ Stores in QM EMAIL file
✅ Skips duplicates automatically
✅ Uses Gmail message ID as key
✅ Preserves threading information

## Query Your Emails

After import, query in QM:

```
LIST EMAIL
LIST EMAIL WITH DATE_SENT >= "2025-10-01"
LIST EMAIL WITH EADD_FROM LIKE "...@gmail.com"
SELECT EMAIL WITH SUBJECT LIKE "...meeting..."
```

## Troubleshooting

**"Module not found" error:**
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**"credentials.json not found":**
- Follow Step 3 above to download credentials
- Save to `c:\QMSYS\HAL\config\gmail_credentials.json`

**"EMAIL file not found":**
```bash
python PY\setup_email_file.py
```

**Authentication issues:**
- Delete `config/gmail_token.pickle`
- Run import again to re-authenticate
