# Trealla Prolog Migration Guide for TraductAL

## Overview

This guide explains how to use **Trealla Prolog** instead of **Janus-Prolog (SWI-Prolog)** in the TraductAL hybrid neural-symbolic machine translation system.

## Background

TraductAL is a hybrid system combining:
- **Neural/Statistical Component**: NLLB-200, Flair Parser, Stanza (Stanford NLP)
- **Symbolic Component**: Prolog for DCG-based parsing and error correction
- **Original Bridge**: Janus (SWI-Prolog ↔ Python)

## Key Differences: SWI-Prolog vs Trealla

| Feature | SWI-Prolog + Janus | Trealla Prolog |
|---------|-------------------|----------------|
| Python Integration | Native Janus bridge | Subprocess or FFI |
| ISO Compliance | Extended ISO | Strict ISO + extensions |
| Size | ~30MB | ~2MB |
| Speed | Good | Excellent |
| Module System | Full modules | Basic modules |
| FFI | Yes | Yes (experimental) |

## Migration Options

### Option 1: Subprocess Communication (Implemented) ⭐

**Status**: Ready to use
**Files**: `trealla_interface.py`, `parse_glossary_trealla.pl`

This approach:
- Uses Trealla as a subprocess
- Communicates via stdin/stdout
- No FFI/C programming needed
- Drop-in replacement for most use cases

**Pros**:
- Simple implementation
- No compilation needed
- Compatible with existing code structure

**Cons**:
- Higher latency per query (not suitable for real-time per-sentence queries)
- Best for batch processing

### Option 2: FFI Integration (Future)

**Status**: Not yet implemented
**Complexity**: High

This approach:
- Uses Trealla's Foreign Function Interface
- Direct C/Python ↔ Prolog calls
- Lower latency, better for real-time use

**Pros**:
- Near-native performance
- Suitable for real-time translation

**Cons**:
- Requires C programming or ctypes/cffi
- More complex setup

## Using Trealla Interface

### Installation

1. **Install Trealla Prolog** (already done):
   ```bash
   cd ~/NLP/trealla
   make
   make install
   ```

2. **Verify installation**:
   ```bash
   tpl --version
   which tpl  # Should show ~/bin/tpl
   ```

3. **Add ~/bin to PATH** (if not already):
   ```bash
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Basic Usage

#### Python API (Drop-in Replacement)

```python
# OLD: Using Janus
from glossary_parser.janus_interface import JanusGlossaryParser
parser = JanusGlossaryParser()

# NEW: Using Trealla
from glossary_parser.trealla_interface import TreallaGlossaryParser
parser = TreallaGlossaryParser()

# Same API!
entries = parser.parse_file("input.txt")
for entry in entries:
    print(f"{entry['headword']} ({entry['pos']}): {entry['definition']}")
```

#### Command Line

```bash
cd ~/TraductAL/TraductAL/glossary_parser

# Parse with Trealla
python3 trealla_interface.py \
    --input glossaire-vaudois.txt \
    --output parsed-trealla.csv \
    --backend trealla

# Or use Trealla directly
tpl parse_glossary_trealla.pl \
    glossaire-vaudois.txt \
    parsed-output.csv
```

## Integration with TraductAL Translation Pipeline

### Current Architecture (Janus)

```
User Input (Text)
    ↓
NLLB-200 Neural Translation
    ↓
Stanza/Flair NLP Analysis
    ↓
Janus → SWI-Prolog DCG Parser
    ↓
Error Detection & Correction
    ↓
Final Translation Output
```

### Proposed Architecture (Trealla)

```
User Input (Text)
    ↓
NLLB-200 Neural Translation
    ↓
Stanza/Flair NLP Analysis
    ↓
Trealla Interface → Trealla Prolog DCG Parser
    ↓
Error Detection & Correction
    ↓
Final Translation Output
```

### Adapting Your Code

#### Step 1: Replace Import

```python
# In your translation pipeline
# OLD:
# from glossary_parser.janus_interface import JanusGlossaryParser

# NEW:
from glossary_parser.trealla_interface import TreallaGlossaryParser as GlossaryParser
```

#### Step 2: Update Initialization

```python
# Initialize parser (same API)
parser = GlossaryParser(
    grammar_file="glossary_parser/grammar.pl",
    lexicon_file="glossary_parser/lexicon.pl"
)
```

#### Step 3: Use Parser (No Changes Needed)

```python
# Parse entries (API unchanged)
entries = parser.parse_file("glossary.txt")

