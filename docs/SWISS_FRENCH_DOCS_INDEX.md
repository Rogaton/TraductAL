# 📚 Swiss French Dialect Project - Documentation Index

**Quick Navigation**: Find the right document for your task

---

## 🚀 Getting Started

| I want to... | Read this document |
|--------------|-------------------|
| **Get a quick overview** | [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md) ⭐ **START HERE** |
| **Understand the project in 5 minutes** | [`SWISS_FRENCH_QUICKSTART.md`](SWISS_FRENCH_QUICKSTART.md) |
| **See current progress** | [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md) (Stats section) |

---

## 🔧 Working with Glossaries

| I want to... | Read this document |
|--------------|-------------------|
| **Parse a new glossary** | [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md) ⭐ |
| **Extract PDF text** | [`PDF_GLOSSARY_EXTRACTION_GUIDE.md`](PDF_GLOSSARY_EXTRACTION_GUIDE.md) |
| **Quick glossary extraction** | [`GLOSSARY_EXTRACTION_QUICKSTART.md`](GLOSSARY_EXTRACTION_QUICKSTART.md) |
| **Understand the DCG parser** | [`DCG_PARSER_SUMMARY.md`](DCG_PARSER_SUMMARY.md) |
| **Debug parsing issues** | [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md) (Troubleshooting section) |

### Quick Commands
```bash
# Parse a glossary
cd /home/aldn/TraductAL/TraductAL/glossary_parser
./parse_vaudois.sh -i INPUT.txt -o OUTPUT.csv

# Get help
./parse_vaudois.sh --help
```

---

## 📊 Dataset Management

| I want to... | Read this document |
|--------------|-------------------|
| **Understand dataset structure** | [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) |
| **Import glossary CSV** | [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) (Import section) |
| **Check dataset statistics** | [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md) (Stats section) |
| **Generate synthetic data** | [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) (Synthetic section) |
| **Validate dataset quality** | [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) (Validation section) |
| **Export to HuggingFace** | [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) (Export section) |

### Quick Commands
```bash
# Import glossary
cd /home/aldn/TraductAL/TraductAL
python3 swiss_french_dataset_builder.py --dialect DIALECT --import-csv FILE.csv

# Check stats
python3 swiss_french_dataset_builder.py --stats

# Get help
python3 swiss_french_dataset_builder.py --help
```

---

## 🔗 TraductAL Integration

| I want to... | Read this document |
|--------------|-------------------|
| **See if integration is possible** | [`INTEGRATION_SUMMARY.md`](INTEGRATION_SUMMARY.md) ⭐ **QUICK ANSWER** |
| **Understand integration architecture** | [`INTEGRATION_ARCHITECTURE.md`](INTEGRATION_ARCHITECTURE.md) |
| **Plan integration timeline** | [`SWISS_FRENCH_INTEGRATION_ROADMAP.md`](SWISS_FRENCH_INTEGRATION_ROADMAP.md) |
| **See code changes needed** | [`INTEGRATION_ARCHITECTURE.md`](INTEGRATION_ARCHITECTURE.md) (Code Modification section) |
| **Understand modality support** | [`INTEGRATION_SUMMARY.md`](INTEGRATION_SUMMARY.md) (Feature Matrix section) |

### Key Findings
✅ **Text translation**: Full support
⚠️ **Speech translation**: Good support (input via Whisper)
❌ **Text-to-speech**: Limited (workarounds available)

---

## 📖 Technical Reference

| I want to... | Read this document |
|--------------|-------------------|
| **Understand DCG parser internals** | [`glossary_parser/README.md`](glossary_parser/README.md) |
| **See dataset format specification** | [`datasets/swiss_french/README.md`](datasets/swiss_french/README.md) |
| **Review Prolog grammar rules** | [`glossary_parser/grammar.pl`](glossary_parser/grammar.pl) (code) |
| **Understand lexicon structure** | [`glossary_parser/lexicon.pl`](glossary_parser/lexicon.pl) (code) |

