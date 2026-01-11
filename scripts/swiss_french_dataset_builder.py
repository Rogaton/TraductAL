#!/usr/bin/env python3
"""
Swiss French Dialect Dataset Builder

Creates datasets for Swiss French dialects following the Romansh dataset structure.
Includes tools for:
- Directory setup
- Dictionary import
- Synthetic data generation
- Human validation workflow
- JSONL export in HuggingFace format
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import argparse


class SwissFrenchDatasetBuilder:
    """Build Swiss French dialect datasets from scratch."""

    # Swiss French dialect definitions
    DIALECTS = {
        "valais": "Valais",
        "geneva": "Geneva",
        "fribourg": "Fribourg",
        "vaud": "Vaud",
        "neuchatel": "Neuchâtel",
        "jura": "Jura"
    }

    # Common Swiss French expressions (starter vocabulary)
    STARTER_VOCABULARY = {
        "valais": {
            "panosse": "serpillière (mop)",
            "linge": "serviette (towel)",
            "se refroidir": "attraper froid (catch a cold)",
            "faire le réduit": "faire le ménage (clean)",
            "ça joue": "ça va (how are you)",
            "déjeuner": "petit-déjeuner (breakfast)",
            "dîner": "déjeuner (lunch)",
            "souper": "dîner (dinner)",
            "nonante": "quatre-vingt-dix (90)",
            "huitante": "quatre-vingts (80)",
            "septante": "soixante-dix (70)",
            "une fois": "donc, alors (so, then)",
            "tout de bon": "vraiment (really)",
            "se pouiller": "se dépêcher (hurry up)",
            "cornet": "sac plastique (plastic bag)"
        },
        "geneva": {
            "ça joue?": "ça va? (how are you?)",
            "il drache": "il pleut fort (it's raining hard)",
            "ribouis": "débris, désordre (mess)",
            "poutzer": "nettoyer (clean)",
            "carnotzet": "cave aménagée (wine cellar room)",
            "s'encoubler": "trébucher (stumble)",
            "crousille": "argent (money)",
            "pive": "pomme de pin (pine cone)",
            "bobet": "niais, idiot (fool)",
            "se thuser": "se taire (shut up)"
        },
        "fribourg": {
            "bolze": "bonbon (candy)",
            "bricelets": "gaufres fines (thin waffles)",
            "bredzon": "tablier (apron)",
            "cheni": "désordre (mess)",
            "gouille": "flaque (puddle)",
            "mouttre": "montre (watch)",
            "poutser": "nettoyer (clean)",
            "bouébé": "bébé (baby)"
        }
    }

    def __init__(self, base_dir: str = "./datasets/swiss_french"):
        """Initialize dataset builder."""
        self.base_dir = Path(base_dir)
        self.stats = {
            "dictionary_entries": 0,
            "sentence_pairs": 0,
            "idioms": 0,
            "human_translations": 0,
            "synthetic_translations": 0
        }

    def setup_structure(self):
        """Create directory structure mirroring Romansh dataset."""
        print("🏗️  Setting up Swiss French dataset structure...")

        subdirs = [
            "Dictionary",
            "Human_Translations",
            "Idiom_identification",
            "Synthetic_Translation",
            "Raw_Data",  # For collecting unprocessed data
            "Validation"  # For human validation workflow
        ]

        for subdir in subdirs:
            path = self.base_dir / subdir
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {path}")

        # Create README
        readme_path = self.base_dir / "README.md"
        with open(readme_path, "w") as f:
            f.write(self._generate_readme())
        print(f"  ✅ Created: {readme_path}")

        print(f"\n✅ Dataset structure ready at: {self.base_dir.absolute()}")

    def _generate_readme(self) -> str:
        """Generate README for dataset."""
        return f"""# Swiss French Dialect Dataset

**Created**: {datetime.now().strftime("%Y-%m-%d")}
**Format**: JSONL (JSON Lines) for HuggingFace datasets
**Purpose**: Fine-tuning Apertus8B for Swiss French dialect support

## Structure

