# TraductAL - Hybrid Neural-Symbolic Translation Engine

A completely offline, privacy-focused multilingual translation system supporting **50+ languages** and combining two state-of-the-art translation engines with Prolog-based linguistic validation. The system uses **Meta's NLLB-200** for mainstream languages (200+ available) and the open-source **Apertus-8B** LLM for low-resource and endangered languages (1811 languages), with **Trealla Prolog** DCG parsers providing symbolic validation and error correction.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   TraductAL Hybrid System                    │
│              65+ Languages Production Ready                  │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
         ┌──────────▼──────────┐   ┌───▼────────────────────┐
         │   NLLB-200 (Meta)   │   │  Apertus-8B (HF)       │
         │   200+ languages    │   │  1811 languages        │
         │   50 in UI          │   │  15+ low-resource      │
         │   Fast & accurate   │   │  Specialized dialects  │
         └──────────┬──────────┘   └───┬────────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │  Trealla Prolog   │
                    │  DCG Validation   │
                    │  - Grammar check  │
                    │  - Glossary parse │
                    │  - Error detect   │
                    └───────────────────┘
```

## ⚠️ Development Status & Disclaimer

**USE AT YOUR OWN RISK** - This system is currently in active development and not ready for production use.

### Known Limitations:
- **Incomplete translations**: Some words or text segments may be missing from output
- **Quality varies**: Translation accuracy depends on language pair and text complexity
- **No quality guarantees**: Results may not be suitable for professional or critical use
- **Model limitations**: Base models may require fine-tuning for specific domains
- **Low-resource language support**: Continuously being expanded and validated
- **UI Language Support**: Web interfaces now support **50+ mainstream languages** plus **15+ low-resource/Swiss languages**
  - NLLB-200: 50 most common languages in UI (200+ available via API/CLI)
  - Apertus-8B: 15+ low-resource languages including all Romansh variants (1811 languages available via API/CLI)
  - Expanded from original 12 languages in December 2025
- **NLLB-1.3B in UI**: Web interfaces use the faster 1.3B model, not the higher-quality 3.3B model

### Recommended Use:
- ✅ Development and testing purposes
- ✅ Research on low-resource languages and dialects
- ✅ Privacy-focused translation where perfect accuracy isn't critical
- ✅ Linguistic analysis with Prolog validation
- ❌ Production systems requiring reliable translations
- ❌ Professional document translation without human review
- ❌ Critical communications or legal documents

## 🔒 Privacy & Security
- **100% Offline**: No internet connection required after setup
- **Zero Data Leakage**: All processing happens locally
- **Professional Grade**: Suitable for confidential document translation
- **No Logging**: No translation history stored externally
- **Open Source**: Apertus-8B is fully open-source (unlike proprietary NLLB-200)

## 🌍 Language Support

TraductAL now supports **65+ languages** in its web interface, with access to 200+ (NLLB-200) and 1811 (Apertus-8B) languages via API/CLI.

### NLLB-200 (Mainstream Languages) - 50 Languages in UI
**Core European Languages (6)**:
English, French, German, Italian, Spanish, Portuguese

**Major World Languages (6)**:
Russian, Chinese, Hindi, Arabic, Japanese, Korean

**Additional European Languages (12)**:
Dutch, Polish, Czech, Swedish, Danish, Norwegian, Finnish, Greek, Turkish, Hungarian, Romanian, Icelandic

**Major Asian Languages (8)**:
Vietnamese, Thai, Indonesian, Malay, Tamil, Bengali, Urdu, Persian, Hebrew (9 total)

**African Languages (4)**:
Swahili, Amharic, Hausa, Yoruba

**Regional European Languages (3)**:
Catalan, Galician, Basque

**Slavic Languages (9)**:
Ukrainian, Bulgarian, Serbian, Croatian, Slovak, Slovenian, Macedonian, Lithuanian, Latvian

**Baltic & Other (3)**:
Albanian, Estonian, Latvian

*Plus 150+ more languages available via API/CLI*

### Apertus-8B (Low-Resource & Endangered Languages) - 15+ Languages in UI
**Swiss-German Dialects (6)**:
All major Romansh variants (Sursilvan, Vallader, Puter, Surmiran, Sutsilvan, Rumantsch Grischun)

**Celtic & Regional Languages (9)**:
Occitan, Breton, Welsh, Scottish Gaelic, Irish, Luxembourgish, Friulian, Ladin, Sardinian

**Swiss French dialects**: Vaud, Geneva, Fribourg, Valais, Neuchâtel, Jura (in development)

*Plus 1796+ more languages available via API/CLI for endangered and low-resource languages*

**Download**: [Apertus-8B on Hugging Face](https://huggingface.co/apertus-8b)
**Dataset**: [Romansh Dataset on Hugging Face](https://huggingface.co/datasets/romansh-dialects)

### Trealla Prolog (Symbolic Validation)
Provides linguistic validation and dependency parsing:
- **Swiss French glossaries**: DCG parser for 1861 Glossaire Vaudois
- **Grammar validation**: Rule-based error detection and correction
- **Hallucination detection**: Symbolic verification of neural outputs

### Related Projects
TraductAL focuses on Romansh and Swiss dialects. For **Coptic language** support, see these separate projects:
- **Coptic Dependency Parser**: [GitHub](https://github.com/Rogation/coptic-dependency-parser) | [Demo on HF](https://huggingface.co/spaces/Norelad/coptic-dependency-parser)
- **Coptic Translation Interface**: [HF Space](https://huggingface.co/spaces/Norelad/coptic-translation-interface)
- **Note**: Coptic requires specialized models (megalaa) trained on CopticScriptorium data, as neither NLLB-200 nor Apertus-8B support Coptic script or language

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: 8GB minimum, 16GB+ recommended (32GB for Apertus-8B on CPU)
- **Storage**: 10-25GB for models
- **OS**: Linux (tested), macOS, Windows
- **Optional**: NVIDIA GPU with 16GB+ VRAM for faster Apertus-8B inference

### Installation

#### 1. Clone and Install Python Dependencies
```bash
# Clone the repository
git clone <repository-url>
cd TraductAL

