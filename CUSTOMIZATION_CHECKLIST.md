# TraductAL Customization Checklist

**Before publishing or accepting commercial inquiries**

---

## Quick Overview

Use this checklist to customize placeholder information in TraductAL documentation before:
1. Publishing to GitHub/HuggingFace
2. Announcing publicly
3. Accepting commercial inquiries

**Time required**: 30-60 minutes

---

## ✅ Step 1: Contact Information

Replace these placeholders in ALL files listed:

### Your Personal/Company Details

```
[Your Name] → Your actual name
[Your Email] → Your primary contact email
[Support Email] → Support email (can be same as primary)
[Your Company/Name] → Legal entity name
[Your Address] → Physical/legal address (if needed)
[Your Country] → Your jurisdiction (e.g., Switzerland, France, USA)
[Your Jurisdiction] → Legal jurisdiction for contracts
[University Name] → Your academic institution (if applicable)
```

### Files to Update:

- [ ] `COMMERCIAL_LICENSE.md` (multiple instances)
- [ ] `COMMERCIAL_SERVICES.md` (multiple instances)
- [ ] `LICENSING_SUMMARY.md` (contact section)
- [ ] `AUTHORSHIP_AND_ATTRIBUTION.md` (authorship sections)

### Find and Replace Commands:

```bash
cd /home/aldn/TraductAL/TraductAL

# Preview what will be replaced
grep -r "\[Your Name\]" *.md
grep -r "\[Your Email\]" *.md

# Interactive replace (do this for each placeholder)
# Use your text editor's find-replace or:
sed -i 's/\[Your Name\]/John Doe/g' COMMERCIAL_LICENSE.md
sed -i 's/\[Your Email\]/contact@example.com/g' COMMERCIAL_LICENSE.md
# ... repeat for each file and placeholder
```

---

## ✅ Step 2: Repository URLs

Update these placeholders:

```
<repository-url> → https://github.com/yourusername/TraductAL
[Repository URL] → https://github.com/yourusername/TraductAL
[HF Space URL] → https://huggingface.co/spaces/yourusername/TraductAL
[Your Website] → https://yourwebsite.com (or remove if no website)
```

### Files to Update:

- [ ] `README.md` (Quick Start section, line ~20)
- [ ] `COMMERCIAL_SERVICES.md` (bottom contact section)
- [ ] Any documentation in `docs/` that references repository

---

## ✅ Step 3: Academic/Research Information

If you want to include your academic background:

### In `AUTHORSHIP_AND_ATTRIBUTION.md`:

- [ ] Line 25: Add your name
- [ ] Line 26: Add your Master's thesis details
  - University name
  - Year (1989-1991 or your actual years)
  - Thesis title

- [ ] Lines 362-365: Add contact information in "Contact & Questions" section

### Citation Format (lines 52-58):

```
[Your Name]. (1989-1991). [Your Thesis Title].
Master's Thesis in Computational Linguistics, [University Name].

[Your Name]. (2025-2026). TraductAL: Hybrid Neural-Symbolic Translation System
with DCG-based Validation. Research Project.
```

---

## ✅ Step 4: Optional: Company/Legal Entity

If you're setting up a company or legal entity:

### In `COMMERCIAL_LICENSE.md` (bottom section):

- [ ] Line ~450: "Legal Notices" section
  ```
  This Commercial License is offered by:
  **[Your Company Name or Personal Name]**
  **[Address]**
  **[Country]**
  **[VAT/Tax ID if applicable]**
  ```

### In `COMMERCIAL_SERVICES.md` (bottom section):

- [ ] Line ~580: "Legal and Compliance" section
  ```
  **Entity:** [Your Company/Name]
  **Location:** [Your Country]
  **Registered:** [Registration number if applicable]
  ```

---

## ✅ Step 5: Payment Information (When Ready)

When you're ready to accept payments, add:

### In `COMMERCIAL_LICENSE.md` (section "Payment Terms"):

- [ ] Payment methods you accept:
  - [ ] Bank transfer (add bank details)
  - [ ] Stripe link
  - [ ] PayPal email
  - [ ] Other payment processors

### In `COMMERCIAL_SERVICES.md`:

- [ ] Update contact information for billing inquiries
- [ ] Add invoice template reference (if you have one)

---

## ✅ Step 6: Optional Website/Social Media

If you have these, add them:

### Social/Professional Links:

```
🌐 Website: [Your Website]
🐙 GitHub: github.com/yourusername
🤗 HuggingFace: huggingface.co/yourusername
🔗 LinkedIn: linkedin.com/in/yourprofile
🎓 Google Scholar: scholar.google.com/yourprofile
📧 Email: your@email.com
```

