#!/usr/bin/env python3
"""
Apertus8B Integration for Romansh Translation
Specialized wrapper for Swiss languages including Romansh (Sursilvan)
"""

import os
import sys
import time
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print("✅ Required packages loaded successfully")
except ImportError as e:
    print("❌ Error: Required packages not installed")
    print(f"Missing: {e}")
    sys.exit(1)


class ApertusTranslator:
    """
    Apertus8B translator for Swiss languages, optimized for Romansh.

    Apertus8B supports 1811 languages including:
    - Romansh (Sursilvan, Vallader, Puter, Surmiran, Sutsilvan, Rumantsch Grischun)
    - German, French, Italian, English
    """

    def __init__(self, model_path=None):
        # Try multiple paths in order of preference
        if model_path is None:
            # 1. Environment variable
            # 2. Relative to project root
            # 3. Common install locations
            model_path = os.environ.get('APERTUS_PATH') or \
                         os.environ.get('APERTUS8B_PATH') or \
                         './models/apertus-8b'

        self.model_path = Path(model_path)
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Language mappings for Romansh variants
        self.romansh_variants = {
            'rm-sursilv': 'Romansh Sursilvan',
            'rm-vallader': 'Romansh Vallader',
            'rm-puter': 'Romansh Puter',
            'rm-surmiran': 'Romansh Surmiran',
            'rm-sutsilv': 'Romansh Sutsilvan',
            'rm-rumgr': 'Rumantsch Grischun',
            'rm': 'Romansh'  # Generic
        }

        self.supported_languages = {
            # Core European languages
            'de': 'German',
            'fr': 'French',
            'it': 'Italian',
            'en': 'English',
            'es': 'Spanish',
            'pt': 'Portuguese',
            # World languages (added Dec 2025)
            'ru': 'Russian',
            'zh': 'Chinese',
            'hi': 'Hindi',
            'ar': 'Arabic',
            'ja': 'Japanese',
            'ko': 'Korean',
            # Romansh variants
            **self.romansh_variants
        }

        print("🇨🇭 Apertus8B Translator for Swiss Languages")
        print(f"📁 Model path: {self.model_path}")
        print(f"💾 Device: {self.device}")

    def load_model(self):
        """Load Apertus8B model and tokenizer."""
        if self.model is not None:
            print("✅ Model already loaded")
            return True

        try:
            print("⏳ Loading Apertus8B (8B parameters, ~16GB)...")
            print("   This may take 30-60 seconds on first load...")
            start_time = time.time()

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

            # Load model with optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )

            if self.device == "cpu":
                self.model = self.model.to(self.device)

            load_time = time.time() - start_time
            print(f"✅ Model loaded in {load_time:.1f}s")
            print(f"📊 Parameters: 8B")
            print(f"🌍 Languages: 1811 (including all Romansh variants)")

            return True

        except Exception as e:
            print(f"❌ Failed to load model: {str(e)}")
            return False

    def translate(self, text, src_lang='de', tgt_lang='rm-sursilv', max_tokens=512):
        """
        Translate text using Apertus8B.

        Args:
            text: Source text to translate
            src_lang: Source language code (de, fr, en, it)
            tgt_lang: Target language code (rm-sursilv, rm-vallader, etc.)
            max_tokens: Maximum output tokens

        Returns:
            dict with translation results and metadata
        """
        if not self.model:
            if not self.load_model():
                return {"error": "Failed to load model"}

        # Validate languages
        src_name = self.supported_languages.get(src_lang, src_lang)
        tgt_name = self.supported_languages.get(tgt_lang, tgt_lang)

        # Create translation prompt
        # Apertus8B is a causal LLM, so we use instruction prompting
        prompt = f"""Translate the following text from {src_name} to {tgt_name}.
Provide only the translation, without explanations.

{src_name}: {text}
{tgt_name}:"""

        try:
            start_time = time.time()

            # Prepare messages for chat template
            messages = [
                {"role": "user", "content": prompt}
            ]

            # Apply chat template
            text_input = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            # Tokenize
            model_inputs = self.tokenizer(
                [text_input],
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.model.device)

            # Generate translation
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **model_inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )

            # Decode output (skip input prompt)
            output_ids = generated_ids[0][len(model_inputs.input_ids[0]):]
            translation = self.tokenizer.decode(output_ids, skip_special_tokens=True)

            # Clean up translation (remove any trailing explanations)
            translation = translation.strip()
            # If translation contains multiple lines, take first substantial one
            lines = [l.strip() for l in translation.split('\n') if l.strip()]
            if lines:
                translation = lines[0]

            translation_time = time.time() - start_time

            return {
                "translation": translation,
                "model": "Apertus-8B",
                "model_type": "Causal LLM (1811 languages)",
                "time": f"{translation_time:.2f}s",
                "src_lang": f"{src_lang} ({src_name})",
                "tgt_lang": f"{tgt_lang} ({tgt_name})",
                "device": self.device
            }

        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}

    def list_languages(self):
        """List supported languages."""
        print("\n🌍 Supported Languages (Apertus8B):")
        print("=" * 50)
        print("\n📌 Common languages:")
        for code, name in sorted(self.supported_languages.items()):
            if not code.startswith('rm'):
                print(f"  {code}: {name}")

        print("\n🇨🇭 Romansh variants:")
        for code, name in sorted(self.romansh_variants.items()):
            print(f"  {code}: {name}")

        print(f"\n💡 Total: 1811 languages supported")
        print(f"   (Showing most relevant for Swiss context)")


def main():
    """Test the Apertus translator."""
    import argparse

    parser = argparse.ArgumentParser(description="Apertus8B Translator for Romansh")
    parser.add_argument("--src", default="de", help="Source language code")
    parser.add_argument("--tgt", default="rm-sursilv", help="Target language (Romansh variant)")
    parser.add_argument("--text", help="Text to translate")
    parser.add_argument("--list-languages", action="store_true", help="List supported languages")

    args = parser.parse_args()

    translator = ApertusTranslator()

    if args.list_languages:
        translator.list_languages()
        return

    # Test translation
    if not args.text:
        # Default test
        test_text = "Guten Tag! Wie geht es Ihnen?"
        print(f"\n🧪 Testing with: '{test_text}'")
        result = translator.translate(test_text, args.src, args.tgt)
    else:
        result = translator.translate(args.text, args.src, args.tgt)

    # Display results
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"\n🔤 Original ({result['src_lang']}): {args.text or 'Guten Tag! Wie geht es Ihnen?'}")
        print(f"🌍 Translation ({result['tgt_lang']}): {result['translation']}")
        print(f"🤖 Model: {result['model']} ({result['model_type']})")
        print(f"⏱️  Time: {result['time']}")
        print(f"💾 Device: {result['device']}")


if __name__ == "__main__":
    main()
