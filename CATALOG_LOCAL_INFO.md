# Using CATALOG LOCAL in OpenQM

**Why you should use CATALOG LOCAL for account-specific programs**

---

## 🎯 The Difference

### CATALOG (Global)
```tcl
CATALOG BP PROGRAM
```
- Catalogs to **global** system directory
- Available to **all accounts**
- Requires **administrative privileges** on some systems
- Can conflict with system programs

### CATALOG LOCAL (Account-Specific)
```tcl
CATALOG BP PROGRAM LOCAL
```
- Catalogs to **account-specific** directory
- Available only in **current account** (HAL)
- No special privileges needed
- No conflicts with other accounts
- **Recommended best practice**

---

## ✅ When to Use CATALOG LOCAL

**Use LOCAL for**:
- ✅ Account-specific utilities (VIEW.DOC, FIND.DOC)
- ✅ Custom programs for one application
- ✅ Development and testing
- ✅ Programs that reference account data
- ✅ Any HAL-specific programs

**Use GLOBAL (no LOCAL) for**:
- ⚠️ System-wide utilities needed everywhere
- ⚠️ Administrative tools
- ⚠️ Shared utilities across accounts
- ⚠️ When explicitly required by documentation

---

## 📁 Where Programs Get Cataloged

### Without LOCAL (Global)
```
C:\qmsys\gcat\            (Windows)
/usr/qmsys/gcat/          (Linux)
```
- Shared across all OpenQM accounts
- Requires write permission to system directory

### With LOCAL (Account-Specific)
```
C:\qmsys\hal\cat\         (Windows - in account directory)
/usr/qmsys/hal/cat/       (Linux - in account directory)
```
- Private to HAL account
- No system permission issues
- Clean separation

---

## 🔧 Correct Commands for HAL Programs

### Documentation Viewer Programs

```tcl
LOGTO HAL

* Compile
BASIC BP VIEW.DOC
BASIC BP FIND.DOC
BASIC BP TEST.DOC.ACCESS

* Catalog LOCAL (correct)
CATALOG BP VIEW.DOC LOCAL
CATALOG BP FIND.DOC LOCAL
CATALOG BP TEST.DOC.ACCESS LOCAL

* Run (works because we're in HAL account)
VIEW.DOC
FIND.DOC medication
TEST.DOC.ACCESS
```

---

## ⚠️ What Happens Without LOCAL

### Problem
```tcl
CATALOG BP VIEW.DOC    * No LOCAL keyword
```

**Possible issues**:
1. May fail with permission error
2. May overwrite existing global program with same name
3. May not be found when running from HAL account
4. Makes program available to accounts that shouldn't access it

### Solution
```tcl
CATALOG BP VIEW.DOC LOCAL    * With LOCAL keyword
```

**Benefits**:
1. Always works (no permission issues)
2. No conflicts with other accounts
3. Clearly scoped to HAL account
4. Proper isolation

---

## 🧪 Testing Catalog Location

### Check Where Program is Cataloged

```tcl
* List local catalog
LIST.CATALOG LOCAL

* List global catalog (may require admin)
LIST.CATALOG

* View catalog entry details
ED $CATALOGUE VIEW.DOC
* Shows full path to cataloged program
```

### Verify LOCAL Catalog Works

```tcl
LOGTO HAL
CATALOG BP VIEW.DOC LOCAL
* Try to run
VIEW.DOC
* If menu appears, LOCAL catalog worked correctly
```

---

## 📊 Comparison Matrix

| Aspect | CATALOG | CATALOG LOCAL |
|--------|---------|---------------|
| **Scope** | All accounts | Current account only |
| **Location** | C:\qmsys\gcat\ | C:\qmsys\hal\cat\ |
| **Permissions** | May need admin | Always works |
| **Conflicts** | Possible | None |
| **Best Practice** | Rarely | Default choice |
| **Isolation** | No | Yes |
| **Maintenance** | System-wide | Account-specific |

---

## 🎯 HAL Programs - All Should Use LOCAL

All HAL-specific programs should be cataloged with LOCAL:

