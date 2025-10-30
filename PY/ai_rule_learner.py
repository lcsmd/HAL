#!/usr/bin/env python3
"""
AI Rule Learner for HAL Transaction System

This module analyzes transactions that don't match existing rules and uses AI
to propose new rules or modifications to existing rules. It follows the principle:

1. AI analyzes unmatched data
2. AI creates/modifies/deletes rules based on patterns
3. AI escalates ambiguous cases to user for resolution
4. User decisions feed back into the learning system

Usage:
    python PY/ai_rule_learner.py analyze [--batch-id BATCH_ID] [--confidence 0.8]
    python PY/ai_rule_learner.py review [--pending-only]
    python PY/ai_rule_learner.py apply [--rule-id RULE_ID]
"""

import sys
import os
import json
from datetime import datetime
from collections import defaultdict
import re

# Add QM bin directory to path for QMClient
sys.path.insert(0, "C:\\QMSYS\\bin")

try:
    import qmclient as qm
except ImportError:
    print("ERROR: QMClient not available")
    print("Make sure qmclient.py is in C:\\QMSYS\\bin")
    sys.exit(1)


class AIRuleLearner:
    """AI-assisted rule learning for transaction processing"""
    
    def __init__(self, account="HAL"):
        # Connect to QM using qmclient module
        self.session = qm.Connect('localhost', 4243, account, '', '')
        if not self.session:
            raise Exception("Failed to connect to QM")
        self.confidence_threshold = 0.8
        
    def analyze_unmatched_transactions(self, batch_id=None):
        """
        Analyze transactions that don't match any rules.
        Returns proposed rules with confidence scores.
        """
        print("Analyzing unmatched transactions...")
        
        # Get transactions without standardized payees
        query = "SELECT TRANSACTION WITH STANDARDIZED.PAYEE = ''"
        if batch_id:
            query += f" AND IMPORT.BATCH.ID = '{batch_id}'"
        
        trans_list = self.qm.select("TRANSACTION", query)
        
        if not trans_list:
            print("No unmatched transactions found.")
            return []
        
        print(f"Found {len(trans_list)} unmatched transactions")
        
        # Group by similar patterns
        patterns = self._extract_patterns(trans_list)
        
        # Generate rule proposals
        proposals = []
        for pattern_group in patterns:
            proposal = self._generate_rule_proposal(pattern_group)
            if proposal:
                proposals.append(proposal)
        
        return proposals
    
    def _extract_patterns(self, trans_list):
        """
        Extract patterns from unmatched transactions.
        Groups similar payee names together.
        """
        # Group by cleaned payee name
        groups = defaultdict(list)
        
        for trans_id in trans_list:
            trans = self.qm.read("TRANSACTION", trans_id)
            if trans:
                original_payee = trans.get(2, "")  # ORIGINAL_PAYEE
                
                # Clean and normalize
                cleaned = self._clean_payee_name(original_payee)
                
                groups[cleaned].append({
                    'id': trans_id,
                    'original': original_payee,
                    'cleaned': cleaned,
                    'amount': trans.get(4, 0),
                    'category': trans.get(5, ""),
                    'memo': trans.get(7, ""),
                    'date': trans.get(1, "")
                })
        
        # Convert to list of pattern groups
        pattern_groups = []
        for cleaned_name, transactions in groups.items():
            if len(transactions) >= 2:  # Only if pattern appears multiple times
                pattern_groups.append({
                    'cleaned_name': cleaned_name,
                    'transactions': transactions,
                    'count': len(transactions),
                    'variations': list(set([t['original'] for t in transactions]))
                })
        
        # Sort by frequency
        pattern_groups.sort(key=lambda x: x['count'], reverse=True)
        
        return pattern_groups
    
    def _clean_payee_name(self, payee):
        """Clean and normalize payee name for pattern matching"""
        if not payee:
            return ""
        
        # Convert to uppercase
        cleaned = payee.upper()
        
        # Remove common suffixes
        suffixes = [
            r'#\d+',           # #123
            r'\d{3,}',         # 000, 1234
            r'- PURCHASE',
            r'- PAYMENT',
            r'\*+',            # ***
            r'\.COM',
            r'\.NET',
            r'\.ORG',
            r'\s+INC\.?',
            r'\s+LLC\.?',
            r'\s+CORP\.?',
            r'\s+CO\.?',
        ]
        
        for suffix in suffixes:
            cleaned = re.sub(suffix, '', cleaned)
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned.strip()
    
    def _generate_rule_proposal(self, pattern_group):
        """
        Generate a rule proposal based on a pattern group.
        Uses heuristics to determine rule type and confidence.
        """
        cleaned_name = pattern_group['cleaned_name']
        transactions = pattern_group['transactions']
        variations = pattern_group['variations']
        count = pattern_group['count']
        
        # Determine rule type based on variation analysis
        if len(variations) == 1:
            # Exact match - all variations are identical
            rule_type = "EXACT.MATCH"
            pattern = variations[0]
            confidence = 0.95
        elif all(v.upper().startswith(cleaned_name[:5]) for v in variations if len(cleaned_name) >= 5):
            # All start with same prefix
            rule_type = "STARTS.WITH"
            pattern = cleaned_name[:min(len(cleaned_name), 10)]
            confidence = 0.90
        else:
            # Contains pattern
            rule_type = "PAYEE.MATCH"
            pattern = cleaned_name
            confidence = 0.85
        
        # Adjust confidence based on frequency
        if count >= 10:
            confidence += 0.05
        elif count >= 5:
            confidence += 0.02
        
        # Determine standard name (use most common variation or cleaned name)
        standard_name = cleaned_name.title()
        
        # Check for reimbursable patterns
        reimbursable_keywords = ['MEDICAL', 'PHARMACY', 'DOCTOR', 'HOSPITAL', 'CVS', 'WALGREENS']
        is_reimbursable = any(kw in cleaned_name for kw in reimbursable_keywords)
        
        proposal = {
            'rule_type': rule_type,
            'pattern': pattern,
            'standard_name': standard_name,
            'confidence': min(confidence, 0.99),  # Cap at 0.99
            'transaction_count': count,
            'variations': variations,
            'sample_transactions': transactions[:5],  # First 5 as examples
            'is_reimbursable': is_reimbursable,
            'status': 'pending',
            'created_date': datetime.now().isoformat(),
            'reason': self._generate_reason(pattern_group, rule_type)
        }
        
        return proposal
    
    def _generate_reason(self, pattern_group, rule_type):
        """Generate human-readable reason for the rule proposal"""
        count = pattern_group['count']
        variations = len(pattern_group['variations'])
        
        reason = f"Found {count} transactions with {variations} variation(s) of this payee. "
        
        if rule_type == "EXACT.MATCH":
            reason += "All instances are identical - exact match recommended."
        elif rule_type == "STARTS.WITH":
            reason += "All instances start with the same prefix - starts-with match recommended."
        else:
            reason += "Variations detected - contains match recommended."
        
        return reason
    
    def save_proposals(self, proposals, filename="config/rule_proposals.json"):
        """Save rule proposals to file for review"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Load existing proposals
        existing = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing = json.load(f)
        
        # Add new proposals
        for proposal in proposals:
            # Check if similar proposal already exists
            duplicate = False
            for existing_prop in existing:
                if (existing_prop['pattern'] == proposal['pattern'] and 
                    existing_prop['rule_type'] == proposal['rule_type']):
                    duplicate = True
                    break
            
            if not duplicate:
                existing.append(proposal)
        
        # Save
        with open(filename, 'w') as f:
            json.dump(existing, f, indent=2)
        
        print(f"Saved {len(proposals)} proposals to {filename}")
        return filename
    
    def review_proposals(self, pending_only=True):
        """Display proposals for user review"""
        filename = "config/rule_proposals.json"
        
        if not os.path.exists(filename):
            print("No proposals found.")
            return
        
        with open(filename, 'r') as f:
            proposals = json.load(f)
        
        if pending_only:
            proposals = [p for p in proposals if p.get('status') == 'pending']
        
        if not proposals:
            print("No pending proposals.")
            return
        
        print(f"\n{'='*80}")
        print(f"RULE PROPOSALS FOR REVIEW ({len(proposals)} pending)")
        print(f"{'='*80}\n")
        
        for i, proposal in enumerate(proposals, 1):
            self._display_proposal(i, proposal)
        
        return proposals
    
    def _display_proposal(self, index, proposal):
        """Display a single proposal"""
        print(f"Proposal #{index}")
        print(f"  Rule Type: {proposal['rule_type']}")
        print(f"  Pattern: {proposal['pattern']}")
        print(f"  Standard Name: {proposal['standard_name']}")
        print(f"  Confidence: {proposal['confidence']:.2%}")
        print(f"  Transactions: {proposal['transaction_count']}")
        print(f"  Variations: {', '.join(proposal['variations'][:3])}")
        if len(proposal['variations']) > 3:
            print(f"              ... and {len(proposal['variations']) - 3} more")
        print(f"  Reason: {proposal['reason']}")
        
        if proposal.get('is_reimbursable'):
            print(f"  ** Potentially reimbursable **")
        
        print()
    
    def apply_proposal(self, proposal_index=None, auto_apply_threshold=None):
        """
        Apply a rule proposal to the RULE file.
        
        If auto_apply_threshold is set, automatically applies proposals
        with confidence >= threshold.
        """
        filename = "config/rule_proposals.json"
        
        if not os.path.exists(filename):
            print("No proposals found.")
            return
        
        with open(filename, 'r') as f:
            proposals = json.load(f)
        
        pending = [p for p in proposals if p.get('status') == 'pending']
        
        if not pending:
            print("No pending proposals.")
            return
        
        # Auto-apply high confidence rules
        if auto_apply_threshold:
            applied = 0
            for proposal in pending:
                if proposal['confidence'] >= auto_apply_threshold:
                    self._create_rule_from_proposal(proposal)
                    proposal['status'] = 'applied'
                    proposal['applied_date'] = datetime.now().isoformat()
                    applied += 1
            
            # Save updated proposals
            with open(filename, 'w') as f:
                json.dump(proposals, f, indent=2)
            
            print(f"Auto-applied {applied} high-confidence rules (>= {auto_apply_threshold:.0%})")
            return
        
        # Manual apply specific proposal
        if proposal_index is not None:
            if 1 <= proposal_index <= len(pending):
                proposal = pending[proposal_index - 1]
                self._display_proposal(proposal_index, proposal)
                
                response = input("Apply this rule? (Y/N): ").strip().upper()
                if response == 'Y':
                    self._create_rule_from_proposal(proposal)
                    proposal['status'] = 'applied'
                    proposal['applied_date'] = datetime.now().isoformat()
                    
                    # Save updated proposals
                    with open(filename, 'w') as f:
                        json.dump(proposals, f, indent=2)
                    
                    print("Rule applied successfully!")
                else:
                    print("Rule not applied.")
            else:
                print(f"Invalid proposal index: {proposal_index}")
    
    def _create_rule_from_proposal(self, proposal):
        """Create a RULE record from a proposal"""
        rule_id = f"AI{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        rule_rec = {}
        rule_rec[1] = proposal['rule_type']           # RULE_TYPE
        rule_rec[2] = proposal['pattern']             # PATTERN
        rule_rec[3] = "STANDARDIZE"                   # ACTION
        rule_rec[4] = proposal['standard_name']       # TARGET_VALUE
        rule_rec[5] = 20                              # PRIORITY (AI rules get medium priority)
        rule_rec[6] = "Y"                             # ACTIVE_FLAG
        rule_rec[7] = datetime.now().strftime("%Y%m%d")  # CREATED_DATE
        rule_rec[9] = "AI"                            # CREATED_BY
        rule_rec[10] = f"AI-generated: {proposal['reason']}"  # DESCRIPTION
        
        self.qm.write("RULE", rule_id, rule_rec)
        print(f"Created rule: {rule_id}")
        
        # If reimbursable, create reimbursement rule too
        if proposal.get('is_reimbursable'):
            reimb_rule_id = f"AIR{datetime.now().strftime('%Y%m%d%H%M%S')}"
            reimb_rec = {}
            reimb_rec[1] = "PAYEE.MATCH"
            reimb_rec[2] = proposal['pattern']
            reimb_rec[3] = "TAG.REIMBURSABLE"
            reimb_rec[4] = "MEDICAL.EXPENSE"
            reimb_rec[5] = 20
            reimb_rec[6] = "Y"
            reimb_rec[7] = datetime.now().strftime("%Y%m%d")
            reimb_rec[9] = "AI"
            reimb_rec[10] = "AI-generated reimbursable rule"
            
            self.qm.write("RULE", reimb_rule_id, reimb_rec)
            print(f"Created reimbursement rule: {reimb_rule_id}")
    
    def close(self):
        """Close QM connection"""
        self.qm.disconnect()


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    learner = AIRuleLearner()
    
    try:
        if command == "analyze":
            # Parse options
            batch_id = None
            confidence = 0.8
            
            for i, arg in enumerate(sys.argv[2:]):
                if arg == "--batch-id" and i + 1 < len(sys.argv) - 2:
                    batch_id = sys.argv[i + 3]
                elif arg == "--confidence" and i + 1 < len(sys.argv) - 2:
                    confidence = float(sys.argv[i + 3])
            
            learner.confidence_threshold = confidence
            proposals = learner.analyze_unmatched_transactions(batch_id)
            
            if proposals:
                learner.save_proposals(proposals)
                print(f"\nGenerated {len(proposals)} rule proposals")
                print("Review with: python PY/ai_rule_learner.py review")
            else:
                print("No patterns found requiring new rules")
        
        elif command == "review":
            pending_only = "--all" not in sys.argv
            learner.review_proposals(pending_only)
        
        elif command == "apply":
            if "--auto" in sys.argv:
                # Auto-apply high confidence rules
                threshold = 0.90
                for i, arg in enumerate(sys.argv):
                    if arg == "--threshold" and i + 1 < len(sys.argv):
                        threshold = float(sys.argv[i + 1])
                
                learner.apply_proposal(auto_apply_threshold=threshold)
            else:
                # Manual apply
                if "--rule-id" in sys.argv:
                    idx = sys.argv.index("--rule-id")
                    if idx + 1 < len(sys.argv):
                        rule_index = int(sys.argv[idx + 1])
                        learner.apply_proposal(rule_index)
                else:
                    print("Specify --rule-id <index> or --auto")
        
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)
    
    finally:
        learner.close()


if __name__ == "__main__":
    main()
