#!/usr/bin/env python3
"""
Test script to verify the expanded language lists in gradio_app.py
"""

import sys
import os
from pathlib import Path

# Import the language dictionaries
try:
    # Add parent directory to path if running as script
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    sys.path.insert(0, str(project_root))

    from gradio_app import (
        NLLB_LANGUAGES,
        APERTUS_LANGUAGES,
        ROMANSH_VARIANTS,
        COMMON_LANGUAGES,
        TTS_LANGUAGES,
        ALL_LANGUAGES,
        STT_LANGUAGES
    )
    print("✅ Successfully imported language dictionaries from gradio_app.py")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("LANGUAGE EXPANSION TEST RESULTS")
print("="*70)

# Test 1: Count languages
print("\n📊 LANGUAGE COUNTS:")
print(f"  NLLB_LANGUAGES: {len(NLLB_LANGUAGES)} languages")
print(f"  APERTUS_LANGUAGES: {len(APERTUS_LANGUAGES)} languages")
print(f"  ALL_LANGUAGES (combined): {len(ALL_LANGUAGES)} languages")
print(f"  TTS_LANGUAGES: {len(TTS_LANGUAGES)} languages")
print(f"  STT_LANGUAGES: {len(STT_LANGUAGES)} languages")
print(f"  ROMANSH_VARIANTS: {len(ROMANSH_VARIANTS)} languages")

# Test 2: Verify minimum requirements
print("\n✓ VERIFICATION:")
MIN_NLLB = 50
if len(NLLB_LANGUAGES) >= MIN_NLLB:
    print(f"  ✅ NLLB has {len(NLLB_LANGUAGES)} languages (target: {MIN_NLLB}+)")
else:
    print(f"  ❌ NLLB has only {len(NLLB_LANGUAGES)} languages (target: {MIN_NLLB}+)")

if len(APERTUS_LANGUAGES) >= 6:
    print(f"  ✅ Apertus has {len(APERTUS_LANGUAGES)} languages (6 Romansh + extras)")
else:
    print(f"  ⚠️  Apertus has only {len(APERTUS_LANGUAGES)} languages")

if len(ROMANSH_VARIANTS) == 6:
    print(f"  ✅ Romansh variants: {len(ROMANSH_VARIANTS)} (correct)")
else:
    print(f"  ⚠️  Romansh variants: {len(ROMANSH_VARIANTS)} (expected 6)")

# Test 3: Check backward compatibility
print("\n🔄 BACKWARD COMPATIBILITY:")
if COMMON_LANGUAGES == NLLB_LANGUAGES:
    print("  ✅ COMMON_LANGUAGES = NLLB_LANGUAGES (backward compatible)")
else:
    print("  ❌ COMMON_LANGUAGES ≠ NLLB_LANGUAGES")

# Test 4: Verify no duplicates
print("\n🔍 DUPLICATE CHECK:")
nllb_codes = set(NLLB_LANGUAGES.values())
apertus_codes = set(APERTUS_LANGUAGES.values())
overlap = nllb_codes & apertus_codes

if overlap:
    print(f"  ⚠️  Found {len(overlap)} overlapping codes: {overlap}")
else:
    print("  ✅ No duplicate language codes between NLLB and Apertus")

# Test 5: Sample languages from each category
print("\n📝 SAMPLE LANGUAGES:")
print("\n  NLLB - Core European:")
for lang in ["German", "English", "French", "Italian", "Spanish"]:
    if lang in NLLB_LANGUAGES:
        print(f"    ✅ {lang}: {NLLB_LANGUAGES[lang]}")

print("\n  NLLB - Asian:")
for lang in ["Chinese", "Japanese", "Korean", "Hindi", "Vietnamese"]:
    if lang in NLLB_LANGUAGES:
        print(f"    ✅ {lang}: {NLLB_LANGUAGES[lang]}")

print("\n  NLLB - Slavic:")
for lang in ["Russian", "Polish", "Czech", "Ukrainian"]:
    if lang in NLLB_LANGUAGES:
        print(f"    ✅ {lang}: {NLLB_LANGUAGES[lang]}")

print("\n  Apertus - Romansh:")
for lang in ROMANSH_VARIANTS:
    print(f"    ✅ {lang}: {ROMANSH_VARIANTS[lang]}")

print("\n  Apertus - Low-Resource:")
for lang in ["Occitan", "Breton", "Welsh", "Irish"]:
    if lang in APERTUS_LANGUAGES:
        print(f"    ✅ {lang}: {APERTUS_LANGUAGES[lang]}")

# Test 6: TTS support verification
print("\n🔊 TTS LANGUAGE CHECK:")
print(f"  Total TTS-supported languages: {len(TTS_LANGUAGES)}")
for lang in ["English", "German", "French", "Spanish", "Russian", "Hindi", "Arabic"]:
    if lang in TTS_LANGUAGES:
        print(f"    ✅ {lang}: {TTS_LANGUAGES[lang]}")

# Test 7: List all NLLB languages (sorted)
print("\n📋 ALL NLLB LANGUAGES (sorted):")
for i, (name, code) in enumerate(sorted(NLLB_LANGUAGES.items()), 1):
    print(f"  {i:2d}. {name:20s} ({code})")

# Test 8: List all Apertus languages (sorted)
print("\n📋 ALL APERTUS LANGUAGES (sorted):")
for i, (name, code) in enumerate(sorted(APERTUS_LANGUAGES.items()), 1):
    print(f"  {i:2d}. {name:20s} ({code})")

print("\n" + "="*70)
print("✅ LANGUAGE EXPANSION TEST COMPLETE")
print("="*70)
