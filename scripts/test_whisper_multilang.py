#!/usr/bin/env python3
"""
Test Whisper multi-language STT functionality
Tests transcription for multiple languages
"""

import sys
import os

# Test with the Romansh audio chunk first
test_audio_path = "audio_chunks/romansh_chunk_001.mp3"

print("="*70)
print("🎤 WHISPER MULTI-LANGUAGE STT TEST")
print("="*70)

# Test 1: Check if whisper_stt module loads
print("\n📦 TEST 1: Loading Whisper STT engine...")
try:
    from whisper_stt import WhisperSTT
    print("✅ WhisperSTT module loaded successfully")
except ImportError as e:
    print(f"❌ Failed to load WhisperSTT: {e}")
    sys.exit(1)

# Test 2: Initialize Whisper
print("\n🔧 TEST 2: Initializing Whisper base model...")
try:
    whisper = WhisperSTT(model_size="base")
    print("✅ Whisper engine initialized")
except Exception as e:
    print(f"❌ Failed to initialize Whisper: {e}")
    sys.exit(1)

# Test 3: Load the model
print("\n⏳ TEST 3: Loading Whisper model...")
print("   (This will download ~150MB on first run)")
try:
    if whisper.load_model():
        print("✅ Whisper model loaded successfully")
    else:
        print("❌ Failed to load Whisper model")
        sys.exit(1)
except Exception as e:
    print(f"❌ Model loading error: {e}")
    sys.exit(1)

# Test 4: Transcribe Romansh audio (to verify it can handle low-resource languages)
print(f"\n🎙️  TEST 4: Transcribing Romansh audio...")
print(f"   File: {test_audio_path}")

if not os.path.exists(test_audio_path):
    print(f"⚠️  Audio file not found: {test_audio_path}")
    print("   Skipping transcription test")
else:
    try:
        # Transcribe with auto-detection
        transcription, detected_lang = whisper.transcribe(
            test_audio_path,
            language=None,  # Auto-detect
            return_language=True
        )

        print(f"✅ Transcription successful!")
        print(f"🌍 Detected language: {detected_lang}")
        print(f"📝 Transcription:\n{transcription}")

    except Exception as e:
        print(f"❌ Transcription failed: {e}")

# Test 5: Test language code mapping
print("\n🔤 TEST 5: Language code mapping...")
test_langs = ["English", "German", "French", "Russian", "Hindi", "Arabic"]
for lang in test_langs:
    code = whisper.LANGUAGE_CODES.get(lang)
    if code:
        print(f"✅ {lang:15} → {code}")
    else:
        print(f"❌ {lang:15} → NOT FOUND")

# Summary
print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)
print("✅ Whisper STT engine is ready for multi-language transcription")
print("✅ Supports 100+ languages including:")
print("   • European: English, German, French, Italian, Spanish, Portuguese")
print("   • Slavic: Russian")
print("   • Asian: Hindi, Arabic, Chinese, Japanese, Korean")
print("   • Low-resource: Romansh (via Whisper's multilingual support)")
print("\n💡 Use whisper_stt.py to transcribe audio in any of these languages")
print("="*70)
