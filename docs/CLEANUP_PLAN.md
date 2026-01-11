# TraductAL Directory Cleanup Plan

## Current Status
- **Total files**: 103 files in root directory
- **Markdown docs**: 43 documentation files
- **Python/Shell scripts**: 37 executable files
- **Problem**: Too cluttered for distribution to linguists/computational linguists

## Essential Files for Linguists & Computational Linguists

### Core Documentation (Keep in Root)
1. `README.md` - Main user-facing documentation
2. `LICENSE` - Legal requirements
3. `QUICKSTART.md` - Quick start guide
4. `AUTHORSHIP_AND_ATTRIBUTION.md` - Academic citation info

### Core Application Files (Keep in Root)
1. `gradio_app.py` - Main web interface (65+ languages)
2. `unified_translator.py` - Unified translation engine
3. `nllb_translator.py` - NLLB-200 engine
4. `apertus_translator.py` - Apertus-8B engine
5. `apertus_trealla_hybrid.py` - Hybrid neural-symbolic system
6. `whisper_stt.py` - Speech-to-text
7. `tts_engine.py` - Text-to-speech
8. `startup_check.py` - System verification

### Core Scripts (Keep in Root)
1. `start_gradio.sh` - Launch main interface
2. `translate_enhanced.sh` - CLI translation
3. `download_nllb_200.py` - Model downloader

### Core Requirements (Keep in Root)
1. `requirements.txt` - Python dependencies
2. `requirements_enhanced.txt` - Optional features

### Core Directories (Keep)
1. `glossary_parser/` - Prolog DCG parser (linguistic focus)
2. `models/` - Model storage (created on first run)
3. `datasets/` - Training data (if exists)

---

## Files to MOVE to docs/ folder

### Documentation Files (43 total → Move 39 to docs/)
**Move to docs/:**
- `README_DETAILED.md` ⭐ (detailed technical docs)
- `ADD_LANGUAGES_GUIDE.md`
- `APERTUS_TREALLA_INTEGRATION.md`
- `APERTUS_TREALLA_QUICKSTART.md`
- `BATCH_TRANSLATION_EXAMPLES.md`
- `CHAMPOLLION_INSIGHT.md`
- `DCG_PARSER_SUMMARY.md`
- `DEPLOYMENT_GUIDE.md`
- `DOCKER_DEPLOYMENT.md`
- `EVALUATION_SUMMARY.md`
- `FUTURE_RESEARCH_DIRECTIONS.md`
- `GLOSSARY_EXTRACTION_QUICKSTART.md`
- `INTEGRATION_ARCHITECTURE.md`
- `INTEGRATION_SUMMARY.md`
- `ISSUES_AND_SOLUTIONS.md`
- `LANGUAGE_EXPANSION_SUMMARY.md`
- `LICENSE_INFO.md`
- `MIGRATION_SUMMARY.md`
- `MULTIMODAL_GUIDE.md`
- `NLLB_UPGRADE_GUIDE.md`
- `PDF_GLOSSARY_EXTRACTION_GUIDE.md`
- `PRODUCTION_DEPLOYMENT_SUMMARY.md`
- `PRODUCTION_READINESS.md`
- `PROJECT_COMPLETION_SUMMARY.md`
- `QUICK_REFERENCE.md`
- `QUICK_START_TTS.md`
- `README_DOCKER_SPACE.md`
- `README_HF.md`
- `ROMANSH_GUIDE.md`
- `SWISS_FRENCH_DATASET_GUIDE.md`
- `SWISS_FRENCH_DOCS_INDEX.md`
- `SWISS_FRENCH_INTEGRATION_ROADMAP.md`
- `SWISS_FRENCH_PROJECT_STATUS.md`
- `SWISS_FRENCH_QUICKSTART.md`
- `SWISS_FRENCH_README.md`
- `SWISS_FRENCH_SETUP_SUMMARY.md`
- `TRAINING_GUIDE.md`
- `TRAINING_SOLUTIONS.md`
- `TTS_INTEGRATION_SUMMARY.md`
- `WHISPER_INTEGRATION.md`