# Or parse single entry
entry = parser.parse_entry("ABANDONNER, v.a. Laisser, quitter")
```

## Performance Considerations

### When to Use Trealla

✅ **Good for**:
- Batch processing of documents
- Offline analysis
- Glossary parsing
- Rule-based error detection on complete documents

❌ **Not ideal for**:
- Real-time per-word/per-sentence queries (use FFI instead)
- Interactive REPL-style usage
- Frequent small queries (subprocess overhead)

### Optimization Tips

1. **Batch Processing**: Process multiple entries at once
   ```python
   # Good: Batch processing
   entries = parser.parse_file("input.txt")  # Fast

   # Avoid: Per-line subprocess calls
   # for line in lines:
   #     entry = parser.parse_entry(line)  # Slow
   ```

2. **Caching**: Cache parsed results
   ```python
   import functools

   @functools.lru_cache(maxsize=1000)
   def parse_cached(text):
       return parser.parse_entry(text)
   ```

3. **Parallel Processing**: Use multiprocessing for large datasets
   ```python
   from multiprocessing import Pool

   with Pool(4) as p:
       results = p.map(parser.parse_entry, texts)
   ```

## Compatibility Notes

### SWI-Prolog Features Not in Trealla

Some SWI-Prolog specific features may need adaptation:

1. **Module system**: Trealla has simpler modules
2. **Tabling**: Not yet supported in Trealla
3. **Constraints**: CLP(FD) has different syntax
4. **Some built-ins**: Check Trealla docs for equivalents

### DCG Compatibility

✅ Trealla fully supports **DCG (Definite Clause Grammars)**
✅ Your existing grammar.pl should work with minimal changes

### Required Changes for Trealla

```prolog
% SWI-Prolog
:- use_module(library(dcg/basics)).

% Trealla - May need to define basics manually or simplify
% (Trealla has core DCG support built-in)
```

## Testing

### Test Trealla Parser

```bash
cd ~/TraductAL/TraductAL/glossary_parser

# Test with sample input
echo "ABANDONNER, v.a. Laisser, quitter" > test.txt
python3 trealla_interface.py --input test.txt --output test.csv

# Check output
cat test.csv
```

### Compare Janus vs Trealla

```bash
# Parse with Janus
python3 janus_interface.py --input sample.txt --output janus-output.csv

# Parse with Trealla
python3 trealla_interface.py --input sample.txt --output trealla-output.csv

# Compare results
diff janus-output.csv trealla-output.csv
```

## Troubleshooting

### Issue: "tpl not found"

**Solution**: Add ~/bin to PATH
```bash
export PATH="$HOME/bin:$PATH"
```

### Issue: Module errors in Trealla

**Solution**: Simplify module declarations
```prolog
% SWI-Prolog
:- use_module(library(lists)).

% Trealla - Built-in
% (No import needed for basic lists)
```

### Issue: Slow parsing

**Solution**: Use batch processing instead of per-entry parsing
```python
# Use parse_file() instead of multiple parse_entry() calls
entries = parser.parse_file("input.txt")
```

## Future Enhancements

1. **FFI Integration**: Implement low-latency FFI bridge
2. **Streaming Parser**: Process large files line-by-line
3. **Neural-Symbolic Fusion**: Tighter integration with NLLB-200
4. **Error Correction Rules**: Expand Prolog rules for hallucination detection

## References

- [Trealla Prolog GitHub](https://github.com/trealla-prolog/trealla)
- [Trealla Documentation](https://github.com/trealla-prolog/trealla/wiki)
- [SWI-Prolog Janus](https://www.swi-prolog.org/pldoc/doc_for?object=section%28%27packages/janus.html%27%29)
- [DCG Tutorial](https://www.metalevel.at/prolog/dcg)

## Support

For issues specific to:
- **Trealla integration**: Check `trealla_interface.py`
- **DCG grammar**: Check `grammar.pl` and `parse_glossary_trealla.pl`
- **TraductAL pipeline**: Check main TraductAL documentation

## Summary

✅ **Trealla is ready to use** for TraductAL
✅ **Drop-in replacement** for batch processing use cases
⚠️ **Subprocess-based**: Best for batch, not real-time queries
🚀 **Future FFI**: Will enable real-time integration

Happy translating with Trealla! 🎉