---

## 🔍 Troubleshooting

| Problem | Solution Document |
|---------|------------------|
| **Parser not working** | [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md) (Troubleshooting section) |
| **PDF extraction failing** | [`PDF_GLOSSARY_EXTRACTION_GUIDE.md`](PDF_GLOSSARY_EXTRACTION_GUIDE.md) (Troubleshooting) |
| **Low parsing accuracy** | [`DCG_PARSER_SUMMARY.md`](DCG_PARSER_SUMMARY.md) (Quality section) |
| **Dataset import errors** | [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) (Validation) |
| **Integration questions** | [`SWISS_FRENCH_INTEGRATION_ROADMAP.md`](SWISS_FRENCH_INTEGRATION_ROADMAP.md) (FAQ) |

---

## 📂 Document Types

### Overview Documents (Start Here)
1. [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md) - **Master status report** ⭐
2. [`SWISS_FRENCH_QUICKSTART.md`](SWISS_FRENCH_QUICKSTART.md) - Quick start guide
3. [`INTEGRATION_SUMMARY.md`](INTEGRATION_SUMMARY.md) - Integration quick answer

### Detailed Guides
4. [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) - Dataset management
5. [`PDF_GLOSSARY_EXTRACTION_GUIDE.md`](PDF_GLOSSARY_EXTRACTION_GUIDE.md) - PDF extraction
6. [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md) - Parser usage
7. [`SWISS_FRENCH_INTEGRATION_ROADMAP.md`](SWISS_FRENCH_INTEGRATION_ROADMAP.md) - Integration master plan

### Quick References
8. [`GLOSSARY_EXTRACTION_QUICKSTART.md`](GLOSSARY_EXTRACTION_QUICKSTART.md) - Glossary quick start
9. [`INTEGRATION_ARCHITECTURE.md`](INTEGRATION_ARCHITECTURE.md) - Technical architecture

### Technical Deep Dives
10. [`DCG_PARSER_SUMMARY.md`](DCG_PARSER_SUMMARY.md) - DCG parser internals
11. [`glossary_parser/README.md`](glossary_parser/README.md) - Parser README
12. [`datasets/swiss_french/README.md`](datasets/swiss_french/README.md) - Dataset README

### Supporting Documentation
13. [`SWISS_FRENCH_SETUP_SUMMARY.md`](SWISS_FRENCH_SETUP_SUMMARY.md) - Setup summary
14. [`WHISPER_INTEGRATION.md`](WHISPER_INTEGRATION.md) - Whisper STT integration
15. [`TTS_INTEGRATION_SUMMARY.md`](TTS_INTEGRATION_SUMMARY.md) - TTS integration

---

## 🎯 Task-Based Navigation

### "I Just Found a New Glossary!"

**Follow this workflow**:

1. **Extract text from PDF**
   - Read: [`PDF_GLOSSARY_EXTRACTION_GUIDE.md`](PDF_GLOSSARY_EXTRACTION_GUIDE.md)
   - Command:
     ```bash
     cd /home/aldn/TraductAL/TraductAL
     python3 glossary_extractor.py --pdf GLOSSARY.pdf --output raw_glossaire_DIALECT.txt --extract-text-only
     ```

2. **Parse with DCG**
   - Read: [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md)
   - Command:
     ```bash
     cd glossary_parser
     ./parse_vaudois.sh -i ../raw_glossaire_DIALECT.txt -o DIALECT-glossary.csv
     ```

3. **Import to dataset**
   - Read: [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md)
   - Command:
     ```bash
     cd ..
     python3 swiss_french_dataset_builder.py --dialect DIALECT --import-csv glossary_parser/DIALECT-glossary.csv
     ```

4. **Check progress**
   - Command:
     ```bash
     python3 swiss_french_dataset_builder.py --stats
     ```

### "I Want to Generate More Data"