# Install core dependencies
pip install -r requirements.txt

# Optional: Install enhanced features (Whisper STT, TTS, training)
pip install -r requirements_enhanced.txt
```

#### 2. Download Translation Models

**For NLLB-200 (mainstream languages):**
```bash
# Download NLLB models (1.3B or 3.3B variant)
python download_nllb_200.py
```

**For Apertus-8B (low-resource languages):**
```bash
# Download from Hugging Face
# Option 1: Using huggingface-cli
huggingface-cli download apertus-8b

# Option 2: Using Python
python -c "from transformers import AutoModel; AutoModel.from_pretrained('apertus-8b')"

# Download Romansh dataset
python download_romansh_dataset.py
```

#### 3. Install Trealla Prolog (Optional, for validation)
```bash
# Install Trealla Prolog for DCG validation
cd glossary_parser
./setup_janus.sh
```

### Basic Usage

#### Command-Line Interface
```bash
# NLLB-200: Simple mainstream language translation
./translate_enhanced.sh en fr "Hello, how are you?"

# Apertus-8B: Romansh translation
python apertus_translator.py --src de --tgt rm-sursilv --text "Guten Tag"

# Hybrid with validation
python apertus_trealla_hybrid.py --text "Hello world" --src en --tgt rm-sursilv

# Interactive mode
./translate_enhanced.sh interactive en fr

# List available languages
./translate_enhanced.sh list-languages

# System health check
./translate_enhanced.sh check
```

#### Python API

**Basic NLLB-200 translation:**
```python
from nllb_translator import EnhancedOfflineTranslator

translator = EnhancedOfflineTranslator()
result = translator.translate("Hello world", "en", "fr")
print(result["translation"])  # "Bonjour le monde"
```

**Apertus-8B for low-resource languages:**
```python
from apertus_translator import ApertusTranslator

# Initialize Apertus translator (auto-downloads from HuggingFace if not present)
translator = ApertusTranslator(model_path="apertus-8b")  # HuggingFace model ID
translator.load_model()

# Translate to Romansh Sursilvan
result = translator.translate(
    text="Good morning, how are you?",
    src_lang="en",
    tgt_lang="rm-sursilv"
)

print(f"Translation: {result['translation']}")
print(f"Model: {result['model']}")
print(f"Time: {result['time']}")
```

**Hybrid translation with Prolog validation:**
```python
from apertus_trealla_hybrid import HybridTranslationValidator

# Initialize hybrid validator (uses HuggingFace model)
validator = HybridTranslationValidator(config={
    'apertus_model_id': 'apertus-8b',  # HuggingFace model ID
    'enable_validation': True
})

# Translate with automatic validation
result = validator.translate(
    text="Guten Tag",
    src_lang="de",
    tgt_lang="rm-sursilv",
    validate=True
)

print(f"Translation: {result['translation']}")
print(f"Validation: {result['validation']['status']}")
if result['corrected']:
    print(f"Original: {result['original_neural']}")
```

#### Web Interface (Gradio)

**Option 1: Basic Interface (NLLB-200 only, requires venv)**
```bash
# Launch basic interface with 12 mainstream languages
python app.py

# Access at http://localhost:7860
# Note: Only uses NLLB-200, no Apertus-8B or Romansh support
# Languages: English, French, German, Spanish, Italian, Portuguese, Russian, Swedish, Chinese, Japanese, Korean, Arabic
```

**Option 2: Full Interface (NLLB-200 + Apertus-8B, with venv) - RECOMMENDED**
```bash
# Launch complete interface with both engines
./start_gradio.sh

# Access at http://localhost:7860
# Includes: 50 NLLB mainstream languages + 15+ Apertus low-resource languages
# Uses: NLLB-200-1.3B + Apertus-8B
# Features: Text translation, STT, TTS, Batch translation
# Total: 65+ languages in UI
```

**✨ What's New (December 2025):**
- **Expanded from 12 to 50+ mainstream languages** in the Gradio interface
- **Added 9+ additional low-resource languages** (Celtic, regional European languages)
- **All 6 Romansh variants** fully supported with TTS
- **Major world languages**: Russian, Chinese, Hindi, Arabic, Japanese, Korean now in UI
- **Enhanced coverage**: Slavic, Baltic, Asian, African language families

**📏 Text & Audio Length Handling:**
- **Short texts/audio**: ✅ Optimized for sentences and short paragraphs
- **Long texts**: ⚠️ Limited by model context windows
  - NLLB-200: Handles up to ~512 tokens (approximately 400-500 words)
  - Apertus-8B: Default max_tokens=512 (configurable in Python API)
  - **Workaround**: Use batch translation tab for multi-paragraph documents
- **Long audio files**: ✅ Whisper handles long audio natively (tested with files up to several minutes)
  - Processes entire audio file in one pass
  - No chunking required
- **Audio-to-Audio pipeline**: ⚠️ Inherits text translation length limits
  - STT works with long audio
  - Translation limited by model context window
  - TTS works with generated translation length

## 📊 Model Options & Performance

### NLLB-200-1.3B (Used in Current Gradio Interface)
- **Size**: ~2.6GB
- **Speed**: 0.5-1.0 seconds per sentence (CPU)
- **Memory**: ~3GB RAM
- **Quality**: Very High for common language pairs
- **Languages Available**: 200+ (50 shown in production UI, 12 in basic UI)
- **UI Coverage**: Core European (6) + Major World (6) + Extended European (12) + Asian (9) + African (4) + Regional (3) + Slavic/Baltic (12)
- **Use cases**: All mainstream language pairs including Russian, Chinese, Hindi, Arabic, Japanese, Korean
- **Interface**: Used by both `app.py` (12 languages) and `./start_gradio.sh` (50 languages)

### NLLB-200-3.3B (Available but Not in UI)
- **Size**: ~6.6GB
- **Speed**: 1.0-2.0 seconds per sentence (CPU)
- **Memory**: ~7GB RAM
- **Quality**: Excellent (better than 1.3B)
- **Languages Available**: 200+
- **Use cases**: High-stakes translations, complex texts
- **Interface**: Can be used via Python API and CLI, not in Gradio UI
- **Note**: Recommended for production use requiring maximum quality

### Apertus-8B (Specialized for Low-Resource Languages)
- **Size**: ~16GB (bfloat16)
- **Speed**: 1-3 seconds per sentence (GPU), 5-10 seconds (CPU)
- **Memory**: 16-24GB RAM (GPU), 32GB+ RAM (CPU)
- **Quality**: State-of-the-art for rare languages
- **Languages Available**: 1811 (15+ shown in production UI)
- **UI Coverage**: 6 Romansh variants + 9+ Celtic & Regional European languages (Occitan, Breton, Welsh, Scottish Gaelic, Irish, Luxembourgish, Friulian, Ladin, Sardinian)
- **Use cases**: Swiss dialects (Romansh), Celtic languages, endangered languages, linguistic research
- **Interface**: Available in `./start_gradio.sh` (15+ languages) and via Python API/CLI for all 1811 languages

### Automatic Model Selection
The system automatically selects the best model based on language pair:
```python
# Automatically routes to NLLB-200 for common pairs
translate(text="Hello", src="en", tgt="fr")  # → NLLB-200

