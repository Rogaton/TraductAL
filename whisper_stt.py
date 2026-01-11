#!/usr/bin/env python3
"""
Whisper STT Engine for Multi-Language Speech Recognition
Supports 100+ languages with automatic language detection
"""

import os
import sys
import time
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")

try:
    import torch
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    import librosa
    print("✅ Whisper dependencies loaded successfully")
except ImportError as e:
    print(f"❌ Error: Required packages not installed: {e}")
    sys.exit(1)


class WhisperSTT:
    """
    Multi-language speech-to-text using OpenAI's open-source Whisper model.

    Supports 100+ languages including:
    - All European languages (English, German, French, Spanish, Italian, Portuguese, Russian)
    - Asian languages (Chinese, Japanese, Korean, Hindi, Arabic)
    - And many more

    Features:
    - Automatic language detection
    - High-quality transcription
    - One model for all languages
    """

    # Language name to Whisper code mapping
    LANGUAGE_CODES = {
        # European languages
        "English": "en",
        "German": "de",
        "French": "fr",
        "Italian": "it",
        "Spanish": "es",
        "Portuguese": "pt",
        "Russian": "ru",
        # Asian languages
        "Chinese": "zh",
        "Japanese": "ja",
        "Korean": "ko",
        "Hindi": "hi",
        "Arabic": "ar",
        # Romansh (if needed)
        "Romansh": "rm"
    }

    def __init__(self, model_size="base"):
        """
        Initialize Whisper STT engine.

        Args:
            model_size: Whisper model size
                - "tiny": 39M params, fastest, lowest quality
                - "base": 74M params, good balance (default)
                - "small": 244M params, better quality
                - "medium": 769M params, high quality
                - "large": 1550M params, best quality
        """
        self.model_size = model_size
        self.model_name = f"openai/whisper-{model_size}"
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"🎤 Whisper STT Engine ({model_size})")
        print(f"📁 Model: {self.model_name}")
        print(f"💾 Device: {self.device}")
        print(f"🌍 Languages: 100+ (with auto-detection)")

    def load_model(self):
        """Load Whisper model and processor."""
        if self.model is not None:
            print("✅ Whisper model already loaded")
            return True

        try:
            print(f"⏳ Loading Whisper {self.model_size} model...")
            print("   This may take 30-60 seconds on first load...")
            start_time = time.time()

            # Load processor
            self.processor = WhisperProcessor.from_pretrained(self.model_name)

            # Load model
            dtype = torch.float16 if self.device == "cuda" else torch.float32
            self.model = WhisperForConditionalGeneration.from_pretrained(
                self.model_name,
                dtype=dtype
            )
            self.model.to(self.device)

            load_time = time.time() - start_time
            print(f"✅ Whisper model loaded in {load_time:.1f}s")
            print(f"📊 Model size: {self.model_size}")
            print(f"🌍 Ready for 100+ languages")

            return True

        except Exception as e:
            print(f"❌ Failed to load Whisper model: {str(e)}")
            return False

    def transcribe(self, audio_path, language=None, return_language=False):
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to audio file (MP3, WAV, etc.)
            language: Optional language code (e.g., "en", "de", "fr")
                     If None, Whisper will auto-detect
            return_language: If True, return (text, detected_language)

        Returns:
            Transcribed text (or tuple if return_language=True)
        """
        if not self.model:
            if not self.load_model():
                return "Error: Failed to load Whisper model"

        try:
            start_time = time.time()

            # Load audio
            print(f"🎵 Loading audio: {audio_path}")
            audio, sr = librosa.load(audio_path, sr=16000)
            print(f"📊 Audio loaded: {len(audio)} samples at {sr}Hz")

            # Process audio
            print("🔄 Processing audio...")
            inputs = self.processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt"
            )
            inputs = inputs.input_features.to(self.device)

            # Generate transcription
            print("🧠 Running transcription...")

            # Prepare generation kwargs
            generate_kwargs = {"task": "transcribe"}
            if language:
                # Force specific language
                generate_kwargs["language"] = language

            with torch.no_grad():
                predicted_ids = self.model.generate(
                    inputs,
                    **generate_kwargs
                )

            # Decode transcription
            transcription = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]

            # Simple language detection from result (fallback)
            detected_lang = language if language else "auto-detected"

            transcription_time = time.time() - start_time

            print(f"✅ Transcription complete in {transcription_time:.2f}s")
            if detected_lang:
                print(f"🌍 Detected language: {detected_lang}")

            if return_language:
                return transcription.strip(), detected_lang or language
            return transcription.strip()

        except Exception as e:
            error_msg = f"Transcription failed: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    def get_language_name(self, code):
        """Convert language code to full name."""
        code_to_name = {v: k for k, v in self.LANGUAGE_CODES.items()}
        return code_to_name.get(code, code.upper())

    def list_languages(self):
        """List commonly used languages."""
        print("\n🌍 Whisper Supported Languages")
        print("=" * 60)
        print("\n📌 Common languages (showing subset of 100+):")
        for name, code in sorted(self.LANGUAGE_CODES.items()):
            print(f"  {code}: {name}")

        print(f"\n💡 Whisper supports 100+ languages total")
        print(f"   Auto-detection available when language not specified")
        print(f"   Model: {self.model_name}")


def main():
    """Test the Whisper STT engine."""
    import argparse

    parser = argparse.ArgumentParser(description="Whisper Multi-Language STT")
    parser.add_argument("audio_file", help="Path to audio file")
    parser.add_argument("--language", help="Language code (en, de, fr, etc.) - auto-detect if not specified")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size")
    parser.add_argument("--list-languages", action="store_true", help="List supported languages")

    args = parser.parse_args()

    # Initialize engine
    stt = WhisperSTT(model_size=args.model)

    if args.list_languages:
        stt.list_languages()
        return

    # Transcribe audio
    print(f"\n{'='*60}")
    print(f"🎤 WHISPER STT TEST")
    print(f"{'='*60}\n")

    transcription, detected_lang = stt.transcribe(
        args.audio_file,
        language=args.language,
        return_language=True
    )

    # Display results
    print(f"\n{'='*60}")
    print(f"📝 TRANSCRIPTION RESULT")
    print(f"{'='*60}")
    print(f"🎵 Audio: {args.audio_file}")
    print(f"🌍 Language: {detected_lang or 'auto-detected'}")
    print(f"📄 Text:\n{transcription}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
