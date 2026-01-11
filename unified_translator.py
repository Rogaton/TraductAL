#!/usr/bin/env python3
"""
Unified TraductAL Translation Engine
Combines NLLB-200 (200 languages) + Apertus8B (1811 languages, Romansh specialist)
"""

import os
import sys
import time
import argparse
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

try:
    from nllb_translator import EnhancedOfflineTranslator
    from apertus_translator import ApertusTranslator
    print("✅ Translation engines loaded successfully")
except ImportError as e:
    print(f"❌ Error loading translation engines: {e}")
    sys.exit(1)


class UnifiedTranslator:
    """
    Unified translation engine combining:
    - NLLB-200: 200 languages, seq2seq, optimized for common languages
    - Apertus8B: 1811 languages, causal LLM, specialized for Swiss languages
    """

    def __init__(self, models_dir="./models/deployed_models"):
        self.models_dir = Path(models_dir)
        self.nllb_translator = None
        self.apertus_translator = None

        # Romansh language codes (Apertus8B specialty)
        self.romansh_languages = {
            'rm': 'Romansh (generic)',
            'rm-sursilv': 'Romansh Sursilvan',
            'rm-vallader': 'Romansh Vallader',
            'rm-puter': 'Romansh Puter',
            'rm-surmiran': 'Romansh Surmiran',
            'rm-sutsilv': 'Romansh Sutsilvan',
            'rm-rumgr': 'Rumantsch Grischun'
        }

        # Common languages supported by both (expanded Dec 2025)
        self.common_languages = {
            # Original 6 languages
            'de': 'German',
            'en': 'English',
            'fr': 'French',
            'it': 'Italian',
            'es': 'Spanish',
            'pt': 'Portuguese',
            # New languages added Dec 2025
            'ru': 'Russian',
            'zh': 'Chinese',
            'hi': 'Hindi',
            'ar': 'Arabic',
            'ja': 'Japanese',
            'ko': 'Korean'
        }

        print("🌍 Unified TraductAL Translation Engine")
        print("=" * 60)
        print("📦 NLLB-200: 200 languages (fast, optimized)")
        print("🇨🇭 Apertus8B: 1811 languages (Romansh specialist)")
        print("=" * 60)

    def _init_nllb(self):
        """Lazy load NLLB-200 translator."""
        if self.nllb_translator is None:
            print("\n⏳ Initializing NLLB-200...")
            self.nllb_translator = EnhancedOfflineTranslator(self.models_dir)
        return self.nllb_translator

    def _init_apertus(self):
        """Lazy load Apertus8B translator."""
        if self.apertus_translator is None:
            print("\n⏳ Initializing Apertus8B...")
            self.apertus_translator = ApertusTranslator()
        return self.apertus_translator

    def _is_romansh(self, lang_code):
        """Check if language code is Romansh variant."""
        return lang_code.startswith('rm')

    def auto_select_engine(self, src_lang, tgt_lang):
        """
        Automatically select best translation engine.

        Rules (updated Dec 2025):
        1. If either language is Romansh AND target is common EU language → Use Apertus8B
        2. If Romansh AND target is world language (Hindi/Russian/Arabic/etc) → Use NLLB
        3. If both languages in NLLB-200 → Use NLLB (faster, broader coverage)
        4. Otherwise → Use Apertus8B
        """
        # Check if Romansh involved
        is_src_romansh = self._is_romansh(src_lang)
        is_tgt_romansh = self._is_romansh(tgt_lang)

        # If Romansh involved
        if is_src_romansh or is_tgt_romansh:
            # If target is core European language, use Apertus (specialized)
            apertus_preferred = {'de', 'en', 'fr', 'it', 'es', 'pt'}
            other_lang = tgt_lang if is_src_romansh else src_lang

            if other_lang in apertus_preferred:
                return "apertus"

            # For Romansh + world languages (Hindi, Russian, etc.), use NLLB
            # Check if NLLB supports both languages
            nllb = self._init_nllb()
            nllb_src = nllb.nllb_languages.get(src_lang) or src_lang
            nllb_tgt = nllb.nllb_languages.get(tgt_lang) or tgt_lang

            if nllb_src in nllb.nllb_languages.values() and nllb_tgt in nllb.nllb_languages.values():
                return "nllb"

            # Fallback to Apertus
            return "apertus"

        # No Romansh: check if both languages supported by NLLB
        nllb = self._init_nllb()
        if src_lang in nllb.nllb_languages and tgt_lang in nllb.nllb_languages:
            return "nllb"

        return "apertus"

    def translate(self, text, src_lang, tgt_lang, engine=None, model_name=None):
        """
        Translate text using the best available engine.

        Args:
            text: Text to translate
            src_lang: Source language code
            tgt_lang: Target language code
            engine: Force specific engine ("nllb" or "apertus"), or None for auto
            model_name: Specific NLLB model to use (if engine="nllb")

        Returns:
            dict with translation and metadata
        """
        if not text.strip():
            return {"error": "Empty text provided"}

        # Auto-select engine if not specified
        if engine is None:
            engine = self.auto_select_engine(src_lang, tgt_lang)
            print(f"🤖 Auto-selected engine: {engine.upper()}")

        try:
            start_time = time.time()

            if engine == "nllb":
                translator = self._init_nllb()
                result = translator.translate(text, src_lang, tgt_lang, model_name)

                # Ensure result is dict format
                if isinstance(result, str):
                    result = {"translation": result, "model": model_name or "NLLB-200"}

                result["engine"] = "NLLB-200"

            elif engine == "apertus":
                translator = self._init_apertus()
                result = translator.translate(text, src_lang, tgt_lang)
                result["engine"] = "Apertus8B"

            else:
                return {"error": f"Unknown engine: {engine}"}

            total_time = time.time() - start_time
            result["total_time"] = f"{total_time:.2f}s"

            return result

        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}

    def list_languages(self):
        """List all supported languages."""
        print("\n" + "=" * 60)
        print("🌍 SUPPORTED LANGUAGES")
        print("=" * 60)

        print("\n🇨🇭 ROMANSH VARIANTS (Apertus8B only):")
        for code, name in sorted(self.romansh_languages.items()):
            print(f"  ✅ {code:15} {name}")

        print("\n🌐 COMMON LANGUAGES (Both engines):")
        for code, name in sorted(self.common_languages.items()):
            print(f"  ✅ {code:15} {name}")

        print("\n📊 COVERAGE:")
        print(f"  • NLLB-200:   200 languages")
        print(f"  • Apertus8B:  1,811 languages")
        print(f"  • Total:      1,811+ unique languages")

        print("\n💡 USAGE:")
        print("  • Romansh: Always uses Apertus8B (specialist)")
        print("  • Common langs: Prefers NLLB-200 (faster)")
        print("  • Rare langs: Uses Apertus8B (broader coverage)")

    def list_models(self):
        """List available models."""
        print("\n" + "=" * 60)
        print("🤖 AVAILABLE TRANSLATION MODELS")
        print("=" * 60)

        print("\n📦 NLLB-200 Models:")
        nllb = self._init_nllb()
        nllb.list_models()

        print("\n🇨🇭 Apertus8B Model:")
        print("  ✅ Apertus-8B")
        print("     Type: Causal LLM (decoder-only)")
        print("     Languages: 1,811")
        print("     Specialty: Swiss languages (Romansh)")
        print("     Quality: Very High")
        print("     Size: 8B parameters (~16GB)")

    def benchmark(self, text="Hello, how are you?", src_lang="en", tgt_lang="de"):
        """Compare NLLB vs Apertus performance."""
        print("\n" + "=" * 60)
        print("🏁 ENGINE BENCHMARK")
        print("=" * 60)
        print(f"Text: {text}")
        print(f"Language pair: {src_lang} → {tgt_lang}")

        # Test NLLB
        print("\n⏱️  Testing NLLB-200...")
        result_nllb = self.translate(text, src_lang, tgt_lang, engine="nllb")

        # Test Apertus
        print("\n⏱️  Testing Apertus8B...")
        result_apertus = self.translate(text, src_lang, tgt_lang, engine="apertus")

        # Display results
        print("\n" + "=" * 60)
        print("📊 RESULTS")
        print("=" * 60)

        if "error" not in result_nllb:
            print(f"\n🔹 NLLB-200:")
            print(f"   Translation: {result_nllb.get('translation', 'N/A')}")
            print(f"   Time: {result_nllb.get('time', 'N/A')}")

        if "error" not in result_apertus:
            print(f"\n🔹 Apertus8B:")
            print(f"   Translation: {result_apertus.get('translation', 'N/A')}")
            print(f"   Time: {result_apertus.get('time', 'N/A')}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Unified TraductAL Translation Engine (NLLB-200 + Apertus8B)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-select engine
  %(prog)s de en "Guten Tag"

  # Force Apertus8B for Romansh
  %(prog)s de rm-sursilv "Guten Tag" --engine apertus

  # Use NLLB for common languages
  %(prog)s en fr "Hello" --engine nllb

  # List all supported languages
  %(prog)s --list-languages

  # Compare engines
  %(prog)s --benchmark
        """
    )

    parser.add_argument("src_lang", nargs="?", help="Source language (de, en, fr, rm-sursilv, etc.)")
    parser.add_argument("tgt_lang", nargs="?", help="Target language")
    parser.add_argument("text", nargs="?", help="Text to translate")
    parser.add_argument("--engine", choices=["nllb", "apertus"], help="Force specific engine")
    parser.add_argument("--model", help="Specific NLLB model (if using NLLB)")
    parser.add_argument("--list-languages", action="store_true", help="List supported languages")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--benchmark", action="store_true", help="Compare NLLB vs Apertus")
    parser.add_argument("--clean", action="store_true", help="Output only translation")

    args = parser.parse_args()

    # Initialize unified translator
    translator = UnifiedTranslator()

    # Handle list commands
    if args.list_languages:
        translator.list_languages()
        return

    if args.list_models:
        translator.list_models()
        return

    if args.benchmark:
        translator.benchmark()
        return

    # Check required arguments
    if not all([args.src_lang, args.tgt_lang, args.text]):
        parser.error("src_lang, tgt_lang, and text are required for translation")

    # Perform translation
    result = translator.translate(
        args.text,
        args.src_lang,
        args.tgt_lang,
        engine=args.engine,
        model_name=args.model
    )

    # Display results
    if args.clean:
        if "error" in result:
            print(result["error"])
        else:
            print(result.get("translation", ""))
    else:
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print("\n" + "=" * 60)
            print(f"🔤 Original ({result.get('src_lang', args.src_lang)}):")
            print(f"   {args.text}")
            print(f"\n🌍 Translation ({result.get('tgt_lang', args.tgt_lang)}):")
            print(f"   {result.get('translation', '')}")
            print(f"\n🤖 Engine: {result.get('engine', 'Unknown')}")
            print(f"📊 Model: {result.get('model', 'Unknown')}")
            print(f"⏱️  Time: {result.get('total_time', result.get('time', 'Unknown'))}")
            print("=" * 60)


if __name__ == "__main__":
    main()
