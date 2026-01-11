# 📚 Historical Glossary PDF Extraction Guide

**Tool**: `glossary_extractor.py`
**Purpose**: Extract lexical data from historical Swiss French dialect glossaries (PDF format)
**Example**: Glossaire vaudois (1861)

---

## 🎯 What This Tool Does

Converts historical PDF glossaries into structured CSV data for your Swiss French dataset:

```
PDF Glossary (1861)     →    CSV Database    →    Swiss French Dataset
┌─────────────────┐          ┌──────────────┐     ┌─────────────────────┐
│ PANOSSE, f.     │          │ panosse,serp│     │ {"Prompt": "Trans-  │
│ Serpillière     │    →     │ illière,vaud│  →  │ late: panosse",     │
│                 │          │ ,feminine,...│     │  "Answer": "serp-   │
│ LINGE, m.       │          │ linge,servie│     │  illière"}         │
│ Serviette       │          │ tte,vaud,...│     └─────────────────────┘
└─────────────────┘          └──────────────┘
```

---

## 🚀 Quick Start

### Step 1: Install PDF Library

Choose one (or install all for best compatibility):

```bash
# Option 1: PyPDF2 (simplest, most compatible)
pip install PyPDF2

# Option 2: pdfplumber (best for complex layouts)
pip install pdfplumber

# Option 3: PyMuPDF (best for OCR'd/scanned PDFs)
pip install pymupdf

# Recommended: Install all three
pip install PyPDF2 pdfplumber pymupdf
```

### Step 2: Extract Your Glossary

```bash
# Basic extraction
python3 glossary_extractor.py \
  --pdf glossaire_vaudois_1861.pdf \
  --dialect vaud

# This creates:
# datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv
```

### Step 3: Review and Import

```bash
# Review the CSV
head datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv

# Import into dataset
python3 swiss_french_dataset_builder.py \
  --dialect vaud \
  --import-csv datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv

# Check statistics
python3 swiss_french_dataset_builder.py --stats
```

---

## 📖 Detailed Usage

### Basic Extraction

```bash
python3 glossary_extractor.py --pdf your_glossary.pdf --dialect vaud
```

**Output**:
- ✅ CSV file with structured data
- ✅ Statistics about extraction
- ✅ Sample entries displayed

### Save Raw Text for Review

If extraction quality is poor, save raw text first:

```bash
python3 glossary_extractor.py \
  --pdf glossaire_vaudois_1861.pdf \
  --save-raw raw_text.txt
```

**Then review** `raw_text.txt` to:
1. See what the PDF extractor sees
2. Identify patterns in the glossary structure
3. Find where the actual glossary starts (after preface)

### Process Pre-extracted Text

After reviewing, process the text directly:

```bash
python3 glossary_extractor.py \
  --raw-text raw_text.txt \
  --dialect vaud \
  --output vaud_dictionary.csv
```

### Save JSON for Review

To review entries before CSV export:

```bash
python3 glossary_extractor.py \
  --pdf glossaire.pdf \
  --dialect vaud \
  --json review_entries.json
```

**Review** `review_entries.json` to check:
- Entry parsing accuracy
- Definition extraction
- Standard French detection

### Manual Glossary Start

If auto-detection fails, manually specify start line:

```bash
# First, save raw text and find the line number
python3 glossary_extractor.py --pdf glossaire.pdf --save-raw raw.txt

# Open raw.txt, find where glossary starts (e.g., line 120)

# Then extract from that line
python3 glossary_extractor.py \
  --raw-text raw.txt \
  --start-line 120 \
  --dialect vaud
```

---

## 📋 Supported Glossary Formats

The tool recognizes common historical glossary patterns:

### Format 1: "WORD, gender. Definition"
```
PANOSSE, f. Serpillière pour laver le sol
LINGE, m. Serviette de toilette
```

### Format 2: "WORD (gender) Definition"
```
PANOSSE (f.) Serpillière pour laver le sol
LINGE (m.) Serviette de toilette
```

### Format 3: "WORD. — Definition"
```
PANOSSE. — Serpillière pour laver le sol
LINGE. — Serviette de toilette
```

### Format 4: "WORD, Definition"
```
Panosse, serpillière
Linge, serviette
```

---

## 🔧 Troubleshooting

### Issue 1: No Text Extracted

**Symptoms**: "Extracted 0 characters"

**Causes**:
1. PDF is image-based (scanned) without OCR
2. PDF has security restrictions
3. Encoding issues

**Solutions**:

