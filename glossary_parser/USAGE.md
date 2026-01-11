# 📖 Prolog Glossary Parser - Usage Guide

## 🎯 Quick Answer to Your Question

**Your question**: *Why doesn't `swipl parse_glossary.pl -i input.txt -o output.csv` work?*

**Answer**: SWI-Prolog interprets `-i`, `-o` as its own flags, not script arguments.

**Solution**: Use the wrapper script `parse_vaudois.sh` instead!

---

## ✅ Three Ways to Run the Parser

### **Method 1: Wrapper Script (RECOMMENDED)**

This is the **easiest** and works like you expect:

```bash
./parse_vaudois.sh -i ../raw_glossaire_vaud.txt -o vaud-glossary.csv
```

**Advantages**:
- ✅ User-friendly syntax
- ✅ Argument validation
- ✅ Helpful error messages
- ✅ Works like standard Unix tools

**Help**:
```bash
./parse_vaudois.sh --help
```

---

### **Method 2: Direct SWI-Prolog (Long Form)**

If you need more control:

```bash
swipl -s parse_glossary.pl \
      -g "main(['-i', '../raw_glossaire_vaud.txt', '-o', 'output.csv']), halt"
```

**Explanation**:
- `-s parse_glossary.pl` - Load the Prolog script
- `-g "goal"` - Execute the goal
- `main([...])` - Call main with argument list
- `halt` - Exit after completion

---

### **Method 3: Interactive Prolog Session**

For debugging/testing:

```bash
swipl

?- consult('parse_glossary.pl').
true.

?- main(['-i', '../raw_glossaire_vaud.txt', '-o', 'test.csv']).
📖 Parsing glossary: ../raw_glossaire_vaud.txt
...
true.
```

**Useful for**:
- Testing individual DCG rules
- Debugging parse failures
- Experimenting with the grammar

---

## 🔧 Why SWI-Prolog Arguments Are Tricky

### **What Doesn't Work**

```bash
# ❌ This doesn't work
swipl parse_glossary.pl -i input.txt -o output.csv
```

**Why**: SWI-Prolog's command-line parser sees:
- `parse_glossary.pl` - Script to load
- `-i input.txt` - SWI-Prolog's own `-i` flag (initialization)
- `-o output.csv` - SWI-Prolog's own `-o` flag (optimization)

The arguments never reach your Prolog script!

### **What Works**

```bash
# ✅ Use wrapper script
./parse_vaudois.sh -i input.txt -o output.csv

# ✅ Or explicit goal
swipl -s parse_glossary.pl -g "main(['-i', 'input.txt', '-o', 'output.csv']), halt"
```

---

## 📋 Complete Command Reference

### **Wrapper Script**

```bash
# Basic usage
./parse_vaudois.sh -i INPUT -o OUTPUT

# With full paths
./parse_vaudois.sh -i /path/to/input.txt -o /path/to/output.csv

# Help
./parse_vaudois.sh --help

# Example: Parse Vaudois glossary
./parse_vaudois.sh -i ../raw_glossaire_vaud.txt -o vaud-glossary.csv
```

### **Direct SWI-Prolog**

```bash
# Long form (recommended for scripts)
swipl -s parse_glossary.pl -g "main(['-i', 'input.txt', '-o', 'output.csv']), halt"

# Short form (if parse_glossary.pl is executable with shebang)
./parse_glossary.pl -i input.txt -o output.csv  # This won't work!

# Why? Shebangs with args are problematic:
#!/usr/bin/env swipl  # Can't pass additional flags here
```

---

## 🧪 Testing & Debugging

### **Test Parser on Sample**

```bash
# Create test input
head -100 ../raw_glossaire_vaud.txt > test_input.txt

# Parse sample
./parse_vaudois.sh -i test_input.txt -o test_output.csv

# Check results
wc -l test_output.csv
head test_output.csv
```

### **Debug Individual Entry**

