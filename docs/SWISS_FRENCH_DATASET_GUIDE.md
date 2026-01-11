# 🇨🇭 Swiss French Dataset Collection Guide

**Goal**: Create high-quality datasets for Swiss French dialects (Valais, Geneva, Fribourg) to extend TraductAL with Apertus8B fine-tuning.

**Target**: 20,000-50,000 parallel examples per dialect (matching Romansh dataset structure)

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Data Collection Tools](#data-collection-tools)
3. [Data Sources](#data-sources)
4. [Collection Workflow](#collection-workflow)
5. [Quality Control](#quality-control)
6. [Training Dataset Creation](#training-dataset-creation)

---

## 🚀 Quick Start

### Step 1: Setup Dataset Structure

```bash
cd /home/aldn/TraductAL/TraductAL

# Create directory structure and starter data
python3 swiss_french_dataset_builder.py --setup --create-all
```

**This creates:**
- ✅ Directory structure (mirroring Romansh dataset)
- ✅ Starter dictionaries for 3 dialects (~150 entries each)
- ✅ Sentence templates (~50 per dialect)
- ✅ Idiom identification examples
- ✅ Validation templates (CSV files)

### Step 2: Generate Synthetic Data

```bash
# Generate 30 translations for Valais dialect with validation workflow
python3 swiss_french_synthetic_generator.py \
  --dialect valais \
  --generate 30 \
  --validation
```

### Step 3: Check Progress

```bash
python3 swiss_french_dataset_builder.py --stats
```

---

## 🛠️ Data Collection Tools

### Tool 1: `swiss_french_dataset_builder.py`

**Main dataset management tool**

```bash
# Setup structure
python3 swiss_french_dataset_builder.py --setup

# Create starter dictionary for Valais
python3 swiss_french_dataset_builder.py --dialect valais --dictionary

# Create sentence templates
python3 swiss_french_dataset_builder.py --dialect geneva --sentences

# Create idiom examples
python3 swiss_french_dataset_builder.py --dialect fribourg --idioms

# Import CSV dictionary
python3 swiss_french_dataset_builder.py \
  --dialect valais \
  --import-csv my_valais_dictionary.csv

# Create validation template
python3 swiss_french_dataset_builder.py \
  --dialect geneva \
  --validation-template

# Import validated CSV
python3 swiss_french_dataset_builder.py \
  --dialect valais \
  --import-validated datasets/swiss_french/Validation/validation_template_valais.csv

# Show statistics
python3 swiss_french_dataset_builder.py --stats

# Export to HuggingFace format
python3 swiss_french_dataset_builder.py --export
```

### Tool 2: `swiss_french_synthetic_generator.py`

**AI-powered synthetic data generation using Apertus8B**

```bash
# Generate 50 translations with validation workflow
python3 swiss_french_synthetic_generator.py \
  --dialect valais \
  --generate 50 \
  --validation

# Generate from custom input file
python3 swiss_french_synthetic_generator.py \
  --dialect geneva \
  --input my_sentences.txt \
  --generate 100 \
  --validation

# Import validated synthetic data
python3 swiss_french_synthetic_generator.py \
  --import-validated datasets/swiss_french/Validation/synthetic_valais_20251224_120000.json
```

---

## 📚 Data Sources

### Priority 1: Dictionary Data (5,000-15,000 entries)

#### A. **Glossaire des patois de la Suisse romande**
- Website: https://www.gpsr.ch/
- Content: Comprehensive Swiss French dialect dictionary
- Format: Manual extraction required

**Collection method:**
1. Create CSV file: `swiss_french_dictionary_source.csv`
   ```csv
   swiss_french,standard_french,dialect,source
   panosse,serpillière,valais,GPSR
   linge,serviette,valais,GPSR
   ça joue,ça va,geneva,GPSR
   ```
2. Import: `python3 swiss_french_dataset_builder.py --dialect valais --import-csv swiss_french_dictionary_source.csv`

#### B. **Regional Dictionaries**
- "Le français de chez nous" (Geneva)
- "Mots de Romandie" (various regions)
- "Trésor des patois romands" (Valais)

**Collection method:**
- Manually transcribe entries to CSV format
- Focus on most common terms first (frequency-based)

### Priority 2: Corpus Collection (10,000-30,000 sentences)

#### A. **Regional Newspapers**

Online sources:
- **Le Nouvelliste** (Valais): https://www.lenouvelliste.ch/
- **Tribune de Genève** (Geneva): https://www.tdg.ch/
- **La Liberté** (Fribourg): https://www.laliberte.ch/
- **24 heures** (Vaud): https://www.24heures.ch/

**Collection method:**
```bash
# Create text file with articles containing dialectal terms
# datasets/swiss_french/Raw_Data/articles_valais.txt

# Then create parallel translations (manual or synthetic)
```

#### B. **RTS (Radio Télévision Suisse) Archives**

Source: https://www.rts.ch/archives/

**Collection method:**
1. Search for regional programs (especially from Valais, Geneva)
2. Transcribe audio with dialectal speech
3. Create parallel standard French translations

#### C. **Social Media & Forums**

Sources:
- Swiss French subreddits: r/Switzerland (French posts)
- Facebook groups: "Mots et expressions de Romandie"
- Forums: forum.wordreference.com (Swiss French threads)

**Collection method:**
- Collect authentic Swiss French expressions
- Create standard French equivalents
- **Important**: Respect privacy and terms of service

### Priority 3: Human Translation (2,000-10,000 validated pairs)

#### A. **Crowdsourcing**

**Platforms:**
- Amazon Mechanical Turk
- Toloka
- Fiverr (hire native speakers)

**Task design:**
```
Task: Translate standard French to Swiss French (Valais dialect)

Instructions:
- Use authentic Valais vocabulary (panosse, linge, etc.)
- Use dialectal number system (septante, huitante, nonante)
- Use meal terminology (déjeuner=breakfast, dîner=lunch, souper=dinner)

Example:
Standard French: "Je vais faire le ménage avec la serpillière"
Swiss French (Valais): "Je vais faire le réduit avec la panosse"
```

#### B. **Academic Partnerships**

Contact:
- **Université de Neuchâtel**: Centre de dialectologie et d'étude du français régional
- **Université de Fribourg**: Département de français
- **Université de Genève**: Linguistique

**Proposal:**
- Offer access to final dataset
- Request existing corpora or student participation
- Potential research collaboration

#### C. **Native Speaker Recruitment**

**Where to find:**
- Swiss universities (language students)
- Swiss linguistic societies
- Local cultural associations in Valais, Geneva, Fribourg

**Payment:**
- Rate: €10-15 per 100 translations
- Quality bonus for accuracy

### Priority 4: Synthetic Generation (5,000-20,000 examples)

**Using Apertus8B:**

```bash
# Generate with validation
python3 swiss_french_synthetic_generator.py \
  --dialect valais \
  --generate 100 \
  --validation

# This creates a JSON file for human review
```

**Advantages:**
- ✅ Fast generation
- ✅ Scalable
- ✅ Good baseline for human correction

**Disadvantages:**
- ⚠️ Requires quality validation
- ⚠️ May not capture all dialectal nuances

---

## 🔄 Collection Workflow

### Phase 1: Foundation (Week 1-2)

**Goal**: 5,000 examples across 3 dialects

```bash
# Day 1-2: Setup and starter data
python3 swiss_french_dataset_builder.py --setup --create-all

# Day 3-5: Dictionary collection
# Manually create CSV from GPSR and regional dictionaries
# Import: python3 swiss_french_dataset_builder.py --dialect valais --import-csv dictionary.csv

# Day 6-10: Synthetic generation
# Generate 500 sentences per dialect
for dialect in valais geneva fribourg; do
  python3 swiss_french_synthetic_generator.py \
    --dialect $dialect \
    --generate 500 \
    --validation
done

# Day 11-14: Human validation
# Review and validate synthetic data
# Import validated data

# Check progress
python3 swiss_french_dataset_builder.py --stats
```

**Deliverable**: ~5,000 examples (minimum viable dataset)

### Phase 2: Growth (Week 3-6)

**Goal**: 20,000 examples (production-ready)

```bash
# Week 3-4: Corpus collection
# - Extract sentences from newspapers
# - Transcribe RTS archives
# - Collect social media expressions

# Week 5-6: Human translation
# - Recruit native speakers
# - Translate high-value sentences
# - Focus on domain-specific vocabulary
```

**Deliverable**: ~20,000 examples (match minimum Romansh target)

### Phase 3: Maturity (Week 7-12)

**Goal**: 50,000+ examples (exceed Romansh baseline)

```bash
# Week 7-9: Academic partnerships
# - Obtain existing corpora
# - Student translation projects

# Week 10-12: Quality improvement
# - Review and correct existing entries
# - Add domain-specific data (medical, legal, etc.)
# - Balance dialect coverage
```

**Deliverable**: 50,000+ examples (production-grade dataset)

---

## ✅ Quality Control

### Validation Checklist

For each translation pair, verify:

1. **Authenticity**
   - [ ] Uses genuine dialectal vocabulary
   - [ ] Follows regional grammar patterns
   - [ ] Natural phrasing (not word-for-word translation)

2. **Dialectal Features**
   - [ ] Correct number system (septante, huitante, nonante)
   - [ ] Correct meal terminology (déjeuner, dîner, souper)
   - [ ] Regional vocabulary (panosse, linge, etc.)

3. **Accuracy**
   - [ ] Meaning preserved from standard French
   - [ ] No translation errors
   - [ ] Appropriate register (formal/informal)

4. **Format**
   - [ ] Valid JSON/JSONL format
   - [ ] Proper UTF-8 encoding
   - [ ] No duplicates

### Validation Workflow

```bash
# 1. Create validation template
python3 swiss_french_dataset_builder.py --dialect valais --validation-template

# 2. Fill in translations in CSV/Excel
# Open: datasets/swiss_french/Validation/validation_template_valais.csv

# 3. Import validated data
python3 swiss_french_dataset_builder.py \
  --dialect valais \
  --import-validated datasets/swiss_french/Validation/validation_template_valais.csv

# 4. For synthetic data:
# Review JSON file, set approved: true for good translations
python3 swiss_french_synthetic_generator.py \
  --import-validated datasets/swiss_french/Validation/synthetic_valais_*.json
```

### Quality Metrics

Track these metrics:

```python
# Run statistics
python3 swiss_french_dataset_builder.py --stats

# Target metrics:
# - Dictionary entries: 5,000+ per dialect
# - Sentence pairs: 10,000+ per dialect
# - Human-validated: 20%+ of total
# - Idioms: 500+ per dialect
```

---

## 🎓 Training Dataset Creation

### Step 1: Consolidate Data

```bash
# Generate statistics and review
python3 swiss_french_dataset_builder.py --stats

# Expected structure:
# datasets/swiss_french/
# ├── Dictionary/
# │   ├── sft_dictionary_valais.jsonl (5,000+ entries)
# │   ├── sft_dictionary_geneva.jsonl (5,000+ entries)
# │   └── sft_dictionary_fribourg.jsonl (5,000+ entries)
# ├── Human_Translations/
# │   └── SFT_Human.jsonl (2,000+ entries)
# ├── Idiom_identification/
# │   └── sft_idiom_identification.jsonl (1,000+ entries)
# └── Synthetic_Translation/
#     ├── sft_valais_quality_filtered.jsonl (3,000+ entries)
#     ├── sft_geneva_quality_filtered.jsonl (3,000+ entries)
#     └── sft_fribourg_quality_filtered.jsonl (3,000+ entries)
```

### Step 2: Export to HuggingFace

```bash
# Export combined dataset
python3 swiss_french_dataset_builder.py --export

# Creates: datasets/swiss_french/huggingface_export/
```

### Step 3: Upload to HuggingFace (Optional)

```bash
# Install HuggingFace CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create dataset repo
huggingface-cli repo create swiss-french-dialects --type dataset

# Upload
cd datasets/swiss_french/huggingface_export
git init
git add .
git commit -m "Initial Swiss French dialect dataset"
git remote add origin https://huggingface.co/datasets/YOUR_USERNAME/swiss-french-dialects
git push -u origin main
```

### Step 4: Fine-tune Apertus8B

```bash
# Use existing training infrastructure
# Adapt train_nllb_hf_spaces.py for Apertus8B

# Or use HuggingFace Trainer
python train_apertus_swiss_french.py \
  --model ~/Apertus8B \
  --dataset datasets/swiss_french/huggingface_export \
  --epochs 10 \
  --learning-rate 2e-5
```

---

## 📊 Dataset Size Targets

| Milestone | Examples | Timeline | Status |
|-----------|----------|----------|--------|
| MVP | 5,000 | Week 1-2 | Starter data ready ✅ |
| Minimum | 20,000 | Week 3-6 | Collection phase |
| Target | 46,000 | Week 7-10 | Match Romansh |
| Stretch | 100,000+ | Week 11-16 | Exceed baseline |

---

## 🎯 Recommended Collection Strategy

### Best ROI Approach

1. **Dictionary focus** (Week 1-2)
   - High impact per entry
   - Foundation for synthetic generation
   - Target: 10,000 terms across dialects

2. **Synthetic + validation** (Week 3-4)
   - Scale quickly with AI
   - Human validation for quality
   - Target: 10,000 validated sentences

3. **Corpus collection** (Week 5-6)
   - Authentic language use
   - Domain coverage
   - Target: 5,000+ real-world sentences

4. **Human translation** (Week 7-8)
   - High-quality validation
   - Fill gaps
   - Target: 5,000+ validated pairs

**Total**: ~30,000 examples in 8 weeks (viable for training)

---

## 📞 Resources & Support

### Documentation
- This guide: `SWISS_FRENCH_DATASET_GUIDE.md`
- Dataset builder: `swiss_french_dataset_builder.py`
- Synthetic generator: `swiss_french_synthetic_generator.py`

### External Resources
- **GPSR**: https://www.gpsr.ch/
- **RTS Archives**: https://www.rts.ch/archives/
- **Swiss French Reddit**: r/Switzerland (French section)

### Academic Contacts
- **Université de Neuchâtel**: Centre de dialectologie
- **Université de Fribourg**: Linguistique française
- **Université de Genève**: ELCF (Étude du français en Suisse)

---

## ✅ Next Steps

1. **Run setup**: `python3 swiss_french_dataset_builder.py --setup --create-all`
2. **Generate synthetic data**: Try generating 30 translations for testing
3. **Start dictionary collection**: Focus on GPSR and common terms
4. **Set up validation workflow**: Create templates and recruit validators

**Your journey to Swiss French dialect support starts here!** 🇨🇭🚀
