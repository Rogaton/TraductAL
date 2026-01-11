# 🌍 Adding New Languages to TraductAL

## Overview

TraductAL can support many more languages beyond the current 6 mainstream languages. The system architecture supports:

- **Translation**: 200 languages (NLLB-200) + 1,811 languages (Apertus8B)
- **TTS**: 1,107 languages (Facebook MMS-TTS)

## 🎯 Popular Languages Ready to Add

| Language | Translation | TTS | Status |
|----------|-------------|-----|--------|
| **Russian** 🇷🇺 | ✅ rus_Cyrl | ✅ rus | Ready to add |
| **Chinese (Mandarin)** 🇨🇳 | ✅ zho_Hans | ✅ cmn | Ready to add |
| **Hindi** 🇮🇳 | ✅ hin_Deva | ✅ hin | Ready to add |
| **Arabic** 🇸🇦 | ✅ arb_Arab | ✅ ara | Ready to add |
| **Japanese** 🇯🇵 | ✅ jpn_Jpan | ✅ jpn | Ready to add |
| **Korean** 🇰🇷 | ✅ kor_Hang | ✅ kor | Ready to add |
| **Turkish** 🇹🇷 | ✅ tur_Latn | ✅ tur | Ready to add |
| **Polish** 🇵🇱 | ✅ pol_Latn | ✅ pol | Ready to add |
| **Dutch** 🇳🇱 | ✅ nld_Latn | ✅ nld | Ready to add |
| **Swedish** 🇸🇪 | ✅ swe_Latn | ✅ swe | Ready to add |

---

## 📝 Step-by-Step: Adding Languages

### Step 1: Update Language Codes in `gradio_app.py`

**Location**: Lines 43-50

**Current code**:
```python
COMMON_LANGUAGES = {
    "German": "de",
    "English": "en",
    "French": "fr",
    "Italian": "it",
    "Spanish": "es",
    "Portuguese": "pt"
}
```

**Add new languages**:
```python
COMMON_LANGUAGES = {
    "German": "de",
    "English": "en",
    "French": "fr",
    "Italian": "it",
    "Spanish": "es",
    "Portuguese": "pt",
    "Russian": "ru",              # NEW!
    "Chinese": "zh",              # NEW!
    "Hindi": "hi",                # NEW!
    "Arabic": "ar",               # NEW!
    "Japanese": "ja",             # NEW!
    "Korean": "ko"                # NEW!
}
```

### Step 2: Update TTS Language Codes in `tts_engine.py`

**Location**: Lines 24-31

**Current code**:
```python
LANGUAGE_CODES = {
    "English": "eng",
    "German": "deu",
    "French": "fra",
    "Italian": "ita",
    "Spanish": "spa",
    "Portuguese": "por"
}
```

**Add new languages**:
```python
LANGUAGE_CODES = {
    "English": "eng",
    "German": "deu",
    "French": "fra",
    "Italian": "ita",
    "Spanish": "spa",
    "Portuguese": "por",
    "Russian": "rus",             # NEW!
    "Chinese": "cmn",             # NEW! (Mandarin Chinese)
    "Hindi": "hin",               # NEW!
    "Arabic": "ara",              # NEW!
    "Japanese": "jpn",            # NEW!
    "Korean": "kor"               # NEW!
}
```

### Step 3: Update `unified_translator.py` (if needed)

The unified translator should already support these languages through NLLB-200. Check the language mapping:

**NLLB-200 Language Codes**:
- Russian: `rus_Cyrl` (Cyrillic script)
- Chinese (Simplified): `zho_Hans` (Hans = Simplified)
- Chinese (Traditional): `zho_Hant` (Hant = Traditional)
- Hindi: `hin_Deva` (Devanagari script)
- Arabic: `arb_Arab` (Arabic script)
- Japanese: `jpn_Jpan` (Japanese script)
- Korean: `kor_Hang` (Hangul script)

### Step 4: Test the New Languages

After adding languages, test each one:

**Test TTS**:
```bash
cd /home/aldn/TraductAL/TraductAL
source /home/aldn/Apertus8B/alvenv/bin/activate
python
```

```python
from tts_engine import TTSEngine

tts = TTSEngine()

# Test Russian
audio_path, sr = tts.text_to_speech(
    "Привет! Добро пожаловать в TraductAL.",
    "Russian"
)
print(f"✅ Russian TTS: {audio_path}")

# Test Chinese
audio_path, sr = tts.text_to_speech(
    "你好！欢迎来到 TraductAL。",
    "Chinese"
)
print(f"✅ Chinese TTS: {audio_path}")

# Test Hindi
audio_path, sr = tts.text_to_speech(
    "नमस्ते! TraductAL में आपका स्वागत है।",
    "Hindi"
)
print(f"✅ Hindi TTS: {audio_path}")
```

**Test Translation**:
```python
from unified_translator import UnifiedTranslator

translator = UnifiedTranslator()

# English to Russian
result = translator.translate(
    "Hello, how are you?",
    "en",
    "ru"
)
print(f"✅ English→Russian: {result['translation']}")

# English to Chinese
result = translator.translate(
    "Hello, how are you?",
    "en",
    "zh"
)
print(f"✅ English→Chinese: {result['translation']}")
```

---

## 🔍 Language Code References

