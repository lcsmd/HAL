# AI Classification System - Priority, Urgency, Categories & Notifications

## Overview

The AI Classification System analyzes data to make intelligent decisions about:

- **Priority** - HIGH, MEDIUM, LOW based on importance
- **Urgency** - URGENT, NORMAL, DEFER based on time sensitivity
- **Categories** - Intelligent categorization based on patterns
- **Notifications** - ALERT, NOTIFY, SILENT based on significance

## Philosophy

AI should handle the tedious work of analyzing patterns and making routine classification decisions, while escalating ambiguous or critical cases to humans.

## Use Cases

### 1. Transaction Classification

**Large Amounts**
- Threshold: 3x average or >$1000
- Priority: HIGH
- Notification: ALERT
- Message: "Large transaction: [Payee] - $[Amount]"

**Unusual Patterns**
- Amount 3x normal for vendor
- Urgency: URGENT
- Notification: ALERT
- Message: "Unusual amount for [Payee]: $[Amount]"

**New Vendors**
- First time seeing this payee
- Notification: ALERT (if >$100) or NOTIFY (if <$100)
- Message: "New vendor: [Payee] - $[Amount]"

**Duplicates**
- Same payee, amount, and date
- Urgency: URGENT
- Notification: ALERT
- Message: "Possible duplicate transaction"

**Category Assignment**
- Based on payee's default category
- Notification: SILENT (auto-apply)

### 2. Task Classification

**Overdue Tasks**
- Due date < today
- Urgency: URGENT
- Priority: HIGH
- Notification: ALERT
- Message: "OVERDUE: [Task Title]"

**Due Soon**
- Due within 1 day
- Urgency: URGENT
- Notification: ALERT
- Message: "DUE SOON: [Task Title]"

**Upcoming**
- Due within 7 days
- Priority: HIGH
- Notification: NOTIFY
- Message: "Upcoming: [Task] (due in X days)"

**Keyword-Based Priority**
- Title contains: urgent, critical, important, asap, emergency
- Priority: HIGH
- Notification: NOTIFY

### 3. Email Classification

**VIP Senders**
- From important contacts
- Priority: HIGH
- Notification: ALERT

**Urgent Keywords**
- Subject contains: urgent, asap, important, action required
- Urgency: URGENT
- Notification: ALERT

**Spam Indicators**
- Suspicious patterns
- Category: SPAM
- Notification: SILENT

## Confidence Levels

### High Confidence (≥ 90%)
- Clear, unambiguous criteria
- Auto-apply without user review
- Examples: Overdue tasks, exact duplicates, large amounts

### Medium Confidence (80-89%)
- Likely correct but worth reviewing
- Present to user for approval
- Examples: Unusual patterns, new vendors

### Low Confidence (< 80%)
- Ambiguous or uncertain
- Escalate to user for decision
- Examples: Complex categorization, edge cases

## Usage

### Analyze Transactions

```bash
# Analyze all transactions
python PY/ai_classifier.py analyze-transactions

# Analyze specific batch
python PY/ai_classifier.py analyze-transactions --batch-id 19876-123456
```

### Analyze Tasks

```bash
python PY/ai_classifier.py analyze-tasks
```

### Review Proposals

```bash
python PY/ai_classifier.py review-rules
```

Output shows:
- Classification type (PRIORITY, URGENCY, CATEGORY, NOTIFICATION)
- Target (TRANSACTION, TASK, EMAIL)
- Action and value
- Confidence score
- Notification level
- Reason for classification
- Number of affected records

### Apply Classifications

```bash
# Auto-apply high confidence (≥90%)
python PY/ai_classifier.py apply-rules

# Custom threshold
python PY/ai_classifier.py apply-rules --threshold 0.85
```

## Complete Workflow

### For Transactions

```bash
# 1. Import transactions
qm -kHAL -c"IMPORT.QUICKEN C:/Downloads/quicken.csv"

# 2. Analyze for classification
python PY/ai_classifier.py analyze-transactions

# 3. Auto-apply high confidence
python PY/ai_classifier.py apply-rules

# 4. Review proposals
python PY/ai_classifier.py review-rules

# 5. Check notifications
# (Would integrate with notification system)
```

### For Tasks

```bash
# 1. Analyze tasks
python PY/ai_classifier.py analyze-tasks

# 2. Auto-apply classifications
python PY/ai_classifier.py apply-rules

# 3. View urgent tasks
qm -kHAL -c"LIST TASK WITH URGENCY = 'URGENT'"

# 4. View high priority tasks
qm -kHAL -c"LIST TASK WITH PRIORITY = 'HIGH'"
```

## Classification Rules Format

Rules are saved in `config/classification_rules.json`:

```json
{
  "CLS20250124200000": {
    "type": "PRIORITY",
    "target": "TRANSACTION",
    "criteria": {
      "field": "AMOUNT",
      "operator": ">=",
      "value": 1000
    },
    "action": "SET_PRIORITY",
    "value": "HIGH",
    "notification": "ALERT",
    "notification_message": "Large transaction detected",
    "confidence": 0.90,
    "created_date": "20250124",
    "created_by": "AI",
    "status": "ACTIVE"
  }
}
```

## Notification Levels

### ALERT
- Immediate attention required
- Push notification
- Email alert
- SMS (optional)
- Examples: Large amounts, overdue tasks, duplicates

### NOTIFY
- Informational
- In-app notification
- Email digest
- Examples: New vendors, upcoming deadlines

### SILENT
- No notification
- Applied automatically
- Logged for audit
- Examples: Category assignment, routine classifications

## Integration Points

### With Transaction System

