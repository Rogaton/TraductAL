# GitHub Setup Guide - TraductAL

**How to publish TraductAL to GitHub**

---

## Prerequisites

- [x] Code fixes completed (hardcoded paths removed)
- [x] .gitignore updated
- [ ] Your information added (see YOUR_INFO_HERE.md)
- [ ] Basic testing done (optional but recommended)

---

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website (Easier)

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `TraductAL` (or `traductal` lowercase)
   - **Description**: "Multilingual translation system - 65+ languages, 100% offline, hybrid neural-symbolic"
   - **Public** (recommended) or Private
   - **Do NOT** initialize with README (you already have one)
3. Click "Create repository"

### Option B: Via GitHub CLI (If you have gh installed)

```bash
cd /home/aldn/TraductAL/TraductAL
gh repo create TraductAL --public --source=. --remote=origin --push
```

---

## Step 2: Prepare Local Repository

### A. Check Current Git Status

```bash
cd /home/aldn/TraductAL/TraductAL

# See what's in git currently
git status

# See your git history
git log --oneline -10
```

### B. Stage All New Files

```bash
# Add all new documentation
git add COMMERCIAL_LICENSE.md COMMERCIAL_SERVICES.md LICENSING_SUMMARY.md
git add AUTHORSHIP_AND_ATTRIBUTION.md CUSTOMIZATION_CHECKLIST.md
git add PRE_PUBLICATION_AUDIT.md GITHUB_SETUP_GUIDE.md
git add .env.example

# Add Python files (if not already tracked)
git add *.py
git add scripts/
git add glossary_parser/
git add docker/
git add docs/

# Add updated files
git add .gitignore
git add README.md
git add requirements*.txt

# Remove deleted files from git
git add -u

# Check what will be committed
git status
```

### C. Verify Nothing Sensitive

```bash
# Double-check no sensitive data
git diff --cached | grep -i "password\|token\|secret"

# Should return nothing
```

### D. Check Repository Size

```bash
# Make sure models aren't in git
du -sh .git

# Should be < 10MB
# If > 100MB, you have model files in git (bad!)
# Check: git ls-files | grep -E '\.bin$|\.pt$'
```

**If you see model files in git:**
```bash
# Remove large files from git
git rm --cached models/deployed_models/**/*.bin
git rm --cached models/deployed_models/**/*.pt

# Commit the removal
git commit -m "Remove large model files from git"
```

---

## Step 3: Create Commit

```bash
git commit -m "Prepare TraductAL for public release

- Add dual licensing structure (MIT + Commercial)
- Add comprehensive documentation (40+ files)
- Fix hardcoded paths for portability
- Update .gitignore for model files
- Add commercial services framework
- Update README with licensing info

TraductAL is a multilingual, multimodal translation system:
- 65+ languages (mainstream + low-resource)
- 100% offline operation
- Hybrid neural-symbolic architecture
- Open-source with commercial licensing option
"
```

---

## Step 4: Connect to GitHub

### If you created repo via website (Option A):

GitHub will show you commands like:
```bash
git remote add origin https://github.com/yourusername/TraductAL.git
git branch -M main
git push -u origin main
```

Copy and run those commands.

### If you used gh CLI (Option B):

Already done! Repository is created and pushed.

---

## Step 5: Verify Upload

1. Go to your repository URL: `https://github.com/yourusername/TraductAL`
2. Check:
   - [ ] README.md renders correctly
   - [ ] LICENSE file visible
   - [ ] All directories present (scripts, docs, glossary_parser, etc.)
   - [ ] No model files (.bin, .pt) in repository
   - [ ] Documentation files present

3. Click around:
   - [ ] Links in README work
   - [ ] COMMERCIAL_LICENSE.md opens correctly
   - [ ] AUTHORSHIP_AND_ATTRIBUTION.md displays properly

---

## Step 6: Configure Repository Settings

On GitHub, go to Settings:

### A. Description and Topics

