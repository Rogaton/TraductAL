# Pre-Publication Readiness Audit

**Date**: January 11, 2026
**Status**: 🟡 NEEDS FIXES before GitHub/HF publication

---

## Executive Summary

TraductAL is **80% ready** for public release. Main issues to fix:
- ❌ Hardcoded paths in 3 Python files
- ⚠️ Large model files need proper .gitignore handling
- ⚠️ Placeholder contact information in new licensing docs
- ✅ No sensitive credentials found (good!)
- ✅ Good .gitignore already in place
- ✅ Documentation is comprehensive

**Estimated time to fix**: 2-4 hours

---

## Critical Issues (Must Fix Before Publication)

### 1. Hardcoded User-Specific Paths 🔴

**Issue**: Three files contain hardcoded `/home/aldn/` paths

**Files**:
1. `apertus_translator.py:33` - Default model path
2. `apertus_trealla_hybrid.py:67,89` - Apertus path configuration
3. `scripts/test_language_expansion.py:11` - sys.path insertion

**Impact**: Code will fail for other users

**Fix Required**:
```python
# Instead of:
model_path="/home/aldn/Apertus8B"

# Use relative or environment-based:
model_path=os.path.join(os.getcwd(), "models/apertus-8b")
# OR
model_path=os.environ.get('APERTUS_PATH', './models/apertus-8b')
```

**Priority**: CRITICAL - Must fix before publication

---

### 2. Placeholder Contact Information 🟡

**Issue**: New licensing documents contain placeholder text

**Files**:
- `COMMERCIAL_LICENSE.md` - [Your Name], [Your Email], [Your Address]
- `COMMERCIAL_SERVICES.md` - [Your Email], [Support Email], etc.
- `LICENSING_SUMMARY.md` - Contact placeholders

**Impact**: Looks unprofessional, cannot process commercial inquiries

**Fix Required**: Replace all placeholders with actual contact info

**Priority**: HIGH - Must do before announcing commercially

**Note**: Can publish to GitHub with placeholders IF you're not ready to accept commercial inquiries yet. Just add a note: "Commercial licensing coming soon - contact [your academic email] for information"

---

### 3. Large Model Files in Repository ⚠️

**Issue**: Model directories exist in repository

**Current State**:
```
models/deployed_models/nllb_200_3.3b/  (~3.3GB)
models/deployed_models/nllb_200_1.3b/  (~1.3GB)
```

**Impact**: Git repo size will be huge, GitHub may reject push

**Fix Required**: Ensure these are properly .gitignored or use Git LFS

**Current .gitignore**: Does NOT explicitly exclude models/

**Priority**: CRITICAL - Will cause push failure

---

## Medium Priority Issues (Should Fix)

### 4. Untracked Files in Git Status ⚠️

**From your git status**:
```
?? AUTHORSHIP_AND_ATTRIBUTION.md
?? DIRECTORY_STRUCTURE.txt
?? QUICKSTART.md
?? apertus_translator.py
?? apertus_trealla_hybrid.py
?? audio_chunks/
?? data/
?? datasets/
?? docker/
?? docs/
?? glossary_parser/
?? gradio_app.py
?? models/
?? requirements_enhanced.txt
?? scripts/
?? start_gradio.sh
?? startup_check.py
?? tts_engine.py
?? unified_translator.py
?? whisper_stt.py
```

**Issue**: Many core files are untracked (never been committed)

**Impact**: These files won't be pushed to GitHub unless you `git add` them

**Fix Required**:
```bash
git add AUTHORSHIP_AND_ATTRIBUTION.md
git add QUICKSTART.md
git add *.py
git add scripts/
git add docs/
git add docker/
# etc...

# OR (if you trust everything is good):
git add -A
```

**Priority**: MEDIUM - You need to add files before pushing

---

### 5. Deleted Files Not Committed ⚠️

**From your git status**:
```
D EVALUATION_SUMMARY.md
D LICENSE_INFO.md
D MIGRATION_SUMMARY.md
D NLLB_UPGRADE_GUIDE.md
D QUICK_REFERENCE.md
D app.py
```

**Issue**: Files deleted locally but not committed to git

**Fix**: `git add -u` (stages deleted files) or `git rm <file>`

---

### 6. Missing Documentation References 🟢

**Issue**: Some docs reference files that may not exist

