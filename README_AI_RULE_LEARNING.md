# AI-Assisted Rule Learning System

## Philosophy

The AI Rule Learner embodies a key principle: **AI should analyze data, propose intelligent heuristics, and escalate ambiguity to humans.**

### The Learning Loop

```
┌─────────────────────────────────────────────────────────────┐
│  1. New Data Arrives (transactions)                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Apply Existing Rules                                    │
│     - Match patterns                                        │
│     - Standardize payees                                    │
│     - Tag reimbursable                                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Identify Unmatched Data                                 │
│     - Transactions without standardized payees              │
│     - Patterns not covered by rules                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  4. AI Analyzes Patterns                                    │
│     - Group similar payee names                             │
│     - Extract common patterns                               │
│     - Calculate confidence scores                           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  5. AI Proposes Rules                                       │
│     - EXACT.MATCH for identical names                       │
│     - STARTS.WITH for common prefixes                       │
│     - PAYEE.MATCH for contains patterns                     │
│     - Confidence score for each proposal                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├─────────────────┬──────────────────────────┐
                 │                 │                          │
                 ▼                 ▼                          ▼
┌────────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│ High Confidence    │  │ Medium           │  │ Low Confidence       │
│ (>= 90%)           │  │ Confidence       │  │ (< 80%)              │
│                    │  │ (80-90%)         │  │                      │
│ AUTO-APPLY         │  │ USER REVIEW      │  │ ESCALATE TO USER     │
└────────────────────┘  └──────────────────┘  └──────────────────────┘
         │                       │                        │
         └───────────────────────┴────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ 6. Apply Approved Rules│
                    └────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ 7. Re-process Data     │
                    └────────────────────────┘
```

## How It Works

### 1. Pattern Detection

The AI analyzes unmatched transactions and groups them by similarity:

- Cleans payee names (removes numbers, suffixes, etc.)
- Groups variations together
- Counts frequency of each pattern
- Identifies common prefixes and substrings

### 2. Rule Generation

For each pattern group, the AI proposes a rule:

**EXACT.MATCH** - When all variations are identical
- Example: "CVS PHARMACY" appears 10 times exactly
- Confidence: 95%

**STARTS.WITH** - When all variations start the same way
- Example: "AMAZON.COM #123", "AMAZON.COM #456", "AMAZON.COM #789"
- Pattern: "AMAZON"
- Confidence: 90%

**PAYEE.MATCH** - When variations contain common substring
- Example: "WALGREENS #123", "WALGREENS STORE", "WALGREENS PHARMACY"
- Pattern: "WALGREENS"
- Confidence: 85%

### 3. Confidence Scoring

Confidence is calculated based on:

- **Pattern consistency** - How similar are the variations?
- **Frequency** - How many times does this pattern appear?
- **Clarity** - Is the pattern unambiguous?

Adjustments:
- +5% if pattern appears 10+ times
- +2% if pattern appears 5-9 times
- Capped at 99% (never 100% - always room for human override)

### 4. Decision Thresholds

**High Confidence (≥ 90%)**
- Auto-apply without user intervention
- Clear, unambiguous patterns
- High frequency

**Medium Confidence (80-89%)**
- Present to user for review
- Likely correct but worth checking
- User can approve/reject/modify

**Low Confidence (< 80%)**
- Flag for user attention
- Ambiguous or rare patterns
- Requires human judgment

### 5. Reimbursable Detection

AI also detects potentially reimbursable transactions:

Keywords: MEDICAL, PHARMACY, DOCTOR, HOSPITAL, CVS, WALGREENS, etc.

When detected, AI proposes TWO rules:
1. Payee standardization rule
2. Reimbursement tagging rule

## Usage

### Analyze Unmatched Transactions

After importing transactions:

```bash
python PY/ai_rule_learner.py analyze
```

With specific batch:

```bash
python PY/ai_rule_learner.py analyze --batch-id 19876-123456
```

With custom confidence threshold:

```bash
python PY/ai_rule_learner.py analyze --confidence 0.85
```

### Review Proposals

```bash
python PY/ai_rule_learner.py review
```

This displays all pending proposals with:
- Rule type and pattern
- Confidence score
- Number of transactions affected
- Sample variations
- AI's reasoning

### Apply Rules

**Auto-apply high confidence rules (≥ 90%):**

```bash
python PY/ai_rule_learner.py apply --auto
```

**Auto-apply with custom threshold:**

```bash
python PY/ai_rule_learner.py apply --auto --threshold 0.85
```

**Manually apply specific rule:**

```bash
python PY/ai_rule_learner.py apply --rule-id 3
```

You'll be prompted to confirm before applying.

## Complete Workflow

### Initial Setup

1. Import transactions
2. Run AI analysis
3. Review proposals
4. Apply approved rules
5. Re-run standardization

```bash
# Import
qm -kHAL -c"IMPORT.QUICKEN C:/Downloads/quicken.csv"

# AI analysis
python PY/ai_rule_learner.py analyze

# Review proposals
python PY/ai_rule_learner.py review

# Auto-apply high confidence
python PY/ai_rule_learner.py apply --auto

# Review medium confidence
python PY/ai_rule_learner.py review

# Apply specific rules
python PY/ai_rule_learner.py apply --rule-id 1
python PY/ai_rule_learner.py apply --rule-id 3

# Re-run standardization with new rules
qm -kHAL -c"STANDARDIZE.PAYEES"
```

