#!/usr/bin/env python3
"""
Swiss French Synthetic Data Generator

Uses Apertus8B to generate synthetic Swiss French translations.
Requires quality filtering and human validation afterward.
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from apertus_translator import ApertusTranslator
    APERTUS_AVAILABLE = True
except ImportError:
    APERTUS_AVAILABLE = False
    print("⚠️  Warning: apertus_translator not available")


class SwissFrenchSyntheticGenerator:
    """Generate synthetic Swiss French data using Apertus8B."""

    # Example dialectal features for prompting
    DIALECTAL_FEATURES = {
        "valais": {
            "vocabulary": [
                "panosse (mop)", "linge (towel)", "se refroidir (catch cold)",
                "faire le réduit (clean)", "cornet (plastic bag)", "se pouiller (hurry)"
            ],
            "numbers": "septante (70), huitante (80), nonante (90)",
            "meals": "déjeuner=breakfast, dîner=lunch, souper=dinner"
        },
        "geneva": {
            "vocabulary": [
                "ça joue (how are you)", "il drache (raining hard)", "ribouis (mess)",
                "poutzer (clean)", "carnotzet (wine cellar)", "crousille (money)"
            ],
            "expressions": "très familier et urbain (very colloquial and urban)"
        },
        "fribourg": {
            "vocabulary": [
                "bolze (candy)", "cheni (mess)", "gouille (puddle)",
                "poutser (clean)", "bredzon (apron)", "bouébé (baby)"
            ],
            "influence": "influence germanique notable (notable German influence)"
        }
    }

    # Standard French sentences for translation
    STANDARD_SENTENCES = [
        "Bonjour, comment allez-vous aujourd'hui?",
        "Je vais bien, merci beaucoup",
        "Il fait très beau aujourd'hui",
        "Il pleut beaucoup dehors",
        "Voulez-vous boire un café?",
        "Je dois aller faire les courses",
        "Pouvez-vous m'aider s'il vous plaît?",
        "Quelle heure est-il maintenant?",
        "Je suis très fatigué ce soir",
        "Nous allons dîner au restaurant",
        "Il faut nettoyer la maison",
        "Les enfants jouent dans le jardin",
        "J'ai attrapé un rhume",
        "C'est combien pour ce produit?",
        "Je ne comprends pas très bien",
        "Il faut se dépêcher maintenant",
        "Où sont les toilettes s'il vous plaît?",
        "Je vais prendre le petit-déjeuner",
        "Il y a quatre-vingt-dix personnes",
        "Passe-moi la serpillière",
        "Donne-moi un sac plastique",
        "C'est un grand désordre ici",
        "J'ai faim, quand mangeons-nous?",
        "Il fait très froid dehors",
        "Attention à la flaque d'eau!",
        "Les enfants mangent des bonbons",
        "Je vais nettoyer la cuisine",
        "Bonne journée à vous!",
        "Au revoir et à bientôt",
        "Merci pour votre aide"
    ]

    def __init__(self, output_dir: str = "./datasets/swiss_french"):
        """Initialize generator."""
        self.output_dir = Path(output_dir)
        self.translator = None

        if APERTUS_AVAILABLE:
            try:
                print("🤖 Loading Apertus8B translator...")
                self.translator = ApertusTranslator()
                print("✅ Apertus8B loaded successfully")
            except Exception as e:
                print(f"⚠️  Could not load Apertus8B: {e}")

    def create_translation_prompt(self, text: str, dialect: str, context: str = "") -> str:
        """Create a detailed prompt for Apertus8B."""
        features = self.DIALECTAL_FEATURES.get(dialect, {})

        prompt = f"""Translate the following standard French sentence into Swiss French ({dialect.capitalize()} dialect).