**A. Run OCR on the PDF first:**
```bash
# Install ocrmypdf
pip install ocrmypdf

# OCR the PDF (creates searchable text layer)
ocrmypdf glossaire_original.pdf glossaire_ocr.pdf --language fra

# Then extract
python3 glossary_extractor.py --pdf glossaire_ocr.pdf --dialect vaud
```

**B. Use online OCR:**
- Upload to Google Drive → Open with Google Docs → Download as PDF
- Or use: https://www.onlineocr.net/

**C. Try different PDF library:**
```bash
# PyMuPDF is often best for scanned PDFs
pip install pymupdf
python3 glossary_extractor.py --pdf glossaire.pdf --dialect vaud
```

### Issue 2: Poor Entry Parsing

**Symptoms**: "Parsed 0 entries" or very few entries

**Solutions**:

**A. Review raw text:**
```bash
python3 glossary_extractor.py --pdf glossaire.pdf --save-raw raw.txt
less raw.txt  # Review the structure
```

**B. Check glossary format:**
Look for the entry pattern in `raw.txt`. If it's different from supported formats, you may need to:

1. **Edit the entry patterns** in `glossary_extractor.py`:
   ```python
   # Around line 30-45
   ENTRY_PATTERNS = [
       # Add your custom pattern here
       r'^YOUR_PATTERN$',
       # ... existing patterns
   ]
   ```

2. **Or do manual preprocessing:**
   - Edit `raw.txt` to normalize entries
   - Then run: `python3 glossary_extractor.py --raw-text raw.txt`

**C. Manually specify start:**
```bash
# Find where glossary actually starts
grep -n "^A\." raw.txt  # Find first "A." section

# Extract from that line
python3 glossary_extractor.py --raw-text raw.txt --start-line 150
```

### Issue 3: Incorrect Standard French Extraction

**Symptoms**: `standard_french` column is empty or wrong

**Solution**: Manual post-processing

```bash
# Extract first
python3 glossary_extractor.py --pdf glossaire.pdf --output temp.csv

# Manually review and fill in standard_french column in Excel/LibreOffice
libreoffice temp.csv

# Then import
python3 swiss_french_dataset_builder.py --dialect vaud --import-csv temp.csv
```

### Issue 4: Special Characters Garbled

**Symptoms**: "è" becomes "Ã¨", accents broken

**Solutions**:

**A. Force UTF-8 encoding:**
```python
# Edit glossary_extractor.py around line 150
# Change: open(output, 'w', encoding='utf-8')
# To: open(output, 'w', encoding='utf-8', errors='replace')
```

**B. Convert encoding:**
```bash
# After extraction, convert
iconv -f ISO-8859-1 -t UTF-8 output.csv > output_utf8.csv
```

---

## 💡 Best Practices

### 1. **Start with Small Test**

```bash
# Extract and save raw text first
python3 glossary_extractor.py --pdf glossaire.pdf --save-raw raw.txt

# Review first 100 lines
head -100 raw.txt

# Check if it looks correct before full extraction
```

### 2. **Use Two-Stage Process**

```bash
# Stage 1: Extract to JSON for review
python3 glossary_extractor.py \
  --pdf glossaire.pdf \
  --json entries.json

# Stage 2: Review JSON, then convert to CSV
# (manually if needed, or re-run with adjustments)
```

### 3. **Quality Check**

After extraction:

```bash
# Check number of entries
wc -l extracted_vaud_glossary.csv

# View sample
head -20 extracted_vaud_glossary.csv

# Check for obvious errors
grep "???" extracted_vaud_glossary.csv  # OCR errors often have ???
```

### 4. **Iterative Refinement**

For best results:

1. **First pass**: Extract with defaults
2. **Review**: Check sample entries
3. **Adjust**: Modify patterns if needed
4. **Re-extract**: Run again with adjustments
5. **Manual cleanup**: Fix remaining issues in CSV
6. **Import**: Load into dataset

---

## 📊 Expected Output

### CSV Format

```csv
swiss_french,standard_french,dialect,part_of_speech,definition,source,notes
panosse,serpillière,vaud,feminine noun,Serpillière pour laver le sol,Glossaire vaud (1861),Line 150
linge,serviette,vaud,masculine noun,Serviette de toilette,Glossaire vaud (1861),Line 151
```

### Statistics

```
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
```

---

## 🎯 Real-World Example: Glossaire Vaudois (1861)

### Scenario

You have: `glossaire_vaudois_1861.pdf` (reproduced from original 1861 edition)

**Structure:**
- Pages 1-10: Cover, title page, preface
- Pages 11-250: Glossary entries (A-Z)
- Format: "WORD, gender. Definition in French"

### Process