```tcl
LOGTO HAL

* Password management
CATALOG BP PASSWORD.MENU LOCAL
CATALOG BP PASSWORD.ADD LOCAL
CATALOG BP PASSWORD.VIEW LOCAL
CATALOG BP PASSWORD.SEARCH LOCAL

* Medical programs  
CATALOG BP MEDICATION.MENU LOCAL
CATALOG BP MEDICAL.MENU LOCAL

* Financial programs
CATALOG BP MANAGE.RULES LOCAL
CATALOG BP REPORT.REIMBURSABLE LOCAL
CATALOG BP TAG.REIMBURSABLE LOCAL
CATALOG BP STANDARDIZE.PAYEES LOCAL

* Documentation programs
CATALOG BP VIEW.DOC LOCAL
CATALOG BP FIND.DOC LOCAL
CATALOG BP TEST.DOC.ACCESS LOCAL

* Voice system
CATALOG BP VOICE.LISTENER LOCAL
CATALOG BP VOICE.HANDLE.MEDICATION LOCAL

* Schema programs
CATALOG BP SCHEMA.MANAGER LOCAL
CATALOG BP BUILD.SCHEMA LOCAL
```

---

## 🔍 Finding Cataloged Programs

### List All Local Programs in HAL
```tcl
LOGTO HAL
LIST.CATALOG LOCAL
```

### Search for Specific Program
```tcl
* Check if VIEW.DOC is cataloged locally
SSELECT $CATALOGUE WITH @ID = "VIEW.DOC"
LIST $CATALOGUE
```

### View Program Details
```tcl
* Show catalog entry
ED $CATALOGUE VIEW.DOC
* Shows path, compilation date, etc.
```

---

## 🚨 Common Mistakes

### ❌ WRONG: Cataloging without LOCAL
```tcl
CATALOG BP VIEW.DOC
* May fail or cause conflicts
```

### ✅ RIGHT: Always use LOCAL for account programs
```tcl
CATALOG BP VIEW.DOC LOCAL
* Correct - account-specific
```

### ❌ WRONG: Trying to run global from wrong account
```tcl
LOGTO OTHER.ACCOUNT
VIEW.DOC
* Fails - program is LOCAL to HAL
```

### ✅ RIGHT: Run from correct account
```tcl
LOGTO HAL
VIEW.DOC
* Works - we're in the account where it's cataloged
```

---

## 📝 Standard Practice for HAL

**All future programs should**:
1. Be compiled in HAL account: `LOGTO HAL`
2. Be cataloged with LOCAL: `CATALOG BP PROGRAM LOCAL`
3. Be documented with LOCAL: Include in comments
4. Be tested in HAL account

---

## 🔧 Fixing Existing Catalogs

### If Program Was Cataloged Without LOCAL

```tcl
* Remove old global catalog (if you have permission)
DELETE.CATALOG PROGRAM

* Or just recatalog with LOCAL (overrides for account)
LOGTO HAL
CATALOG BP PROGRAM LOCAL

* Verify
LIST.CATALOG LOCAL
* Should show PROGRAM in list
```

---

## 📚 Related Commands

```tcl
* Catalog program locally
CATALOG BP PROGRAM LOCAL

* Catalog subroutine locally
CATALOG BP SUBROUTINE LOCAL

* Remove from local catalog
DELETE.CATALOG PROGRAM LOCAL

* List local catalog
LIST.CATALOG LOCAL

* List global catalog
LIST.CATALOG

* View catalog entry
ED $CATALOGUE PROGRAM
```

---

## ✅ Best Practices Summary

1. **Always use LOCAL** for account-specific programs
2. **Document it** in program headers
3. **Test locally** after cataloging
4. **List catalog** to verify
5. **Stay organized** - LOCAL keeps things clean

---

## 🎯 All HAL Documentation Programs

**Corrected catalog commands**:

```tcl
LOGTO HAL

BASIC BP VIEW.DOC
CATALOG BP VIEW.DOC LOCAL

BASIC BP FIND.DOC
CATALOG BP FIND.DOC LOCAL

BASIC BP TEST.DOC.ACCESS
CATALOG BP TEST.DOC.ACCESS LOCAL
```

**Status**: ✅ All documentation updated to use LOCAL

---

**Remember**: When in doubt, use LOCAL! It's safer, cleaner, and the recommended practice for application-specific programs.

---

**Last Updated**: 2025-11-27  
**Applies To**: All HAL OpenQM BASIC programs  
**Status**: MANDATORY - Always use CATALOG LOCAL for HAL programs