**Check needed**:
- Does `docs/README_DETAILED.md` exist? ✅ (found in grep results)
- Does `docs/ADD_LANGUAGES_GUIDE.md` exist? (needs verification)
- Does `docs/BATCH_TRANSLATION_EXAMPLES.md` exist? (needs verification)

**Priority**: LOW - Can be added later

---

## Low Priority (Nice to Have)

### 7. Example Configuration File ✨

**Suggestion**: Add `config.example.json` showing:
```json
{
  "apertus_path": "./models/apertus-8b",
  "cache_dir": "./models",
  "device": "auto",
  "verbose": false
}
```

Users can copy to `config.json` (which should be .gitignored)

---

### 8. Installation Test Script ✨

**Suggestion**: Add `test_install.sh` that:
- Checks Python version
- Verifies dependencies
- Tests model downloads
- Runs basic translation test

---

### 9. CONTRIBUTING.md ✨

**Suggestion**: Add contributor guidelines:
- How to report bugs
- How to submit PRs
- Code style guidelines
- DCG grammar contribution process

---

## Security Check ✅

### Good News: No Sensitive Data Found

✅ No API keys or tokens found
✅ No passwords or credentials found
✅ No private keys found
✅ `.env` files already in .gitignore
✅ `.venv/` directories ignored

**Verdict**: Security-wise, safe to publish

---

## Required Actions Before GitHub Push

### Step 1: Fix Hardcoded Paths
- [ ] Fix `apertus_translator.py` (line 33)
- [ ] Fix `apertus_trealla_hybrid.py` (lines 67, 89)
- [ ] Fix `scripts/test_language_expansion.py` (line 11)

### Step 2: Update .gitignore for Models
```bash
# Add to .gitignore:
models/deployed_models/
models/*.bin
models/*.pt
*.pth
audio_chunks/
```

### Step 3: Clean Git Status
```bash
# Add new files
git add AUTHORSHIP_AND_ATTRIBUTION.md COMMERCIAL_*.md LICENSING_SUMMARY.md
git add QUICKSTART.md DIRECTORY_STRUCTURE.txt
git add *.py
git add scripts/ docs/ docker/ glossary_parser/
git add requirements_enhanced.txt

# Stage deletions
git add -u

# Check what will be committed
git status
```

### Step 4: Commit Everything
```bash
git commit -m "Prepare for public release

- Add dual licensing structure (MIT + Commercial)
- Add comprehensive documentation
- Add commercial services page
- Update README with licensing info
- Clean up old files
"
```

### Step 5: Verify Before Push
```bash
# Check repository size
du -sh .git

# If > 100MB, you have model files in git (bad!)
# Use git lfs or ensure models/ is gitignored
```

---

## Required Actions Before Accepting Commercial Inquiries

### Step 1: Replace Placeholders
- [ ] Add your name to all licensing docs
- [ ] Add contact email(s)
- [ ] Add location/jurisdiction
- [ ] Add support email (can be same as main)

### Step 2: Set Up Payment Infrastructure
- [ ] Create Stripe account (if accepting cards)
- [ ] Set up PayPal (if needed)
- [ ] Bank details for wire transfer
- [ ] Invoice template

### Step 3: Legal Review (Recommended)
- [ ] Have lawyer review COMMERCIAL_LICENSE.md
- [ ] Verify jurisdiction choice (Switzerland?)
- [ ] Check if you need company registration
- [ ] Understand tax implications

---

## Recommended Publication Strategy

### Option A: Academic-Only Launch (Fastest)

**Timeline**: This week

**Steps**:
1. Fix hardcoded paths (1 hour)
2. Update .gitignore for models (10 minutes)
3. Commit and push to GitHub (30 minutes)
4. Create HuggingFace Space (2 hours)
5. Announce on academic forums only

**Licensing**: MIT License only (remove commercial docs temporarily OR add "Coming Soon" notice)

**Advantage**: Get feedback quickly, build community
**Disadvantage**: No revenue path yet

---

### Option B: Full Dual-License Launch (More Preparation)

**Timeline**: 1-2 weeks

**Steps**:
1. Fix all technical issues (3-4 hours)
2. Customize all placeholders (1 hour)
3. Legal review of commercial license (2-5 days)
4. Set up payment infrastructure (1-2 days)
5. Create professional website/landing page (optional, 1 week)
6. Commit and push to GitHub
7. Create HuggingFace Space
8. Announce broadly (academic + commercial)

