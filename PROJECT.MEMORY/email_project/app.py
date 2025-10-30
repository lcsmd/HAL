#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pathlib import Path
import secrets

from openqm_interface import OpenQMInterface, EmailRecord

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

BASE_DIR = Path('C:/email_management_system')
QM_ACCOUNT = 'EMAILSYS'

qm = OpenQMInterface(account=QM_ACCOUNT)
email_rec = EmailRecord(qm)


class EmailService:
    @staticmethod
    def get_emails(limit=50, offset=0, filters=None):
        criteria = ''
        if filters:
            if filters.get('sender'):
                criteria += f"WITH 1 LIKE '...{filters['sender']}...'"
            if filters.get('subject'):
                if criteria:
                    criteria += ' AND '
                criteria += f"WITH 8 LIKE '...{filters['subject']}...'"
                
        email_ids = qm.select_records('EMAILS', criteria)
        
        start = offset
        end = offset + limit
        page_ids = email_ids[start:end]
        
        emails = []
        for email_id in page_ids:
            email_data = email_rec.get(email_id)
            if email_data:
                emails.append(email_data)
                
        return {
            'emails': emails,
            'total': len(email_ids),
            'has_more': end < len(email_ids)
        }
    
    @staticmethod
    def get_email(email_id: str):
        email_data = email_rec.get(email_id)
        
        if email_data:
            body_id = email_data.get('body_id', '')
            if body_id:
                body_path = BASE_DIR / 'bodies' / f"{body_id}.bod"
                if body_path.exists():
                    with open(body_path, 'r', encoding='utf-8') as f:
                        email_data['body_content'] = f.read()
                        
        return email_data
    
    @staticmethod
    def get_statistics():
        config_data = qm.read_record('SYSTEM.CONFIG', 'COUNTERS')
        
        if config_data:
            return {
                'total_emails': config_data.get(1, 0),
                'total_threads': config_data.get(2, 0),
                'total_attachments': config_data.get(3, 0),
                'total_contacts': config_data.get(4, 0)
            }
            
        return {'total_emails': 0, 'total_threads': 0, 'total_attachments': 0, 'total_contacts': 0}


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/api/emails')
def api_emails():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    filters = {}
    if request.args.get('sender'):
        filters['sender'] = request.args.get('sender')
    if request.args.get('subject'):
        filters['subject'] = request.args.get('subject')
        
    result = EmailService.get_emails(limit=limit, offset=offset, filters=filters)
    return jsonify(result)


@app.route('/api/emails/<email_id>')
def api_email_detail(email_id):
    email = EmailService.get_email(email_id)
    
    if email:
        return jsonify(email)
    else:
        return jsonify({'error': 'Email not found'}), 404


@app.route('/api/stats')
def api_stats():
    stats = EmailService.get_statistics()
    return jsonify(stats)


@app.route('/emails')
def emails_page():
    return render_template('emails.html')


@app.route('/emails/<email_id>')
def email_detail_page(email_id):
    return render_template('email_detail.html', email_id=email_id)


if __name__ == '__main__':
    print("="*60)
    print("Web Server Starting")
    print("="*60)
    print(f"Base Directory: {BASE_DIR}")
    print(f"Access at: http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
