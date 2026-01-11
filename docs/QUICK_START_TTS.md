# 🚀 Quick Start Guide - TTS Features

## ⚡ Start TraductAL with TTS

```bash
cd /home/aldn/TraductAL/TraductAL
source /home/aldn/Apertus8B/alvenv/bin/activate
./start_gradio.sh
```

Open browser: **http://localhost:7860**

---

## 🔊 New TTS Tabs

### Tab 5: Text-to-Speech
1. Enter text in any supported language
2. Select language (English/German/French/Italian/Spanish/Portuguese)
3. Click "🔊 Generate Speech"
4. Download the audio file

### Tab 6: Translate & Speak
1. Enter text in source language
2. Select source and target languages
3. Click "🌍→🔊 Translate & Speak"
4. Get translation text + downloadable audio

### Tab 7: Audio to Audio
1. Upload Romansh audio file (use files from `./audio_chunks/`)
2. Select target language
3. Click "🎤→🔊 Complete Pipeline"
4. Get transcription + translation + spoken audio

---

## 📂 Test Files Available

**Location**: `./audio_chunks/`
- 37 audio chunks (30 seconds each)
- Files: `romansh_chunk_000.mp3` through `romansh_chunk_036.mp3`
- Use these for testing the audio-to-audio pipeline

---

## 🧪 Quick Tests

### Test 1: Simple TTS
```bash
source /home/aldn/Apertus8B/alvenv/bin/activate
python tts_engine.py
```
Expected: Creates 2 audio files (English + German)

### Test 2: Audio Transcription
```bash
source /home/aldn/Apertus8B/alvenv/bin/activate
python test_transcription.py audio_chunks/romansh_chunk_001.mp3
```
Expected: Displays Romansh transcription

### Test 3: Web Interface
```bash
./start_gradio.sh
```
Expected: Opens web interface with 8 tabs

---

## 💡 Example Workflows

### Workflow 1: Text → Speech
1. Go to "🔊 Text-to-Speech" tab
2. Enter: "Hello! Welcome to TraductAL."
3. Select: English
4. Click generate
5. Download and play audio

### Workflow 2: Translate → Speak
1. Go to "🌍→🔊 Translate & Speak" tab
2. Enter: "Bun di!" (Romansh)
3. Source: Romansh Sursilvan
4. Target: German
5. Get: "Guten Tag!" + German audio

### Workflow 3: Audio → Audio
1. Go to "🎤→🔊 Audio to Audio" tab
2. Upload: `audio_chunks/romansh_chunk_001.mp3`
3. Target: German
4. Get: Romansh transcription + German translation + German audio

---

## 📖 Full Documentation

- **`TTS_INTEGRATION_SUMMARY.md`** - Complete implementation details
- **`MULTIMODAL_GUIDE.md`** - Full system guide with use cases
- **`ROMANSH_GUIDE.md`** - Romansh-specific features

---

## ✅ Supported Languages (TTS)

- 🇬🇧 English
- 🇩🇪 German (Deutsch)
- 🇫🇷 French (Français)
- 🇮🇹 Italian (Italiano)
- 🇪🇸 Spanish (Español)
- 🇵🇹 Portuguese (Português)

---

## 🎯 What Can You Do Now?

✅ Transcribe Romansh audio
✅ Translate to 200+ languages
✅ Generate speech in 6 languages
✅ Complete audio-to-audio translation
✅ Create spoken translations
✅ Language learning with audio
✅ Accessibility features

---

**Enjoy your enhanced TraductAL system!** 🎉
