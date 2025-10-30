# Transaction System Quick Start

## 5-Minute Setup

### 1. Build the Schema (1 minute)

```bash
qm -kHAL
```

At the QM prompt:

```
:BUILD.SCHEMA
```

Wait for completion. You should see:
- Processing TRANSACTION (trn)...
- Processing PAYEE (pye)...
- Processing RULE (rul)...
- Processing REIMBURSEMENT (rmb)...
- Processing IMPORT_LOG (iml)...

### 2. Compile Programs (2 minutes)

```
:BASIC BP IMPORT.QUICKEN
:BASIC BP STANDARDIZE.PAYEES
:BASIC BP TAG.REIMBURSABLE
:BASIC BP MANAGE.RULES
:BASIC BP REPORT.REIMBURSABLE
```

### 3. Catalog Programs (1 minute)

```
:CATALOG BP IMPORT.QUICKEN
:CATALOG BP STANDARDIZE.PAYEES
:CATALOG BP TAG.REIMBURSABLE
:CATALOG BP MANAGE.RULES
:CATALOG BP REPORT.REIMBURSABLE
```

Answer "Y" to remove from local catalog for each.

### 4. Load Sample Rules (1 minute)

```
:MANAGE.RULES
```

- Select option **8** (Import sample rules)
- Select option **9** (Exit)

## First Import

### Export from Quicken

1. Open Quicken
2. Go to **File > Export > Export to CSV**
3. Select your account(s)
4. Choose date range
5. Save to a known location (e.g., `C:\Downloads\quicken.csv`)

### Import to HAL

```
:IMPORT.QUICKEN C:/Downloads/quicken.csv
```

Note the **Batch ID** shown (e.g., `19876-123456`)

### Process Transactions

```
:STANDARDIZE.PAYEES 19876-123456
:TAG.REIMBURSABLE 19876-123456
```

### View Results

```
:REPORT.REIMBURSABLE SUMMARY
```

## Common Commands

### Import new transactions
```
:IMPORT.QUICKEN C:/path/to/file.csv
```

### Process all unprocessed transactions
```
:STANDARDIZE.PAYEES
:TAG.REIMBURSABLE
```

### View reimbursable summary
```
:REPORT.REIMBURSABLE SUMMARY
```

### View detailed list
```
:REPORT.REIMBURSABLE DETAIL
```

### Query transactions
```
:LIST TRANSACTION WITH REIMBURSABLE.FLAG = "Y"
:LIST TRANSACTION WITH TRANS.DATE >= "20250101"
:COUNT TRANSACTION BY STANDARDIZED.PAYEE
```

### Manage rules
```
:MANAGE.RULES
```

## Typical Workflow

**Monthly processing:**

1. Export from Quicken
2. Import: `:IMPORT.QUICKEN C:/Downloads/quicken.csv`
3. Note batch ID
4. Standardize: `:STANDARDIZE.PAYEES [batch_id]`
5. Tag: `:TAG.REIMBURSABLE [batch_id]`
6. Report: `:REPORT.REIMBURSABLE BATCH [batch_id]`

**Review and adjust:**

1. `:MANAGE.RULES` - Add/edit rules as needed
2. Re-run standardization and tagging
3. Generate final report

## Need Help?

See full documentation: `README_TRANSACTION_SYSTEM.md`

## Troubleshooting

**"Cannot open TRANSACTION file"**
→ Run `:BUILD.SCHEMA` first

**"Program not found"**
→ Run `:CATALOG BP [programname]`

**"No fields mapped"**
→ Check CSV has header row with standard field names (Date, Payee, Amount, etc.)

**"Date conversion failed"**
→ Ensure dates are MM/DD/YYYY, MM/DD/YY, or YYYY-MM-DD format
