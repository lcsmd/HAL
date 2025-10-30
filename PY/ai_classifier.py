#!/usr/bin/env python3
"""
AI Classifier for HAL - Priority, Urgency, Categories, and Notifications

This module uses AI to analyze data and make intelligent decisions about:
- Priority levels (HIGH, MEDIUM, LOW)
- Urgency assessment (URGENT, NORMAL, DEFER)
- Category assignment
- Notification triggers (ALERT, NOTIFY, SILENT)

Philosophy:
1. AI analyzes patterns in historical data
2. AI proposes classification rules
3. AI escalates ambiguous cases to user
4. User decisions train the system

Usage:
    python PY/ai_classifier.py analyze-transactions [--batch-id BATCH_ID]
    python PY/ai_classifier.py analyze-tasks
    python PY/ai_classifier.py analyze-emails
    python PY/ai_classifier.py review-rules
    python PY/ai_classifier.py apply-rules [--auto]
"""

import sys
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from qmclient import QMClient
except ImportError:
    print("ERROR: QMClient not available")
    sys.exit(1)


class AIClassifier:
    """AI-assisted classification for priority, urgency, categories, and notifications"""
    
    def __init__(self, account="HAL"):
        self.qm = QMClient()
        self.qm.connect(account)
        self.rules_file = "config/classification_rules.json"
        self.proposals_file = "config/classification_proposals.json"
        
    def analyze_transactions(self, batch_id=None):
        """
        Analyze transactions to determine:
        - Priority (HIGH for large amounts, unusual vendors)
        - Urgency (URGENT for duplicates, fraud indicators)
        - Category refinement
        - Notification triggers (ALERT for large amounts, new vendors)
        """
        print("Analyzing transactions for classification...")
        
        query = "SELECT TRANSACTION"
        if batch_id:
            query += f" WITH IMPORT.BATCH.ID = '{batch_id}'"
        
        trans_list = self.qm.select("TRANSACTION", query)
        
        if not trans_list:
            print("No transactions found.")
            return []
        
        proposals = []
        
        # Analyze for various classification criteria
        proposals.extend(self._analyze_large_amounts(trans_list))
        proposals.extend(self._analyze_unusual_patterns(trans_list))
        proposals.extend(self._analyze_new_vendors(trans_list))
        proposals.extend(self._analyze_duplicates(trans_list))
        proposals.extend(self._analyze_category_patterns(trans_list))
        
        return proposals
    
    def _analyze_large_amounts(self, trans_list):
        """Identify transactions with unusually large amounts"""
        proposals = []
        amounts = []
        
        # Collect all amounts
        for trans_id in trans_list:
            trans = self.qm.read("TRANSACTION", trans_id)
            if trans:
                amount = float(trans.get(4, 0))
                amounts.append(amount)
        
        if not amounts:
            return proposals
        
        # Calculate statistics
        avg_amount = sum(amounts) / len(amounts)
        max_amount = max(amounts)
        
        # Threshold: 3x average or > $1000
        threshold = max(avg_amount * 3, 1000)
        
        # Find large transactions
        for trans_id in trans_list:
            trans = self.qm.read("TRANSACTION", trans_id)
            if trans:
                amount = float(trans.get(4, 0))
                payee = trans.get(3) or trans.get(2)
                
                if amount >= threshold:
                    proposals.append({
                        'type': 'PRIORITY',
                        'target': 'TRANSACTION',
                        'criteria': {
                            'field': 'AMOUNT',
                            'operator': '>=',
                            'value': threshold
                        },
                        'action': 'SET_PRIORITY',
                        'value': 'HIGH',
                        'confidence': 0.90,
                        'reason': f'Amount ${amount:.2f} exceeds threshold ${threshold:.2f}',
                        'notification': 'ALERT',
                        'notification_message': f'Large transaction: {payee} - ${amount:.2f}',
                        'examples': [trans_id]
                    })
        
        return proposals
    
    def _analyze_unusual_patterns(self, trans_list):
        """Identify unusual transaction patterns"""
        proposals = []
        
        # Group by payee and analyze frequency
        payee_transactions = defaultdict(list)
        
        for trans_id in trans_list:
            trans = self.qm.read("TRANSACTION", trans_id)
            if trans:
                payee = trans.get(3) or trans.get(2)
                date = trans.get(1)
                amount = float(trans.get(4, 0))
                
                payee_transactions[payee].append({
                    'id': trans_id,
                    'date': date,
                    'amount': amount
                })
        
        # Analyze each payee
        for payee, transactions in payee_transactions.items():
            if len(transactions) < 3:
                continue
            
            amounts = [t['amount'] for t in transactions]
            avg_amount = sum(amounts) / len(amounts)
            
            # Check for unusual amounts (3x average)
            for trans in transactions:
                if trans['amount'] >= avg_amount * 3:
                    proposals.append({
                        'type': 'URGENCY',
                        'target': 'TRANSACTION',
                        'criteria': {
                            'field': 'STANDARDIZED_PAYEE',
                            'operator': '=',
                            'value': payee,
                            'and': {
                                'field': 'AMOUNT',
                                'operator': '>=',
                                'value': avg_amount * 3
                            }
                        },
                        'action': 'SET_URGENCY',
                        'value': 'URGENT',
                        'confidence': 0.85,
                        'reason': f'Amount ${trans["amount"]:.2f} is 3x normal for {payee} (avg ${avg_amount:.2f})',
                        'notification': 'ALERT',
                        'notification_message': f'Unusual amount for {payee}: ${trans["amount"]:.2f}',
                        'examples': [trans['id']]
                    })
        
        return proposals
    
    def _analyze_new_vendors(self, trans_list):
        """Identify transactions with new/unknown vendors"""
        proposals = []
        
        # Get list of known payees
        known_payees = set()
        all_payees = self.qm.select("PAYEE")
        for payee_id in all_payees:
            payee_rec = self.qm.read("PAYEE", payee_id)
            if payee_rec:
                known_payees.add(payee_rec.get(1, ""))
        
        # Check transactions for new vendors
        for trans_id in trans_list:
            trans = self.qm.read("TRANSACTION", trans_id)
            if trans:
                payee = trans.get(3) or trans.get(2)
                amount = float(trans.get(4, 0))
                
                if payee and payee not in known_payees:
                    # New vendor - determine notification level
                    notification = 'ALERT' if amount >= 100 else 'NOTIFY'
                    
                    proposals.append({
                        'type': 'NOTIFICATION',
                        'target': 'TRANSACTION',
                        'criteria': {
                            'field': 'STANDARDIZED_PAYEE',
                            'operator': 'NOT_IN',
                            'value': 'KNOWN_PAYEES'
                        },
                        'action': 'NOTIFY',
                        'value': notification,
                        'confidence': 0.95,
                        'reason': f'New vendor: {payee}',
                        'notification': notification,
                        'notification_message': f'New vendor: {payee} - ${amount:.2f}',
                        'examples': [trans_id]
                    })
        
        return proposals
    
    def _analyze_duplicates(self, trans_list):
        """Identify potential duplicate transactions"""
        proposals = []
        
        # Group by payee, amount, and date
        transaction_groups = defaultdict(list)
        
        for trans_id in trans_list:
            trans = self.qm.read("TRANSACTION", trans_id)
            if trans:
                payee = trans.get(3) or trans.get(2)
                amount = float(trans.get(4, 0))
                date = trans.get(1)
                
                key = (payee, amount, date)
                transaction_groups[key].append(trans_id)
        
        # Find duplicates
        for key, trans_ids in transaction_groups.items():
            if len(trans_ids) > 1:
                payee, amount, date = key
                proposals.append({
                    'type': 'URGENCY',
                    'target': 'TRANSACTION',
                    'criteria': {
                        'field': 'DUPLICATE_CHECK',
                        'operator': 'SAME_PAYEE_AMOUNT_DATE',
                        'value': None
                    },
                    'action': 'SET_URGENCY',
                    'value': 'URGENT',
                    'confidence': 0.95,
                    'reason': f'Potential duplicate: {payee} - ${amount:.2f} on {date}',
                    'notification': 'ALERT',
                    'notification_message': f'Possible duplicate transaction: {payee} - ${amount:.2f}',
                    'examples': trans_ids
                })
        
        return proposals
    
    def _analyze_category_patterns(self, trans_list):
        """Analyze and suggest category assignments"""
        proposals = []
        
        # Analyze transactions without categories
        uncategorized = []
        
        for trans_id in trans_list:
            trans = self.qm.read("TRANSACTION", trans_id)
            if trans:
                category = trans.get(5)
                if not category or category == "":
                    uncategorized.append({
                        'id': trans_id,
                        'payee': trans.get(3) or trans.get(2),
                        'amount': float(trans.get(4, 0)),
                        'memo': trans.get(7, "")
                    })
        
        # Group by payee and suggest categories
        payee_categories = defaultdict(list)
        
        for trans in uncategorized:
            payee = trans['payee']
            
            # Check if this payee has a default category
            payee_rec = self._find_payee_by_name(payee)
            if payee_rec and payee_rec.get(3):  # DEFAULT_CATEGORY
                default_category = payee_rec.get(3)
                
                proposals.append({
                    'type': 'CATEGORY',
                    'target': 'TRANSACTION',
                    'criteria': {
                        'field': 'STANDARDIZED_PAYEE',
                        'operator': '=',
                        'value': payee,
                        'and': {
                            'field': 'CATEGORY',
                            'operator': '=',
                            'value': ''
                        }
                    },
                    'action': 'SET_CATEGORY',
                    'value': default_category,
                    'confidence': 0.90,
                    'reason': f'Payee {payee} typically categorized as {default_category}',
                    'notification': 'SILENT',
                    'examples': [trans['id']]
                })
        
        return proposals
    
    def _find_payee_by_name(self, payee_name):
        """Find payee record by name"""
        all_payees = self.qm.select("PAYEE")
        for payee_id in all_payees:
            payee_rec = self.qm.read("PAYEE", payee_id)
            if payee_rec and payee_rec.get(1) == payee_name:
                return payee_rec
        return None
    
    def analyze_tasks(self):
        """
        Analyze tasks to determine:
        - Priority (based on deadlines, dependencies)
        - Urgency (based on due dates)
        - Category (based on keywords, project)
        - Notification triggers (deadline approaching)
        """
        print("Analyzing tasks for classification...")
        
        task_list = self.qm.select("TASK")
        
        if not task_list:
            print("No tasks found.")
            return []
        
        proposals = []
        today = datetime.now().date()
        
        for task_id in task_list:
            task = self.qm.read("TASK", task_id)
            if not task:
                continue
            
            title = task.get(2, "")
            due_date_str = task.get(5, "")
            status = task.get(6, "")
            priority = task.get(7, "")
            
            # Skip completed tasks
            if status == "COMPLETED":
                continue
            
            # Parse due date
            if due_date_str:
                try:
                    # Assuming YYYYMMDD format
                    due_date = datetime.strptime(due_date_str, "%Y%m%d").date()
                    days_until_due = (due_date - today).days
                    
                    # Urgency based on due date
                    if days_until_due < 0:
                        # Overdue
                        proposals.append({
                            'type': 'URGENCY',
                            'target': 'TASK',
                            'criteria': {
                                'field': 'DUE_DATE',
                                'operator': '<',
                                'value': 'TODAY'
                            },
                            'action': 'SET_URGENCY',
                            'value': 'URGENT',
                            'confidence': 0.99,
                            'reason': f'Task overdue by {abs(days_until_due)} days',
                            'notification': 'ALERT',
                            'notification_message': f'OVERDUE: {title}',
                            'examples': [task_id]
                        })
                    elif days_until_due <= 1:
                        # Due today or tomorrow
                        proposals.append({
                            'type': 'URGENCY',
                            'target': 'TASK',
                            'criteria': {
                                'field': 'DUE_DATE',
                                'operator': '<=',
                                'value': 'TODAY+1'
                            },
                            'action': 'SET_URGENCY',
                            'value': 'URGENT',
                            'confidence': 0.95,
                            'reason': f'Task due in {days_until_due} day(s)',
                            'notification': 'ALERT',
                            'notification_message': f'DUE SOON: {title}',
                            'examples': [task_id]
                        })
                    elif days_until_due <= 7:
                        # Due within a week
                        proposals.append({
                            'type': 'PRIORITY',
                            'target': 'TASK',
                            'criteria': {
                                'field': 'DUE_DATE',
                                'operator': '<=',
                                'value': 'TODAY+7'
                            },
                            'action': 'SET_PRIORITY',
                            'value': 'HIGH',
                            'confidence': 0.85,
                            'reason': f'Task due in {days_until_due} days',
                            'notification': 'NOTIFY',
                            'notification_message': f'Upcoming: {title} (due in {days_until_due} days)',
                            'examples': [task_id]
                        })
                except ValueError:
                    pass
            
            # Priority based on keywords
            high_priority_keywords = ['urgent', 'critical', 'important', 'asap', 'emergency']
            if any(kw in title.lower() for kw in high_priority_keywords):
                proposals.append({
                    'type': 'PRIORITY',
                    'target': 'TASK',
                    'criteria': {
                        'field': 'TITLE',
                        'operator': 'CONTAINS',
                        'value': high_priority_keywords
                    },
                    'action': 'SET_PRIORITY',
                    'value': 'HIGH',
                    'confidence': 0.90,
                    'reason': f'Title contains priority keyword',
                    'notification': 'NOTIFY',
                    'notification_message': f'High priority task: {title}',
                    'examples': [task_id]
                })
        
        return proposals
    
    def save_proposals(self, proposals):
        """Save classification proposals for review"""
        os.makedirs(os.path.dirname(self.proposals_file), exist_ok=True)
        
        # Load existing
        existing = []
        if os.path.exists(self.proposals_file):
            with open(self.proposals_file, 'r') as f:
                existing = json.load(f)
        
        # Add new proposals (avoid duplicates)
        for proposal in proposals:
            proposal['created_date'] = datetime.now().isoformat()
            proposal['status'] = 'pending'
            
            # Check for duplicates
            duplicate = False
            for exist in existing:
                if (exist.get('type') == proposal['type'] and
                    exist.get('criteria') == proposal['criteria'] and
                    exist.get('value') == proposal['value']):
                    duplicate = True
                    break
            
            if not duplicate:
                existing.append(proposal)
        
        # Save
        with open(self.proposals_file, 'w') as f:
            json.dump(existing, f, indent=2)
        
        print(f"Saved {len(proposals)} classification proposals")
        return self.proposals_file
    
    def review_proposals(self, pending_only=True):
        """Display proposals for user review"""
        if not os.path.exists(self.proposals_file):
            print("No proposals found.")
            return []
        
        with open(self.proposals_file, 'r') as f:
            proposals = json.load(f)
        
        if pending_only:
            proposals = [p for p in proposals if p.get('status') == 'pending']
        
        if not proposals:
            print("No pending proposals.")
            return []
        
        print(f"\n{'='*80}")
        print(f"CLASSIFICATION PROPOSALS FOR REVIEW ({len(proposals)} pending)")
        print(f"{'='*80}\n")
        
        for i, proposal in enumerate(proposals, 1):
            self._display_proposal(i, proposal)
        
        return proposals
    
    def _display_proposal(self, index, proposal):
        """Display a single proposal"""
        print(f"Proposal #{index}")
        print(f"  Type: {proposal['type']}")
        print(f"  Target: {proposal['target']}")
        print(f"  Action: {proposal['action']} = {proposal['value']}")
        print(f"  Confidence: {proposal['confidence']:.2%}")
        print(f"  Notification: {proposal.get('notification', 'SILENT')}")
        if proposal.get('notification_message'):
            print(f"  Message: {proposal['notification_message']}")
        print(f"  Reason: {proposal['reason']}")
        print(f"  Examples: {len(proposal.get('examples', []))} record(s)")
        print()
    
    def apply_proposals(self, auto_threshold=0.90):
        """Apply classification proposals"""
        if not os.path.exists(self.proposals_file):
            print("No proposals found.")
            return
        
        with open(self.proposals_file, 'r') as f:
            proposals = json.load(f)
        
        pending = [p for p in proposals if p.get('status') == 'pending']
        
        if not pending:
            print("No pending proposals.")
            return
        
        applied = 0
        for proposal in pending:
            if proposal['confidence'] >= auto_threshold:
                self._apply_classification(proposal)
                proposal['status'] = 'applied'
                proposal['applied_date'] = datetime.now().isoformat()
                applied += 1
        
        # Save updated proposals
        with open(self.proposals_file, 'w') as f:
            json.dump(proposals, f, indent=2)
        
        print(f"Applied {applied} high-confidence classifications (>= {auto_threshold:.0%})")
    
    def _apply_classification(self, proposal):
        """Apply a classification to matching records"""
        # This would update records based on criteria
        # For now, just create a classification rule
        rule_id = f"CLS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        rule_rec = {
            'type': proposal['type'],
            'target': proposal['target'],
            'criteria': json.dumps(proposal['criteria']),
            'action': proposal['action'],
            'value': proposal['value'],
            'notification': proposal.get('notification', 'SILENT'),
            'notification_message': proposal.get('notification_message', ''),
            'confidence': proposal['confidence'],
            'created_date': datetime.now().strftime("%Y%m%d"),
            'created_by': 'AI',
            'status': 'ACTIVE'
        }
        
        # Save to classification rules file
        self._save_classification_rule(rule_id, rule_rec)
        print(f"Created classification rule: {rule_id}")
    
    def _save_classification_rule(self, rule_id, rule_rec):
        """Save classification rule to file"""
        os.makedirs(os.path.dirname(self.rules_file), exist_ok=True)
        
        rules = {}
        if os.path.exists(self.rules_file):
            with open(self.rules_file, 'r') as f:
                rules = json.load(f)
        
        rules[rule_id] = rule_rec
        
        with open(self.rules_file, 'w') as f:
            json.dump(rules, f, indent=2)
    
    def close(self):
        """Close QM connection"""
        self.qm.disconnect()


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    classifier = AIClassifier()
    
    try:
        if command == "analyze-transactions":
            batch_id = None
            if "--batch-id" in sys.argv:
                idx = sys.argv.index("--batch-id")
                if idx + 1 < len(sys.argv):
                    batch_id = sys.argv[idx + 1]
            
            proposals = classifier.analyze_transactions(batch_id)
            if proposals:
                classifier.save_proposals(proposals)
                print(f"\nGenerated {len(proposals)} classification proposals")
        
        elif command == "analyze-tasks":
            proposals = classifier.analyze_tasks()
            if proposals:
                classifier.save_proposals(proposals)
                print(f"\nGenerated {len(proposals)} task classification proposals")
        
        elif command == "review-rules":
            classifier.review_proposals()
        
        elif command == "apply-rules":
            threshold = 0.90
            if "--threshold" in sys.argv:
                idx = sys.argv.index("--threshold")
                if idx + 1 < len(sys.argv):
                    threshold = float(sys.argv[idx + 1])
            
            classifier.apply_proposals(threshold)
        
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
    
    finally:
        classifier.close()


if __name__ == "__main__":
    main()
