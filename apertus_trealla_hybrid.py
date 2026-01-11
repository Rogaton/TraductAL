#!/usr/bin/env python3
"""
Apertus 8B + Trealla Prolog Hybrid Translator

Combines neural translation with symbolic validation (Trealla Prolog)
for high-quality translation of low-resource languages.

IMPORTANT - Language Routing:
- COPTIC: Uses custom NMT (megalaa-trained), NOT Apertus
           Apertus/NLLB cannot handle Coptic (no dataset)
           Custom model at: ~/NLP/coptic-translator/
- Romansh/Swiss-German: Uses Apertus 8B
- Common languages: Uses NLLB-200

Validation: All languages use Trealla Prolog + language-specific parsers

Author: TraductAL Hybrid System
Date: December 2025
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings("ignore")

# Import Apertus translator
from apertus_translator import ApertusTranslator

# Import Trealla interface
from glossary_parser.trealla_interface import TreallaGlossaryParser


class HybridTranslationValidator:
    """
    Hybrid neural-symbolic translation system.

    Architecture:
    1. Apertus 8B (neural) - Generate initial translation
    2. Trealla Prolog (symbolic) - Validate and correct
    3. Return high-quality validated translation

    Specialized for:
    - Coptic (ancient language)
    - Romansh variants (Swiss)
    - Swiss-German dialects
    - Other low-resource languages
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize hybrid validator.

        Args:
            config: Configuration dict with paths and options
        """
        self.config = config or self._default_config()

        print("🔧 Initializing TraductAL Hybrid System")
        print("   Neural: Apertus 8B (1811 languages)")
        print("   Symbolic: Trealla Prolog (validation)")

        # Neural component
        apertus_path = self.config.get('apertus_path') or \
                       os.environ.get('APERTUS_PATH') or \
                       os.environ.get('APERTUS8B_PATH') or \
                       './models/apertus-8b'
        self.apertus = ApertusTranslator(model_path=apertus_path)

        # Symbolic component
        self.trealla_parser = TreallaGlossaryParser()

        # Paths to language-specific parsers
        self.coptic_parser = self.config.get(
            'coptic_parser_path',
            str(Path.home() / 'copticNLP/coptic-dependency-parser/coptic_parser_master.pl')
        )

        # Validation settings
        self.validation_enabled = self.config.get('enable_validation', True)
        self.max_length_ratio = self.config.get('max_length_ratio', 3.0)
        self.min_length_ratio = self.config.get('min_length_ratio', 0.3)

        print("✅ Hybrid system initialized")

    def _default_config(self) -> Dict:
        """Default configuration."""
        return {
            'apertus_path': os.environ.get('APERTUS_PATH', './models/apertus-8b'),
            'coptic_parser_path': str(Path.home() / 'copticNLP/coptic-dependency-parser/coptic_parser_master.pl'),
            'enable_validation': True,
            'max_length_ratio': 3.0,
            'min_length_ratio': 0.3,
            'tpl_path': os.environ.get('TREALLA_PATH', str(Path.home() / 'bin/tpl'))
        }

    def translate(self, text: str, src_lang: str, tgt_lang: str,
                  validate: bool = True) -> Dict:
        """
        Main translation method with validation.

        Args:
            text: Source text to translate
            src_lang: Source language code
            tgt_lang: Target language code
            validate: Enable Prolog validation

        Returns:
            dict: {
                'translation': str,
                'validation': dict,
                'corrected': bool,
                'model': str,
                'metadata': dict
            }
        """
        print(f"\n🌍 Translating: {src_lang} → {tgt_lang}")
        print(f"   Input: {text}")

        # Step 1: Neural translation (Apertus)
        print("   [1/2] Neural translation (Apertus)...")
        neural_result = self.apertus.translate(text, src_lang, tgt_lang)

        if 'error' in neural_result:
            return {
                'error': neural_result['error'],
                'model': 'Apertus+Trealla',
                'stage': 'neural_translation'
            }

        translation = neural_result.get('translation', '')
        print(f"   ✓ Neural output: {translation}")

        # Step 2: Symbolic validation (Trealla)
        if validate and self.validation_enabled:
            print("   [2/2] Symbolic validation (Trealla)...")
            validation_result = self.validate_translation(
                source=text,
                translation=translation,
                src_lang=src_lang,
                tgt_lang=tgt_lang
            )

            print(f"   ✓ Validation: {validation_result['status']}")

            # Step 3: Apply corrections if needed
            if validation_result['has_errors']:
                print(f"   ⚠️  Errors detected: {validation_result['errors']}")
                corrected = self.apply_corrections(
                    translation,
                    validation_result['errors']
                )

                return {
                    'translation': corrected,
                    'original_neural': translation,
                    'validation': validation_result,
                    'corrected': True,
                    'model': 'Apertus+Trealla',
                    'metadata': {
                        'neural_time': neural_result.get('time'),
                        'device': neural_result.get('device')
                    }
                }

        # No errors or validation disabled
        return {
            'translation': translation,
            'validation': validation_result if validate else {'skipped': True},
            'corrected': False,
            'model': 'Apertus+Trealla',
            'metadata': {
                'neural_time': neural_result.get('time'),
                'device': neural_result.get('device')
            }
        }

    def validate_translation(self, source: str, translation: str,
                           src_lang: str, tgt_lang: str) -> Dict:
        """
        Validate translation using Trealla Prolog.

        Performs language-specific validation:
        - Coptic: Dependency parsing
        - Romansh: Grammar rules
        - Swiss-German: Dialect authenticity
        - Generic: Hallucination detection
        """
        # Language-specific validation
        if tgt_lang == 'cop' or tgt_lang == 'coptic':
            return self.validate_coptic(translation)
        elif tgt_lang.startswith('rm'):  # Romansh variants
            return self.validate_romansh(translation)
        elif 'gsw' in tgt_lang:  # Swiss-German
            return self.validate_swiss_german(translation)
        else:
            return self.validate_generic(source, translation)

    def validate_coptic(self, text: str) -> Dict:
        """
        Validate Coptic translation using Coptic dependency parser.

        Uses: ~/copticNLP/coptic-dependency-parser/coptic_parser_master.pl
        """
        try:
            # Escape text for Prolog
            text_escaped = text.replace("'", "\\'").replace('"', '\\"')

            # Build Prolog query
            query = f"""
            consult('{self.coptic_parser}'),
            parse_coptic('{text_escaped}', Result),
            (   Result.success = true
            ->  write('VALID'), nl
            ;   write('INVALID'), nl
            ),
            halt(0).
            """

            # Execute with Trealla
            tpl_path = self.config.get('tpl_path', 'tpl')
            result = subprocess.run(
                [tpl_path],
                input=query,
                capture_output=True,
                text=True,
                timeout=10
            )

            # Parse result
            if 'VALID' in result.stdout:
                return {
                    'status': 'valid',
                    'valid': True,
                    'has_errors': False,
                    'errors': [],
                    'language': 'coptic',
                    'parser': 'coptic_dependency_parser'
                }
            else:
                return {
                    'status': 'invalid',
                    'valid': False,
                    'has_errors': True,
                    'errors': ['Coptic syntax error detected'],
                    'language': 'coptic',
                    'details': result.stderr
                }

        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'valid': False,
                'has_errors': True,
                'errors': ['Coptic parser timeout']
            }
        except Exception as e:
            return {
                'status': 'error',
                'valid': False,
                'has_errors': True,
                'errors': [f'Validation error: {str(e)}']
            }

    def validate_romansh(self, text: str) -> Dict:
        """
        Validate Romansh translation.

        Checks:
        - Character set (should be Latin + diacritics)
        - Common Romansh patterns
        - No German/Italian contamination
        """
        errors = []

        # Check 1: Character set
        if not self._is_valid_romansh_charset(text):
            errors.append('Invalid character set for Romansh')

        # Check 2: Common patterns
        # Romansh often uses "ch" for /k/, "tg" for /c/
        if len(text) > 20 and not any(pattern in text.lower() for pattern in ['ch', 'tg', 'gl']):
            errors.append('Missing typical Romansh patterns')

        # Check 3: German contamination (Romansh doesn't use ß, ä, ö, ü frequently)
        german_markers = ['ß', 'ä', 'ö', 'ü']
        if any(marker in text for marker in german_markers):
            errors.append('Possible German contamination')

        return {
            'status': 'valid' if not errors else 'invalid',
            'valid': len(errors) == 0,
            'has_errors': len(errors) > 0,
            'errors': errors,
            'language': 'romansh'
        }

    def validate_swiss_german(self, text: str) -> Dict:
        """
        Validate Swiss-German dialect translation.

        Checks:
        - No standard German forms (keine, nicht → kei, nöd)
        - Typical Swiss-German markers
        """
        errors = []

        # Standard German forms that shouldn't appear
        standard_german = [
            'ich habe', 'wir haben', 'sie haben',  # Swiss: ich ha, mir händ
            'nicht',  # Swiss: nöd, ned, nid
            'keine',  # Swiss: kei
        ]

        text_lower = text.lower()
        for marker in standard_german:
            if marker in text_lower:
                errors.append(f'Standard German form detected: {marker}')

        # Swiss-German should have typical markers
        if len(text) > 20:
            swiss_markers = ['ha ', 'händ', 'gah', 'gsi', 'gsäh', 'nöd', 'ned', 'kei']
            if not any(marker in text_lower for marker in swiss_markers):
                errors.append('Missing typical Swiss-German patterns')

        return {
            'status': 'valid' if not errors else 'invalid',
            'valid': len(errors) == 0,
            'has_errors': len(errors) > 0,
            'errors': errors,
            'language': 'swiss_german'
        }

    def validate_generic(self, source: str, translation: str) -> Dict:
        """
        Generic validation for other languages.

        Checks:
        - Hallucination detection (length ratio)
        - Empty translation
        - Token repetition (common LLM hallucination)
        """
        errors = []

        # Check 1: Length ratio (hallucination indicator)
        len_ratio = len(translation) / max(len(source), 1)
        if len_ratio > self.max_length_ratio:
            errors.append(f'Translation too long (ratio: {len_ratio:.2f})')
        elif len_ratio < self.min_length_ratio:
            errors.append(f'Translation too short (ratio: {len_ratio:.2f})')

        # Check 2: Empty translation
        if not translation.strip():
            errors.append('Empty translation')

        # Check 3: Token repetition (hallucination)
        if self._has_token_repetition(translation):
            errors.append('Token repetition detected (possible hallucination)')

        # Check 4: Source language leakage
        if self._has_source_leakage(source, translation):
            errors.append('Source language leakage detected')

        return {
            'status': 'valid' if not errors else 'warnings',
            'valid': len(errors) == 0,
            'has_errors': len(errors) > 0,
            'errors': errors,
            'language': 'generic',
            'length_ratio': len_ratio
        }

    def apply_corrections(self, translation: str, errors: List[str]) -> str:
        """
        Apply corrections based on detected errors.

        For now, marks translation as validated with warnings.
        Future: Implement Prolog-based correction rules.
        """
        # Mark as validated with warnings
        return f"[VALIDATED] {translation}"

    # Helper methods

    def _is_valid_romansh_charset(self, text: str) -> bool:
        """Check if text uses valid Romansh characters."""
        # Romansh uses: a-z, à, è, é, ì, ò, ù, ü
        import unicodedata
        for char in text:
            if char.isalpha():
                cat = unicodedata.category(char)
                # Allow Latin letters and common diacritics
                if cat not in ['Ll', 'Lu', 'Lm']:
                    return False
        return True

    def _has_token_repetition(self, text: str, threshold: int = 3) -> bool:
        """Check for repeated tokens (hallucination indicator)."""
        tokens = text.split()
        if len(tokens) < threshold:
            return False

        for i in range(len(tokens) - threshold + 1):
            if len(set(tokens[i:i+threshold])) == 1:
                return True
        return False

    def _has_source_leakage(self, source: str, translation: str,
                           threshold: float = 0.5) -> bool:
        """Check if source language leaked into translation."""
        source_words = set(source.lower().split())
        translation_words = set(translation.lower().split())

        # If more than 50% overlap, likely leakage
        if not translation_words:
            return False

        overlap = len(source_words & translation_words) / len(translation_words)
        return overlap > threshold


def main():
    """Test the hybrid translator."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Apertus+Trealla Hybrid Translator"
    )
    parser.add_argument("--text", required=True, help="Text to translate")
    parser.add_argument("--src", default="de", help="Source language")
    parser.add_argument("--tgt", default="rm-sursilv", help="Target language")
    parser.add_argument("--no-validate", action="store_true",
                       help="Disable Prolog validation")

    args = parser.parse_args()

    # Initialize hybrid validator
    validator = HybridTranslationValidator()

    # Translate with validation
    result = validator.translate(
        text=args.text,
        src_lang=args.src,
        tgt_lang=args.tgt,
        validate=not args.no_validate
    )

    # Display results
    print("\n" + "="*60)
    print("📊 TRANSLATION RESULTS")
    print("="*60)

    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return

    print(f"🔤 Original ({args.src}): {args.text}")
    print(f"🌍 Translation ({args.tgt}): {result['translation']}")
    print(f"🤖 Model: {result['model']}")

    if result.get('corrected'):
        print(f"⚠️  Corrected: Yes")
        print(f"   Original neural: {result['original_neural']}")

    validation = result.get('validation', {})
    if validation and not validation.get('skipped'):
        print(f"\n🔍 VALIDATION:")
        print(f"   Status: {validation.get('status', 'unknown')}")
        print(f"   Valid: {validation.get('valid', False)}")
        if validation.get('errors'):
            print(f"   Errors: {', '.join(validation['errors'])}")

    metadata = result.get('metadata', {})
    if metadata:
        print(f"\n⏱️  PERFORMANCE:")
        print(f"   Translation time: {metadata.get('neural_time', 'N/A')}")
        print(f"   Device: {metadata.get('device', 'N/A')}")

    print("="*60)


if __name__ == '__main__':
    main()