### Ongoing Use

After each import:

```bash
# Import new transactions
qm -kHAL -c"IMPORT.QUICKEN C:/Downloads/new_transactions.csv"

# Let AI learn from unmatched
python PY/ai_rule_learner.py analyze

# Auto-apply high confidence
python PY/ai_rule_learner.py apply --auto

# Review and apply medium confidence
python PY/ai_rule_learner.py review
python PY/ai_rule_learner.py apply --rule-id X

# Process with updated rules
qm -kHAL -c"STANDARDIZE.PAYEES"
qm -kHAL -c"TAG.REIMBURSABLE"
```

## Proposal File Format

Proposals are saved in `config/rule_proposals.json`:

```json
{
  "rule_type": "STARTS.WITH",
  "pattern": "AMAZON",
  "standard_name": "Amazon.com",
  "confidence": 0.92,
  "transaction_count": 15,
  "variations": [
    "AMAZON.COM #123",
    "AMAZON.COM #456",
    "AMAZON MARKETPLACE"
  ],
  "sample_transactions": [...],
  "is_reimbursable": false,
  "status": "pending",
  "created_date": "2025-01-24T20:00:00",
  "reason": "Found 15 transactions with 3 variations..."
}
```

## Human Oversight

### When AI Escalates

AI escalates to you when:

1. **Low confidence** (< 80%) - Pattern is ambiguous
2. **Conflicting patterns** - Multiple possible interpretations
3. **New vendor types** - First time seeing this category
4. **Edge cases** - Unusual transaction characteristics

### Your Role

You provide:

1. **Judgment** - Is this rule correct?
2. **Context** - Business knowledge AI doesn't have
3. **Corrections** - Modify AI proposals
4. **Feedback** - Reject incorrect proposals

### Feedback Loop

Your decisions train the system:

- **Approved rules** → AI learns what patterns work
- **Rejected rules** → AI learns what to avoid
- **Modified rules** → AI learns refinements
- **Manual rules** → AI learns from your examples

## Advanced Features

### Pattern Cleaning

AI automatically cleans payee names:

- Removes transaction numbers (#123, 000, etc.)
- Removes suffixes (- PURCHASE, - PAYMENT)
- Removes corporate designators (INC, LLC, CORP)
- Removes domain extensions (.COM, .NET)
- Normalizes whitespace

### Variation Analysis

AI groups variations intelligently:

```
"AMAZON.COM #123"     ┐
"AMAZON.COM #456"     ├─→ Pattern: "AMAZON"
"AMAZON MARKETPLACE"  ┘    Type: STARTS.WITH
                           Confidence: 92%
```

### Frequency Weighting

More frequent patterns get higher confidence:

- 10+ occurrences: +5% confidence
- 5-9 occurrences: +2% confidence
- 2-4 occurrences: Base confidence

### Reimbursable Detection

AI detects medical/reimbursable keywords and proposes both:
1. Standardization rule
2. Reimbursement tagging rule

## Integration with HAL

### QMClient Integration

Uses QMClient for database access:
- Reads TRANSACTION records
- Writes RULE records
- Maintains data integrity

### Schema Compliance

Generated rules follow HAL schema:
- Proper field positions
- Correct data types
- Standard naming conventions

### Audit Trail

All AI-generated rules include:
- Created date
- Created by: "AI"
- Description with reasoning
- Link to proposal data

## Best Practices

### 1. Start Conservative

Begin with high threshold (90%+):

```bash
python PY/ai_rule_learner.py apply --auto --threshold 0.90
```

### 2. Review Regularly

Check proposals weekly:

```bash
python PY/ai_rule_learner.py review
```

### 3. Monitor Results

After applying rules, check:

```bash
qm -kHAL -c"LIST RULE WITH CREATED.BY = 'AI'"
```

### 4. Refine Iteratively

- Apply high confidence rules immediately
- Review medium confidence weekly
- Manually handle low confidence

### 5. Trust but Verify

- AI is good at patterns
- You're good at context
- Together = optimal results

## Troubleshooting

**No proposals generated**
- All transactions already matched by existing rules
- Run after importing new data

**Low confidence scores**
- Payee names are highly variable
- Consider manual rule creation
- Or wait for more data

**Incorrect proposals**
- Reject the proposal
- Create manual rule with correct pattern
- AI will learn from your rule

**Too many proposals**
- Increase confidence threshold
- Focus on high-frequency patterns first

## Future Enhancements

Potential additions:

1. **Machine Learning** - Train on historical decisions
2. **Category Prediction** - Suggest transaction categories
3. **Anomaly Detection** - Flag unusual transactions
4. **Budget Forecasting** - Predict future expenses
5. **Duplicate Detection** - Identify duplicate transactions
6. **Vendor Consolidation** - Merge similar vendors

## Philosophy in Action

This system embodies the principle:

> **AI analyzes → AI proposes → Human decides → System learns**

- AI handles the tedious pattern analysis
- AI proposes intelligent rules
- You provide judgment and context
- System improves over time

The result: **Less manual work, better accuracy, continuous improvement.**

---

**Version**: 1.0
**Last Updated**: 2025-01-24
**Requires**: Python 3.6+, QMClient