# Automatically routes to Apertus-8B for Romansh
translate(text="Hello", src="en", tgt="rm-sursilv")  # → Apertus-8B
```

## 🛠️ System Requirements

### Minimum (NLLB-200 only)
- **Python**: 3.8+
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 3-7GB for NLLB models
- **OS**: Linux, macOS, Windows
- **CPU**: Any modern x86_64 processor

### Recommended (NLLB-200 + Apertus-8B)
- **Python**: 3.10+
- **RAM**: 16GB (32GB for CPU-only Apertus)
- **Storage**: 25GB (models + workspace)
- **OS**: Linux (Ubuntu 20.04+)
- **GPU**: NVIDIA GPU with 16GB+ VRAM (for Apertus-8B)
- **CPU**: Modern multi-core processor (if no GPU)

### For Development & Training
- **RAM**: 32GB+
- **Storage**: 50GB+
- **GPU**: NVIDIA GPU with 24GB+ VRAM (A100, RTX 4090, etc.)
- **CUDA**: 11.8+ for PyTorch

## 📁 Project Structure

```
TraductAL/
├── README.md                          # This file
├── requirements.txt                   # Core Python dependencies
├── requirements_enhanced.txt          # Enhanced features (STT/TTS)
├── requirements_training.txt          # Training dependencies
│
├── Core Translation Engines
│   ├── nllb_translator.py            # NLLB-200 translator (200+ languages)
│   ├── apertus_translator.py         # Apertus-8B translator (1811 languages)
│   ├── apertus_trealla_hybrid.py     # Hybrid neural-symbolic system
│   └── unified_translator.py         # Unified interface (auto-routing)
│
├── Multimodal Components
│   ├── whisper_stt.py                # Speech-to-text (Whisper)
│   ├── tts_engine.py                 # Text-to-speech (MMS-TTS)
│   └── multimodal_translator.py      # Audio-to-audio pipeline
│
├── Prolog/DCG Parsers
│   └── glossary_parser/
│       ├── grammar.pl                # DCG grammar rules
│       ├── lexicon.pl                # Lexicon module
│       ├── trealla_interface.py      # Trealla-Python bridge
│       └── setup_janus.sh            # Prolog setup script
│
├── Web Interfaces
│   ├── app.py                        # Basic Gradio UI
│   ├── enhanced_app.py               # Multimodal Gradio UI
│   └── gradio_app.py                 # Advanced Gradio interface
│
├── Command-Line Tools
│   ├── translate_enhanced.sh         # Main CLI wrapper
│   ├── translate_romansh.sh          # Romansh-specific CLI
│   └── batch_news_translator.py      # Batch processing
│
├── Dataset & Training
│   ├── swiss_french_dataset_builder.py     # Build training datasets
│   ├── glossary_extractor.py               # Extract glossaries
│   ├── train_nllb_hf_spaces.py             # Fine-tuning script
│   └── datasets/                            # Training data
│
├── Documentation
│   ├── APERTUS_TREALLA_INTEGRATION.md      # Hybrid system docs
│   ├── APERTUS_TREALLA_QUICKSTART.md       # Quick start guide
│   ├── DCG_PARSER_SUMMARY.md               # Parser documentation
│   ├── INTEGRATION_ARCHITECTURE.md         # System architecture
│   ├── ROMANSH_GUIDE.md                    # Romansh translation guide
│   ├── MULTIMODAL_GUIDE.md                 # Audio translation guide
│   ├── WHISPER_INTEGRATION.md              # STT integration
│   ├── SWISS_FRENCH_README.md              # Swiss French project
│   └── TRAINING_GUIDE.md                   # Model training guide
│
└── Models
    ├── models/deployed_models/
    │   ├── nllb_200_1.3b/          # NLLB 1.3B model
    │   └── nllb_200_3.3b/          # NLLB 3.3B model
    └── apertus-8b/                 # Downloaded from HuggingFace
