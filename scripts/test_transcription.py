#!/usr/bin/env python3
"""
Quick test script for wav2vec2 Romansh transcription
"""

import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import sys

def transcribe_audio(audio_file):
    """Transcribe Romansh audio to text using wav2vec2."""
    try:
        print("🔄 Loading wav2vec2 model from Hugging Face...")

        # Load wav2vec2 model from Hugging Face
        model_name = "sammy786/wav2vec2-xlsr-romansh_sursilvan"
        processor = Wav2Vec2Processor.from_pretrained(model_name)
        model = Wav2Vec2ForCTC.from_pretrained(model_name)

        print("✅ Model loaded successfully!")
        print(f"🎵 Loading audio file: {audio_file}")

        # Load and preprocess audio
        audio, rate = librosa.load(audio_file, sr=16000)

        print(f"📊 Audio loaded: {len(audio)} samples at {rate}Hz")
        print("🔄 Processing audio...")

        # Process audio
        inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)

        print("🧠 Running inference...")
        with torch.no_grad():
            logits = model(inputs.input_values).logits

        # Decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

        print("\n" + "="*60)
        print("✅ TRANSCRIPTION SUCCESSFUL!")
        print("="*60)
        print(f"\n{transcription}\n")
        print("="*60)

        return transcription

    except Exception as e:
        print(f"\n❌ Transcription error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        audio_file = "magazin_radio_AUDI20251222_RS_0007_37f4da7a98124418a448857858fb2035.mp3"
        print(f"⚠️  No audio file specified, using default: {audio_file}")
    else:
        audio_file = sys.argv[1]

    transcribe_audio(audio_file)