- Description: "Multilingual translation system - 65+ languages, 100% offline, hybrid neural-symbolic architecture"
- Website: (add if you have one)
- Topics (tags):
  - `translation`
  - `neural-machine-translation`
  - `nllb`
  - `multilingual`
  - `offline`
  - `prolog`
  - `computational-linguistics`
  - `low-resource-languages`
  - `romansh`
  - `swiss-languages`

### B. Features

- [ ] ✅ Issues (enable for bug reports)
- [ ] ✅ Wiki (optional)
- [ ] ❌ Discussions (optional - enable later if community grows)
- [ ] ❌ Projects (not needed initially)

### C. Social Preview

Upload a social preview image (optional):
- Size: 1280×640 pixels
- Could be TraductAL logo or screenshot of interface

---

## Step 7: Add Repository Badges

Edit your README.md to add badges at the top:

```markdown
# TraductAL - Offline Neural Translation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/TraductAL?style=social)](https://github.com/yourusername/TraductAL)

**65+ languages • 100% offline • Privacy-focused • No data collection**
```

Commit and push:
```bash
git add README.md
git commit -m "Add repository badges"
git push
```

---

## Step 8: Create First Release (Optional)

Once everything looks good:

```bash
# Tag this version
git tag -a v0.1.0 -m "Initial public release - TraductAL 0.1.0"
git push origin v0.1.0
```

On GitHub:
1. Go to "Releases" → "Draft a new release"
2. Choose tag: v0.1.0
3. Title: "TraductAL v0.1.0 - Initial Public Release"
4. Description:
```markdown
## TraductAL v0.1.0 - Initial Public Release

First public release of TraductAL, a multilingual translation system combining neural and symbolic approaches.

### Features
- 65+ languages (NLLB-200 + Apertus-8B)
- 100% offline operation
- Hybrid neural-symbolic validation
- Web interface + CLI tools
- Optional speech-to-text and text-to-speech

### Installation
See [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)

### License
- Academic/Research: MIT License (free)
- Commercial: See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md)

### Known Limitations
- Beta software - use at your own risk
- Model download required (~3-10GB)
- Translation quality varies by language pair

### Acknowledgments
Built with:
- NLLB-200 (Meta AI)
- Apertus-8B (Open Source)
- Trealla Prolog
- OpenAI Whisper
```

5. Publish release

---

## Troubleshooting

### Problem: Push Rejected (Large Files)

```
remote: error: File models/something.bin is 1.5 GB; this exceeds GitHub's file size limit
```

**Solution:**
```bash
# Remove from git
git rm --cached models/deployed_models/**/*.bin
git commit -m "Remove large model files"
git push
```

### Problem: Authentication Failed

```
remote: Support for password authentication was removed
```

**Solution:**
Use a Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Generate new token
2. Select scopes: `repo` (all)
3. Copy token
4. Use token as password when pushing

Or set up SSH keys:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub  # Add this to GitHub SSH keys
git remote set-url origin git@github.com:yourusername/TraductAL.git
```

### Problem: Already Exists

```
fatal: remote origin already exists
```

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/yourusername/TraductAL.git
```

---

## Next Steps After Publishing

1. **Wait 5-10 minutes** for GitHub to index your repository
2. **Test cloning** in a fresh directory:
   ```bash
   cd /tmp
   git clone https://github.com/yourusername/TraductAL.git
   cd TraductAL
   ls -la
   ```
3. **Follow your own installation instructions** to verify they work
4. **Create HuggingFace Space** (separate guide)
5. **Announce** on social media, academic forums

---

## GitHub Repository Checklist

Before announcing publicly, verify:

- [ ] README.md displays correctly
- [ ] LICENSE file visible
- [ ] Installation instructions clear
- [ ] No sensitive information visible
- [ ] No large model files in repository
- [ ] Links in README work
- [ ] Repository description set
- [ ] Topics/tags added
- [ ] Issues enabled
- [ ] (Optional) Release created

---

## Post-Publication Monitoring

Keep an eye on:

- **GitHub Issues**: Respond within 2-3 days
- **Stars/Forks**: Track adoption
- **Clone traffic**: Settings → Insights → Traffic
- **Security alerts**: GitHub will notify you of vulnerabilities

---

**Ready to publish?** Follow these steps and your research will be public! 🚀