```

## 🖥️ User Interfaces Overview

TraductAL provides multiple interfaces for different use cases:

### Web Interface Comparison

| Feature | `app.py` | `./start_gradio.sh` | Python API | CLI |
|---------|----------|---------------------|------------|-----|
| **Model Support** | NLLB-200 only | NLLB-200 + Apertus-8B | Both | Both |
| **Languages Shown** | 12 mainstream | 65+ (50 NLLB + 15 Apertus) | All 200+/1811 | All 200+/1811 |
| **Romansh Support** | ❌ No | ✅ Yes (6 variants) | ✅ Yes | ✅ Yes |
| **World Languages** | ✅ 6 major | ✅ 50+ major | ✅ 200+ | ✅ 200+ |
| **Low-Resource** | ❌ No | ✅ 15+ languages | ✅ 1811 | ✅ 1811 |
| **Model Selection** | Automatic | User choice | User choice | User choice |
| **STT/TTS** | ❌ No | ✅ Yes | ✅ Yes | Partial |
| **NLLB Version** | 1.3B | 1.3B | 1.3B or 3.3B | 1.3B or 3.3B |
| **Virtual Env** | Required | Required | Optional | Optional |
| **Best For** | Quick demos | Production use | Integration | Automation |

### Interface Details

#### 1. Basic Gradio Interface (`app.py`)
```bash
python app.py
```
- **Purpose**: Simple web interface for mainstream languages
- **Languages**: 12 (English, French, German, Spanish, Italian, Portuguese, Russian, Swedish, Chinese, Japanese, Korean, Arabic)
- **Model**: NLLB-200-1.3B only
- **Romansh**: Not supported
- **Apertus-8B**: Not used
- **Good for**: Quick translations between major languages

#### 2. Full Gradio Interface (`./start_gradio.sh`) - **RECOMMENDED**
```bash
./start_gradio.sh
```
- **Purpose**: Complete production-ready multimodal translation system
- **Languages**: 65+ total
  - **50 mainstream languages** (via NLLB-200-1.3B)
    - Core European: English, French, German, Italian, Spanish, Portuguese
    - Major World: Russian, Chinese, Hindi, Arabic, Japanese, Korean
    - Extended European: Dutch, Polish, Czech, Swedish, Danish, Norwegian, Finnish, Greek, Turkish, Hungarian, Romanian, and more
    - Asian: Vietnamese, Thai, Indonesian, Malay, Tamil, Bengali, Urdu, Persian, Hebrew
    - African: Swahili, Amharic, Hausa, Yoruba
    - Slavic & Baltic: Ukrainian, Bulgarian, Serbian, Croatian, Slovak, Slovenian, and more
  - **15+ low-resource languages** (via Apertus-8B)
    - 6 Romansh variants (Sursilvan, Vallader, Puter, Surmiran, Sutsilvan, Rumantsch Grischun)
    - 9+ Celtic & Regional: Occitan, Breton, Welsh, Scottish Gaelic, Irish, Luxembourgish, Friulian, Ladin, Sardinian
- **Model Selection**: User can choose "Auto", "NLLB-200", or "Apertus-8B"
- **Features**: Text translation + Speech-to-Text + Text-to-Speech + Batch translation
- **Romansh**: Full support for all 6 variants with TTS
- **Good for**: Production use, development, testing, comprehensive language coverage

#### 3. Python API (Full Access)
```python
from nllb_translator import EnhancedOfflineTranslator
from apertus_translator import ApertusTranslator
```
- **Purpose**: Programmatic integration
- **Languages**: All supported (200+ NLLB, 1811 Apertus)
- **Model Selection**: Full control (including NLLB-3.3B)
- **Good for**: Custom applications, batch processing, research

#### 4. Command-Line Interface
```bash
./translate_enhanced.sh en fr "Hello world"
python apertus_translator.py --src de --tgt rm-sursilv --text "Guten Tag"
```
- **Purpose**: Shell scripting and automation
- **Languages**: All supported
- **Model Selection**: Full control
- **Good for**: Pipelines, automation, testing

### Language List Status

**✅ Production Ready (December 2025):**
- Full Gradio interface (`./start_gradio.sh`) now includes **65+ languages**
- **NLLB-200**: Expanded to 50 mainstream languages (from original 12)
- **Apertus-8B**: Expanded to 15+ low-resource languages (from original 6 Romansh)
- Covers all major world languages plus Swiss dialects and Celtic languages
- Full model capabilities (200+ and 1811 languages) still available via API/CLI

**📋 Further Expansion:**
To add more languages beyond the current 65+, see `ADD_LANGUAGES_GUIDE.md`:
- Step-by-step instructions for adding any NLLB-200 or Apertus-8B language
- TTS integration for new languages
- Testing procedures

### Model Version in Interfaces

**Current Configuration:**
- Both `app.py` and `./start_gradio.sh` use **NLLB-200-1.3B**
- Higher-quality **NLLB-200-3.3B** is available but not used in web interfaces

**To Use NLLB-3.3B:**
```bash
# Via CLI
./translate_enhanced.sh en fr "Hello" --model nllb_200_3_3b

# Via Python API
translator = EnhancedOfflineTranslator()
result = translator.translate("Hello", "en", "fr", model="nllb_200_3_3b")
```

**Production Recommendation:**
- Consider using NLLB-3.3B for critical translations
- Trade-off: ~2x slower but significantly better quality
- Can be configured in web interfaces by modifying model initialization

## 🔧 Advanced Usage

### Handling Long Texts & Documents

**Length Capability Summary:**

| Modality | Component | Short Content | Long Content | Notes |
|----------|-----------|---------------|--------------|-------|
| **Text Translation** | NLLB-200 | ✅ Perfect | ⚠️ Limited | ~512 tokens (400-500 words) max |
| | Apertus-8B | ✅ Perfect | ⚠️ Limited | ~512 tokens default (configurable) |
| **Audio → Text** | Whisper STT | ✅ Perfect | ✅ Perfect | No length limits, handles hours |
| **Text → Audio** | MMS-TTS | ✅ Perfect | ✅ Good | Synthesizes any length text |
| **Audio → Audio** | Full Pipeline | ✅ Perfect | ⚠️ Limited | Limited by translation step |
| **Batch Files** | Gradio Tab | ✅ Perfect | ✅ Perfect | Line-by-line translation |

**Current Limitations:**
- Translation models have context window limits (~512 tokens ≈ 400-500 words)
- Single-pass translation works best for sentences and short paragraphs
- Long documents require chunking strategies
- **Workaround**: Batch translation tab or Python chunking (see below)

**Option 1: Batch Translation (Gradio Interface)**

The Gradio interface includes a dedicated "Batch Translation" tab for handling multiple sentences or paragraphs.

**Step-by-step Guide:**

1. **Launch the full Gradio interface:**
```bash
./start_gradio.sh
```

2. **Navigate to the "📄 Batch Translation" tab**

3. **Prepare your text file** (one sentence/paragraph per line):
```text
# Example file: document.txt
Guten Morgen! Wie geht es Ihnen?
Ich freue mich, Sie kennenzulernen.
Die Schweiz ist ein schönes Land mit vier Sprachen.
Romansch ist eine der Landessprachen der Schweiz.
Es gibt sechs verschiedene Romansch-Dialekte.
```

4. **Upload the file or paste the text directly**

5. **Select languages:**
   - Source: German
   - Target: Romansh Sursilvan

6. **Click "🌍 Translate All"**

7. **Results** (one translation per line):
```text
Bun di! Co vai a Vus?
Jau ma legrel da enconuscher Vus.
La Svizra è in bel pajais cun quatter linguas.
Il rumantsch è ina da las linguas naziunalas da la Svizra.
I ha ses differents dialects rumantschs.
```

**Key Features:**
- ✅ Each line translated independently
- ✅ No length limit per file (can have hundreds of lines)
- ✅ Preserves line structure
- ✅ Works with all 18 languages in the interface
- ✅ Can paste directly or upload .txt files

**Option 2: Python API with Chunking**
```python
from nllb_translator import EnhancedOfflineTranslator

