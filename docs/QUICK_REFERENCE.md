# Quick Reference - Offline Neural MT

## 🚀 Essential Commands

### Basic Translation
```bash
cd ~/neural_mt_offline
conda run -n neural_mt_offline python standalone_neural_mt_clean.py \
  --source en --target fr --text "Your text here"
```

### Interactive Mode
```bash
conda run -n neural_mt_offline python standalone_neural_mt_clean.py \
  --source en --target fr --interactive
```

## 🌐 Language Support Matrix

| From/To | English | French | German | Spanish | Italian |
|---------|---------|--------|--------|---------|---------|
| **English** | - | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **French** | ⭐⭐⭐⭐⭐ | - | ❌ | ❌ | ❌ |
| **German** | ⭐⭐⭐⭐⭐ | ❌ | - | ❌ | ❌ |
| **Spanish** | ⭐⭐ | ❌ | ❌ | - | ❌ |
| **Italian** | ⭐⭐ | ❌ | ❌ | ❌ | - |

**Legend**: ⭐⭐⭐⭐⭐ Excellent (OPUS-MT) | ⭐⭐⭐⭐ Good (T5) | ⭐⭐ Limited (T5) | ❌ Not supported

## 📋 Language Codes
- `en` = English
- `fr` = French  
- `de` = German
- `es` = Spanish
- `it` = Italian
- `ro` = Romanian

## ⚡ One-Liners

### Common Translations
```bash
# English to French
conda run -n neural_mt_offline python standalone_neural_mt_clean.py --source en --target fr --text "Hello world"

# English to German  
conda run -n neural_mt_offline python standalone_neural_mt_clean.py --source en --target de --text "Good morning"

# Get just the translation (requires jq)
conda run -n neural_mt_offline python standalone_neural_mt_clean.py --source en --target fr --text "Hello" | jq -r '.translation'
```

### File Translation
```bash
# Translate file content
conda run -n neural_mt_offline python standalone_neural_mt_clean.py --source en --target fr --text "$(cat file.txt)"

# Line by line translation
while read line; do conda run -n neural_mt_offline python standalone_neural_mt_clean.py --source en --target fr --text "$line"; done < input.txt
```

## 🔧 System Commands

### Health Check
```bash
cd ~/neural_mt_offline
conda run -n neural_mt_offline python -c "import torch; from transformers import T5ForConditionalGeneration; print('✅ System OK')"
```

### Model Status
```bash
ls -lh ~/neural_mt_offline/models/deployed_models/t5_small/
# Should show ~234MB total
```

### Environment Check
```bash
conda env list | grep neural_mt_offline
conda run -n neural_mt_offline python --version
```

## 📊 Performance Expectations

| Metric | Value |
|--------|-------|
| **Startup Time** | 3-4 seconds |
| **Translation Speed** | ~0.8s/sentence (OPUS-MT), ~0.4s (T5) |
| **Memory Usage** | ~3GB RAM |
| **Model Size** | 2.5GB total |
| **Best Sentence Length** | 5-50 words |

## 🐛 Quick Fixes

### Model Not Loading
```bash
# Check model files exist
ls ~/neural_mt_offline/models/deployed_models/t5_small/
# Should show: config.json, model.safetensors, tokenizer files
```

### Environment Issues
```bash
# Recreate environment if needed
conda create -n neural_mt_offline python=3.11
conda run -n neural_mt_offline pip install torch transformers
```

### Poor Translation Quality
- ✅ Use English as source language
- ✅ Keep sentences under 50 words
- ✅ Include proper punctuation
- ❌ Avoid slang or idioms

## 💡 Pro Tips

1. **Interactive Mode**: Use for multiple translations to avoid startup delay
2. **Batch Processing**: Group translations by language pair
3. **JSON Output**: Pipe to `jq` for clean text extraction
4. **File Backup**: Keep a backup of your working t5_small model
5. **Memory**: Close other applications for large translation jobs

## 🔒 Privacy Features
- ✅ 100% offline operation
- ✅ No data sent externally  
- ✅ No translation logging
- ✅ Suitable for confidential documents
- ✅ Air-gap compatible

## 📞 Emergency Commands

### System Reset
```bash
cd ~/neural_mt_offline
conda run -n neural_mt_offline python standalone_neural_mt_clean.py --source en --target fr --text "test" > /dev/null
echo $? # Should return 0 if working
```

### Backup Working System
```bash
tar -czf neural_mt_backup.tar.gz ~/neural_mt_offline/models/deployed_models/t5_small/
```

### Restore from Backup
```bash
cd ~/neural_mt_offline/models/deployed_models/
tar -xzf ~/neural_mt_backup.tar.gz
```

---
**Print this page for offline reference!**