---

## Files to MOVE to scripts/ folder

### Utility Scripts
**Move to scripts/:**
- `app.py` (basic interface, superseded by gradio_app.py)
- `batch_news_translator.py`
- `diagnostic_app.py`
- `download_finetuned_model.py`
- `download_romansh_dataset.py`
- `enhanced_app.py`
- `examine_dataset.py`
- `fixed_multi_model_translator.py`
- `glossary_extractor.py`
- `multi_model_translator.py`
- `professional_app.py`
- `professional_app_fixed.py`
- `progressive_app_v1.py`
- `progressive_app_v2.py`
- `simple_working_app.py`
- `swiss_french_dataset_builder.py`
- `swiss_french_synthetic_generator.py`
- `test_language_expansion.py`
- `test_new_languages.py`
- `test_transcription.py`
- `test_whisper_multilang.py`
- `train_nllb_hf_spaces.py`
- `translate_romansh.sh`
- `example_dataset_workflow.sh`
- `run_training.sh`
- `test_pdf_extraction.sh`

### Training Files
**Move to scripts/training/:**
- `train_nllb_colab.ipynb`

---

## Files to MOVE to data/ folder

### Test Data and Sample Files
**Move to data/samples/:**
- `input.txt`
- `osage-full.txt`
- `raw_glossaire_vaud.txt`
- `test_extraction_vaud.txt`
- `manual_sample_vaud.csv`
- `vaud_entries.json`
- `vaud_entries_corrected.json`
- `magazin_radio_AUDI20251222_RS_0007_37f4da7a98124418a448857858fb2035.mp3`

---

## Files to MOVE to docker/ folder

**Move to docker/:**
- `Dockerfile`
- `Dockerfile.production`
- `docker-compose.yml`
- `.dockerignore` (if exists)

---

## Directories to Keep/Create

### Keep:
- `glossary_parser/` - Core linguistic component
- `models/` - Auto-created
- `datasets/` - If exists
- `__pycache__/` - Auto-generated (add to .gitignore)
- `audio_chunks/` - Auto-created during use

### Create:
- `docs/` - All documentation
- `scripts/` - Utility scripts
- `scripts/training/` - Training-related scripts
- `data/` - Sample data
- `data/samples/` - Test files
- `docker/` - Docker files

---

## Final Clean Root Structure (17 files + 5 dirs)

### Files (17):
```
README.md
LICENSE
QUICKSTART.md
AUTHORSHIP_AND_ATTRIBUTION.md
gradio_app.py
unified_translator.py
nllb_translator.py
apertus_translator.py
apertus_trealla_hybrid.py
whisper_stt.py
tts_engine.py
startup_check.py
start_gradio.sh
translate_enhanced.sh
download_nllb_200.py
requirements.txt
requirements_enhanced.txt
```

### Directories (5):
```
glossary_parser/    (Core linguistic component)
docs/               (39 documentation files)
scripts/            (26 utility scripts + training/)
data/               (8 sample files)
docker/             (3 Docker files)
```

---

## Benefits of Cleanup

1. **Cleaner presentation** for linguists and computational linguists
2. **Easier to navigate** - core files immediately visible
3. **Professional appearance** for academic distribution
4. **Better for GitHub/Hugging Face** eventual upload
5. **Maintains all functionality** - nothing deleted, just organized

---

## Implementation Steps

1. Create new directories: `docs/`, `scripts/`, `scripts/training/`, `data/samples/`, `docker/`
2. Move files according to plan above
3. Update README.md documentation links
4. Update import paths if necessary (unlikely - Python files stay functional)
5. Test that `./start_gradio.sh` still works
6. Update .gitignore to exclude `__pycache__/`, `audio_chunks/`, `models/`

---

## Ready for Distribution

After cleanup, the root directory will show:
- Clear purpose (translation system)
- Core files only
- Easy to understand structure
- Professional organization
- Ready for linguists/computational linguists mailing lists