### Files to Update:

- [ ] `README.md` (add at bottom, optional)
- [ ] `COMMERCIAL_SERVICES.md` (bottom contact section)
- [ ] `AUTHORSHIP_AND_ATTRIBUTION.md` (contact section)

---

## ✅ Step 7: Verification Checklist

After making changes, verify:

### A. No Placeholders Remain

```bash
# Search for any remaining placeholders
cd /home/aldn/TraductAL/TraductAL
grep -r "\[Your" *.md
grep -r "<your" *.md
grep -r "PLACEHOLDER" *.md

# Should return no results if all are replaced
```

### B. All Links Work

- [ ] Test GitHub repository URL (after you create it)
- [ ] Test HuggingFace Space URL (after you create it)
- [ ] Test email addresses (send yourself a test)
- [ ] Test any website links

### C. Consistent Information

- [ ] Same email used everywhere (or clearly different support vs. sales)
- [ ] Same name spelling everywhere
- [ ] Same company name everywhere
- [ ] Consistent jurisdiction/country everywhere

---

## ✅ Step 8: Optional Content Adjustments

### Remove Commercial Features (If Academic-Only Launch):

If you want to launch without commercial offerings initially:

**Option A**: Remove commercial files entirely
```bash
cd /home/aldn/TraductAL/TraductAL
git rm COMMERCIAL_LICENSE.md
git rm COMMERCIAL_SERVICES.md
git rm LICENSING_SUMMARY.md
```

Then update `README.md` to remove commercial licensing references.

**Option B**: Add "Coming Soon" notices

In each commercial file, add at the top:
```markdown
> ⚠️ **COMING SOON**: Commercial licensing is under development.
> For inquiries, contact [your-email@example.com]
```

---

## Quick Reference: Minimum Required Changes

If you're in a hurry, these are CRITICAL:

### For GitHub Publication:

1. ✅ Replace `[Your Email]` in all files (for bug reports, contact)
2. ✅ Replace `<repository-url>` in README.md
3. ✅ Add your name to AUTHORSHIP_AND_ATTRIBUTION.md
4. ✅ Verify no `/home/aldn/` paths in code (already fixed!)

### For Commercial Launch:

All of the above, PLUS:

5. ✅ Complete contact information in COMMERCIAL_LICENSE.md
6. ✅ Complete contact information in COMMERCIAL_SERVICES.md
7. ✅ Legal entity information (if applicable)
8. ✅ Payment methods ready

---

## Automated Helper Script

To help find all placeholders:

```bash
#!/bin/bash
# Save as: check_placeholders.sh

echo "Checking for remaining placeholders..."
echo ""

echo "=== Email Placeholders ==="
grep -n "\[.*Email\]" *.md

echo ""
echo "=== Name Placeholders ==="
grep -n "\[Your Name\]" *.md

echo ""
echo "=== URL Placeholders ==="
grep -n "<repository-url>" *.md
grep -n "\[.*URL\]" *.md

echo ""
echo "=== Other Placeholders ==="
grep -n "\[Your" *.md | grep -v "Email\|Name\|URL"

echo ""
echo "If nothing appears above, you're done! ✅"
```

Run with:
```bash
chmod +x check_placeholders.sh
./check_placeholders.sh
```

---

## After Customization

Once you've completed this checklist:

### Next Steps:

1. **Commit Changes**:
   ```bash
   git add COMMERCIAL_LICENSE.md COMMERCIAL_SERVICES.md LICENSING_SUMMARY.md AUTHORSHIP_AND_ATTRIBUTION.md README.md
   git commit -m "Customize contact information and licensing details"
   ```

2. **Review Files**:
   - Read through each customized file
   - Check for typos, inconsistencies
   - Verify all information is accurate

3. **Legal Review** (Recommended):
   - Have a lawyer review COMMERCIAL_LICENSE.md
   - Especially if you're in EU (GDPR), US, or have specific regulations
   - Cost: $500-2000 typically

4. **Test Links**:
   - After publishing to GitHub, test all internal links
   - Verify README renders correctly
   - Check that all referenced files exist

---

## Help

If you get stuck or have questions:

1. **Missing file references**: Use `find . -name "filename.md"` to locate
2. **Broken links**: GitHub will show them as grey, not blue
3. **Placeholder checker**: Run the script above to find remaining items

---

**Remember**: You can always update these later. It's better to launch with minimal information (just your email) than to delay indefinitely!

The most important thing is that people can reach you. Everything else can evolve.