**Synthetic generation workflow**:

1. **Understand synthetic generation**
   - Read: [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md) (Synthetic section)

2. **Generate translations**
   - Command:
     ```bash
     python3 swiss_french_synthetic_generator.py --dialect DIALECT --count 1000
     ```

3. **Validate quality**
   - Command:
     ```bash
     python3 swiss_french_dataset_builder.py --validate DIALECT
     ```

### "I'm Ready to Integrate into TraductAL"

**Integration planning workflow**:

1. **Quick feasibility check**
   - Read: [`INTEGRATION_SUMMARY.md`](INTEGRATION_SUMMARY.md) (2-minute read)

2. **Understand architecture**
   - Read: [`INTEGRATION_ARCHITECTURE.md`](INTEGRATION_ARCHITECTURE.md)

3. **Plan implementation**
   - Read: [`SWISS_FRENCH_INTEGRATION_ROADMAP.md`](SWISS_FRENCH_INTEGRATION_ROADMAP.md)

4. **Check dataset size**
   - Need 20,000-30,000 examples minimum
   - Command: `python3 swiss_french_dataset_builder.py --stats`

---

## 📊 Document Sizes & Read Times

| Document | Size | Read Time | Type |
|----------|------|-----------|------|
| `SWISS_FRENCH_PROJECT_STATUS.md` | ~25KB | 10 min | Overview |
| `INTEGRATION_SUMMARY.md` | 3.6KB | 2 min | Quick ref |
| `SWISS_FRENCH_QUICKSTART.md` | 9KB | 5 min | Quick start |
| `glossary_parser/USAGE.md` | 12KB | 8 min | Usage guide |
| `SWISS_FRENCH_INTEGRATION_ROADMAP.md` | 16KB | 12 min | Planning |
| `INTEGRATION_ARCHITECTURE.md` | 17KB | 15 min | Technical |
| `SWISS_FRENCH_DATASET_GUIDE.md` | 14KB | 10 min | Guide |
| `PDF_GLOSSARY_EXTRACTION_GUIDE.md` | 15KB | 10 min | Guide |
| `DCG_PARSER_SUMMARY.md` | 8KB | 6 min | Technical |

---

## 🔖 Document Status

| Document | Status | Last Updated | Notes |
|----------|--------|--------------|-------|
| `SWISS_FRENCH_PROJECT_STATUS.md` | ✅ Current | Dec 24, 2025 | Master status |
| `INTEGRATION_SUMMARY.md` | ✅ Current | Dec 24, 2025 | Complete |
| `INTEGRATION_ARCHITECTURE.md` | ✅ Current | Dec 24, 2025 | Complete |
| `SWISS_FRENCH_INTEGRATION_ROADMAP.md` | ✅ Current | Dec 24, 2025 | Complete |
| `glossary_parser/USAGE.md` | ✅ Current | Dec 24, 2025 | Complete |
| `SWISS_FRENCH_DATASET_GUIDE.md` | ✅ Current | Dec 24, 2025 | Complete |
| All others | ✅ Current | Dec 24, 2025 | Complete |

---

## 💡 Quick Tips

### First Time Here?
**Start with**: [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md)

### Need to Parse a Glossary?
**Go to**: [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md)

### Wondering About Integration?
**Read**: [`INTEGRATION_SUMMARY.md`](INTEGRATION_SUMMARY.md) (2 minutes)

### Want Technical Details?
**See**: [`INTEGRATION_ARCHITECTURE.md`](INTEGRATION_ARCHITECTURE.md)

### Lost or Confused?
**Return to**: This index document

---

## 📞 Command Cheat Sheet