```
swiss_french/
├── Dictionary/              # Dictionary entries (term → translation)
│   ├── sft_dictionary_valais.jsonl
│   ├── sft_dictionary_geneva.jsonl
│   └── sft_dictionary_fribourg.jsonl
├── Human_Translations/      # Human-validated translations
│   └── SFT_Human.jsonl
├── Idiom_identification/    # Idioms and dialect identification
│   └── sft_idiom_identification.jsonl
├── Synthetic_Translation/   # AI-generated, quality-filtered
│   ├── sft_valais_quality_filtered.jsonl
│   ├── sft_geneva_quality_filtered.jsonl
│   └── sft_fribourg_quality_filtered.jsonl
├── Raw_Data/               # Unprocessed source material
└── Validation/             # Files pending human validation
```

## Data Format

Each JSONL file contains entries with:
- `Prompt`: Instruction or source text
- `Answer`: Expected response or translation

Example:
```json
{{"Prompt": "Translate to Swiss French (Valais): Je vais faire le ménage", "Answer": "Je vais faire le réduit"}}
{{"Prompt": "What does 'panosse' mean?", "Answer": "Panosse is Swiss French for serpillière (mop)"}}
```

## Dialects Covered

- Valais French (Valais/Wallis)
- Geneva French (Genève)
- Fribourg French (Fribourg)
- Vaud French (optional)
- Neuchâtel French (optional)
- Jura French (optional)

## Usage

1. Collect data using `swiss_french_dataset_builder.py`
2. Validate translations manually
3. Export to HuggingFace format
4. Fine-tune Apertus8B on the dataset

## Statistics

- Dictionary entries: {self.stats['dictionary_entries']}
- Sentence pairs: {self.stats['sentence_pairs']}
- Idioms: {self.stats['idioms']}
- Total examples: {sum(self.stats.values())}

## License

