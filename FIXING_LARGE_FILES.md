# Fixing Large Files Issue

**Problem**: Git history contains files too large for GitHub (LIES/ has 4GB files)

---

## 🚨 The Issue

GitHub rejected the push because:
- `LIES/%0` - 4,008 MB (4 GB!)
- `LIES/%1` - 4,054 MB (4 GB!)
- `UPLOADS/*.zip` - 94 MB
- `LCS.TXT/conversations.json` - 93 MB

Even though these are in `.gitignore`, they're **already in git history** from previous commits.

---

## ✅ Solution: Rewrite Git History

We need to remove these files from **all commits** in git history.

### Option 1: Automated Script (Recommended)

```powershell
.\fix_large_files.ps1
```

This will:
1. Install git-filter-repo (if needed)
2. Remove LIES/, LCS.TXT/, UPLOADS/ from all commits
3. Force push cleaned history to GitHub

---

### Option 2: Manual Steps

#### Step 1: Install git-filter-repo

```powershell
pip install git-filter-repo
```

#### Step 2: Remove directories from history

```powershell
# Remove LIES/ from all commits
git filter-repo --path LIES/ --invert-paths --force

# Remove LCS.TXT/ from all commits  
git filter-repo --path LCS.TXT/ --invert-paths --force

# Remove UPLOADS/ from all commits
git filter-repo --path UPLOADS/ --invert-paths --force
```

#### Step 3: Re-add remote and push

```powershell
# filter-repo removes remotes for safety
git remote add origin https://github.com/lcsmd/hal.git

# Force push the cleaned history
git push -u origin main --force
```

---

### Option 3: BFG Repo Cleaner (Alternative)

```powershell
# Download BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# Remove folders
java -jar bfg.jar --delete-folders LIES
java -jar bfg.jar --delete-folders LCS.TXT
java -jar bfg.jar --delete-folders UPLOADS

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push
git push -u origin main --force
```

---

## ⚠️ Important Notes

### This Rewrites History

- All commit SHAs will change
- Anyone who cloned the repo needs to re-clone
- Cannot be undone easily

### Files Remain Locally

- Files still exist on your computer in `C:\qmsys\hal\`
- Only removed from git tracking
- Already protected by `.gitignore`

### Why This Happened

These directories were committed before being added to `.gitignore`:
```gitignore
# Already in .gitignore (but were committed before)
LIES/
LCS.TXT/
UPLOADS/
```

---

## 🔍 Verify Before Pushing

After cleaning:

```powershell
# Check repository size
git count-objects -vH

# Check what will be pushed
git log --oneline -10

# Verify large files are gone
git ls-files | Select-String "LIES|LCS.TXT|UPLOADS"
```

Should return empty (no results).

---

## 📊 Expected Results

### Before Cleanup
- Repository size: ~1.5 GB
- 6,302 objects
- Files: LIES/, LCS.TXT/, UPLOADS/ in history

### After Cleanup
- Repository size: ~50-100 MB
- Fewer objects (large files removed)
- Files: Gone from all commits

---

## 🎯 Quick Command

Just run this:

```powershell
pip install git-filter-repo
git filter-repo --path LIES/ --invert-paths --force
git filter-repo --path LCS.TXT/ --invert-paths --force
git filter-repo --path UPLOADS/ --invert-paths --force
git remote add origin https://github.com/lcsmd/hal.git
git push -u origin main --force
```

---

## 🚨 Troubleshooting

### Error: "git-filter-repo not found"

```powershell
# Install with pip
pip install git-filter-repo

# Or download standalone
# https://github.com/newren/git-filter-repo/
```

### Error: "Remote origin already exists"

```powershell
git remote remove origin
git remote add origin https://github.com/lcsmd/hal.git
```

### Error: "Failed to push"

Check GitHub repository isn't protected:
- Go to: https://github.com/lcsmd/hal/settings/branches
- Ensure no branch protection rules on `main`

---

## ✅ After Successful Push

1. Visit: https://github.com/lcsmd/hal
2. Check repository size (should be much smaller)
3. Verify DOCS/, BP/, PY/ are present
4. Verify LIES/, LCS.TXT/, UPLOADS/ are absent

---

## 📝 What Gets Pushed

### ✅ Included (Code & Docs)
- BP/ - OpenQM programs
- PY/ - Python scripts
- DOCS/ - Documentation (80+ files)
- SCHEMA/ - Database schema
- mac_deployment_package/
- Configuration files
- README.md

### ❌ Excluded (Large Files)
- LIES/ - 8+ GB files
- LCS.TXT/ - 93 MB+ files
- UPLOADS/ - 94 MB+ files
- All .log files
- Python cache

---

**Ready?** Run:

```powershell
.\fix_large_files.ps1
```

Or manually:
```powershell
pip install git-filter-repo
git filter-repo --path LIES/ --invert-paths --force
git filter-repo --path LCS.TXT/ --invert-paths --force
git filter-repo --path UPLOADS/ --invert-paths --force
git remote add origin https://github.com/lcsmd/hal.git
git push -u origin main --force
```

---

**Last Updated**: 2025-11-27  
**Status**: Ready to clean and push
