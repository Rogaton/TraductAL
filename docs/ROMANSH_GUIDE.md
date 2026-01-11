# TraductAL with Romansh Support 🇨🇭

Complete guide for German/English/French to Romansh (Sursilvan) translation using your TraductAL engine with Apertus8B integration.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Overview](#system-overview)
3. [Usage Examples](#usage-examples)
4. [Available Models](#available-models)
5. [Romansh Variants](#romansh-variants)
6. [Dataset Information](#dataset-information)
7. [Fine-tuning Guide](#fine-tuning-guide)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Translate German to Romansh Sursilvan

```bash
cd /home/aldn/TraductAL/TraductAL
./translate_romansh.sh de rm-sursilv "Guten Tag, wie geht es Ihnen?"
```

**Output:**
```
🔤 Original (de (German)): Guten Tag, wie geht es Ihnen?
🌍 Translation (rm-sursilv (Romansh Sursilvan)): Bun di, co va cun vos?
🤖 Engine: Apertus8B
⏱️  Time: 12.30s
```

### List All Supported Languages

```bash
./translate_romansh.sh --list-languages
```

### List Available Models

```bash
./translate_romansh.sh --list-models
```

---

## 🎯 System Overview

Your TraductAL engine now combines **two powerful translation systems**:

### 1. **NLLB-200** (Meta AI)
- **Languages**: 200
- **Type**: Seq2seq encoder-decoder
- **Speed**: ⚡ Fast (0.5-2s per sentence)
- **Best for**: Common language pairs (en-de, fr-es, etc.)
- **Quality**: Excellent for trained pairs

### 2. **Apertus8B** (Swiss AI)
- **Languages**: 1,811 (including all Romansh variants)
- **Type**: Causal LLM (decoder-only)
- **Speed**: 🐢 Slower (10-15s per sentence on CPU)
- **Best for**: Romansh and low-resource languages
- **Quality**: Very high for Swiss languages

### 🤖 Automatic Engine Selection

The system **automatically** chooses the best engine:

| Scenario | Engine Used | Reason |
|----------|-------------|---------|
| German → Romansh | Apertus8B | Romansh specialist |
| English → German | NLLB-200 | Faster for common pairs |
| French → Romansh | Apertus8B | Romansh specialist |
| Romansh → German | Apertus8B | Romansh specialist |

---

## 💡 Usage Examples

### Example 1: Basic Translation

```bash
./translate_romansh.sh de rm-sursilv "Willkommen in der Schweiz"
```

### Example 2: French to Romansh

```bash
./translate_romansh.sh fr rm-sursilv "Bonjour, comment allez-vous?"
```

### Example 3: Force Specific Engine

```bash
# Force Apertus8B
./translate_romansh.sh en de "Hello" --engine apertus

# Force NLLB-200
./translate_romansh.sh en de "Hello" --engine nllb
```

### Example 4: Clean Output (No Formatting)

```bash
./translate_romansh.sh de rm-sursilv "Guten Tag" --clean
# Output: Bun di
```

### Example 5: Using Python API Directly

```python
from unified_translator import UnifiedTranslator

translator = UnifiedTranslator()

# Translate with auto engine selection
result = translator.translate(
    "Guten Tag",
    src_lang="de",
    tgt_lang="rm-sursilv"
)

print(result["translation"])  # Output: Bun di
```

### Example 6: Compare Engines (Benchmark)

```bash
./translate_romansh.sh --benchmark
```

---

## 🤖 Available Models

### NLLB-200 Models

Located in: `/home/aldn/TraductAL/TraductAL/models/deployed_models/`

| Model | Size | Languages | Speed | Quality |
|-------|------|-----------|-------|---------|
| nllb_200_1.3b | ~2.6GB | 200 | Fast | Very Good |
| nllb_200_3.3b | ~6.6GB | 200 | Medium | High |

### Apertus8B Model

Located in: `/home/aldn/Apertus8B/`

| Model | Size | Languages | Speed | Quality |
|-------|------|-----------|-------|---------|
| Apertus-8B | ~16GB | 1,811 | Slower | Very High |

---

## 🇨🇭 Romansh Variants Supported

The system supports **all 6 Romansh variants**:

| Code | Variant | Speakers | Status |
|------|---------|----------|--------|
| `rm-sursilv` | Sursilvan | 55% | ✅ Primary |
| `rm-vallader` | Vallader | 20% | ✅ Supported |
| `rm-puter` | Puter | 12% | ✅ Supported |
| `rm-surmiran` | Surmiran | 10% | ✅ Supported |
| `rm-sutsilv` | Sutsilvan | 3% | ✅ Supported |
| `rm-rumgr` | Rumantsch Grischun | Standard | ✅ Supported |

### Usage with Different Variants

```bash
# Sursilvan (most common)
./translate_romansh.sh de rm-sursilv "Guten Tag"

# Vallader
./translate_romansh.sh de rm-vallader "Guten Tag"

# Rumantsch Grischun (official standard)
./translate_romansh.sh de rm-rumgr "Guten Tag"
```

---

## 📊 Dataset Information

### Downloaded Dataset

**Location**: `/home/aldn/TraductAL/TraductAL/datasets/romansh/`

| Dataset | Language Pair | Size | Source |
|---------|--------------|------|--------|
| swiss-ai/apertus-posttrain-romansh | German ↔ Romansh | 46,092 pairs | HuggingFace |

### Dataset Structure

```python
from datasets import load_from_disk

dataset = load_from_disk("./datasets/romansh")
print(len(dataset['train']))  # 46,092 examples

# Sample entry
sample = dataset['train'][0]
# Contains: German text → Romansh translation
```

### Dataset Contents

- **Dictionary translations**: Single words and phrases
- **Sentence-level translations**: Complete sentences
- **Idiom identification**: Romansh idioms and expressions
- **Instruction data**: Small set of human-translated instructions

---

## 🔧 Fine-tuning Guide (Optional)

If you want to **improve** translation quality for specific domains:

### When to Fine-tune

- ✅ You have domain-specific terminology (medical, legal, technical)
- ✅ You want better accuracy for specific Romansh variants
- ✅ You have additional parallel data
- ❌ Current quality is already good for general use

### Fine-tuning Apertus8B

**Note**: Apertus8B is already pre-trained on Romansh data, so fine-tuning is optional.

```bash
# Using your existing training infrastructure
cd /home/aldn/TraductAL/TraductAL

# Adapt the training script for Apertus8B
# (This requires modifications to train_nllb_hf_spaces.py for causal LM)
```

### Fine-tuning NLLB-200 for Romansh

Since NLLB-200 doesn't natively support Romansh, you can fine-tune it:

```bash
# Use the existing training script with the Romansh dataset
python train_nllb_hf_spaces.py \
  --model facebook/nllb-200-distilled-600M \
  --dataset ./datasets/romansh \
  --language-pair de-rm \
  --epochs 10
```

**Requirements**:
- HuggingFace Spaces with T4 GPU
- 2-6 hours training time
- See `TRAINING_GUIDE.md` for details

---

## 🐛 Troubleshooting

### Issue: "Model not found"

**Solution**: Check Apertus8B installation:
```bash
ls -la ~/Apertus8B/
# Should contain: model-00001-of-00004.safetensors, etc.
```

### Issue: "Translation is slow"

**Cause**: Apertus8B runs on CPU (8B parameters)

**Solutions**:
1. **Use GPU** (if available):
   - Automatically detected if CUDA available
   - ~5x speedup
2. **Use NLLB for non-Romansh pairs**:
   ```bash
   ./translate_romansh.sh en de "Hello" --engine nllb
   ```

### Issue: "Virtual environment not found"

**Solution**: Activate manually:
```bash
cd /home/aldn/TraductAL/TraductAL
source .venv/bin/activate
python unified_translator.py de rm-sursilv "Test"
```

### Issue: "datasets library not found"

**Solution**: Already installed! If issues persist:
```bash
source .venv/bin/activate
pip install datasets
```

### Issue: "Translation quality is poor"

**Solutions**:
1. **Try different Romansh variants**:
   - Each variant has different training data
   - Sursilvan (`rm-sursilv`) is most common
2. **Use more context**:
   - Provide full sentences instead of single words
   - Include punctuation
3. **Consider fine-tuning**:
   - Add domain-specific data
   - See Fine-tuning Guide above

---

## 📝 Python API Reference

### UnifiedTranslator Class

```python
from unified_translator import UnifiedTranslator

translator = UnifiedTranslator()

# Translate with auto engine selection
result = translator.translate(
    text="Guten Tag",
    src_lang="de",
    tgt_lang="rm-sursilv"
)

# Force specific engine
result = translator.translate(
    text="Hello",
    src_lang="en",
    tgt_lang="de",
    engine="nllb"  # or "apertus"
)

# Result structure
{
    "translation": "Bun di",
    "model": "Apertus-8B",
    "engine": "Apertus8B",
    "time": "12.30s",
    "src_lang": "de (German)",
    "tgt_lang": "rm-sursilv (Romansh Sursilvan)",
    "device": "cpu"
}
```

### ApertusTranslator Class (Direct)

```python
from apertus_translator import ApertusTranslator

translator = ApertusTranslator()

result = translator.translate(
    text="Guten Tag",
    src_lang="de",
    tgt_lang="rm-sursilv",
    max_tokens=512
)

# List supported languages
translator.list_languages()
```

### NLLB Translator Class (Direct)

```python
from nllb_translator import EnhancedOfflineTranslator

translator = EnhancedOfflineTranslator()

result = translator.translate(
    text="Hello",
    src_lang="en",
    tgt_lang="de",
    model_name="nllb_200_1.3b"
)
```

---

## 🎓 Language Code Reference

### Common Source Languages

| Code | Language | Example |
|------|----------|---------|
| `de` | German | Guten Tag |
| `en` | English | Hello |
| `fr` | French | Bonjour |
| `it` | Italian | Buongiorno |

### Romansh Target Languages

| Code | Variant | Example Translation |
|------|---------|-------------------|
| `rm-sursilv` | Sursilvan | Bun di |
| `rm-vallader` | Vallader | Bun dí |
| `rm-puter` | Puter | Bun dì |
| `rm-rumgr` | Rumantsch Grischun | Bun di |

---

## 📞 Support & Resources

### File Locations

```
TraductAL/
├── TraductAL/
│   ├── unified_translator.py     # Main interface
│   ├── apertus_translator.py     # Apertus8B wrapper
│   ├── nllb_translator.py        # NLLB-200 engine
│   ├── translate_romansh.sh      # Shell wrapper
│   ├── download_romansh_dataset.py
│   └── datasets/
│       └── romansh/              # Downloaded dataset
│
~/Apertus8B/                      # Apertus8B model
    ├── model-*.safetensors       # Model weights
    ├── config.json               # Model config
    └── tokenizer.json            # Tokenizer
```

### Documentation

- **TraductAL**: `README.md`, `TRAINING_GUIDE.md`
- **NLLB-200**: `NLLB_UPGRADE_GUIDE.md`
- **Romansh**: `ROMANSH_GUIDE.md` (this file)

### External Resources

- **Apertus8B**: https://huggingface.co/swiss-ai/Apertus-8B-2509
- **NLLB-200**: https://huggingface.co/facebook/nllb-200-1.3B
- **Romansh Dataset**: https://huggingface.co/datasets/swiss-ai/apertus-posttrain-romansh

---

## ✅ Summary

You now have a **complete Romansh translation system** that:

✅ Translates German/English/French → Romansh (all variants)
✅ Automatically selects the best engine
✅ Supports 1,811 languages total
✅ Includes 46,092 German-Romansh training examples
✅ Works 100% offline
✅ Respects privacy (no data sent to external servers)

**Main command**:
```bash
cd /home/aldn/TraductAL/TraductAL
./translate_romansh.sh de rm-sursilv "Guten Tag"
```

**Enjoy translating!** 🇨🇭
