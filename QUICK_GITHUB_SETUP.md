# Quick GitHub Setup - 3 Steps

**The fastest way to create the repository and push to GitHub**

---

## 🚀 Automated Method (Recommended)

### Step 1: Run the Script

```cmd
cd C:\qmsys\hal
create_and_push_to_github.cmd
```

This script will:
1. Authenticate you with GitHub (opens browser)
2. Create the repository `lcsmd/hal`
3. Push all commits

**Time**: 2-3 minutes

---

## 🖱️ Manual Method (If Script Fails)

### Step 1: Authenticate (30 seconds)

```cmd
gh auth login
```

Follow the prompts:
1. Choose: **GitHub.com**
2. Choose: **HTTPS**
3. Choose: **Login with a web browser**
4. Copy the one-time code
5. Press Enter (opens browser)
6. Paste code and authorize

---

### Step 2: Create Repository (10 seconds)

```cmd
cd C:\qmsys\hal
gh repo create lcsmd/hal --private --source=. --remote=origin --description "HAL Personal AI Assistant - OpenQM database with medical, financial, and voice interface"
```

This creates a **private** repository.

For **public** repository, use:
```cmd
gh repo create lcsmd/hal --public --source=. --remote=origin --description "HAL Personal AI Assistant - OpenQM database with medical, financial, and voice interface"
```

---

### Step 3: Push (30 seconds)

```cmd
git push -u origin main
```

**Done!** Visit: https://github.com/lcsmd/hal

---

## ✅ What Gets Pushed

**17 commits** including:
- Complete DOCS/ organization (80+ files)
- Mac/Windows deployment guides
- OpenQM BASIC programs (VIEW.DOC, FIND.DOC, TEST.DOC.ACCESS)
- Network troubleshooting guides
- All source code (BP/, PY/ directories)
- Database schema
- Configuration files

**Total**: ~500 files, ~50MB

---

## 🔍 Verify It Worked

After pushing:

```cmd
# Check remote
git remote -v

# Check what's on GitHub
git fetch
git log origin/main --oneline -5

# Open in browser
gh repo view --web
```

---

## 🚨 Troubleshooting

### Error: "gh: command not found"

**Solution**: GitHub CLI not in PATH, use full path:
```cmd
"C:\Program Files\GitHub CLI\gh.exe" auth login
```

### Error: "Authentication failed"

**Solution**: Try web browser authentication:
```cmd
gh auth login -w
```

### Error: "Repository already exists"

**Solution**: Just push directly:
```cmd
git push -u origin main
```

### Error: "Permission denied"

**Solution**: Check you're authenticated:
```cmd
gh auth status
```

If not:
```cmd
gh auth login
```

---

## 🎯 Quick Command Summary

```cmd
# One-time setup
gh auth login

# Create repo and push
cd C:\qmsys\hal
gh repo create lcsmd/hal --private --source=. --remote=origin
git push -u origin main

# Verify
gh repo view --web
```

---

## 📝 After Repository is Created

### Clone on Another Machine

```bash
# HTTPS
git clone https://github.com/lcsmd/hal.git

# SSH (if configured)
git clone git@github.com:lcsmd/hal.git
```

### Update README on GitHub

The README.md will automatically display on the repository home page.

### Add Collaborators

```cmd
gh repo add-collaborator lcsmd/hal USERNAME
```

---

## 🔐 Repository Settings

After creation, consider:

1. **Branch Protection**:
   ```cmd
   gh api repos/lcsmd/hal/branches/main/protection -X PUT -f "required_status_checks[strict]=true"
   ```

2. **Topics** (tags for discovery):
   ```cmd
   gh repo edit lcsmd/hal --add-topic openqm --add-topic personal-assistant --add-topic voice-interface
   ```

3. **About Section**:
   Visit: https://github.com/lcsmd/hal/settings

---

## ✅ Success Indicators

You'll know it worked when:

✓ `gh repo view --web` opens your repository  
✓ https://github.com/lcsmd/hal shows your files  
✓ README.md is displayed on the home page  
✓ All commits are visible in history  
✓ DOCS/ directory structure is intact  

---

## 🎉 Next Steps After Push

1. **Verify on GitHub**: https://github.com/lcsmd/hal
2. **Clone on Mac**: 
   ```bash
   git clone https://github.com/lcsmd/hal.git ~/Documents/hal
   ```
3. **Set up branch protection** (optional)
4. **Add repository topics** (optional)
5. **Invite collaborators** (if needed)

---

**Ready?**

Run:
```cmd
create_and_push_to_github.cmd
```

Or manually:
```cmd
gh auth login
gh repo create lcsmd/hal --private --source=. --remote=origin
git push -u origin main
```

---

**Last Updated**: 2025-11-27  
**Estimated Time**: 2-3 minutes total  
**Success Rate**: 99% with GitHub CLI
