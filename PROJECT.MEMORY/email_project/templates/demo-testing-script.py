#!/usr/bin/env python3
"""
Demo & Testing Script
Demonstrates system capabilities and runs integration tests
"""

import sys
from pathlib import Path
from datetime import datetime
import random

# Import our modules
from openqm_interface import OpenQMInterface, EmailRecord
from rule_engine import RuleEngine


class EmailSystemDemo:
    """Demonstration and testing of email management system"""
    
    def __init__(self, qm_account='EMAILSYS'):
        self.qm = OpenQMInterface(account=qm_account)
        self.email_rec = EmailRecord(self.qm)
        self.rule_engine = RuleEngine(qm_account=qm_account)
        
        print("="*60)
        print("Email Management System - Demo & Testing")
        print("="*60)
        print()
    
    def test_openqm_connection(self):
        """Test OpenQM database connection"""
        print("1. Testing OpenQM Connection")
        print("-" * 40)
        
        try:
            # Try to read system config
            config = self.qm.read_record('SYSTEM.CONFIG', 'COUNTERS')
            
            if config:
                print("✓ OpenQM connection successful")
                print(f"  Email count: {config.get(1, 0)}")
                print(f"  Thread count: {config.get(2, 0)}")
                print(f"  Attachment count: {config.get(3, 0)}")
                return True
            else:
                print("✗ Could not read system config")
                return False
                
        except Exception as e:
            print(f"✗ OpenQM connection failed: {e}")
            return False
    
    def create_sample_emails(self, count=10):
        """Create sample emails for testing"""
        print(f"\n2. Creating {count} Sample Emails")
        print("-" * 40)
        
        senders = [
            'john.doe@example.com',
            'jane.smith@company.com',
            'support@github.com',
            'newsletter@marketing.com',
            'boss@work.com',
            'friend@personal.com',
            'invoice@finance.com',
            'alert@security.com'
        ]
        
        subjects = [
            'Quarterly Report Review',
            'Team Meeting Tomorrow',
            'Invoice #12345',
            'Weekly Newsletter',
            'Project Update: Q4',
            'Urgent: Security Alert',
            'Coffee next week?',
            'GitHub: Pull request merged',
            'Monthly Statement',
            'Re: Budget Approval'
        ]
        
        created = []
        
        for i in range(count):
            sender = random.choice(senders)
            subject = random.choice(subjects)
            
            email_data = {
                'from': sender,
                'to': ['recipient@example.com'],
                'subject': f"{subject} #{i+1}",
                'date_sent': datetime.now().isoformat(),
                'body_id': f'SAMPLE{i:05d}',
                'format': 'text',
                'attachments': [],
                'categories': [],
                'priority': random.randint(1, 10)
            }
            
            email_id = self.email_rec.create(email_data)
            
            if email_id:
                created.append(email_id)
                print(f"  ✓ Created: {email_id} - {subject}")
        
        print(f"\n✓ Created {len(created)} sample emails")
        return created
    
    def create_sample_categories(self):
        """Create sample categories"""
        print("\n3. Creating Sample Categories")
        print("-" * 40)
        
        categories = [
            ('Work', 'Work-related emails'),
            ('Personal', 'Personal correspondence'),
            ('Finance', 'Bills, invoices, financial'),
            ('Newsletters', 'Marketing and newsletters'),
            ('Important', 'High priority items'),
            ('Development', 'Code and technical discussions')
        ]
        
        created = []
        
        for name, description in categories:
            cat_id = f"CAT{self.qm.get_next_id('CATEGORY.COUNT'):06d}"
            
            record = {
                1: name,
                2: '',
                3: '',
                4: 0,
                5: description
            }
            
            if self.qm.write_record('CATEGORIES', cat_id, record):
                created.append((cat_id, name))
                print(f"  ✓ Created: {name} ({cat_id})")
        
        print(f"\n✓ Created {len(created)} categories")
        return created
    
    def create_sample_rules(self, categories):
        """Create sample rules"""
        print("\n4. Creating Sample Rules")
        print("-" * 40)
        
        # Get category IDs by name
        cat_map = {name: cat_id for cat_id, name in categories}
        
        rules = [
            ('domain', 'github.com', [cat_map.get('Development')], 'GitHub notifications'),
            ('domain', 'company.com', [cat_map.get('Work')], 'Company emails'),
            ('subject', 'invoice', [cat_map.get('Finance')], 'Invoice emails'),
            ('subject', 'newsletter', [cat_map.get('Newsletters')], 'Newsletter emails'),
            ('subject', 'urgent', [cat_map.get('Important')], 'Urgent emails'),
            ('sender', 'boss@work.com', [cat_map.get('Work'), cat_map.get('Important')], 'Emails from boss')
        ]
        
        created = []
        
        for rule_type, pattern, cats, description in rules:
            # Filter out None categories
            cats = [c for c in cats if c]
            
            if cats:
                rule_id = self.rule_engine.create_rule(
                    rule_type=rule_type,
                    pattern=pattern,
                    categories=cats,
                    prefix=self.rule_engine.PREFIX_USER,
                    description=description
                )
                
                if rule_id:
                    created.append(rule_id)
                    print(f"  ✓ Created: {description} ({rule_id})")
        
        print(f"\n✓ Created {len(created)} rules")
        return created
    
    def test_rule_application(self):
        """Test applying rules to emails"""
        print("\n5. Testing Rule Application")
        print("-" * 40)
        
        stats = self.rule_engine.apply_rules_to_all_emails(verbose=False)
        
        print(f"  Emails processed: {stats['emails_processed']}")
        print(f"  Rules applied: {stats['rules_applied']}")
        print(f"  Categories added: {stats['categories_added']}")
        print(f"  Emails with matches: {stats['emails_with_matches']}")
        
        print("\n✓ Rule application test complete")
        return stats
    
    def display_categorized_emails(self):
        """Display categorized emails"""
        print("\n6. Displaying Categorized Emails")
        print("-" * 40)
        
        email_ids = self.qm.select_records('EMAILS', '')
        
        categorized = []
        uncategorized = []
        
        for email_id in email_ids:
            email = self.email_rec.get(email_id)
            if email:
                cats = email.get('categories', [])
                if cats and len(cats) > 0:
                    categorized.append(email)
                else:
                    uncategorized.append(email)
        
        print(f"\nCategorized: {len(categorized)} emails")
        print(f"Uncategorized: {len(uncategorized)} emails")
        
        if categorized:
            print("\nSample categorized emails:")
            for email in categorized[:5]:
                cats = email.get('categories', [])
                
                # Get category names
                cat_names = []
                for cat_id in cats:
                    cat_data = self.qm.read_record('CATEGORIES', cat_id)
                    if cat_data:
                        cat_names.append(cat_data.get(1, ''))
                
                print(f"  • {email['subject'][:40]}")
                print(f"    From: {email['from']}")
                print(f"    Categories: {', '.join(cat_names)}")
        
        print("\n✓ Display complete")
    
    def test_email_retrieval(self):
        """Test retrieving emails"""
        print("\n7. Testing Email Retrieval")
        print("-" * 40)
        
        email_ids = self.qm.select_records('EMAILS', '')
        
        if not email_ids:
            print("✗ No emails found")
            return False
        
        # Test retrieving a random email
        test_id = random.choice(email_ids)
        email = self.email_rec.get(test_id)
        
        if email:
            print(f"✓ Successfully retrieved email: {test_id}")
            print(f"  Subject: {email['subject']}")
            print(f"  From: {email['from']}")
            print(f"  Date: {email.get('date_sent', 'N/A')}")
            return True
        else:
            print(f"✗ Failed to retrieve email: {test_id}")
            return False
    
    def display_system_stats(self):
        """Display system statistics"""
        print("\n8. System Statistics")
        print("-" * 40)
        
        config = self.qm.read_record('SYSTEM.CONFIG', 'COUNTERS')
        
        if config:
            print(f"Total Emails: {config.get(1, 0)}")
            print(f"Total Threads: {config.get(2, 0)}")
            print(f"Total Attachments: {config.get(3, 0)}")
            print(f"Total Contacts: {config.get(4, 0)}")
        
        # Category count
        cat_ids = self.qm.select_records('CATEGORIES', '')
        print(f"Total Categories: {len(cat_ids)}")
        
        # Rule count
        rules = self.rule_engine.get_all_rules()
        print(f"Total Rules: {len(rules)}")
        
        # Rule statistics
        if rules:
            total_applications = sum(r['applied_count'] for r in rules)
            print(f"Total Rule Applications: {total_applications}")
            
            print("\nTop 3 Rules by Usage:")
            sorted_rules = sorted(rules, key=lambda r: r['applied_count'], reverse=True)
            for rule in sorted_rules[:3]:
                desc = rule['parameters'].get('description', rule['id'])
                print(f"  • {desc}: {rule['applied_count']} applications")
        
        print("\n✓ Statistics displayed")
    
    def run_full_demo(self):
        """Run complete demonstration"""
        print("\nRunning Full System Demo")
        print("="*60)
        
        # Test connection
        if not self.test_openqm_connection():
            print("\n✗ OpenQM connection failed. Please check your setup.")
            return False
        
        # Create sample data
        email_ids = self.create_sample_emails(count=20)
        categories = self.create_sample_categories()
        rules = self.create_sample_rules(categories)
        
        # Test rule application
        self.test_rule_application()
        
        # Display results
        self.display_categorized_emails()
        self.test_email_retrieval()
        self.display_system_stats()
        
        print("\n" + "="*60)
        print("Demo Complete!")
        print("="*60)
        print()
        print("Next steps:")
        print("  1. Start the web interface: ./start_web.sh")
        print("  2. Visit: http://localhost:5000")
        print("  3. Import real emails: ./ingest_emails.sh")
        print("  4. Try AI categorization from the web interface")
        print()
        
        return True
    
    def cleanup_demo_data(self):
        """Clean up demo data"""
        print("\nCleaning Up Demo Data")
        print("-" * 40)
        
        response = input("This will delete all sample data. Continue? (yes/no): ")
        
        if response.lower() != 'yes':
            print("Cleanup cancelled")
            return
        
        # Delete sample emails
        email_ids = self.qm.select_records('EMAILS', '')
        for email_id in email_ids:
            if email_id.startswith('E'):
                self.qm.delete_record('EMAILS', email_id)
        
        # Delete categories
        cat_ids = self.qm.select_records('CATEGORIES', '')
        for cat_id in cat_ids:
            self.qm.delete_record('CATEGORIES', cat_id)
        
        # Delete rules
        rule_ids = self.qm.select_records('RULES', '')
        for rule_id in rule_ids:
            self.qm.delete_record('RULES', rule_id)
        
        print("✓ Demo data cleaned up")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Email System Demo & Testing')
    parser.add_argument('--account', default='EMAILSYS', help='OpenQM account')
    parser.add_argument('--cleanup', action='store_true', help='Clean up demo data')
    parser.add_argument('--test-only', action='store_true', help='Only test connection')
    
    args = parser.parse_args()
    
    demo = EmailSystemDemo(qm_account=args.account)
    
    if args.cleanup:
        demo.cleanup_demo_data()
    elif args.test_only:
        demo.test_openqm_connection()
    else:
        demo.run_full_demo()


if __name__ == '__main__':
    main()