### NLLB-200 Translation Codes

Common pattern: `{language_code}_{script_code}`

| Language | Code | Example |
|----------|------|---------|
| Russian | rus_Cyrl | Cyrillic script |
| Chinese (Simplified) | zho_Hans | Simplified Chinese |
| Chinese (Traditional) | zho_Hant | Traditional Chinese |
| Hindi | hin_Deva | Devanagari script |
| Arabic | arb_Arab | Arabic script |
| Japanese | jpn_Jpan | Japanese script |
| Korean | kor_Hang | Hangul script |
| Turkish | tur_Latn | Latin script |
| Polish | pol_Latn | Latin script |
| Dutch | nld_Latn | Latin script |

**Full list**: See NLLB-200 documentation at https://github.com/facebookresearch/flores/blob/main/flores200/README.md

### MMS-TTS Language Codes (ISO 639-3)

| Language | Code | Notes |
|----------|------|-------|
| Russian | rus | |
| Chinese (Mandarin) | cmn | Standard Mandarin |
| Hindi | hin | |
| Arabic | ara | Modern Standard Arabic |
| Japanese | jpn | |
| Korean | kor | |
| Turkish | tur | |
| Polish | pol | |
| Dutch | nld | |
| Swedish | swe | |

**Full list**: See MMS documentation at https://huggingface.co/facebook/mms-tts

---

## 🚀 Quick Implementation

### Option A: Add 3 Major Languages (Russian, Chinese, Hindi)

**Files to modify**:
1. `gradio_app.py` - Line 43
2. `tts_engine.py` - Line 24

**Benefits**:
- Covers 1.6+ billion native speakers
- Major world languages
- Well-supported by all models

### Option B: Add 10+ Languages

**Add all popular languages**:
- Russian, Chinese, Hindi, Arabic, Japanese, Korean
- Turkish, Polish, Dutch, Swedish

**Benefits**:
- Comprehensive language coverage
- Serves global audience
- Still manageable interface

### Option C: Custom Selection

Pick specific languages based on your use case:
- **European focus**: Add Russian, Polish, Dutch, Swedish, Turkish
- **Asian focus**: Add Chinese, Hindi, Japanese, Korean
- **MENA focus**: Add Arabic, Turkish, Persian (Farsi)

---

## ⚠️ Important Notes

### 1. Script Support

Some languages use different scripts:
- **Cyrillic**: Russian, Bulgarian, Ukrainian
- **Arabic**: Arabic, Urdu, Persian
- **Devanagari**: Hindi, Marathi, Nepali
- **CJK**: Chinese, Japanese, Korean

Make sure your system fonts support these scripts for proper display.

### 2. Translation Quality

Translation quality varies by language pair:
- **High quality**: European languages ↔ English
- **Good quality**: Major world languages (Russian, Chinese, Arabic, Hindi)
- **Variable**: Low-resource languages

### 3. TTS Model Download

Each TTS language model is ~300MB:
- First use will download the model
- Models are cached locally
- Total storage: ~300MB × number of languages

Example for 12 languages: ~3.6GB storage needed

### 4. Romansh Support

For Romansh → Target language:
- Use Apertus8B for best quality (slower)
- NLLB-200 also works (faster)

---

## 🧪 Testing Checklist

After adding new languages:

- [ ] Translation works (text → text)
- [ ] TTS works (text → audio)
- [ ] Translate & Speak works (text → translation → audio)
- [ ] All dropdowns show new languages
- [ ] Audio files download correctly
- [ ] Non-Latin scripts display correctly
- [ ] Web interface remains responsive

---

## 📚 Resources

### Documentation
- **NLLB-200 Languages**: https://github.com/facebookresearch/flores/blob/main/flores200/README.md
- **MMS-TTS Languages**: https://huggingface.co/facebook/mms-tts
- **ISO 639-3 Codes**: https://iso639-3.sil.org/code_tables/639/data

### Model Pages
- **NLLB-200**: https://huggingface.co/facebook/nllb-200-1.3B
- **MMS-TTS**: https://huggingface.co/facebook/mms-tts
- **Apertus8B**: https://huggingface.co/swiss-ai/Apertus-8B-2509

---

## 🎯 Recommendation

**For immediate expansion**, I recommend adding:

### Tier 1: Major World Languages
1. 🇷🇺 **Russian** - 258M speakers
2. 🇨🇳 **Chinese** - 918M speakers
3. 🇮🇳 **Hindi** - 341M speakers

### Tier 2: Additional Major Languages
4. 🇸🇦 **Arabic** - 274M speakers
5. 🇯🇵 **Japanese** - 125M speakers
6. 🇰🇷 **Korean** - 81M speakers

### Total Coverage
- **Current**: 6 languages (~900M speakers)
- **After Tier 1**: 9 languages (~2.4B speakers)
- **After Tier 2**: 12 languages (~3B speakers)

---

## ✅ Would You Like Me to Implement This?

I can add any or all of these languages to your system right now. Just let me know which languages you'd like to add:

- [ ] Russian, Chinese, Hindi (Tier 1)
- [ ] Arabic, Japanese, Korean (Tier 2)
- [ ] All 12 languages
- [ ] Custom selection (specify which ones)

The implementation takes about 5 minutes per tier.

---

**Ready to make TraductAL truly global!** 🌍