**Step 1: OCR (if needed)**
```bash
# Check if text is extractable
python3 glossary_extractor.py --pdf glossaire_vaudois_1861.pdf --save-raw test.txt
head test.txt

# If empty or garbled, run OCR
ocrmypdf glossaire_vaudois_1861.pdf glossaire_vaudois_1861_ocr.pdf --language fra
```

**Step 2: Extract**
```bash
python3 glossary_extractor.py \
  --pdf glossaire_vaudois_1861_ocr.pdf \
  --dialect vaud \
  --save-raw raw_vaud.txt \
  --json vaud_entries.json
```

**Expected output:**
```
📄 Extracting text from: glossaire_vaudois_1861_ocr.pdf
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
PDF file: glossaire_vaudois_1861_ocr.pdf
Dialect: vaud
Total entries extracted: 1,247

💾 Saving to CSV: datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv
   ✅ Saved 1,247 entries

📝 Next step:
   python3 swiss_french_dataset_builder.py --dialect vaud --import-csv datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv
```

**Step 3: Review**
```bash
# Check quality
head -20 datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv

# Review JSON for accuracy
less vaud_entries.json
```

**Step 4: Import**
```bash
python3 swiss_french_dataset_builder.py \
  --dialect vaud \
  --import-csv datasets/swiss_french/Raw_Data/extracted_vaud_glossary.csv

python3 swiss_french_dataset_builder.py --stats
```

**Expected result:**
```
📊 DATASET STATISTICS
Dictionary entries: 2,494 (1,247 from glossary × 2 directions)
Total examples: 2,494
Progress: 5.4% vs. Romansh dataset
```

---

## 🎉 Success Metrics

Your extraction is successful if:

- ✅ **Extraction rate**: >80% of visual entries captured
- ✅ **Accuracy**: >90% of entries correctly parsed
- ✅ **Standard French**: >60% automatically extracted
- ✅ **Clean data**: <5% OCR errors (???, garbled text)

### Typical Results

| Glossary Type | Expected Entries | Extraction Rate | Manual Cleanup |
|--------------|------------------|-----------------|----------------|
| Clean modern PDF | 1,000-2,000 | 95%+ | Minimal |
| Scanned (with OCR) | 1,000-2,000 | 80-90% | 10-20% entries |
| Old/poor quality | 1,000-2,000 | 60-80% | 20-40% entries |

---

## 🚀 Next Steps After Extraction

### 1. Import to Dataset

```bash
python3 swiss_french_dataset_builder.py \
  --dialect vaud \
  --import-csv extracted_vaud_glossary.csv
```

### 2. Check Progress

```bash
python3 swiss_french_dataset_builder.py --stats
```

### 3. Generate Training Examples

From 1,247 dictionary entries, you get:
- 2,494 bidirectional translation pairs
- ~3,741 with idiom identification
- **Total: ~3,700 training examples from one glossary!**

### 4. Find More Glossaries

Search for:
- Other Swiss French dialect glossaries (Geneva, Fribourg, Neuchâtel, Jura)
- GPSR entries (online or PDF)
- Historical regional dictionaries
- Academic linguistic publications

---

## 📚 Resources

### OCR Tools

- **ocrmypdf**: `pip install ocrmypdf` (command-line)
- **Google Drive**: Upload PDF → Open with Google Docs → Download
- **Adobe Acrobat**: Built-in OCR
- **Online**: https://www.onlineocr.net/

### Historical Glossaries

Search terms for finding more:
- "glossaire vaudois"
- "patois romand"
- "dialecte suisse romand"
- "glossaire genevois"
- "parler fribourgeois"

Archives:
- **GPSR**: https://www.gpsr.ch/
- **e-rara**: https://www.e-rara.ch/ (Swiss historical books)
- **Gallica**: https://gallica.bnf.fr/ (French archives)

### PDF Libraries

```bash
# Install all for maximum compatibility
pip install PyPDF2 pdfplumber pymupdf
```

---

## ✅ Summary

**Tool created**: ✅ `glossary_extractor.py`

**Capabilities**:
- Extract text from PDF (3 library options)
- Parse glossary entries (4 common formats)
- Extract metadata (word, gender, definition, standard French)
- Export to CSV (dataset-compatible format)
- Statistics and quality metrics

**Expected impact**:
- **1 glossary** = 1,000-2,000 entries
- **1,000 entries** = 2,000-3,000 training examples
- **3-4 glossaries** = Minimum viable dataset (5,000+ examples)

**Your Glossaire vaudois (1861)** could provide **~3,700 training examples** — that's 74% of your Phase 1 milestone!

---

**Ready to extract your glossary!** 📚→📊