```bash
swipl

?- consult('parse_glossary.pl').
true.

?- parse_line('PANOSSE, s.f. Serpillière pour laver.', Entry).
Entry = entry('PANOSSE', noun_feminine, 'Serpillière pour laver.').

?- parse_line('ABATTRE, v.a. Faire tomber.', Entry).
Entry = entry('ABATTRE', verb_active, 'Faire tomber.').
```

### **Test DCG Rules Directly**

```bash
swipl

?- consult('parse_glossary.pl').

% Test headword parsing
?- phrase(uppercase_word(W), "PANOSSE").
W = "PANOSSE".

% Test POS marker
?- phrase(pos_marker(POS), "s.f.").
POS = noun_feminine.

% Test complete entry
?- phrase(entry(HW, POS, Def), "PANOSSE, s.f. Serpillière.").
HW = 'PANOSSE',
POS = noun_feminine,
Def = 'Serpillière.'.
```

---

## 📊 Output Format

### **CSV Structure**

```csv
swiss_french,standard_french,dialect,part_of_speech,definition,source,notes
PANOSSE,,vaud,noun_feminine,Serpillière pour laver le sol,Glossaire Vaudois (1861),DCG parsed
LINGE,,vaud,noun_masculine,Serviette de toilette,Glossaire Vaudois (1861),DCG parsed
```

### **Fields**

| Field | Description | Example |
|-------|-------------|---------|
| `swiss_french` | Dialectal headword | PANOSSE |
| `standard_french` | French equivalent | serpillière |
| `dialect` | Dialect code | vaud |
| `part_of_speech` | Grammatical category | noun_feminine |
| `definition` | Definition text | Serpillière pour... |
| `source` | Source reference | Glossaire Vaudois (1861) |
| `notes` | Additional info | DCG parsed |

### **POS Values**

```
noun_masculine     - s.m.
noun_feminine      - s.f.
noun_neuter        - s.n.
verb_active        - v.a.
verb_neutral       - v.n.
verb_pronominal    - v.pr.
verb              - v.
adjective         - adj.
adverb            - adv.
unknown           - no POS marker found
```

---

## 🔄 Workflow Integration

### **Full Pipeline**

```bash
cd /home/aldn/TraductAL/TraductAL/glossary_parser

# 1. Parse glossary with DCG
./parse_vaudois.sh \
  -i ../raw_glossaire_vaud.txt \
  -o vaud-glossary.csv

# 2. Check results
wc -l vaud-glossary.csv
head -20 vaud-glossary.csv

# 3. Import to Swiss French dataset
cd ..
source /home/aldn/Apertus8B/alvenv/bin/activate
python3 swiss_french_dataset_builder.py \
  --dialect vaud \
  --import-csv glossary_parser/vaud-glossary.csv

# 4. Check progress
python3 swiss_french_dataset_builder.py --stats
```

### **Process Multiple Glossaries**

```bash
# Parse each glossary
./parse_vaudois.sh -i glossaire_geneva.txt -o geneva-glossary.csv
./parse_vaudois.sh -i glossaire_fribourg.txt -o fribourg-glossary.csv
./parse_vaudois.sh -i glossaire_neuchatel.txt -o neuchatel-glossary.csv

# Import all
cd ..
python3 swiss_french_dataset_builder.py --dialect geneva --import-csv glossary_parser/geneva-glossary.csv
python3 swiss_french_dataset_builder.py --dialect fribourg --import-csv glossary_parser/fribourg-glossary.csv
python3 swiss_french_dataset_builder.py --dialect neuchatel --import-csv glossary_parser/neuchatel-glossary.csv

# Check totals
python3 swiss_french_dataset_builder.py --stats
```

---

## 🐛 Troubleshooting

### **Issue: "Command not found"**

```bash
# Make sure script is executable
chmod +x parse_vaudois.sh

# Or run with bash
bash parse_vaudois.sh -i input.txt -o output.csv
```

### **Issue: "Input file not found"**

