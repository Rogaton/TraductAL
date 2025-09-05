# TraductAL - an offline Neural Machine Translation with NLLB-200

A completely offline, privacy-focused neural machine translation system powered by Meta's NLLB-200 models. All translations happen locally on your machine with no data sent to external servers.

## ⚠️ Development Status & Disclaimer

**USE AT YOUR OWN RISK** - This system is currently in active development and not ready for production use.

### Known Limitations:
- **Incomplete translations**: Some words or text segments may be missing from output
- **Quality varies**: Translation accuracy depends on language pair and text complexity  
- **No quality guarantees**: Results may not be suitable for professional or critical use
- **Model limitations**: Base NLLB-200 models may require fine-tuning for specific domains

### Recommended Use:
- ✅ Development and testing purposes
- ✅ Personal experimentation with offline translation
- ✅ Privacy-focused translation where perfect accuracy isn't critical
- ❌ Production systems requiring reliable translations
- ❌ Professional document translation without human review
- ❌ Critical communications or legal documents

## 🔒 Privacy & Security
- **100% Offline**: No internet connection required after setup
- **Zero Data Leakage**: All processing happens locally
- **Professional Grade**: Suitable for confidential document translation
- **No Logging**: No translation history stored externally

## 🌍 Language Support

NLLB-200 supports 200+ languages with excellent quality for:
- **European languages**: English, French, German, Spanish, Italian, Portuguese, Russian
- **Asian languages**: Chinese, Japanese, Korean, Hindi, Arabic, Turkish
- **Many more**: Including low-resource languages with good quality

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd TraductAL

# Install dependencies
pip install -r requirements.txt

# Download NLLB models
python download_nllb_200.py
```

### Basic Usage
```bash
# Simple translation
./translate_enhanced.sh en fr "Hello, how are you?"

# Interactive mode
./translate_enhanced.sh interactive en fr

# List available languages
./translate_enhanced.sh list-languages

# System health check
./translate_enhanced.sh check
```

### Python API
```python
from nllb_translator import EnhancedOfflineTranslator

translator = EnhancedOfflineTranslator()
result = translator.translate("Hello world", "en", "fr")
print(result["translation"])  # "Bonjour ä tous"
```

## 📊 Model Options

### NLLB-200-1.3B (Recommended)
- **Size**: ~2.6GB
- **Speed**: 0.5-1.0 seconds per sentence
- **Memory**: ~3GB RAM
- **Quality**: Very High

### NLLB-200-3.3B (Maximum Quality)
- **Size**: ~6.6GB  
- **Speed**: 1.0-2.0 seconds per sentence
- **Memory**: ~7GB RAM
- **Quality**: Excellent

## 🛠️ System Requirements

- **Python**: 3.8+
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 3-7GB for models
- **OS**: Linux, macOS, Windows

## 📁 Project Structure

```
TraductAL/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
├── nllb_translator.py        # Main translator class
├── translate_enhanced.sh     # Command-line interface
├── download_nllb_200.py      # Model downloader
├── migrate_to_nllb.py        # Migration utility
├── NLLB_UPGRADE_GUIDE.md     # Detailed upgrade guide
├── QUICK_REFERENCE.md        # Command reference
├── MIGRATION_SUMMARY.md      # Migration documentation
└── models/
    └── deployed_models/
        ├── nllb_200_1.3b/   # NLLB 1.3B model files
        └── nllb_200_3.3b/   # NLLB 3.3B model files
```

## 🔧 Advanced Usage

### Batch Translation
```bash
# Translate multiple lines
echo -e "Hello\nGoodbye\nThank you" | ./translate_enhanced.sh en fr

# Translate from file
./translate_enhanced.sh en fr "$(cat input.txt)"
```

### Model Selection
```python
# Use specific model
translator = EnhancedOfflineTranslator()
result = translator.translate("Hello", "en", "fr", model="nllb_200_3_3b")
```

### Performance Monitoring
```python
result = translator.translate("Hello world", "en", "fr")
print(f"Translation time: {result['time']:.2f}s")
print(f"Model used: {result['method']}")
```

## 🌟 Key Features

- **High-quality translations** with NLLB-200 models
- **200+ language support** including low-resource languages
- **Bidirectional translation** for all language pairs
- **Automatic model selection** based on availability
- **Performance monitoring** and optimization
- **Professional-grade privacy** with offline operation
- **Easy integration** with Python API and shell commands

## 🔄 Migration from Other Systems

If you're migrating from MT5 or other translation systems:

```bash
# Run the migration script
python migrate_to_nllb.py

# Follow the upgrade guide
cat NLLB_UPGRADE_GUIDE.md
```

## 📖 Documentation

- **[NLLB_UPGRADE_GUIDE.md](NLLB_UPGRADE_GUIDE.md)**: Detailed upgrade instructions
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Command reference sheet
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)**: Migration documentation
- **[LICENSE_INFO.md](LICENSE_INFO.md)**: Licensing information

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta AI** for the NLLB-200 models
- **Hugging Face** for the Transformers library
- **PyTorch** team for the deep learning framework

---

**Ready to translate?** Run `python download_nllb_200.py` to get started!