translator = EnhancedOfflineTranslator()

# Split long text into chunks
def chunk_text(text, max_words=400):
    """Split text into chunks by sentences."""
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_words:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')

    return chunks

# Translate long document
long_text = """[Your long document here...]"""
chunks = chunk_text(long_text)
translations = []

for chunk in chunks:
    result = translator.translate(chunk, "en", "fr")
    translations.append(result["translation"])

final_translation = " ".join(translations)
```

**Option 3: Command-Line Batch Translation**

**Method A: Using the batch translator script**
```bash
# Create an input file
cat > articles.txt << 'EOF'
Guten Morgen! Wie geht es Ihnen?
Ich freue mich, Sie kennenzulernen.
Die Schweiz ist ein schönes Land.
Romansch wird in Graubünden gesprochen.
EOF

# Translate with batch_news_translator.py
python batch_news_translator.py --src de --tgt rm-sursilv --input articles.txt --output translated.txt

# View results
cat translated.txt
```

**Method B: Using shell loops**
```bash
# Create input file
cat > input.txt << 'EOF'
Hello, how are you?
Goodbye, see you later.
Thank you very much.
Have a nice day!
EOF

# Translate line by line
while IFS= read -r line; do
    echo "Translating: $line"
    ./translate_enhanced.sh en fr "$line"
    echo "---"
done < input.txt > output.txt

# View results
cat output.txt
```

**Method C: Using Python for batch processing**
```python
# batch_translate.py
from nllb_translator import EnhancedOfflineTranslator

translator = EnhancedOfflineTranslator()

# Read input file
with open('input.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Translate each line
translations = []
for i, line in enumerate(lines, 1):
    line = line.strip()
    if not line:
        translations.append("")
        continue

    print(f"Translating line {i}/{len(lines)}...")
    result = translator.translate(line, "en", "fr")
    translations.append(result["translation"])

# Write output
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(translations))

print(f"✅ Translated {len(translations)} lines")
```

**Real-World Example: Translating a Long Article**
```bash
# Create a multi-paragraph article
cat > long_article.txt << 'EOF'
Die Schweizer Alpen sind weltberühmt.
Sie erstrecken sich über mehrere Kantone.
Viele Touristen besuchen jedes Jahr die Bergregionen.
Im Winter ist Skifahren sehr beliebt.
Im Sommer kommen Wanderer aus aller Welt.
Die Landschaft ist atemberaubend schön.
Kleine Dörfer liegen in den Tälern.
Die Menschen sprechen verschiedene Sprachen.
Die lokale Kultur ist sehr reich.
Traditionelle Feste werden das ganze Jahr über gefeiert.
EOF

# Batch translate German → Romansh Sursilvan
python batch_news_translator.py \
    --src de \
    --tgt rm-sursilv \
    --input long_article.txt \
    --output article_romansh.txt

# View the Romansh translation
cat article_romansh.txt
```

**Expected Output:**
```text
Las Alps svizras èn renumadas en tut il mund.
Ellas sa extendeschan sur plirs chantuns.
Bler turissens visitan mintga onn las regiuns da muntogna.
Tal enviern è il skis fitg popular.
Tal stad vegnian randunadurs da tut il mund.
Il cuntegn è maletg da mussair.
Pitschens vitgs sa chattan en las vals.
La glieud discurra differentas linguas.
La cultura locala è fitg ritga.
Festas tradiziunalas vegnan festivadas tut onn.
```

### Handling Long Audio Files

**Good News:** Audio processing handles long files well!

**Speech-to-Text (No Length Limits):**
```python
from whisper_stt import WhisperSTT

stt = WhisperSTT(model_size="base")  # or "medium" for better quality
stt.load_model()

# Works with long audio files (tested up to 30+ minutes)
transcription = stt.transcribe("long_podcast.mp3", language="en")
print(transcription)
```

**Audio-to-Audio Pipeline (With Text Limitation):**
```python
# Long audio → Text works perfectly
# Text → Translation has 512 token limit
# Translation → Speech works perfectly

# For long audio:
# 1. Transcribe entire audio (works)
# 2. Chunk transcription for translation (required)
# 3. Translate chunks
# 4. Synthesize each chunk to audio
# 5. Concatenate audio chunks

from whisper_stt import WhisperSTT
from unified_translator import UnifiedTranslator
from tts_engine import TTSEngine
import numpy as np
import scipy.io.wavfile

stt = WhisperSTT()
translator = UnifiedTranslator()
tts = TTSEngine()

# Step 1: Transcribe long audio
transcription = stt.transcribe("long_speech.mp3", language="de")

