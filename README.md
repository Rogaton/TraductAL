# TraductAL - Offline Neural Translation System

**65+ languages • 100% offline • Privacy-focused • No data collection**

A multilingual translation system that runs entirely on your computer. No internet required after setup, no data sent anywhere.

---

**📋 Licensing**: Free for academic/research use ([MIT License](LICENSE)) • [Commercial use - contact me](COMMERCIAL_LICENSE.md) • [Possible services](COMMERCIAL_SERVICES.md)

---

## 🎯 What It Does

- Translates text between 65+ languages
- Works completely offline after initial setup
- Supports mainstream languages (English, French, German, Spanish, Russian, Chinese, Arabic, etc.)
- Supports low-resource languages (Romansh dialects, Celtic languages, etc.)
- Optional speech-to-text and text-to-speech
- Web interface + command-line tools

## 🚀 Quick Start

```bash
# 1. Install
git clone https://github.com/Rogaton/TraductAL
cd TraductAL
pip install -r requirements.txt

# 2. Download models (one-time, ~3-10GB)
python download_nllb_200.py

# 3. Launch web interface
./start_gradio.sh

# Open browser to http://localhost:7860
```

## 🌍 Supported Languages

**50 Mainstream Languages** (via NLLB-200):
- European: English, French, German, Italian, Spanish, Portuguese, Dutch, Polish, Swedish, Danish, Norwegian, Finnish, Greek, Turkish, Romanian, Czech, Hungarian, and more
- World: Russian, Chinese, Hindi, Arabic, Japanese, Korean
- Asian: Vietnamese, Thai, Indonesian, Malay, Tamil, Bengali, Urdu, Persian, Hebrew
- African: Swahili, Amharic, Hausa, Yoruba
- Regional: Catalan, Galician, Basque, Ukrainian, Bulgarian, Serbian, Croatian, and more

**15+ Low-Resource Languages** (via Apertus-8B):
- Romansh: All 6 variants (Sursilvan, Vallader, Puter, Surmiran, Sutsilvan, Rumantsch Grischun)
- Celtic: Welsh, Scottish Gaelic, Irish, Breton
- Regional: Occitan, Luxembourgish, Friulian, Ladin, Sardinian

## 🔒 Privacy & Offline

- **100% offline** after initial model download
- **No data collection** - everything stays on your machine
- **No internet required** for translation
- Perfect for confidential documents

## ⚡ Usage

### Web Interface (Recommended)
```bash
./start_gradio.sh
# Open http://localhost:7860
```

### Command Line
```bash
# Simple translation
./translate_enhanced.sh en fr "Hello, how are you?"

# Output: Bonjour, comment allez-vous?
```

### Python API
```python
from unified_translator import UnifiedTranslator

translator = UnifiedTranslator()
result = translator.translate("Hello world", "en", "fr")
print(result["translation"])  # Bonjour le monde
```

## 💻 System Requirements

**Minimum:**
- Python 3.8+
- 8GB RAM
- 5GB disk space

**Recommended:**
- Python 3.10+
- 16GB RAM
- 10GB disk space
- GPU optional (faster with GPU)

## ⚠️ Important Notes

- **Development software**: Use at your own risk
- **Translation quality varies** by language pair
- **Not for critical use**: Professional translation may require human review
- **First run is slow**: Models download automatically (~3-10GB)

## 📚 Documentation

- **Full technical documentation**: See `docs/README_DETAILED.md` for complete details
- **Adding languages**: See `docs/ADD_LANGUAGES_GUIDE.md`
- **Batch translation**: See `docs/BATCH_TRANSLATION_EXAMPLES.md`
- **Audio features**: See `docs/MULTIMODAL_GUIDE.md`
- **Architecture & integration**: See `docs/INTEGRATION_ARCHITECTURE.md`
- **Prolog validation**: See `docs/DCG_PARSER_SUMMARY.md`
- **All documentation**: Browse the `docs/` directory

## 🛠️ Two Models, One System

TraductAL uses two translation engines:

1. **NLLB-200** (Meta): Fast, accurate, 200+ languages
2. **Apertus-8B**: Specialized for low-resource languages (1811 languages)

The system automatically picks the best model for your language pair.

## 🎓 Academic Use

See `AUTHORSHIP_AND_ATTRIBUTION.md` for citation guidelines and transparency about AI-assisted development.

## 📂 Project Structure

```
TraductAL/
├── README.md                    # This file - user guide
├── QUICKSTART.md               # Quick start guide
├── LICENSE                     # MIT License
├── AUTHORSHIP_AND_ATTRIBUTION.md  # Academic citations
├── requirements.txt            # Core dependencies
├── requirements_enhanced.txt   # Optional features (STT/TTS)
│
├── Core Application Files
│   ├── gradio_app.py          # Main web interface (65+ languages)
│   ├── unified_translator.py   # Unified translation engine
│   ├── nllb_translator.py     # NLLB-200 engine
│   ├── apertus_translator.py  # Apertus-8B engine
│   ├── apertus_trealla_hybrid.py  # Hybrid neural-symbolic
│   ├── whisper_stt.py         # Speech-to-text
│   ├── tts_engine.py          # Text-to-speech
│   └── startup_check.py       # System verification
│
├── Scripts
│   ├── start_gradio.sh        # Launch web interface
│   ├── translate_enhanced.sh  # CLI translation
│   └── download_nllb_200.py   # Download models
│
├── glossary_parser/           # Prolog DCG parser (linguistic)
├── docs/                      # All documentation (40+ files)
├── scripts/                   # Utility scripts & training
├── data/samples/              # Test data & samples
└── docker/                    # Docker configuration
```

## 📄 License

### Dual Licensing Options

TraductAL is available under **dual licensing** to serve both academic and commercial needs:

#### 🎓 MIT License (Academic & Non-Commercial)
**FREE** for:
- Universities and research institutions
- Non-profit organizations
- Personal use and experimentation
- Startups with revenue < $100,000 USD
- Open-source projects

See [LICENSE](LICENSE) for full terms.

#### 💼 Commercial Use
**For commercial use**, please contact: relanir@bluewin.ch

I'm open to discussing:
- Commercial licensing arrangements
- Custom adaptations and consulting
- Academic-industry collaborations
- Reasonable terms based on your specific needs

See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) and [COMMERCIAL_SERVICES.md](COMMERCIAL_SERVICES.md) for framework (pricing to be determined based on actual use cases).

### Third-Party Model Licenses

TraductAL integrates open-source models with their own licenses:
- **NLLB-200**: CC-BY-NC 4.0 (non-commercial only) - see COMMERCIAL_LICENSE.md for commercial alternatives
- **Apertus-8B**: Apache 2.0 (commercial use permitted)

---

**Need the full technical documentation?** See `docs/README_DETAILED.md` for complete details.