### Most Used Commands
```bash
# Parse glossary
cd /home/aldn/TraductAL/TraductAL/glossary_parser
./parse_vaudois.sh -i INPUT.txt -o OUTPUT.csv

# Import to dataset
cd /home/aldn/TraductAL/TraductAL
python3 swiss_french_dataset_builder.py --dialect DIALECT --import-csv FILE.csv

# Check stats
python3 swiss_french_dataset_builder.py --stats

# Generate synthetic
python3 swiss_french_synthetic_generator.py --dialect DIALECT --count 1000

# Validate dataset
python3 swiss_french_dataset_builder.py --validate DIALECT

# Get help
./parse_vaudois.sh --help
python3 swiss_french_dataset_builder.py --help
python3 swiss_french_synthetic_generator.py --help
```

---

## 🗂️ File Structure Reference

```
/home/aldn/TraductAL/TraductAL/
│
├── 📚 Documentation (This level)
│   ├── SWISS_FRENCH_PROJECT_STATUS.md      ⭐ START HERE
│   ├── SWISS_FRENCH_DOCS_INDEX.md          ⭐ THIS FILE
│   ├── INTEGRATION_SUMMARY.md              ⭐ QUICK INTEGRATION CHECK
│   ├── SWISS_FRENCH_QUICKSTART.md
│   ├── SWISS_FRENCH_INTEGRATION_ROADMAP.md
│   ├── INTEGRATION_ARCHITECTURE.md
│   ├── SWISS_FRENCH_DATASET_GUIDE.md
│   ├── PDF_GLOSSARY_EXTRACTION_GUIDE.md
│   ├── GLOSSARY_EXTRACTION_QUICKSTART.md
│   ├── DCG_PARSER_SUMMARY.md
│   ├── SWISS_FRENCH_SETUP_SUMMARY.md
│   ├── WHISPER_INTEGRATION.md
│   └── TTS_INTEGRATION_SUMMARY.md
│
├── 🔧 Tools
│   ├── swiss_french_dataset_builder.py     ⭐ Main dataset tool
│   ├── swiss_french_synthetic_generator.py
│   └── glossary_extractor.py
│
├── 📂 glossary_parser/                     ⭐ Parser directory
│   ├── parse_vaudois.sh                    ⭐ Use this to parse!
│   ├── parse_glossary.pl                   (DCG parser)
│   ├── grammar.pl                          (Grammar rules)
│   ├── lexicon.pl                          (Lexicon module)
│   ├── USAGE.md                            ⭐ Parser documentation
│   ├── README.md
│   └── vaud-glossary.csv                   (Latest Vaud extraction)
│
└── 📊 datasets/swiss_french/               ⭐ Dataset directory
    ├── Dictionary/
    │   ├── sft_dictionary_vaud.jsonl       (2,434 entries)
    │   └── sft_dictionary_valais.jsonl     (45 entries)
    ├── Human_Translations/
    ├── Idiom_identification/
    ├── Synthetic_Translation/
    ├── Validation/
    ├── Raw_Data/
    └── README.md
```

---

## ✨ Quick Navigation Links

### By Role

**I'm a linguist** → Start with [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md)
**I'm a developer** → Start with [`INTEGRATION_ARCHITECTURE.md`](INTEGRATION_ARCHITECTURE.md)
**I want quick answers** → Start with [`INTEGRATION_SUMMARY.md`](INTEGRATION_SUMMARY.md)
**I have a glossary** → Start with [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md)

### By Task

**Parsing** → [`glossary_parser/USAGE.md`](glossary_parser/USAGE.md)
**Dataset management** → [`SWISS_FRENCH_DATASET_GUIDE.md`](SWISS_FRENCH_DATASET_GUIDE.md)
**Integration** → [`SWISS_FRENCH_INTEGRATION_ROADMAP.md`](SWISS_FRENCH_INTEGRATION_ROADMAP.md)
**Status check** → [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md)

---

**Last Updated**: December 24, 2025
**Total Documents**: 15
**Status**: ✅ Complete infrastructure, ready for next glossary

**Questions?** Check the document index above or start with [`SWISS_FRENCH_PROJECT_STATUS.md`](SWISS_FRENCH_PROJECT_STATUS.md)