# Step 2: Chunk and translate
chunks = chunk_text(transcription, max_words=400)
translated_chunks = []
for chunk in chunks:
    result = translator.translate(chunk, "de", "en")
    translated_chunks.append(result["translation"])

# Step 3: Synthesize each chunk
audio_chunks = []
for i, chunk in enumerate(translated_chunks):
    audio_path, sr = tts.text_to_speech(chunk, "English")
    audio_data, _ = scipy.io.wavfile.read(audio_path)
    audio_chunks.append(audio_data)

# Step 4: Concatenate audio
final_audio = np.concatenate(audio_chunks)
scipy.io.wavfile.write("output_long.wav", sr, final_audio)
```

### Model Selection & Configuration
```python
# Use specific NLLB model
from nllb_translator import EnhancedOfflineTranslator

translator = EnhancedOfflineTranslator()
result = translator.translate("Hello", "en", "fr", model="nllb_200_3_3b")

# Configure Apertus-8B
from apertus_translator import ApertusTranslator

translator = ApertusTranslator(model_path="apertus-8b")  # HuggingFace model ID
result = translator.translate(
    text="Hello",
    src_lang="en",
    tgt_lang="rm-sursilv",
    max_tokens=512
)
```

### Trealla Prolog DCG Parsing
```python
from glossary_parser.trealla_interface import TreallaGlossaryParser

# Initialize parser
parser = TreallaGlossaryParser()

# Parse Swiss French glossary entry
result = parser.parse_entry("""
ABANDONNER (S'), v.pr. Ce verbe ne peut s'employer
dans l'expression : cet enfant s'abandonne...
""")

print(f"Headword: {result['headword']}")
print(f"POS: {result['pos']}")
print(f"Definition: {result['definition']}")
```

### Hybrid Translation with Validation
```python
from apertus_trealla_hybrid import HybridTranslationValidator

# Initialize hybrid system
validator = HybridTranslationValidator(config={
    'apertus_model_id': 'apertus-8b',  # HuggingFace model ID
    'enable_validation': True,
    'max_length_ratio': 3.0
})

# Translate with automatic validation (Romansh example)
result = validator.translate(
    text="Bonjour le monde",
    src_lang="fr",
    tgt_lang="rm-sursilv",  # Romansh Sursilvan
    validate=True
)

# Check validation results
if result['validation']['valid']:
    print(f"✓ Translation validated: {result['translation']}")
else:
    print(f"⚠ Errors detected: {result['validation']['errors']}")
```

### Multimodal Translation (Speech-to-Speech)
```python
from whisper_stt import WhisperSTT
from unified_translator import UnifiedTranslator
from tts_engine import TTSEngine

# Initialize pipeline
stt = WhisperSTT()
translator = UnifiedTranslator()
tts = TTSEngine()

# Audio-to-audio translation
audio_input = "speech_german.mp3"

# Step 1: Speech to text
text_de = stt.transcribe(audio_input, language="de")

# Step 2: Translate
text_en = translator.translate(text_de, src_lang="de", tgt_lang="en")

# Step 3: Text to speech
tts.synthesize(text_en, language="en", output="speech_english.mp3")
```

### Performance Monitoring
```python
result = translator.translate("Hello world", "en", "fr")
print(f"Translation time: {result['time']:.2f}s")
print(f"Model used: {result['method']}")
print(f"Device: {result.get('device', 'CPU')}")
```

## 🌟 Key Features

### Neural Translation Engines
- **Dual-model architecture**: NLLB-200 (200+ languages) + Apertus-8B (1811 languages)
- **Production-ready language coverage**: 65+ languages in web UI (50 mainstream + 15+ low-resource)
- **Automatic model routing**: System selects optimal engine based on language pair
- **Mainstream excellence**: NLLB-200 for high-quality common language pairs
  - Major world languages: Russian, Chinese, Hindi, Arabic, Japanese, Korean
  - European languages: All major European languages plus Slavic, Baltic, and regional languages
  - Asian languages: Vietnamese, Thai, Indonesian, Malay, Tamil, Bengali, Urdu, Persian, Hebrew
  - African languages: Swahili, Amharic, Hausa, Yoruba
- **Low-resource specialist**: Apertus-8B for endangered, rare, and dialect languages
- **Swiss language focus**: All 6 Romansh variants, Swiss French dialects (in development)
- **Celtic & regional languages**: Occitan, Breton, Welsh, Scottish Gaelic, Irish, and more
- **HuggingFace integration**: Direct download and deployment from HF hub

### Symbolic Validation (Trealla Prolog)
- **DCG-based parsing**: Linguistically-principled grammar analysis
- **Dependency parsing**: Full syntactic structure analysis (Swiss French glossaries)
- **Error detection**: Automatic hallucination and grammar error detection
- **Glossary extraction**: Parse and structure historical linguistic resources (1861 Glossaire Vaudois)
- **Hybrid neural-symbolic**: Combine LLM flexibility with logical validation

### Multimodal Capabilities
- **Speech-to-text**: Whisper integration (99 languages)
- **Text-to-speech**: MMS-TTS synthesis
- **Audio-to-audio**: Complete speech translation pipeline
- **Document processing**: PDF, text, batch file translation

### Privacy & Deployment
- **100% offline**: No internet required after model download
- **Zero telemetry**: All processing local, no data leakage
- **Flexible deployment**: CPU, GPU, or mixed configurations
- **Docker support**: Containerized deployment available
- **API & CLI**: Multiple interfaces for integration

### Developer-Friendly
- **Python API**: Clean, documented interfaces
- **Command-line tools**: Shell scripts for automation
- **Gradio web UI**: Interactive browser-based interface
- **Extensible architecture**: Easy to add new languages/models
- **Training support**: Fine-tuning scripts included

## 🔬 Research & Linguistic Applications

TraductAL is designed for linguistic research and low-resource language preservation:

- **Romansh preservation**: Complete support for all 6 Romansh variants
- **Swiss French dialectology**: Building datasets for 6 regional dialects (Vaud, Geneva, etc.)
- **Glossary digitization**: Extract structured data from historical dictionaries (1861 Glossaire Vaudois)
- **DCG formalism**: Linguistic parser based on proven grammatical frameworks
- **Endangered language documentation**: Support for 1811+ languages via Apertus-8B

### Related Ancient Language Projects
For **Coptic** (ancient Egyptian language), see separate specialized projects:
- These use custom megalaa models trained on CopticScriptorium data
- Neither NLLB-200 nor Apertus-8B support Coptic script
- Links provided in "Related Projects" section above

## 📖 Documentation

### Quick Start Guides
- **[APERTUS_TREALLA_QUICKSTART.md](APERTUS_TREALLA_QUICKSTART.md)**: Get started with hybrid system
- **[QUICKSTART.md](QUICKSTART.md)**: General quick start
- **[ROMANSH_GUIDE.md](ROMANSH_GUIDE.md)**: Romansh translation guide
- **[MULTIMODAL_GUIDE.md](MULTIMODAL_GUIDE.md)**: Audio translation guide
- **[BATCH_TRANSLATION_EXAMPLES.md](BATCH_TRANSLATION_EXAMPLES.md)**: Complete guide to batch translation

### Architecture & Integration
- **[INTEGRATION_ARCHITECTURE.md](INTEGRATION_ARCHITECTURE.md)**: Complete system architecture
- **[APERTUS_TREALLA_INTEGRATION.md](APERTUS_TREALLA_INTEGRATION.md)**: Hybrid system details
- **[DCG_PARSER_SUMMARY.md](DCG_PARSER_SUMMARY.md)**: Prolog parser documentation
- **[WHISPER_INTEGRATION.md](WHISPER_INTEGRATION.md)**: STT integration guide

### Development & Training
- **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)**: Fine-tune models
- **[ADD_LANGUAGES_GUIDE.md](ADD_LANGUAGES_GUIDE.md)**: Add new languages
- **[SWISS_FRENCH_README.md](SWISS_FRENCH_README.md)**: Swiss French project

### Reference
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Command reference
- **[EVALUATION_SUMMARY.md](EVALUATION_SUMMARY.md)**: Quality metrics
- **[PROJECT_COMPLETION_SUMMARY.md](PROJECT_COMPLETION_SUMMARY.md)**: Project status
- **[LICENSE_INFO.md](LICENSE_INFO.md)**: Licensing information

## 🧪 Example Usage Scenarios

### Scenario 1: Translate German to Romansh Sursilvan
```bash
# Using Apertus-8B (automatically selected)
python apertus_translator.py \
    --src de \
    --tgt rm-sursilv \
    --text "Guten Morgen, wie geht es Ihnen heute?"

