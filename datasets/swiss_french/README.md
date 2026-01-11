# Swiss French Dialect Dataset

**Created**: 2025-12-24
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
{"Prompt": "Translate to Swiss French (Valais): Je vais faire le ménage", "Answer": "Je vais faire le réduit"}
{"Prompt": "What does 'panosse' mean?", "Answer": "Panosse is Swiss French for serpillière (mop)"}
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

- Dictionary entries: 0
- Sentence pairs: 0
- Idioms: 0
- Total examples: 0

## License

TBD - Ensure compliance with source material licenses