```python
# After importing transactions
proposals = classifier.analyze_transactions(batch_id)
classifier.save_proposals(proposals)
classifier.apply_proposals(auto_threshold=0.90)
```

### With Task System

```python
# Daily task analysis
proposals = classifier.analyze_tasks()
classifier.save_proposals(proposals)
classifier.apply_proposals(auto_threshold=0.95)
```

### With Notification System

```python
# Get pending notifications
notifications = classifier.get_pending_notifications()
for notif in notifications:
    if notif['level'] == 'ALERT':
        send_push_notification(notif['message'])
    elif notif['level'] == 'NOTIFY':
        add_to_digest(notif['message'])
```

## Decision Criteria Examples

### Transaction Priority

```python
HIGH:
- Amount >= $1000
- Amount >= 3x average
- New vendor with amount >= $500
- Reimbursable and amount >= $100

MEDIUM:
- Amount >= $500
- New vendor with amount < $500
- Category = "Business"

LOW:
- Amount < $500
- Known vendor
- Routine transaction
```

### Task Urgency

```python
URGENT:
- Due date < today (overdue)
- Due date <= today + 1 day
- Title contains urgent keywords
- Blocking other tasks

NORMAL:
- Due date <= today + 7 days
- Standard priority
- No dependencies

DEFER:
- Due date > today + 30 days
- Low priority
- Optional tasks
```

### Notification Triggers

```python
ALERT:
- Amount >= $1000
- Duplicate detected
- Task overdue
- Unusual pattern
- Security concern

NOTIFY:
- New vendor
- Task due soon (7 days)
- Category changed
- Rule applied

SILENT:
- Routine categorization
- Auto-standardization
- Background processing
```

## Advanced Features

### Multi-Criteria Classification

Combine multiple criteria:

```json
{
  "criteria": {
    "field": "AMOUNT",
    "operator": ">=",
    "value": 500,
    "and": {
      "field": "CATEGORY",
      "operator": "=",
      "value": "MEDICAL"
    }
  }
}
```

### Time-Based Rules

```json
{
  "criteria": {
    "field": "DUE_DATE",
    "operator": "<=",
    "value": "TODAY+7"
  }
}
```

### Pattern Matching

```json
{
  "criteria": {
    "field": "TITLE",
    "operator": "CONTAINS",
    "value": ["urgent", "critical", "asap"]
  }
}
```

## Escalation to User

AI escalates when:

1. **Low Confidence** - Unclear pattern or criteria
2. **Conflicting Rules** - Multiple rules apply with different results
3. **New Pattern** - First time seeing this combination
4. **High Impact** - Decision affects many records or critical data
5. **User Override** - Previous user decision contradicts AI suggestion

## User Feedback Loop

Your decisions train the system:

```
User approves HIGH priority → AI learns this pattern
User changes to MEDIUM → AI adjusts confidence
User rejects classification → AI learns to avoid
User creates manual rule → AI incorporates pattern
```

## Best Practices

### 1. Start Conservative

Begin with high thresholds:
- Priority: Only truly important items
- Urgency: Only time-critical items
- Notifications: Only actionable alerts

### 2. Monitor Results

Review classifications weekly:
```bash
python PY/ai_classifier.py review-rules
```

### 3. Adjust Thresholds

Fine-tune based on your needs:
- Too many alerts? Raise thresholds
- Missing important items? Lower thresholds
- Wrong categories? Review and correct

### 4. Provide Feedback

When AI gets it wrong:
- Reject the proposal
- Create correct classification
- AI learns from your decision

### 5. Iterate

Classification improves over time:
- Week 1: 70% accuracy, high review needed
- Month 1: 85% accuracy, moderate review
- Month 3: 95% accuracy, minimal review

## Troubleshooting

**Too many ALERT notifications**
- Raise alert thresholds
- Move some to NOTIFY level
- Review criteria specificity

**Missing important items**
- Lower confidence threshold
- Add more classification criteria
- Review escalated items

**Wrong categories assigned**
- Check payee default categories
- Review category rules
- Provide corrective feedback

**Duplicate classifications**
- AI may propose multiple rules for same pattern
- Review and consolidate
- Keep most specific rule

## Future Enhancements

1. **Machine Learning** - Train on historical decisions
2. **Context Awareness** - Consider time, location, patterns
3. **Predictive Classification** - Anticipate needs before they arise
4. **Smart Grouping** - Batch similar items for efficiency
5. **Adaptive Thresholds** - Automatically adjust based on feedback

## Integration with HAL

### Schema Extensions

Add classification fields to existing schemas:

```csv
PRIORITY,N,Priority level (1-5)
URGENCY,A,Urgency flag (URGENT/NORMAL/DEFER)
NOTIFICATION_LEVEL,A,Notification level
CLASSIFICATION_DATE,D,When classified
CLASSIFIED_BY,A,AI or USER
```

### QMBasic Programs

Create classification programs:

```
CLASSIFY.TRANSACTIONS - Apply classification rules
CLASSIFY.TASKS - Classify tasks by urgency
NOTIFY.ALERTS - Process pending notifications
```

### Reporting

```
LIST TRANSACTION WITH PRIORITY = "HIGH"
LIST TASK WITH URGENCY = "URGENT"
COUNT TRANSACTION BY NOTIFICATION.LEVEL
```

## Summary

The AI Classification System embodies the principle:

> **AI analyzes patterns → AI proposes classifications → Human reviews → System learns → Notifications trigger**

Result: **Smart, automated decision-making with human oversight for critical cases.**

---

**Version**: 1.0
**Last Updated**: 2025-01-24
**Requires**: Python 3.6+, QMClient
**Integrates with**: Transaction System, Task System, Notification System