# Output:
# Translation: Bun di, co vai a Vus oz?
# Model: Apertus-8B
# Time: 2.3s
```

### Scenario 2: Parse Swiss French Glossary
```bash
# Extract entries from 1861 Glossaire Vaudois
python glossary_extractor.py --input glossaire_vaud.txt --output vaud_dataset.csv

# Parse individual entry
python -c "
from glossary_parser.trealla_interface import TreallaGlossaryParser
parser = TreallaGlossaryParser()
result = parser.parse_entry('PANOSSE, s.f. Serpillière, torchon à laver')
print(result)
"
```

### Scenario 3: Validate Romansh Translation
```bash
# Translate with validation
python apertus_trealla_hybrid.py \
    --text "Hello world" \
    --src en \
    --tgt rm-sursilv \
    --validate

# System validates output using Trealla Prolog DCG grammar
```

### Scenario 4: Speech-to-Speech Translation
```python
# German audio → English audio
from whisper_stt import WhisperSTT
from unified_translator import UnifiedTranslator
from tts_engine import TTSEngine

# Pipeline
stt = WhisperSTT()
translator = UnifiedTranslator()
tts = TTSEngine()

# Process
german_text = stt.transcribe("speech_de.mp3", language="de")
english_text = translator.translate(german_text, "de", "en")
tts.synthesize(english_text, "en", "speech_en.mp3")
```

## 🛠️ Trealla Prolog DCG Parser

The TraductAL system includes a powerful DCG (Definite Clause Grammar) parser built on **Trealla Prolog**, adapted from the author's original French 2L error detection parser (1989-1991) and Coptic dependency parser.

### Key Features
- **Pure DCG formalism**: Linguistically-principled grammar rules
- **ISO Prolog compliant**: Portable, standards-based
- **Fast & lightweight**: 2MB binary, <100ms parse time
- **Python integration**: Seamless via subprocess interface
- **Extensible**: Easy to add new language grammars

### Architecture
```
grammar.pl (DCG rules) + lexicon.pl (lexical data)
                 ↓
         Trealla Prolog Engine
                 ↓
     trealla_interface.py (Python bridge)
                 ↓
    Neural translation validation
