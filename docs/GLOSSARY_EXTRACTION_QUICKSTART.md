# 📚 Glossary Extraction Quick Start

**Your situation**: You have Glossaire vaudois (1861) PDF
**Your goal**: Extract lexical data → Import to Swiss French dataset
**Expected result**: ~1,000-2,000 training examples

---

## ⚡ 3-Step Quick Start

### Step 1: Install PDF Library (30 seconds)

```bash
# Install PyPDF2 (easiest)
pip install PyPDF2

# Or install all three for best compatibility
pip install PyPDF2 pdfplumber pymupdf
```

### Step 2: Test Your PDF (1 minute)

```bash
# Replace with your actual PDF filename
./test_pdf_extraction.sh glossaire_vaudois_1861.pdf vaud
```

**This will tell you:**
- ✅ Is text extractable?
- ✅ Does it need OCR?
- ✅ Where does the glossary start?
- ✅ What patterns are present?

### Step 3: Extract (2-5 minutes)

**If test shows "Ready for extraction":**
```bash
python3 glossary_extractor.py \
  --pdf glossaire_vaudois_1861.pdf \
  --dialect vaud
```

**If test shows "Need OCR":**
```bash
# Install OCR tool
pip install ocrmypdf

# Run OCR (creates searchable PDF)
ocrmypdf glossaire_vaudois_1861.pdf glossaire_vaudois_1861_ocr.pdf --language fra

# Then extract
python3 glossary_extractor.py \
  --pdf glossaire_vaudois_1861_ocr.pdf \
  --dialect vaud
```

**Result**: CSV file at `datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv`

---

## 📋 What You'll See

### During Extraction

```
📄 Extracting text from: glossaire_vaudois_1861.pdf
   Pages: 250
   ✅ Extracted 245,892 characters

🧹 Cleaning text...
   Cleaned 3,847 lines from 4,123 total

🔍 Identifying glossary start...
   Found glossary start at line 145: ABAISER, v. Abaisser

📖 Parsing entries from line 145...
   ✅ Parsed 1,247 entries

✨ Enriching entries...
   ✅ Enriched 1,247 entries

============================================================
📊 EXTRACTION STATISTICS
============================================================
PDF file: glossaire_vaudois_1861.pdf
Dialect: vaud
Total entries extracted: 1,247

Part of speech distribution:
   masculine noun: 542
   feminine noun: 423
   verb: 187
   adjective: 95

Entries with standard French: 892 (71.5%)

Sample entries:
   PANOSSE (feminine noun): Serpillière pour laver le sol...
   LINGE (masculine noun): Serviette de toilette...

💾 Saving to CSV: datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv
   ✅ Saved 1,247 entries

📝 Next step:
   python3 swiss_french_dataset_builder.py --dialect vaud --import-csv datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv
```

### CSV Output Format

```csv
swiss_french,standard_french,dialect,part_of_speech,definition,source,notes
panosse,serpillière,vaud,feminine noun,Serpillière pour laver le sol,Glossaire vaud (1861),Line 150
linge,serviette,vaud,masculine noun,Serviette de toilette,Glossaire vaud (1861),Line 151
ça joue,ça va,vaud,expression,Manière de saluer familière,Glossaire vaud (1861),Line 243
```

---

## 🎯 After Extraction: Import to Dataset

```bash
# Import the CSV
python3 swiss_french_dataset_builder.py \
  --dialect vaud \
  --import-csv datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv

# Check your progress
python3 swiss_french_dataset_builder.py --stats
```

**Expected output:**
```
============================================================
📊 DATASET STATISTICS
============================================================
  sft_dictionary_vaud.jsonl: 2,494 examples

✅ Total examples: 2,494
📁 Location: /home/aldn/TraductAL/TraductAL/datasets/swiss_french

📈 Progress vs. Romansh dataset (46,092 examples):
  Current: 5.4%
  🎯 Next milestone: 5,000 examples (dictionary focus)
```

**Impact**: 1,247 entries → 2,494 training examples (bidirectional)

---

## 🔧 Common Issues & Solutions

### Issue 1: No Text Extracted

**Symptom:**
```
📄 Extracting text from: glossaire.pdf
   Pages: 250
   ✅ Extracted 0 characters
```

**Cause**: PDF is image-based (scanned), not searchable

**Solution**: Run OCR
```bash
# Install
pip install ocrmypdf

# Run OCR (French language)
ocrmypdf glossaire_vaudois_1861.pdf glossaire_vaudois_1861_ocr.pdf --language fra

# Extract from OCR'd version
python3 glossary_extractor.py --pdf glossaire_vaudois_1861_ocr.pdf --dialect vaud
```

**Alternative**: Use Google Drive
1. Upload PDF to Google Drive
2. Right-click → Open with Google Docs
3. File → Download → PDF
4. Extract from the downloaded PDF

---

### Issue 2: Few Entries Found

**Symptom:**
```
📖 Parsing entries from line 0...
   ✅ Parsed 23 entries
```

**Cause**: Extraction started too early (preface, table of contents)

**Solution**: Manual start line
```bash
# Save raw text
python3 glossary_extractor.py --pdf glossaire.pdf --save-raw raw.txt

# Open and find where glossary starts
less raw.txt
# Look for first entry like "ABAISER" or "A." section marker

# Extract from correct line (e.g., line 145)
python3 glossary_extractor.py \
  --raw-text raw.txt \
  --start-line 145 \
  --dialect vaud
```

---

### Issue 3: Garbled Characters

**Symptom:**
```
panosse,serpilli̬ère,vaud,...
```

**Cause**: OCR errors or encoding issues

