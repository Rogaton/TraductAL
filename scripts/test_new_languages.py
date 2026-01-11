#!/usr/bin/env python3
"""
Test script for new language support in TraductAL
Tests TTS for all 12 languages: 6 original + 6 new
"""

from tts_engine import TTSEngine
import sys

def test_all_languages():
    """Test TTS for all supported languages."""

    print("\n" + "="*70)
    print("🌍 Testing TraductAL - 12 Language TTS Support")
    print("="*70 + "\n")

    # Initialize TTS engine
    print("🔄 Initializing TTS engine...")
    tts = TTSEngine()
    print(f"✅ TTS engine initialized\n")

    # Test sentences in each language
    test_cases = [
        # Original 6 languages
        ("English", "Hello! Welcome to TraductAL translation system."),
        ("German", "Guten Tag! Willkommen im TraductAL Übersetzungssystem."),
        ("French", "Bonjour! Bienvenue dans le système TraductAL."),
        ("Italian", "Buongiorno! Benvenuti nel sistema TraductAL."),
        ("Spanish", "¡Hola! Bienvenido al sistema TraductAL."),
        ("Portuguese", "Olá! Bem-vindo ao sistema TraductAL."),

        # NEW: Tier 1 - Major World Languages
        ("Russian", "Привет! Добро пожаловать в систему TraductAL."),
        ("Chinese", "你好！欢迎使用 TraductAL 翻译系统。"),
        ("Hindi", "नमस्ते! TraductAL अनुवाद प्रणाली में आपका स्वागत है।"),

        # NEW: Tier 2 - Additional Major Languages
        ("Arabic", "مرحبا! مرحبا بكم في نظام TraductAL للترجمة."),
        ("Japanese", "こんにちは！TraductAL翻訳システムへようこそ。"),
        ("Korean", "안녕하세요! TraductAL 번역 시스템에 오신 것을 환영합니다.")
    ]

    results = []
    errors = []

    for i, (language, text) in enumerate(test_cases, 1):
        tier = "Original" if i <= 6 else ("Tier 1" if i <= 9 else "Tier 2")

        try:
            print(f"[{i}/12] Testing {language} ({tier})...")
            print(f"   Text: {text[:50]}{'...' if len(text) > 50 else ''}")

            # Generate speech
            audio_path, sample_rate = tts.text_to_speech(text, language)

            print(f"   ✅ Success! Audio: {audio_path.split('/')[-1]}")
            print(f"   📊 Sample rate: {sample_rate}Hz\n")

            results.append({
                'language': language,
                'tier': tier,
                'status': 'SUCCESS',
                'audio': audio_path
            })

        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")
            errors.append({
                'language': language,
                'tier': tier,
                'error': str(e)
            })

    # Print summary
    print("="*70)
    print("📊 TEST SUMMARY")
    print("="*70 + "\n")

    print(f"✅ Successful: {len(results)}/12 languages")
    print(f"❌ Failed: {len(errors)}/12 languages\n")

    if results:
        print("✅ WORKING LANGUAGES:")
        for r in results:
            print(f"   • {r['language']} ({r['tier']})")

    if errors:
        print("\n❌ FAILED LANGUAGES:")
        for e in errors:
            print(f"   • {e['language']} ({e['tier']}): {e['error'][:60]}")

    print("\n" + "="*70)

    if len(results) == 12:
        print("🎉 SUCCESS! All 12 languages are working!")
        print("="*70 + "\n")
        return 0
    elif len(results) >= 6:
        print("⚠️  PARTIAL SUCCESS: Original 6 languages work, some new ones failed")
        print("="*70 + "\n")
        return 1
    else:
        print("❌ FAILURE: Critical errors detected")
        print("="*70 + "\n")
        return 2

if __name__ == "__main__":
    exit_code = test_all_languages()
    sys.exit(exit_code)