```

### Applications
- **Swiss French glossary parsing**: Extract 1861+ entries from Glossaire Vaudois
- **Translation validation**: Detect neural hallucinations and errors
- **Grammar error detection**: Rule-based linguistic checks
- **Romansh dialect validation**: Ensure authentic dialectal forms

## 🎓 Authorship & Attribution

**Important for Academic & Research Use:**

This system represents original work by the author:
- **Linguistic Core** (DCG grammar, lexicon): Original research by the author, based on Master's thesis in Computational Linguistics (1989-1991)
- **System Integration** (Python code, interfaces): Developed by the author
- **Translation Models**: Third-party open-source components (Meta, OpenAI, etc.)

**For complete transparency**, see: **[AUTHORSHIP_AND_ATTRIBUTION.md](AUTHORSHIP_AND_ATTRIBUTION.md)**

This document provides:
- Detailed component-by-component attribution
- Citation guidelines for academic papers
- Ethical disclosure statements for grant applications
- Verification methodology for reproducibility
- Teaching guidelines for educational contexts

**Quick Summary:**
- ✅ **Original Work**: Prolog DCG grammars, lexicon, linguistic theory, Python integration
- 🌐 **Third-Party**: Pre-trained ML models (NLLB-200, Apertus-8B, Whisper, MMS-TTS)

This transparent attribution model supports academic integrity while acknowledging modern development practices.

## 🤝 Contributing

Contributions are welcome! Areas of particular interest:
- **New language support**: Add support for additional low-resource languages
- **DCG grammars**: Contribute linguistic rules for new languages
- **Dataset creation**: Build training data for dialects
- **Model fine-tuning**: Improve translation quality for specific domains
- **Documentation**: Improve guides and examples

**Note**: Contributions will be attributed appropriately. Please indicate if AI tools were used in development.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Model Licenses
- **NLLB-200**: CC-BY-NC 4.0 (Meta AI, non-commercial research use)
- **Apertus-8B**: Apache 2.0 (fully open-source)
- **Trealla Prolog**: MIT License
- **Whisper**: MIT License (OpenAI)

## 🙏 Acknowledgments

### Original Research Foundation
- **Author's Master's Thesis** (1989-1991): French 2L Error Detection Parser using DCG formalism, providing the theoretical and methodological foundation for the Prolog-based linguistic components

### Models & Frameworks
- **Meta AI** for the NLLB-200 models and MMS-TTS
- **Apertus Team** for the open-source 8B multilingual LLM
- **OpenAI** for Whisper speech recognition
- **Trealla Prolog** team (Andrew Davison) for the lightweight ISO Prolog implementation
- **Hugging Face** for the Transformers library and model hosting
- **PyTorch** team for the deep learning framework

### Linguistic Resources
- **Lia Rumantscha** for Romansh language resources and datasets
- **Canton de Vaud** for Swiss French glossaries (1861 Glossaire Vaudois)
- **CopticScriptorium** for Coptic text corpora (used in separate Coptic projects)
- **Swiss linguistic archives** for dialectal documentation

### Methodological Influences
- DCG formalism from computational linguistics tradition
- Swiss linguistic tradition of dialect preservation and documentation
- Modern neural-symbolic integration approaches

---

## 🚀 Getting Started

**Ready to translate?**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download models
python download_nllb_200.py  # For mainstream languages (NLLB-200)

# 3. Test translation
python apertus_translator.py --list-languages

# 4. Start web interface
# Option A: Basic interface (NLLB-200 only, 12 languages)
python app.py

# Option B: Full interface (both engines, 65+ languages) - RECOMMENDED
./start_gradio.sh
```

**📝 Important Notes:**
- **Production Ready**: Full Gradio interface now supports 65+ languages (expanded December 2025)
- **Basic interface**: 12 mainstream languages (English, French, German, Spanish, Italian, Portuguese, Russian, Swedish, Chinese, Japanese, Korean, Arabic)
- **Full interface**: 50 NLLB mainstream + 15+ Apertus low-resource languages
- Additional language support (200+ NLLB, 1811 Apertus) available via Python API and CLI
- For NLLB-3.3B (better quality): use Python API or CLI, not web interface

**📚 Additional Resources:**
- Low-resource languages and dialects: [APERTUS_TREALLA_QUICKSTART.md](APERTUS_TREALLA_QUICKSTART.md)
- Linguistic research and DCG parsing: [DCG_PARSER_SUMMARY.md](DCG_PARSER_SUMMARY.md)
- Interface comparison: See "User Interfaces Overview" section above
- Adding more languages: [ADD_LANGUAGES_GUIDE.md](ADD_LANGUAGES_GUIDE.md)

---

## 🎉 Recent Updates (December 2025)

### Major Language Expansion: 12 → 65+ Languages

TraductAL has been significantly expanded to provide production-ready multilingual support:

**NLLB-200 Mainstream Languages**: Expanded from 12 to 50 languages
- ✅ **Original 6**: English, French, German, Italian, Spanish, Portuguese
- ✨ **Added Major World (6)**: Russian, Chinese, Hindi, Arabic, Japanese, Korean
- ✨ **Added European (12)**: Dutch, Polish, Czech, Swedish, Danish, Norwegian, Finnish, Greek, Turkish, Hungarian, Romanian, Icelandic
- ✨ **Added Asian (9)**: Vietnamese, Thai, Indonesian, Malay, Tamil, Bengali, Urdu, Persian, Hebrew
- ✨ **Added African (4)**: Swahili, Amharic, Hausa, Yoruba
- ✨ **Added Regional (3)**: Catalan, Galician, Basque
- ✨ **Added Slavic/Baltic (12)**: Ukrainian, Bulgarian, Serbian, Croatian, Slovak, Slovenian, Macedonian, Albanian, Lithuanian, Latvian, Estonian, and more

**Apertus-8B Low-Resource Languages**: Expanded from 6 to 15+ languages
- ✅ **Original 6**: All Romansh variants (Sursilvan, Vallader, Puter, Surmiran, Sutsilvan, Rumantsch Grischun)
- ✨ **Added Celtic & Regional (9+)**: Occitan, Breton, Welsh, Scottish Gaelic, Irish, Luxembourgish, Friulian, Ladin, Sardinian

**Total Coverage**: 65+ languages now available in the production web interface, covering:
- 🌍 All major world languages
- 🇪🇺 Comprehensive European coverage (including regional and minority languages)
- 🌏 Major Asian languages
- 🌍 Key African languages
- 🇨🇭 All Swiss Romansh dialects
- 🏴󠁧󠁢󠁷󠁬󠁳󠁿 Celtic and endangered European languages

**System Capabilities**:
- Web UI: 65+ languages (production-ready)
- Python API/CLI: 200+ (NLLB-200) + 1811 (Apertus-8B) languages
- Full offline operation with zero data leakage
- Speech-to-text and text-to-speech support
- Batch translation for documents

---

**TraductAL** - Bridging mainstream and endangered languages through hybrid neural-symbolic translation 🌍

*Now supporting 65+ languages with production-ready web interface*
