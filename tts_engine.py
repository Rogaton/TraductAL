#!/usr/bin/env python3
"""
TTS Engine for TraductAL
Provides text-to-speech functionality using Facebook MMS-TTS
Supports 1107 languages including all major European languages
"""

import torch
import numpy as np
import tempfile
import os
from typing import Optional, Tuple
import warnings
warnings.filterwarnings("ignore")


class TTSEngine:
    """
    Text-to-Speech engine using Facebook MMS-TTS models
    Supports caching of models for efficient repeated use
    """

    # Language code mapping for supported languages (ISO 639-3 codes)
    # Note: Only languages with available MMS-TTS checkpoints on HuggingFace
    LANGUAGE_CODES = {
        # Original European languages (TTS available)
        "English": "eng",
        "German": "deu",
        "French": "fra",
        "Spanish": "spa",
        "Portuguese": "por",
        # Tier 1: Major World Languages (added Dec 2025)
        "Russian": "rus",
        "Hindi": "hin",
        # Tier 2: Additional Major Languages (added Dec 2025)
        "Arabic": "ara",   # Modern Standard Arabic
        "Korean": "kor"
        # NOTE: Italian, Chinese (Mandarin), Japanese not available in MMS-TTS
        # These languages work for TRANSLATION only, not TTS
    }

    def __init__(self):
        """Initialize TTS engine with empty model cache."""
        self.models = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔊 TTS Engine initialized (device: {self.device})")

    def get_language_code(self, language_name: str) -> str:
        """
        Convert language name to ISO 639-3 code.

        Args:
            language_name: Full language name (e.g., "English")

        Returns:
            ISO 639-3 language code (e.g., "eng")
        """
        return self.LANGUAGE_CODES.get(language_name, language_name.lower()[:3])

    def load_model(self, language_code: str) -> Tuple:
        """
        Load TTS model for specified language (with caching).

        Args:
            language_code: ISO 639-3 language code (e.g., "eng", "deu")

        Returns:
            Tuple of (model, tokenizer)
        """
        if language_code in self.models:
            print(f"♻️  Using cached model for {language_code}")
            return self.models[language_code]

        try:
            from transformers import VitsModel, AutoTokenizer

            model_name = f"facebook/mms-tts-{language_code}"
            print(f"📥 Loading TTS model: {model_name}...")

            model = VitsModel.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)

            # Move to appropriate device
            model = model.to(self.device)

            # Cache the model
            self.models[language_code] = (model, tokenizer)

            print(f"✅ Model loaded successfully for {language_code}")
            return model, tokenizer

        except Exception as e:
            print(f"❌ Error loading model for {language_code}: {e}")
            raise

    def text_to_speech(
        self,
        text: str,
        language_name: str,
        save_path: Optional[str] = None
    ) -> Tuple[str, int]:
        """
        Convert text to speech audio.

        Args:
            text: Input text to convert to speech
            language_name: Target language name (e.g., "English", "German")
            save_path: Optional path to save audio file (if None, creates temp file)

        Returns:
            Tuple of (audio_file_path, sample_rate)
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Get language code
        language_code = self.get_language_code(language_name)

        try:
            # Load model
            model, tokenizer = self.load_model(language_code)

            print(f"🔄 Synthesizing speech for text length: {len(text)} characters")

            # Tokenize text
            inputs = tokenizer(text, return_tensors="pt")

            # Move inputs to device
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Generate speech
            with torch.no_grad():
                output = model(**inputs).waveform

            # Convert to numpy and get sample rate
            waveform = output.squeeze().cpu().numpy()
            sample_rate = model.config.sampling_rate

            # Normalize audio to prevent clipping
            waveform = waveform / np.max(np.abs(waveform)) * 0.95

            # Save audio file
            if save_path is None:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".wav",
                    prefix=f"tts_{language_code}_"
                )
                save_path = temp_file.name
                temp_file.close()

            # Write audio file
            import scipy.io.wavfile
            scipy.io.wavfile.write(
                save_path,
                rate=sample_rate,
                data=(waveform * 32767).astype(np.int16)
            )

            print(f"✅ Audio saved to: {save_path}")
            print(f"📊 Duration: {len(waveform) / sample_rate:.2f} seconds")

            return save_path, sample_rate

        except Exception as e:
            print(f"❌ TTS Error: {str(e)}")
            raise

    def get_supported_languages(self):
        """Return list of supported language names (with TTS available)."""
        return list(self.LANGUAGE_CODES.keys())

    def has_tts_support(self, language_name: str) -> bool:
        """Check if a language has TTS support available."""
        return language_name in self.LANGUAGE_CODES

    def clear_cache(self):
        """Clear all cached models to free memory."""
        self.models.clear()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("🗑️  Model cache cleared")


# Test function
def test_tts():
    """Test TTS engine with a simple example."""
    print("\n" + "="*60)
    print("Testing TTS Engine")
    print("="*60 + "\n")

    engine = TTSEngine()

    # Test English
    text = "Hello! This is a test of the text to speech system."
    print(f"Input: {text}")

    audio_path, sample_rate = engine.text_to_speech(text, "English")
    print(f"Output: {audio_path} ({sample_rate}Hz)")

    # Test German
    text_de = "Guten Tag! Dies ist ein Test des Text-zu-Sprache-Systems."
    print(f"\nInput: {text_de}")

    audio_path_de, sample_rate_de = engine.text_to_speech(text_de, "German")
    print(f"Output: {audio_path_de} ({sample_rate_de}Hz)")

    print("\n" + "="*60)
    print("✅ TTS Test Complete")
    print("="*60)


if __name__ == "__main__":
    test_tts()