```bash
# Check path
ls -la ../raw_glossaire_vaud.txt

# Use absolute path
./parse_vaudois.sh -i /full/path/to/input.txt -o output.csv
```

### **Issue: "No entries parsed"**

```bash
# Check input file encoding
file ../raw_glossaire_vaud.txt

# View sample
head -20 ../raw_glossaire_vaud.txt

# Test with small sample
head -100 ../raw_glossaire_vaud.txt > test.txt
./parse_vaudois.sh -i test.txt -o test.csv
```

### **Issue: SWI-Prolog warnings**

```bash
# Singleton variable warnings are normal
Warning: Singleton variables: [Variant]

# They don't affect parsing
# Just means some variables are declared but not used
```

---

## 💡 Pro Tips

### **Tip 1: Process in Stages**

```bash
# Parse a sample first
head -1000 ../raw_glossaire_vaud.txt > sample.txt
./parse_vaudois.sh -i sample.txt -o sample.csv

# Review quality
less sample.csv

# Then parse full glossary
./parse_vaudois.sh -i ../raw_glossaire_vaud.txt -o full.csv
```

### **Tip 2: Compare Parsers**

```bash
# DCG parser (this one)
./parse_vaudois.sh -i ../raw_glossaire_vaud.txt -o vaud-dcg.csv
wc -l vaud-dcg.csv

# Regex parser (original)
python3 ../glossary_extractor.py --pdf original.pdf --output vaud-regex.csv
wc -l vaud-regex.csv

# Compare quality
diff <(head -50 vaud-dcg.csv) <(head -50 vaud-regex.csv)
```

### **Tip 3: Batch Processing**

```bash
# Process all glossaries in a directory
for file in ../glossaries/*.txt; do
    basename=$(basename "$file" .txt)
    ./parse_vaudois.sh -i "$file" -o "${basename}-glossary.csv"
done
```

---

## 📚 Technical Details

### **Why Wrapper Script Needed**

SWI-Prolog's argument handling:

```
Command: swipl script.pl -i input.txt

SWI-Prolog sees:
  - Load: script.pl
  - Flag: -i (initialization file)
  - Arg:  input.txt

Your script never sees: ['-i', 'input.txt']
```

**Solution**: Wrapper script constructs proper goal:

```bash
swipl -s parse_glossary.pl \
     -g "main(['-i', 'INPUT', '-o', 'OUTPUT']), halt"
```

Now your script's `main/1` receives: `['-i', 'INPUT', '-o', 'OUTPUT']`

### **Alternative: Standalone Executable**

To make `./parse_glossary.pl -i ... -o ...` work, you'd need:

1. **Complex shebang** (doesn't work well):
   ```prolog
   #!/usr/bin/env swipl
   % Can't pass -g flag here!
   ```

2. **Or modify Prolog to read ARGV** (complicated):
   ```prolog
   main :-
       current_prolog_flag(argv, Argv),
       % Parse Argv...
   ```

**Conclusion**: Wrapper script is simpler and more reliable!

---

## ✅ Summary

**To answer your question**:

❌ **Doesn't work**:
```bash
swipl parse_glossary.pl -i input.txt -o output.csv
```

✅ **Does work**:
```bash
./parse_vaudois.sh -i input.txt -o output.csv
```

✅ **Also works**:
```bash
swipl -s parse_glossary.pl -g "main(['-i', 'input.txt', '-o', 'output.csv']), halt"
```

**Recommended**: Use the wrapper script - it's simple and works as expected!

---

## 🎯 Quick Reference Card

```bash
# Parse glossary
./parse_vaudois.sh -i INPUT.txt -o OUTPUT.csv

# Help
./parse_vaudois.sh --help

# Import to dataset
python3 ../swiss_french_dataset_builder.py --dialect vaud --import-csv OUTPUT.csv

# Check stats
python3 ../swiss_french_dataset_builder.py --stats
```

That's it! 🎓