Use authentic Swiss French dialectal features:
"""

        if features.get("vocabulary"):
            prompt += f"\nDialectal vocabulary: {', '.join(features['vocabulary'])}"

        if features.get("numbers"):
            prompt += f"\nNumbers: {features['numbers']}"

        if features.get("meals"):
            prompt += f"\nMeal terms: {features['meals']}"

        if features.get("expressions"):
            prompt += f"\nStyle: {features['expressions']}"

        if context:
            prompt += f"\nContext: {context}"

        prompt += f"\n\nStandard French: {text}\n\nSwiss French ({dialect.capitalize()}):"

        return prompt

    def generate_synthetic_translation(self, text: str, dialect: str,
                                     context: str = "") -> Optional[str]:
        """Generate a single synthetic translation."""
        if not self.translator:
            print("❌ Apertus8B translator not available")
            return None

        try:
            prompt = self.create_translation_prompt(text, dialect, context)

            result = self.translator.translate(
                text=prompt,
                src_lang="fr",
                tgt_lang="fr",  # Same language, different dialect
                max_tokens=256
            )

            translation = result.get("translation", "").strip()

            # Clean up common artifacts
            if translation.startswith(text):
                translation = translation[len(text):].strip()

            return translation

        except Exception as e:
            print(f"❌ Error generating translation: {e}")
            return None

    def generate_batch(self, dialect: str, num_sentences: int = 30,
                      custom_sentences: Optional[List[str]] = None) -> List[Dict]:
        """Generate a batch of synthetic translations."""
        print(f"\n🔄 Generating synthetic translations for {dialect}...")
        print(f"   Target: {num_sentences} sentences")

        sentences = custom_sentences if custom_sentences else self.STANDARD_SENTENCES[:num_sentences]
        results = []

        for i, sentence in enumerate(sentences, 1):
            print(f"   [{i}/{len(sentences)}] Translating: {sentence[:50]}...")

            translation = self.generate_synthetic_translation(sentence, dialect)

            if translation:
                results.append({
                    "Prompt": f"Translate to Swiss French ({dialect.capitalize()}): {sentence}",
                    "Answer": translation,
                    "metadata": {
                        "generated_at": datetime.now().isoformat(),
                        "method": "apertus8b_synthetic",
                        "needs_validation": True
                    }
                })
                print(f"      ✅ {translation[:60]}...")
            else:
                print(f"      ❌ Failed")

        print(f"\n✅ Generated {len(results)} translations")
        return results

    def save_synthetic_data(self, data: List[Dict], dialect: str,
                          quality_filtered: bool = False):
        """Save synthetic translations to JSONL."""
        subdir = "Synthetic_Translation" if quality_filtered else "Validation"
        filename = f"sft_{dialect}_{'quality_filtered' if quality_filtered else 'unvalidated'}.jsonl"

        output_path = self.output_dir / subdir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Append mode
        mode = "a" if output_path.exists() else "w"

        with open(output_path, mode, encoding="utf-8") as f:
            for entry in data:
                # Remove metadata before saving
                clean_entry = {
                    "Prompt": entry["Prompt"],
                    "Answer": entry["Answer"]
                }
                f.write(json.dumps(clean_entry, ensure_ascii=False) + "\n")

        print(f"📁 Saved to: {output_path}")
        return output_path

    def create_validation_json(self, data: List[Dict], dialect: str):
        """Create JSON file for human validation."""
        output_path = self.output_dir / "Validation" / f"synthetic_{dialect}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        validation_data = {
            "dialect": dialect,
            "generated_at": datetime.now().isoformat(),
            "total_examples": len(data),
            "validated_count": 0,
            "examples": [
                {
                    "id": i,
                    "standard_french": entry["Prompt"].split(": ")[-1],
                    "swiss_french_generated": entry["Answer"],
                    "swiss_french_corrected": "",
                    "quality_score": 0,  # 1-5 scale
                    "notes": "",
                    "approved": False
                }
                for i, entry in enumerate(data, 1)
            ]
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(validation_data, f, ensure_ascii=False, indent=2)

        print(f"📋 Created validation file: {output_path}")
        print(f"\n📝 Validation instructions:")
        print(f"   1. Open {output_path}")
        print(f"   2. For each example:")
        print(f"      - Review 'swiss_french_generated'")
        print(f"      - Correct in 'swiss_french_corrected' if needed")
        print(f"      - Rate quality 1-5 in 'quality_score'")
        print(f"      - Set 'approved': true if acceptable")
        print(f"   3. Run: generator.import_validated_json('{output_path}')")

        return output_path

    def import_validated_json(self, json_path: str):
        """Import validated synthetic data."""
        print(f"\n📥 Importing validated synthetic data...")

        if not Path(json_path).exists():
            print(f"❌ File not found: {json_path}")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        dialect = data.get("dialect", "unknown")
        approved_entries = []

        for example in data.get("examples", []):
            if not example.get("approved", False):
                continue

            # Use corrected version if provided, otherwise use generated
            swiss_french = example.get("swiss_french_corrected", "").strip()
            if not swiss_french:
                swiss_french = example.get("swiss_french_generated", "").strip()

            standard_french = example.get("standard_french", "").strip()

            if swiss_french and standard_french:
                approved_entries.append({
                    "Prompt": f"Translate to Swiss French ({dialect.capitalize()}): {standard_french}",
                    "Answer": swiss_french
                })

        if approved_entries:
            self.save_synthetic_data(approved_entries, dialect, quality_filtered=True)
            print(f"✅ Imported {len(approved_entries)} validated translations")
        else:
            print("⚠️  No approved entries found")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Swiss French Synthetic Data Generator using Apertus8B",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 30 translations for Valais dialect
  %(prog)s --dialect valais --generate 30

  # Generate with custom input file
  %(prog)s --dialect geneva --input my_sentences.txt --generate 50

  # Create validation file
  %(prog)s --dialect fribourg --generate 20 --validation

  # Import validated data
  %(prog)s --import-validated validation_file.json

Note: Requires Apertus8B to be installed and available.
        """
    )

    parser.add_argument("--output-dir", default="./datasets/swiss_french",
                       help="Output directory (default: ./datasets/swiss_french)")
    parser.add_argument("--dialect", choices=["valais", "geneva", "fribourg"],
                       help="Target dialect")
    parser.add_argument("--generate", type=int, metavar="N",
                       help="Generate N synthetic translations")
    parser.add_argument("--input", type=str,
                       help="Input file with standard French sentences (one per line)")
    parser.add_argument("--validation", action="store_true",
                       help="Create validation JSON file")
    parser.add_argument("--import-validated", type=str,
                       help="Import validated JSON file")

    args = parser.parse_args()

    if not APERTUS_AVAILABLE and not args.import_validated:
        print("❌ Error: apertus_translator not available")
        print("Make sure Apertus8B is installed and accessible")
        sys.exit(1)

    generator = SwissFrenchSyntheticGenerator(args.output_dir)

    # Import validated data
    if args.import_validated:
        generator.import_validated_json(args.import_validated)
        return

    # Generate synthetic data
    if args.generate and args.dialect:
        # Load custom sentences if provided
        custom_sentences = None
        if args.input:
            input_path = Path(args.input)
            if input_path.exists():
                with open(input_path, "r", encoding="utf-8") as f:
                    custom_sentences = [line.strip() for line in f if line.strip()]
                print(f"📥 Loaded {len(custom_sentences)} sentences from {args.input}")

        # Generate translations
        results = generator.generate_batch(
            args.dialect,
            args.generate,
            custom_sentences
        )

        if results:
            if args.validation:
                # Create validation file
                generator.create_validation_json(results, args.dialect)
            else:
                # Save directly (unvalidated)
                generator.save_synthetic_data(results, args.dialect, quality_filtered=False)

            print(f"\n✅ Generation complete!")
            print(f"   Generated: {len(results)} translations")
            if args.validation:
                print(f"   Next step: Validate the JSON file and import")
            else:
                print(f"   ⚠️  Warning: Data saved without validation!")
                print(f"   Consider human review before training")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
