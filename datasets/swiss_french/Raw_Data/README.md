# Raw Data Templates

This directory contains templates and examples for collecting Swiss French dialect data.

## Files

### `dictionary_template.csv`
Template for collecting dictionary entries (words and phrases).

**Columns:**
- `swiss_french`: Swiss French dialectal term
- `standard_french`: Standard French equivalent
- `dialect`: Which dialect (valais, geneva, fribourg, all)
- `part_of_speech`: noun, verb, adjective, etc.
- `example_usage`: Example sentence using the term
- `source`: Where you found it (GPSR, native speaker, etc.)
- `notes`: Additional information

**How to use:**
1. Copy this file and rename (e.g., `my_valais_dictionary.csv`)
2. Fill in your collected terms
3. Import: `python3 swiss_french_dataset_builder.py --dialect valais --import-csv my_valais_dictionary.csv`

### `sentences_template.csv`
Template for collecting parallel sentence translations.

**Columns:**
- `id`: Unique identifier
- `standard_french`: Standard French sentence
- `swiss_french_valais`: Valais dialect translation
- `swiss_french_geneva`: Geneva dialect translation
- `swiss_french_fribourg`: Fribourg dialect translation
- `topic`: Category (greetings, household, weather, etc.)
- `difficulty`: easy, medium, hard

**How to use:**
1. Fill in translations for your target dialect(s)
2. Leave blank columns empty if you don't have translations
3. Process using custom scripts or import selectively

## Data Collection Tips

1. **Start with common vocabulary**: Focus on everyday terms first
2. **Document sources**: Always note where you found the data
3. **Include context**: Example sentences help validate usage
4. **Mark dialect coverage**: Not all terms exist in all dialects
5. **Verify with natives**: When possible, validate with native speakers

## Example Sources

- **GPSR** (Glossaire des patois de la Suisse romande): https://www.gpsr.ch/
- **Regional newspapers**: Le Nouvelliste, Tribune de Genève, La Liberté
- **Native speakers**: Interviews, surveys, crowdsourcing
- **Academic works**: Linguistic publications on Swiss French

## Quality Standards

For inclusion in training dataset:
- ✅ Authentic dialectal usage (not artificial constructions)
- ✅ Verified by native speakers or authoritative sources
- ✅ Clear meaning and proper French grammar
- ✅ Appropriate for general audience
- ❌ No offensive or inappropriate content
- ❌ No copyrighted material without permission
