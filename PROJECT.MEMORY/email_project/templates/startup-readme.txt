
# AI-Enhanced Email Management System - Web Interface

## Quick Start Guide

### 1. Prerequisites

Ensure you have completed the setup:
```bash
cd ~/email_management_system
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Directory Structure

The system expects this layout:
```
~/email_management_system/
├── venv/                  # Python virtual environment
├── config/
│   ├── config.ini        # System configuration
│   ├── gmail_credentials.json
│   └── gmail_token.pickle
├── attachments/          # Email attachments
├── html_objects/         # Extracted HTML objects
├── bodies/               # Email body files (.bod, .hbod)
├── logs/                 # Application logs
├── temp/                 # Temporary files
├── templates/            # Flask HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── emails.html
│   ├── email_detail.html
│   ├── threads.html
│   ├── categories.html
│   └── settings.html
├── app.py               # Main Flask application
├── openqm_interface.py  # OpenQM Python wrapper
├── gmail_ingestion.py   # Gmail email ingestion
└── requirements.txt     # Python dependencies
```

### 3. Create Templates Directory

```bash
cd ~/email_management_system
mkdir -p templates
```

Copy all the HTML template files into the `templates/` directory:
- `base.html`
- `dashboard.html`
- `emails.html`
- `email_detail.html`
- `threads.html`
- `categories.html`
- `settings.html`

### 4. Start the Web Server

```bash
cd ~/email_management_system
source venv/bin/activate
python app.py
```

The application will start on: **http://localhost:5000**

### 5. Using the Web Interface

#### Dashboard
- View system statistics (total emails, threads, attachments, contacts)
- See recent emails at a glance
- Quick search across all emails
- Access AI assistant for natural language queries

#### All Emails Page
- Browse all emails with pagination
- Filter by sender, subject, or keywords
- Click any email to view full details
- See categories and metadata

#### Email Detail View
- Read full email content (text or HTML)
- View attachments
- See all headers (from, to, cc, date)
- Manage categories
- View related emails in thread

#### Threads Page
- View reconstructed email conversations
- See message count per thread
- Browse by categories
- Sort by activity date

#### Categories Page
- Create new categories
- View email count per category
- Manage category assignments
- Edit category names

#### AI Assistant (🤖 button)
- Ask questions about your emails
- Get statistics and insights
- Search for specific messages
- Get help with system features

### 6. Example Queries for AI Assistant

- "How many emails do I have?"
- "What categories exist?"
- "Search for emails about project updates"
- "Show me my recent threads"
- "Help me organize my emails"

### 7. API Endpoints

The Flask app provides these REST API endpoints:

#### Email Operations
- `GET /api/emails` - List emails (with pagination & filters)
- `GET /api/emails/<id>` - Get single email details
- `GET /api/search?q=query` - Search emails

#### Thread Operations
- `GET /api/threads` - List email threads

#### Category Operations
- `GET /api/categories` - List categories
- `POST /api/categories` - Create new category

#### System
- `GET /api/stats` - Get system statistics
- `POST /api/ai/chat` - AI assistant chat

### 8. Configuration

Edit `config/config.ini`:

```ini
[openqm]
account = EMAILSYS
host = localhost
port = 4243

[gmail]
credentials_file = config/gmail_credentials.json
token_file = config/gmail_token.pickle

[exchange]
tenant_id = your-tenant-id
client_id = your-client-id
client_secret = your-client-secret

[ai]
anthropic_api_key = your-api-key-here

[system]
base_dir = ~/email_management_system
```

### 9. Ingesting Emails

Before using the web interface, ingest some emails:

```bash
# Ingest from Gmail
python gmail_ingestion.py --max 100

# With filters
python gmail_ingestion.py --max 50 --query "is:unread"
```

### 10. Troubleshooting

#### "Cannot open file" errors
- Ensure OpenQM is running
- Check that EMAILSYS account exists
- Verify files were created during setup

#### No emails showing
- Run email ingestion first: `python gmail_ingestion.py`
- Check OpenQM has data: `qm -A EMAILSYS -K "SELECT EMAILS"`

#### Templates not found
- Ensure templates/ directory exists
- Copy all .html files to templates/
- Check app.py is in the same directory

#### Port already in use
- Change port in app.py: `app.run(port=5001)`
- Or kill existing process: `lsof -ti:5000 | xargs kill`

### 11. Development Mode

For development with auto-reload:
```python
# In app.py, at the bottom:
app.run(debug=True, host='0.0.0.0', port=5000)
```

### 12. Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or with Nginx as reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 13. Security Considerations

- **Authentication**: Add user authentication before production deployment
- **HTTPS**: Use SSL/TLS for production
- **API Keys**: Store credentials securely, not in config files
- **Input Validation**: All user inputs are validated
- **CORS**: Configure CORS appropriately for your environment

### 14. Next Steps

After getting the web interface running:

1. **Thread Reconstruction** - Build the module to link related emails
2. **AI Categorization** - Integrate Claude API for automatic categorization
3. **Rule Engine** - Implement automated rule application
4. **Knowledge Extraction** - Extract facts, contacts, events from emails
5. **Exchange Integration** - Add Microsoft Graph API support
6. **Advanced Search** - Full-text search with Elasticsearch or similar
7. **Email Deduplication** - Detect and handle forwarded/embedded emails

### 15. Support Files

The complete system includes:

**Setup**
- `openqm_setup.py` - Creates OpenQM files and directory structure

**Core Modules**
- `openqm_interface.py` - Python ↔ OpenQM bridge
- `gmail_ingestion.py` - Gmail email retrieval
- `app.py` - Flask web application

**Templates**
- All HTML templates in `templates/` directory

**Configuration**
- `config/config.ini` - System settings
- `requirements.txt` - Python dependencies

---

## Quick Commands Reference

```bash
# Setup
python openqm_setup.py

# Ingest emails
python gmail_ingestion.py --max 100

# Start web server
python app.py

# Access dashboard
http://localhost:5000
```

---

**Built for Dr. Lawrence C. Sullivan**
*AI-Enhanced Email Management System v1.0*
