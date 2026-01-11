# 🎤🌍🔊 TraductAL Multimodal System for Romansh

Complete guide for **Text, Speech-to-Text, and future Text-to-Speech** workflows with Romansh language support.

---

## 📋 Table of Contents

1. [Quick Start - Web UI](#quick-start---web-ui)
2. [Text Translation](#text-translation)
3. [Speech-to-Text (STT)](#speech-to-text-stt)
4. [Audio Translation Pipeline](#audio-translation-pipeline)
5. [Batch News Translation](#batch-news-translation)
6. [Text-to-Speech (TTS) - Future](#text-to-speech-tts---future)
7. [Use Cases](#use-cases)

---

## 🚀 Quick Start - Web UI

### Launch Gradio Interface

```bash
cd /home/aldn/TraductAL/TraductAL
./start_gradio.sh
```

Then open your browser to: **http://localhost:7860**

### What's Available

The web interface provides **8 tabs**:

| Tab | Feature | Description |
|-----|---------|-------------|
| 📝 **Text Translation** | Interactive translation | Translate between any supported languages |
| 📄 **Batch Translation** | Multiple lines/files | Upload .txt files for batch processing |
| 🎤 **Speech to Text** | Audio transcription | Transcribe Romansh audio to text |
| 🎤→🌍 **Audio Translation** | Text pipeline | Romansh audio → text → translation |
| 🔊 **Text-to-Speech** | Speech synthesis | Convert text to speech in 6 languages |
| 🌍→🔊 **Translate & Speak** | Translation + TTS | Translate text and generate audio |
| 🎤→🔊 **Audio to Audio** | Complete pipeline | Romansh audio → spoken translation |
| ℹ️ **About** | System information | Details about models and datasets |

---

## 📝 Text Translation

### Command Line

```bash
# German to Romansh Sursilvan
./translate_romansh.sh de rm-sursilv "Guten Tag, wie geht es Ihnen?"

# French to Romansh Vallader
./translate_romansh.sh fr rm-vallader "Bonjour, comment allez-vous?"

# English to Rumantsch Grischun
./translate_romansh.sh en rm-rumgr "Hello, how are you today?"
```

### Python API

```python
from unified_translator import UnifiedTranslator

translator = UnifiedTranslator()

# Auto engine selection
result = translator.translate(
    "Guten Tag",
    src_lang="de",
    tgt_lang="rm-sursilv"
)

print(result["translation"])  # Bun di
print(result["engine"])        # Apertus8B
```

### Web UI

1. Go to **📝 Text Translation** tab
2. Select source language (e.g., German)
3. Select target language (e.g., Romansh Sursilvan)
4. Enter text and click **🌍 Translate**

---

## 🎤 Speech-to-Text (STT)

Transcribe Romansh Sursilvan audio to text using wav2vec2-xlsr-romansh_sursilvan model.

### Supported Format

- **Model**: wav2vec2-xlsr-romansh_sursilvan
- **Language**: Romansh Sursilvan only
- **Input**: Audio files (WAV, MP3, etc.) or microphone
- **Performance**: WER 13.82% | CER 3.02%

### Using Web UI

1. Go to **🎤 Speech to Text** tab
2. Upload audio file or record directly
3. Click **📝 Transcribe**
4. Get Romansh text transcription

### Python API

```python
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa

# Load model from Hugging Face (downloads automatically if not cached)
model_name = "sammy786/wav2vec2-xlsr-romansh_sursilvan"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

# Load audio
audio, rate = librosa.load("audio.wav", sr=16000)

# Transcribe
inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
with torch.no_grad():
    logits = model(inputs.input_values).logits

predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]

print(transcription)
```

---

## 🎤→🌍 Audio Translation Pipeline

**Complete workflow**: Romansh audio → Romansh text → German/French/English

### Use Case: Translate Romansh Radio Broadcasts

Perfect for translating Radio Rumantsch or RTR broadcasts into other languages.

### Using Web UI

1. Go to **🎤→🌍 Audio Translation** tab
2. Upload Romansh audio file
3. Select target language (German, French, English, etc.)
4. Click **🎤→🌍 Transcribe & Translate**
5. Get both transcription AND translation

### Example Workflow

```
Input: Romansh radio broadcast (audio)
        ↓
Step 1: STT with wav2vec2
        → "Bun di, co va cun vos oz?"
        ↓
Step 2: Translation with Apertus8B
        → "Guten Tag, wie geht es Ihnen heute?"
        ↓
Output: German text
```

---

## 📰 Batch News Translation

Translate multiple news articles or documents at once.

### Use Cases

- Translate Graubünden news from German to Romansh
- Batch process RTR press releases
- Convert historical documents

### Command Line - Single File

```bash
python batch_news_translator.py \
  --file article.txt \
  --output article_romansh.txt \
  --src de \
  --tgt rm-sursilv
```

### Command Line - Directory

```bash
# Translate all .txt files in a directory
python batch_news_translator.py \
  --dir news/ \
  --output-dir news_romansh/ \
  --src de \
  --tgt rm-sursilv
```

### Web UI

1. Go to **📄 Batch Translation** tab
2. Upload .txt file or paste text (one sentence per line)
3. Select source and target languages
4. Click **🌍 Translate All**
5. Download translated text

### Example: Translating News Feed

```bash
# Create a file with news headlines
cat > headlines.txt <<EOF
Graubünden startet neue Tourismusinitiative
Regierung beschliesst Klimamassnahmen
Romanisch-Unterricht wird ausgebaut
EOF

# Translate to Romansh Sursilvan
python batch_news_translator.py \
  --file headlines.txt \
  --src de \
  --tgt rm-sursilv

# Output: headlines_rm-sursilv.txt
```

---

## 🔊 Text-to-Speech (TTS)

### Current Status

✅ **TTS NOW AVAILABLE for mainstream languages!**

**Supported Languages:**
- English, German, French, Italian, Spanish, Portuguese
- Uses Facebook MMS-TTS (1107 languages available)
- High-quality neural speech synthesis
- Fully offline, runs locally

❌ **Romansh TTS still not available** (Romansh not in the 1107-language dataset)

### Using TTS in TraductAL

#### Web UI

The Gradio interface now includes **3 TTS tabs**:

1. **🔊 Text-to-Speech**: Convert text to speech in any supported language
2. **🌍→🔊 Translate & Speak**: Translate text and generate audio
3. **🎤→🔊 Audio to Audio**: Complete pipeline (Romansh audio → spoken translation)

#### Python API

```python
from tts_engine import TTSEngine

# Initialize TTS engine
tts = TTSEngine()

# Generate speech
audio_path, sample_rate = tts.text_to_speech(
    "Hello! This is a test.",
    "English"
)

print(f"Audio saved: {audio_path}")
print(f"Duration: {sample_rate}Hz")
```

#### Command Line Test

```bash
cd /home/aldn/TraductAL/TraductAL
source /home/aldn/Apertus8B/alvenv/bin/activate
python tts_engine.py
```

### Romansh TTS - Future Options

#### Option 1: Fine-tune Existing Model

Use Coqui TTS or VITS to fine-tune on Romansh audio:

**Requirements**:
- Romansh audio recordings with transcriptions
- 5-10 hours of clean speech data
- GPU for training (2-5 days)

**Resources**:
- Coqui TTS: https://github.com/coqui-ai/TTS
- VITS tutorial: https://docs.coqui.ai/en/latest/models/vits.html

#### Option 2: Voice Cloning

Use XTTS-v2 for zero-shot voice cloning:
- Record 6-10 seconds of Romansh speaker
- Clone voice and generate speech in any language
- **Limitation**: Won't sound native Romansh

#### Option 3: Request Romansh Support

Contact Swiss AI institutions:
- ETH Zurich (Apertus team)
- EPFL
- University of Zurich (ZurichNLP)

### Workaround for Now

Use **proxy approach**:
1. Translate Romansh → German
2. Use German TTS (widely available)
3. Manually adjust pronunciation

---

## 🔄 Complete Pipelines

TraductAL now supports **end-to-end multimodal pipelines**:

### Pipeline 1: Text → Text (Translation)
```
Input Text (any language) → Translation Engine → Output Text (target language)
```
**Use**: Standard translation

### Pipeline 2: Audio → Text (STT + Translation)
```
Romansh Audio → wav2vec2 STT → Romansh Text → Translation → Target Text
```
**Use**: Transcribe and translate Romansh broadcasts

### Pipeline 3: Text → Audio (Translation + TTS)
```
Input Text → Translation → Target Text → MMS-TTS → Target Audio
```
**Use**: Create spoken translations, language learning

### Pipeline 4: Audio → Audio (Complete Multimodal)
```
Romansh Audio → STT → Romansh Text → Translation → Target Text → TTS → Target Audio
```
**Use**: Convert Romansh radio broadcasts into spoken German/French/English

### Pipeline 5: Text → Audio (Direct TTS)
```
Text (any supported language) → MMS-TTS → Audio
```
**Use**: Generate speech from text, accessibility features

---

## 🎯 Use Cases

### 1. Radio Broadcast Translation

**Scenario**: Translate Radio Rumantsch broadcasts for non-Romansh speakers

```bash
# Step 1: Record broadcast
# (use audio recording software)

# Step 2: Use web UI Audio Translation tab
# Upload audio → Get German/French translation
```

### 2. News Translation for Graubünden

**Scenario**: Translate German news into Romansh for local communities

```bash
# Download news articles as .txt files
# Batch translate
python batch_news_translator.py \
  --dir srf_news/ \
  --output-dir rtr_news/ \
  --src de \
  --tgt rm-sursilv
```

### 3. Bilingual Content Creation

**Scenario**: Create parallel German-Romansh content

```python
from unified_translator import UnifiedTranslator

translator = UnifiedTranslator()

# Translate press release
german_text = """
Die Regierung von Graubünden hat heute neue Massnahmen
zur Förderung der romanischen Sprache angekündigt.
"""

romansh = translator.translate(
    german_text,
    src_lang="de",
    tgt_lang="rm-sursilv"
)

# Save both versions
with open("press_release_de.txt", "w") as f:
    f.write(german_text)

with open("press_release_rm.txt", "w") as f:
    f.write(romansh["translation"])
```

### 4. Educational Content

**Scenario**: Create Romansh learning materials from German resources

```bash
# Translate German children's books
python batch_news_translator.py \
  --dir books_german/ \
  --output-dir books_romansh/ \
  --src de \
  --tgt rm-sursilv
```

### 5. Meeting Transcription & Translation

**Scenario**: Record Romansh meetings and provide German summaries

**Workflow**:
1. Record meeting (Romansh audio)
2. Use STT → Get Romansh transcript
3. Translate → German summary
4. Share with non-Romansh stakeholders

### 6. Audio-to-Audio Translation (NEW!)

**Scenario**: Convert Romansh radio broadcasts to spoken German

**Workflow using Web UI**:
1. Go to **🎤→🔊 Audio to Audio** tab
2. Upload Romansh audio file (or use chunks from `/audio_chunks/`)
3. Select target language (e.g., German)
4. Click **🎤→🔊 Complete Pipeline**
5. Get:
   - Romansh transcription
   - German translation (text)
   - German spoken audio (downloadable)

**Example**:
```
Input:  Romansh radio broadcast (30-second chunk)
Step 1: "Bun di, co va cun vos oz?"
Step 2: "Guten Tag, wie geht es Ihnen heute?"
Step 3: [German_audio.wav - downloadable]
```

### 7. Accessibility Features (NEW!)

**Scenario**: Create audio versions of Romansh text content

**Workflow**:
1. Translate Romansh text to target language
2. Use **🌍→🔊 Translate & Speak** tab
3. Get both translated text AND audio
4. Share audio with visually impaired users or for audio learning

---

## 🔧 Technical Architecture

### Complete Pipeline

```
┌──────────────────────────────────────────────────┐
│          INPUT MODALITIES                         │
├──────────────────────────────────────────────────┤
│ • Text (12 languages: 6 Romansh + 6 mainstream)  │
│ • Audio (Romansh Sursilvan only)                 │
└─────────────────┬────────────────────────────────┘
                  │
         ┌────────▼────────┐
         │  Processing     │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼──┐     ┌────▼────┐   ┌───▼──────┐
│ STT  │     │  NLLB   │   │ Apertus  │
│wav2  │     │  200    │   │   8B     │
│vec2  │     │(1.3B)   │   │  (8B)    │
└───┬──┘     └────┬────┘   └───┬──────┘
    │             │            │
    │   ┌─────────▼────────────┘
    │   │    Auto Select
    │   │    Best Engine
    └───┼──────────┬
        │          │
        │  ┌───────▼────────┐
        │  │  Translation   │
        │  └───────┬────────┘
        │          │
        │      ┌───▼────┐
        │      │  TTS   │
        │      │  MMS   │
        │      │ (VITS) │
        │      └───┬────┘
        │          │
┌───────▼──────────▼──────────────┐
│      OUTPUT MODALITIES           │
├──────────────────────────────────┤
│ • Text (All 6 Romansh variants   │
│   + 200 languages)               │
│ • Audio (6 mainstream languages) │
│ • Batch files                    │
│ • JSON/structured data           │
└──────────────────────────────────┘
```

### Models Used

| Component | Model | Size | Languages | Status |
|-----------|-------|------|-----------|--------|
| **STT** | wav2vec2-xlsr-romansh_sursilvan | 317M params | Romansh Sursilvan | ✅ Active |
| **Translation** | NLLB-200-1.3B | 1.3B params | 200 languages | ✅ Active |
| **Translation** | Apertus-8B | 8B params | 1,811 languages | ✅ Active |
| **TTS** | facebook/mms-tts (VITS-based) | ~300M per lang | 1,107 languages | ✅ NEW! |

---

## 📊 Performance Benchmarks

### Translation Speed (CPU)

| Engine | Model Size | Speed | Quality |
|--------|-----------|-------|---------|
| NLLB-200-1.3B | 1.3B | 0.5-2s | Very Good |
| NLLB-200-3.3B | 3.3B | 1-3s | High |
| Apertus-8B | 8B | 10-15s | Very High |

### STT Performance

| Metric | Score | Notes |
|--------|-------|-------|
| WER (Word Error Rate) | 13.82% | Test set |
| CER (Character Error Rate) | 3.02% | Test set |
| Training WER | 21.25% | Training set |

### TTS Performance (NEW!)

| Metric | English | German | French | Notes |
|--------|---------|--------|--------|-------|
| **Speed (CPU)** | 1-2s | 1-2s | 1-2s | For ~50 char text |
| **Quality** | Very High | Very High | Very High | Natural-sounding |
| **Model Size** | ~300MB | ~300MB | ~300MB | Downloaded once, cached |
| **Sample Rate** | 16kHz | 16kHz | 16kHz | Standard quality |

---

## 🚦 Roadmap

### ✅ Completed

- [x] Text translation (German/French/English ↔ Romansh)
- [x] All 6 Romansh variants supported
- [x] STT for Romansh Sursilvan
- [x] Audio translation pipeline (audio → text)
- [x] **TTS for 6 mainstream languages (English, German, French, Italian, Spanish, Portuguese)**
- [x] **Complete audio-to-audio pipeline**
- [x] **Translate & Speak functionality**
- [x] Batch translation
- [x] Gradio web UI with 8 tabs
- [x] Dataset integration (46k German-Romansh pairs)

### 🔄 In Progress

- [ ] Romansh TTS model (research/fine-tuning needed)
- [ ] Fine-tuning scripts for domain-specific translation
- [ ] Web scraping for RTR news

### 🔮 Future

- [ ] Fine-tune TTS for Romansh (if voice data available)
- [ ] Support for other Romansh dialects in STT
- [ ] Real-time streaming translation
- [ ] Mobile app integration
- [ ] Subtitle generation for RTR videos

---

## 📚 Resources

### Official Documentation

- **This System**: `ROMANSH_GUIDE.md`, `MULTIMODAL_GUIDE.md`
- **TraductAL**: `README.md`, `TRAINING_GUIDE.md`
- **NLLB-200**: `NLLB_UPGRADE_GUIDE.md`

### External Links

- **Apertus8B**: https://huggingface.co/swiss-ai/Apertus-8B-2509
- **wav2vec2-romansh**: [sammy786/wav2vec2-xlsr-romansh_sursilvan](https://huggingface.co/sammy786/wav2vec2-xlsr-romansh_sursilvan) (auto-downloads from Hugging Face)
- **Dataset**: https://huggingface.co/datasets/swiss-ai/apertus-posttrain-romansh
- **RTR (Radio Televisiun Rumantscha)**: https://www.rtr.ch

### Swiss Language Resources

- **Lia Rumantscha**: https://www.liarumantscha.ch
- **Pledari Grond**: https://www.pledarigrond.ch (Romansh dictionary)
- **Convegn Romansh**: Resources for Romansh learners

---

## ✅ Quick Reference

### Start Web UI
```bash
cd /home/aldn/TraductAL/TraductAL
./start_gradio.sh
```

### Translate Text
```bash
./translate_romansh.sh de rm-sursilv "Text hier"
```

### Batch Translate
```bash
python batch_news_translator.py --dir news/ --src de --tgt rm-sursilv
```

### Python API
```python
from unified_translator import UnifiedTranslator
translator = UnifiedTranslator()
result = translator.translate("Text", "de", "rm-sursilv")
```

---

**Built with ❤️ for Romansh language preservation** 🇨🇭