TBD - Ensure compliance with source material licenses
"""

    def create_starter_dictionary(self, dialect: str = "valais"):
        """Create starter dictionary from predefined vocabulary."""
        if dialect not in self.DIALECTS:
            print(f"❌ Unknown dialect: {dialect}")
            return

        print(f"\n📚 Creating starter dictionary for {self.DIALECTS[dialect]}...")

        vocab = self.STARTER_VOCABULARY.get(dialect, {})
        if not vocab:
            print(f"⚠️  No starter vocabulary for {dialect}")
            return

        entries = []
        for swiss_term, french_translation in vocab.items():
            # Create multiple training formats
            entries.extend([
                {
                    "Prompt": f"Translate to standard French: {swiss_term}",
                    "Answer": french_translation.split("(")[1].rstrip(")")
                },
                {
                    "Prompt": f"What does '{swiss_term}' mean in Swiss French ({self.DIALECTS[dialect]})?",
                    "Answer": f"'{swiss_term}' is Swiss French for {french_translation}"
                },
                {
                    "Prompt": f"How do you say '{french_translation.split('(')[1].rstrip(')')}' in Swiss French ({self.DIALECTS[dialect]})?",
                    "Answer": swiss_term
                }
            ])

        # Save to JSONL
        output_path = self.base_dir / "Dictionary" / f"sft_dictionary_{dialect}.jsonl"
        with open(output_path, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.stats["dictionary_entries"] += len(entries)
        print(f"  ✅ Created {len(entries)} dictionary entries")
        print(f"  📁 Saved to: {output_path}")

    def import_csv_dictionary(self, csv_path: str, dialect: str,
                             swiss_col: str = "swiss_french",
                             standard_col: str = "standard_french"):
        """Import dictionary from CSV file."""
        print(f"\n📥 Importing dictionary from CSV: {csv_path}")

        if not Path(csv_path).exists():
            print(f"❌ File not found: {csv_path}")
            return

        entries = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                swiss_term = row.get(swiss_col, "").strip()
                standard_term = row.get(standard_col, "").strip()

                if not swiss_term or not standard_term:
                    continue

                entries.append({
                    "Prompt": f"Translate to Swiss French ({self.DIALECTS.get(dialect, dialect)}): {standard_term}",
                    "Answer": swiss_term
                })
                entries.append({
                    "Prompt": f"Translate to standard French: {swiss_term}",
                    "Answer": standard_term
                })

        output_path = self.base_dir / "Dictionary" / f"sft_dictionary_{dialect}.jsonl"

        # Append or create
        mode = "a" if output_path.exists() else "w"
        with open(output_path, mode, encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.stats["dictionary_entries"] += len(entries)
        print(f"  ✅ Imported {len(entries)} entries")
        print(f"  📁 Saved to: {output_path}")

    def create_idiom_identification_examples(self, dialect: str = "valais"):
        """Create idiom and dialect identification examples."""
        print(f"\n🗣️  Creating idiom identification examples for {self.DIALECTS[dialect]}...")

        examples = []
        vocab = self.STARTER_VOCABULARY.get(dialect, {})

        for swiss_term, french_translation in vocab.items():
            examples.extend([
                {
                    "Prompt": f"What dialect is this expression from? '{swiss_term}'",
                    "Answer": f"Swiss French ({self.DIALECTS[dialect]})"
                },
                {
                    "Prompt": f"Identify the language variety: '{swiss_term}'",
                    "Answer": f"This is {self.DIALECTS[dialect]} Swiss French dialect"
                }
            ])

        output_path = self.base_dir / "Idiom_identification" / "sft_idiom_identification.jsonl"
        mode = "a" if output_path.exists() else "w"

        with open(output_path, mode, encoding="utf-8") as f:
            for entry in examples:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.stats["idioms"] += len(examples)
        print(f"  ✅ Created {len(examples)} idiom identification examples")
        print(f"  📁 Saved to: {output_path}")

    def create_sentence_templates(self, dialect: str = "valais"):
        """Create sentence-level translation templates."""
        print(f"\n📝 Creating sentence templates for {self.DIALECTS[dialect]}...")

        # Common sentence templates using Swiss French terms
        vocab = self.STARTER_VOCABULARY.get(dialect, {})
        templates = []

        if dialect == "valais":
            templates = [
                ("Je vais faire le réduit", "Je vais faire le ménage"),
                ("Passe-moi la panosse", "Passe-moi la serpillière"),
                ("J'ai attrapé froid, je me suis refroidi", "J'ai attrapé froid"),
                ("On va déjeuner à quelle heure?", "On va prendre le petit-déjeuner à quelle heure?"),
                ("On dîne à midi", "On déjeune à midi"),
                ("Le souper est prêt", "Le dîner est prêt"),
                ("Il y a nonante personnes", "Il y a quatre-vingt-dix personnes"),
                ("J'ai huitante ans", "J'ai quatre-vingts ans"),
                ("Ça fait septante francs", "Ça fait soixante-dix francs"),
                ("Il faut se pouiller!", "Il faut se dépêcher!"),
                ("Donne-moi un cornet", "Donne-moi un sac plastique")
            ]
        elif dialect == "geneva":
            templates = [
                ("Ça joue?", "Ça va?"),
                ("Il drache dehors", "Il pleut très fort dehors"),
                ("C'est le ribouis ici", "C'est le désordre ici"),
                ("Je vais poutzer la maison", "Je vais nettoyer la maison"),
                ("On se retrouve au carnotzet", "On se retrouve à la cave"),
                ("Il s'est encoublé", "Il a trébuché"),
                ("J'ai plus de crousille", "Je n'ai plus d'argent")
            ]
        elif dialect == "fribourg":
            templates = [
                ("Les enfants mangent des bolzes", "Les enfants mangent des bonbons"),
                ("Quel cheni dans ta chambre!", "Quel désordre dans ta chambre!"),
                ("Attention à la gouille!", "Attention à la flaque!"),
                ("Je vais poutser la cuisine", "Je vais nettoyer la cuisine")
            ]

        entries = []
        for swiss, standard in templates:
            entries.append({
                "Prompt": f"Translate to Swiss French ({self.DIALECTS[dialect]}): {standard}",
                "Answer": swiss
            })
            entries.append({
                "Prompt": f"Translate to standard French: {swiss}",
                "Answer": standard
            })

        output_path = self.base_dir / "Synthetic_Translation" / f"sft_{dialect}_sentences.jsonl"
        with open(output_path, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.stats["sentence_pairs"] += len(entries)
        print(f"  ✅ Created {len(entries)} sentence pairs")
        print(f"  📁 Saved to: {output_path}")

    def create_validation_template(self, dialect: str = "valais", num_samples: int = 50):
        """Create CSV template for human validation."""
        print(f"\n✅ Creating validation template for {self.DIALECTS[dialect]}...")

        # Sample French sentences for translation
        sample_sentences = [
            "Bonjour, comment allez-vous?",
            "Je vais bien, merci",
            "Quel temps fait-il aujourd'hui?",
            "Il fait beau",
            "Il pleut",
            "Voulez-vous un café?",
            "J'ai faim",
            "Quelle heure est-il?",
            "Je dois partir maintenant",
            "À bientôt",
            "Merci beaucoup",
            "De rien",
            "Excusez-moi",
            "Je ne comprends pas",
            "Pouvez-vous répéter?",
            "C'est combien?",
            "Où sont les toilettes?",
            "Je suis fatigué",
            "Bonne journée",
            "Au revoir"
        ]

        output_path = self.base_dir / "Validation" / f"validation_template_{dialect}.csv"

        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "standard_french", f"swiss_french_{dialect}", "notes", "validated"])

            for i, sentence in enumerate(sample_sentences[:num_samples], 1):
                writer.writerow([i, sentence, "", "", "no"])

        print(f"  ✅ Created validation template with {num_samples} sentences")
        print(f"  📁 Saved to: {output_path}")
        print(f"\n📝 Instructions:")
        print(f"  1. Open {output_path} in Excel/LibreOffice")
        print(f"  2. Fill in the 'swiss_french_{dialect}' column")
        print(f"  3. Add notes if needed")
        print(f"  4. Mark 'validated' as 'yes' when done")
        print(f"  5. Run: builder.import_validated_csv('{output_path}', '{dialect}')")

    def import_validated_csv(self, csv_path: str, dialect: str):
        """Import validated translations from CSV."""
        print(f"\n📥 Importing validated translations from: {csv_path}")

        if not Path(csv_path).exists():
            print(f"❌ File not found: {csv_path}")
            return

        entries = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("validated", "").lower() != "yes":
                    continue

                standard = row.get("standard_french", "").strip()
                swiss = row.get(f"swiss_french_{dialect}", "").strip()

                if not standard or not swiss:
                    continue

                entries.append({
                    "Prompt": f"Translate to Swiss French ({self.DIALECTS.get(dialect, dialect)}): {standard}",
                    "Answer": swiss
                })
                entries.append({
                    "Prompt": f"Translate to standard French: {swiss}",
                    "Answer": standard
                })

        output_path = self.base_dir / "Human_Translations" / "SFT_Human.jsonl"
        mode = "a" if output_path.exists() else "w"

        with open(output_path, mode, encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.stats["human_translations"] += len(entries)
        print(f"  ✅ Imported {len(entries)} validated translations")
        print(f"  📁 Saved to: {output_path}")

    def generate_statistics(self):
        """Generate dataset statistics."""
        print("\n" + "="*60)
        print("📊 DATASET STATISTICS")
        print("="*60)

        total = 0
        for category in ["Dictionary", "Human_Translations", "Idiom_identification", "Synthetic_Translation"]:
            category_path = self.base_dir / category
            if not category_path.exists():
                continue

            count = 0
            for jsonl_file in category_path.glob("*.jsonl"):
                with open(jsonl_file, "r", encoding="utf-8") as f:
                    file_count = sum(1 for _ in f)
                    count += file_count
                    print(f"  {jsonl_file.name}: {file_count:,} examples")

            if count > 0:
                print(f"  {category} total: {count:,}")
                total += count

        print(f"\n✅ Total examples: {total:,}")
        print(f"📁 Location: {self.base_dir.absolute()}")

        # Compare to Romansh target
        romansh_target = 46092
        percentage = (total / romansh_target) * 100 if total > 0 else 0
        print(f"\n📈 Progress vs. Romansh dataset ({romansh_target:,} examples):")
        print(f"  Current: {percentage:.1f}%")

        if total < 5000:
            print(f"  🎯 Next milestone: 5,000 examples (dictionary focus)")
        elif total < 20000:
            print(f"  🎯 Next milestone: 20,000 examples (MVP dataset)")
        elif total < 46000:
            print(f"  🎯 Next milestone: 46,000 examples (match Romansh)")
        else:
            print(f"  🎉 Dataset size exceeds Romansh baseline!")

        return total

    def export_to_huggingface(self, output_dir: Optional[str] = None):
        """Export dataset in HuggingFace format."""
        if output_dir is None:
            output_dir = self.base_dir / "huggingface_export"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n📦 Exporting to HuggingFace format...")
        print(f"  Output: {output_dir}")

        # Combine all JSONL files
        all_data = []
        for category in ["Dictionary", "Human_Translations", "Idiom_identification", "Synthetic_Translation"]:
            category_path = self.base_dir / category
            if not category_path.exists():
                continue

            for jsonl_file in category_path.glob("*.jsonl"):
                with open(jsonl_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            all_data.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue

        # Save combined dataset
        combined_path = output_dir / "train.jsonl"
        with open(combined_path, "w", encoding="utf-8") as f:
            for entry in all_data:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print(f"  ✅ Exported {len(all_data):,} examples to {combined_path}")

        # Create dataset_dict.json
        dataset_dict = {"splits": ["train"]}
        with open(output_dir / "dataset_dict.json", "w") as f:
            json.dump(dataset_dict, f, indent=2)

        print(f"  ✅ Created dataset_dict.json")
        print(f"\n📝 Next steps:")
        print(f"  1. Upload to HuggingFace: huggingface-cli upload <your-username>/swiss-french-dialects {output_dir}")
        print(f"  2. Or load locally: from datasets import load_dataset; dataset = load_dataset('json', data_files='{combined_path}')")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Swiss French Dialect Dataset Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Setup and create starter data for all dialects
  %(prog)s --setup --create-all

  # Create starter dictionary for specific dialect
  %(prog)s --dialect valais --dictionary

  # Import CSV dictionary
  %(prog)s --dialect geneva --import-csv my_dictionary.csv

  # Create validation template
  %(prog)s --dialect fribourg --validation-template

  # Import validated translations
  %(prog)s --dialect valais --import-validated validation_template_valais.csv

  # Generate statistics
  %(prog)s --stats

  # Export to HuggingFace format
  %(prog)s --export
        """
    )

    parser.add_argument("--base-dir", default="./datasets/swiss_french",
                       help="Base directory for dataset (default: ./datasets/swiss_french)")
    parser.add_argument("--setup", action="store_true",
                       help="Setup directory structure")
    parser.add_argument("--dialect", choices=["valais", "geneva", "fribourg", "vaud", "neuchatel", "jura"],
                       help="Target dialect")
    parser.add_argument("--create-all", action="store_true",
                       help="Create starter data for all dialects")
    parser.add_argument("--dictionary", action="store_true",
                       help="Create starter dictionary")
    parser.add_argument("--sentences", action="store_true",
                       help="Create sentence templates")
    parser.add_argument("--idioms", action="store_true",
                       help="Create idiom identification examples")
    parser.add_argument("--import-csv", type=str,
                       help="Import dictionary from CSV file")
    parser.add_argument("--validation-template", action="store_true",
                       help="Create validation template CSV")
    parser.add_argument("--import-validated", type=str,
                       help="Import validated translations from CSV")
    parser.add_argument("--stats", action="store_true",
                       help="Generate dataset statistics")
    parser.add_argument("--export", action="store_true",
                       help="Export to HuggingFace format")

    args = parser.parse_args()

    # Initialize builder
    builder = SwissFrenchDatasetBuilder(args.base_dir)

    # Setup structure if requested
    if args.setup:
        builder.setup_structure()

    # Create all starter data
    if args.create_all:
        builder.setup_structure()
        for dialect in ["valais", "geneva", "fribourg"]:
            print(f"\n{'='*60}")
            print(f"Creating starter data for {dialect.upper()}")
            print(f"{'='*60}")
            builder.create_starter_dictionary(dialect)
            builder.create_sentence_templates(dialect)
            builder.create_idiom_identification_examples(dialect)
            builder.create_validation_template(dialect)
        builder.generate_statistics()
        return

    # Dialect-specific operations
    if args.dialect:
        if args.dictionary:
            builder.create_starter_dictionary(args.dialect)
        if args.sentences:
            builder.create_sentence_templates(args.dialect)
        if args.idioms:
            builder.create_idiom_identification_examples(args.dialect)
        if args.import_csv:
            builder.import_csv_dictionary(args.import_csv, args.dialect)
        if args.validation_template:
            builder.create_validation_template(args.dialect)
        if args.import_validated:
            builder.import_validated_csv(args.import_validated, args.dialect)

    # Statistics
    if args.stats:
        builder.generate_statistics()

    # Export
    if args.export:
        builder.export_to_huggingface()

    # If no arguments, show help
    if len(vars(args)) == 1:  # Only base_dir
        parser.print_help()


if __name__ == "__main__":
    main()
