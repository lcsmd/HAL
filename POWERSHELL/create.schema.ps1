# Create CATEGORY.csv
@"
 FieldName,FieldNum,Type,Description,Required,Indexed
CATEGORY_NAME,1,A,Category display name,Y,Y
PARENT_CATEGORY_KEY,2,A,Parent category key (hierarchical),N,Y
CATEGORY_LEVEL,3,N,Hierarchy level (1-4),N,N
DEFAULT_REIMB_PCT,4,N,Default reimbursement percentage,N,N
TAG_KEYS,5,M,Associated tag keys (multivalued),N,Y
DESCRIPTION,6,T,Category description,N,N
ACTIVE_FLAG,7,A,Y/N active flag,N,N
CREATED_DATE,8,D,Date created,N,N
USAGE_COUNT,9,N,Number of transactions,N,N
"@ | Out-File -FilePath "SCHEMA\CATEGORY.csv" -Encoding ASCII

# Create TAG.csv
@"
 FieldName,FieldNum,Type,Description,Required,Indexed
TAG_NAME,1,A,Tag display name,Y,Y
TAG_TYPE,2,A,Type (REIMB/CATEGORY/PAYEE/CUSTOM),N,Y
REIMB_PERCENTAGE,3,N,Reimbursement percentage if applicable,N,N
COLOR,4,A,Display color code,N,N
ICON,5,A,Icon name,N,N
DESCRIPTION,6,T,Tag description,N,N
ACTIVE_FLAG,7,A,Y/N active flag,N,N
CREATED_DATE,8,D,Date created,N,N
USAGE_COUNT,9,N,Number of uses,N,N
"@ | Out-File -FilePath "SCHEMA\TAG.csv" -Encoding ASCII

Write-Host "Created CATEGORY.csv and TAG.csv"
