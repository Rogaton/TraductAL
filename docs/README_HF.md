---
title: TraductAL - Swiss Languages Translator
emoji: 🇨🇭
colorFrom: red
colorTo: white
sdk: gradio
sdk_version: 4.0.0
app_file: gradio_app.py
pinned: false
license: apache-2.0
tags:
  - translation
  - swiss-languages
  - romansh
  - nllb
  - multilingual
  - speech-recognition
  - text-to-speech
---

# 🌍 TraductAL - Swiss Languages Translation System

**A comprehensive multilingual translation system specializing in Swiss dialects and low-resource languages.**

## 🎯 Overview

TraductAL combines two state-of-the-art translation engines to provide coverage for 66+ languages with special focus on Swiss linguistic diversity:

- **NLLB-200** (Meta AI): 200+ mainstream languages
- **Apertus-8B** (Swiss AI - ETH Zurich & EPFL): 1,811 languages including all 6 Romansh variants

## ✨ Key Features

### 🔤 Translation
- **66+ languages** available in the interface (51 NLLB + 15 Apertus specialist languages)
- **Automatic engine selection**: Smart routing to the best model for each language pair
- **Batch translation**: Process multiple sentences from text files
- **Searchable language lists**: Easy-to-navigate filterable dropdowns

### 🎤 Speech-to-Text (STT)
- **Whisper** (OpenAI): 100+ languages supported
- **wav2vec2**: Specialized Romansh Sursilvan model
- Automatic language detection
- Support for audio file upload or direct microphone recording

### 🔊 Text-to-Speech (TTS)
- **MMS-TTS** (Meta AI): 27+ languages with high-quality synthesis
- Natural-sounding speech generation
- Integrated with translation pipeline for spoken translations

### 🎧 Complete Pipelines
- **Audio → Text Translation**: Transcribe and translate in one step
- **Text → Spoken Translation**: Translate and synthesize speech
- **Audio → Audio**: Complete pipeline from source audio to translated spoken output

## 🇨🇭 Swiss Languages Support

### Romansh Variants (All 6 Supported)
- **Sursilvan** (55% of speakers)
- **Vallader** (20%)
- **Puter** (12%)
- **Surmiran** (10%)
- **Sutsilvan** (3%)
- **Rumantsch Grischun** (official standard)

### Other Swiss & Low-Resource Languages
- Occitan
- Breton
- Welsh
- Scottish Gaelic
- Irish
- Luxembourgish
- Friulian
- Ladin
- Sardinian

## 🌐 Major Languages Supported

### European
German, English, French, Italian, Spanish, Portuguese, Dutch, Polish, Czech, Swedish, Danish, Norwegian, Finnish, Greek, Turkish, Hungarian, Romanian, Catalan, Galician, Basque, Ukrainian, Bulgarian, Serbian, Croatian, Slovak, Slovenian, Albanian, Macedonian, Lithuanian, Latvian, Estonian, Icelandic

### Asian
Russian, Chinese, Japanese, Korean, Hindi, Vietnamese, Thai, Indonesian, Malay, Tamil, Bengali, Urdu, Persian, Hebrew

### African
Arabic, Swahili, Amharic, Hausa, Yoruba

## 🚀 Usage

1. **Select Languages**: Choose source and target languages from searchable dropdowns
2. **Input**: Type text, paste content, or upload audio
3. **Translate**: Click translate button
4. **Output**: View translation and optionally generate speech

### Example Use Cases

- 📻 **Romansh Radio**: Transcribe Romansh broadcasts and translate to German/French
- 📰 **News Translation**: Convert articles between 50+ languages
- 🎓 **Language Learning**: Practice with text and speech in multiple languages
- 🏛️ **Document Translation**: Batch translate official documents
- 🗣️ **Spoken Communication**: Audio-to-audio translation for meetings

## 🔧 Technical Details

### Models Used

| Component | Model | Parameters | Purpose |
|-----------|-------|------------|---------|
| Translation (General) | NLLB-200-1.3B | 1.3B | 200+ mainstream languages |
| Translation (Swiss) | Apertus-8B-2509 | 8B | Swiss dialects + 1,811 languages |
| Speech-to-Text | Whisper-base | 74M | 100+ languages transcription |
| Speech-to-Text (Romansh) | wav2vec2-xlsr-romansh | 300M | Romansh Sursilvan specialist |
| Text-to-Speech | MMS-TTS | Various | 27+ languages synthesis |

### Training Data

- **swiss-ai/apertus-posttrain-romansh**: 46,092 German-Romansh parallel sentences
- **NLLB-200**: Trained on diverse multilingual corpora
- **Whisper**: Trained on 680,000 hours of multilingual audio
- **MMS-TTS**: Trained on 1,100+ languages

### Performance

- **Translation Speed**: 0.5-2 seconds per sentence (NLLB), 2-5 seconds (Apertus)
- **Transcription**: Real-time to 2x real-time
- **TTS Synthesis**: 1-3 seconds per sentence
- **Device Support**: CPU and GPU (automatically detected)

## 🔒 Privacy & Security

- ✅ **100% offline processing** (when self-hosted)
- ✅ **No data sent to external servers** (except HF model downloads)
- ✅ **All models run locally**
- ✅ **GDPR compliant**
- ✅ **Open source** (Apache 2.0 License)

## 📚 Resources

- **Apertus-8B Model**: [huggingface.co/swiss-ai/Apertus-8B-2509](https://huggingface.co/swiss-ai/Apertus-8B-2509)
- **NLLB-200 Model**: [huggingface.co/facebook/nllb-200-1.3B](https://huggingface.co/facebook/nllb-200-1.3B)
- **Romansh Dataset**: [huggingface.co/datasets/swiss-ai/apertus-posttrain-romansh](https://huggingface.co/datasets/swiss-ai/apertus-posttrain-romansh)
- **Whisper Model**: [huggingface.co/openai/whisper-base](https://huggingface.co/openai/whisper-base)
- **MMS-TTS**: [huggingface.co/facebook/mms-tts](https://huggingface.co/facebook/mms-tts)

## 📖 Documentation

For comprehensive documentation, see:
- `README.md` - Full project documentation
- `QUICKSTART.md` - Quick start guide
- `ADD_LANGUAGES_GUIDE.md` - How to add more languages
- `MULTIMODAL_GUIDE.md` - Audio features guide
- `PRODUCTION_READINESS.md` - Deployment guidelines

## 🙏 Acknowledgments

- **Meta AI** for NLLB-200, Whisper, and MMS-TTS models
- **Swiss AI (ETH Zurich & EPFL)** for Apertus-8B
- **OpenAI** for Whisper speech recognition
- **Mozilla Common Voice** for Romansh training data

## 📄 License

Apache 2.0 License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! This is an open-source project aimed at preserving and promoting Swiss linguistic diversity.

---

**Version**: 2.0.0
**Last Updated**: January 2026
**Status**: Production Ready
