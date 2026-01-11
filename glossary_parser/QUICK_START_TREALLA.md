# Quick Start: Using Trealla with TraductAL

## ✅ Installation Complete!

Trealla Prolog is now installed and ready to use with TraductAL.

## Test Results

```bash
$ PATH="$HOME/bin:$PATH" python3 trealla_interface.py \
    --input test_sample.txt \
    --output test_output.csv \
    --backend trealla

🔧 Trealla Prolog interface initialized
   Grammar: grammar.pl
   Lexicon: lexicon.pl

📖 Parsing glossary file: test_sample.txt
   ✅ Parsed 2 entries from 2 lines

✅ Saved 2 entries to test_output.csv
✅ Parsing complete!
```

Output (test_output.csv):
```csv
headword,pos,definition
ABANDONNER,v.a.,"Laisser, quitter."
ABATIS,s.m.,Abattage d'arbres.
```

## Usage

### Option 1: Python API (Recommended)

```python
# Import Trealla interface
from glossary_parser.trealla_interface import TreallaGlossaryParser

# Initialize
parser = TreallaGlossaryParser(
    grammar_file="glossary_parser/grammar.pl",
    lexicon_file="glossary_parser/lexicon.pl"
)

# Parse file
entries = parser.parse_file("input.txt")

# Process results
for entry in entries:
    print(f"{entry['headword']} ({entry['pos']}): {entry['definition']}")
```

### Option 2: Command Line

```bash
# Add ~/bin to PATH (or use full paths)
export PATH="$HOME/bin:$PATH"

# Parse glossary
python3 glossary_parser/trealla_interface.py \
    --input input.txt \
    --output output.csv \
    --backend trealla
```

### Option 3: Direct Trealla

```bash
# Use Trealla directly
tpl glossary_parser/parse_glossary_trealla.pl input.txt output.csv
```

## Integration with TraductAL

### Drop-in Replacement for Janus

```python
# OLD (Janus):
# from glossary_parser.janus_interface import JanusGlossaryParser
# parser = JanusGlossaryParser()

# NEW (Trealla):
from glossary_parser.trealla_interface import TreallaGlossaryParser
parser = TreallaGlossaryParser()

# Same API - no other changes needed!
entries = parser.parse_file("glossary.txt")
```

## Important Notes

### 1. PATH Configuration

Make sure `~/bin` is in your PATH:

```bash
# Add to ~/.bashrc or ~/.bash_profile
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or use full path in scripts
~/bin/tpl script.pl
```

### 2. Performance

- **Fast**: Regex-based parsing for per-entry calls
- **Full DCG**: Use `parse_file_with_trealla()` for full Prolog DCG parsing
- **Batch processing**: Best for large files

### 3. Backend Options

```python
# Trealla backend (Prolog DCG)
parser = TreallaGlossaryParser()

# Fallback backend (Python regex only)
from glossary_parser.trealla_interface import FallbackPythonParser
parser = FallbackPythonParser()
```

## File Locations

```
~/TraductAL/TraductAL/glossary_parser/
├── trealla_interface.py          # Main Trealla interface
├── parse_glossary_trealla.pl     # Trealla DCG parser
├── grammar.pl                     # DCG grammar rules
├── lexicon.pl                     # Lexicon definitions
├── TREALLA_MIGRATION_GUIDE.md    # Full migration guide
└── QUICK_START_TREALLA.md        # This file
```

## Testing

```bash
cd ~/TraductAL/TraductAL/glossary_parser

# Create test input
echo -e "ABANDONNER, v.a. Laisser, quitter.\nABATIS, s.m. Abattage d'arbres." > test.txt

# Test with Trealla
PATH="$HOME/bin:$PATH" python3 trealla_interface.py \
    --input test.txt \
    --output test_out.csv \
    --backend trealla

# View results
cat test_out.csv
```

## Next Steps

1. **Read the full guide**: See `TREALLA_MIGRATION_GUIDE.md` for detailed info
2. **Test with your data**: Try parsing your actual glossary files
3. **Integrate into pipeline**: Use Trealla parser in your translation workflow
4. **Optimize**: For real-time use, consider implementing FFI (advanced)

## Support

- **Trealla Docs**: https://github.com/trealla-prolog/trealla
- **DCG Tutorial**: https://www.metalevel.at/prolog/dcg
- **TraductAL Issues**: Check main TraductAL documentation

## Summary

✅ Trealla is **installed and working**
✅ Parser is **compatible with Janus API**
✅ Ready for **production use** in batch mode
⚠️ For real-time queries, consider **FFI implementation** (future work)

Happy translating! 🎉