**Licensing**: Full dual licensing from day 1

**Advantage**: Complete professional launch, revenue ready
**Disadvantage**: More upfront work, delays community building

---

### Option C: Hybrid Approach (RECOMMENDED)

**Timeline**: This week + rolling updates

**Phase 1 (This week)**:
1. Fix hardcoded paths ✅
2. Add to .gitignore ✅
3. Customize licensing docs with your info ✅
4. Add note: "Commercial licensing available - contact for details" ✅
5. Push to GitHub (public) ✅
6. Deploy to HuggingFace Space ✅

**Phase 2 (Within 2 weeks)**:
7. Set up payment infrastructure
8. Legal review (parallel with Phase 1)
9. Create detailed commercial FAQ
10. Set up support email system

**Phase 3 (Within 1 month)**:
11. First grant applications
12. University outreach campaign
13. Blog post / press release
14. Conference submissions

**Advantage**: Fast to market, iterate based on feedback
**Disadvantage**: Some "under construction" elements initially

---

## File-by-File Readiness

| File | Status | Action Needed |
|------|--------|---------------|
| `README.md` | ✅ Ready | None (excellent) |
| `LICENSE` | ✅ Ready | None |
| `COMMERCIAL_LICENSE.md` | 🟡 Needs placeholders | Replace [Your Name], etc. |
| `COMMERCIAL_SERVICES.md` | 🟡 Needs placeholders | Replace [Your Email], etc. |
| `LICENSING_SUMMARY.md` | 🟡 Needs placeholders | Replace contact info |
| `AUTHORSHIP_AND_ATTRIBUTION.md` | 🟡 Needs placeholders | Add your name, university |
| `QUICKSTART.md` | ✅ Ready | None |
| `apertus_translator.py` | 🔴 Critical fix needed | Remove hardcoded path |
| `apertus_trealla_hybrid.py` | 🔴 Critical fix needed | Remove hardcoded paths |
| `unified_translator.py` | ✅ Ready | None |
| `gradio_app.py` | ✅ Ready | None |
| `nllb_translator.py` | ✅ Ready | None |
| `whisper_stt.py` | ✅ Ready | None |
| `tts_engine.py` | ✅ Ready | None |
| `.gitignore` | 🟡 Needs update | Add models/, audio_chunks/ |
| `requirements.txt` | ✅ Ready | None |
| `requirements_enhanced.txt` | ✅ Ready | None |

---

## Next Steps

### Immediate (Do Now):
1. **Decision**: Which launch strategy? (A, B, or C above)
2. **Fix hardcoded paths** (critical for any option)
3. **Update .gitignore** (critical for any option)

### Then (Based on Your Choice):
4. **Option A**: Commit and push today
5. **Option B**: Complete all placeholders, get legal review
6. **Option C (Recommended)**: Fix critical issues + minimal placeholders, push this week

### After Launch:
7. Monitor GitHub issues
8. Respond to inquiries (expect 5-20 in first week if you announce)
9. Iterate based on feedback
10. Pursue grants and partnerships

---

## Questions to Answer

Before proceeding, please decide:

1. **Contact Email**: What email should people use for inquiries?
   - Academic email (university)?
   - Personal email?
   - New dedicated email (traductal@...)?

2. **Jurisdiction**: What jurisdiction for commercial license?
   - Switzerland (if you're there)?
   - EU generic?
   - Prefer to leave flexible for now?

3. **Launch Timing**: How soon do you want to go public?
   - This week (Option A or C)?
   - 1-2 weeks (Option B)?
   - Later (need more testing)?

4. **Commercial Readiness**: Are you ready to handle commercial inquiries?
   - Yes, let's set up payment and go (Option B)
   - Not yet, but want to show pricing (Option C)
   - No, academic only for now (Option A)

---

## Conclusion

**Bottom Line**: TraductAL is solid technically. Main blockers are:
1. Hardcoded paths (1 hour fix)
2. Model files in git (10 minute .gitignore update)
3. Commercial placeholder text (30 minutes if you have info ready)

**Recommendation**: Fix items 1-2 today, decide on commercial timing, then push to GitHub this week.

You've built something impressive. Time to share it! 🚀