**Solution A**: Try different PDF library
```bash
# Install pymupdf (often better for OCR)
pip install pymupdf

# Re-extract
python3 glossary_extractor.py --pdf glossaire.pdf --dialect vaud
```

**Solution B**: Manual cleanup in CSV
```bash
# Extract
python3 glossary_extractor.py --pdf glossaire.pdf --output temp.csv

# Open in LibreOffice/Excel and fix manually
libreoffice temp.csv

# Then import
python3 swiss_french_dataset_builder.py --dialect vaud --import-csv temp.csv
```

---

## 💡 Pro Tips

### Tip 1: Always Test First

```bash
# Test with small sample
./test_pdf_extraction.sh glossaire.pdf vaud

# Review output before full extraction
```

### Tip 2: Save Raw Text

```bash
# Always save raw text for review
python3 glossary_extractor.py \
  --pdf glossaire.pdf \
  --save-raw raw_vaud_text.txt \
  --dialect vaud

# You can reprocess without re-extracting PDF
python3 glossary_extractor.py \
  --raw-text raw_vaud_text.txt \
  --dialect vaud
```

### Tip 3: Manual Review is OK

Don't expect 100% automatic accuracy:
- **80-90% automatic** extraction is great
- **10-20% manual cleanup** is normal
- Quality > quantity

### Tip 4: Iterate

1. Extract first pass
2. Review sample entries
3. Adjust if needed
4. Re-extract
5. Manual cleanup
6. Import

---

## 📈 Expected Results by PDF Quality

| PDF Type | Auto Extraction | Manual Work | Total Time |
|----------|----------------|-------------|------------|
| **Modern, searchable** | 95% | 5% | 10 min |
| **OCR'd (good quality)** | 85% | 15% | 30 min |
| **OCR'd (poor quality)** | 70% | 30% | 1-2 hours |
| **Image-only (no OCR)** | 0% → OCR needed | - | +15 min OCR |

**Your Glossaire vaudois (1861)**: Likely "OCR'd (good quality)" category
- Expected: 1,000-1,500 entries automatically
- Manual cleanup: 100-300 entries
- Total time: **30-60 minutes**

---

## 🎯 Realistic Expectations

### From One 1861 Glossary

**Input**: Glossaire vaudois (1861), ~250 pages

**Automatic extraction**:
- 1,200 entries (80% success rate)
- 2,400 training examples (bidirectional)

**After manual cleanup** (1-2 hours):
- 1,500 entries (includes manual fixes)
- 3,000 training examples

**With additional processing**:
- Add example sentences: +1,500 examples
- Add idiom identification: +500 examples
- **Total: ~5,000 examples from one glossary!**

---

## ✅ Success Checklist

After extraction, verify:

- [ ] CSV file created with entries
- [ ] Entry count reasonable (500+)
- [ ] Sample entries look correct
- [ ] Standard French column has values (>50%)
- [ ] No major OCR errors (???, garbled text)

**If all checked**: Import to dataset!

```bash
python3 swiss_french_dataset_builder.py \
  --dialect vaud \
  --import-csv extracted_vaud_glossary.csv

python3 swiss_french_dataset_builder.py --stats
```

---

## 🚀 Next Steps

### Immediate (Today)

1. ✅ Test your PDF: `./test_pdf_extraction.sh glossaire_vaudois_1861.pdf vaud`
2. ✅ Run OCR if needed: `ocrmypdf input.pdf output_ocr.pdf --language fra`
3. ✅ Extract: `python3 glossary_extractor.py --pdf glossaire.pdf --dialect vaud`
4. ✅ Import: `python3 swiss_french_dataset_builder.py --dialect vaud --import-csv extracted.csv`

### This Week

5. Find more glossaries (Geneva, Fribourg, Neuchâtel)
6. Extract each one
7. Target: 5,000 total examples

### This Month

8. Generate synthetic data (fill gaps)
9. Human validation
10. Target: 20,000 examples (production-ready)

---

## 📞 Need Help?

**Documentation**:
- Full guide: `PDF_GLOSSARY_EXTRACTION_GUIDE.md`
- This quickstart: `GLOSSARY_EXTRACTION_QUICKSTART.md`
- Dataset guide: `SWISS_FRENCH_DATASET_GUIDE.md`

**Test commands**:
```bash
# Test PDF
./test_pdf_extraction.sh your_glossary.pdf vaud

# Get help
python3 glossary_extractor.py --help
```

**Common commands**:
```bash
# Basic extraction
python3 glossary_extractor.py --pdf glossary.pdf --dialect vaud

# With OCR
ocrmypdf glossary.pdf glossary_ocr.pdf --language fra
python3 glossary_extractor.py --pdf glossary_ocr.pdf --dialect vaud

# Save raw text for review
python3 glossary_extractor.py --pdf glossary.pdf --save-raw raw.txt

# Process raw text
python3 glossary_extractor.py --raw-text raw.txt --dialect vaud

# Import to dataset
python3 swiss_french_dataset_builder.py --dialect vaud --import-csv extracted.csv
```

---

## 🎊 Summary

**What you have**:
- ✅ Glossaire vaudois (1861) PDF
- ✅ Extraction tool (`glossary_extractor.py`)
- ✅ Test script (`test_pdf_extraction.sh`)
- ✅ Import pipeline (dataset builder)

**What to do**:
1. Test PDF (1 minute)
2. Run OCR if needed (5-15 minutes)
3. Extract glossary (2-5 minutes)
4. Import to dataset (1 minute)

**Expected result**:
- 1,000-1,500 dictionary entries
- 2,000-3,000 training examples
- **Major progress toward 5,000-example milestone!**

**Time investment**: 30-60 minutes total

---

**Your glossary is a goldmine - let's extract it!** 📚💎→📊
