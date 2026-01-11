# Batch Translation Examples - TraductAL

This guide provides practical examples for batch translating multiple sentences, paragraphs, or entire documents using TraductAL.

## Table of Contents
1. [GUI Batch Translation (Easiest)](#gui-batch-translation)
2. [Command-Line Batch Translation](#command-line-batch-translation)
3. [Python API Batch Translation](#python-api-batch-translation)
4. [Real-World Use Cases](#real-world-use-cases)

---

## GUI Batch Translation (Easiest)

### Step-by-Step Tutorial

**1. Launch the Gradio Interface**
```bash
cd /home/aldn/TraductAL/TraductAL
./start_gradio.sh
```

**2. Access the Interface**
- Open browser to: `http://localhost:7860`
- Click on the **"📄 Batch Translation"** tab

**3. Prepare Your Text File**

Create a file with one sentence/paragraph per line:

```bash
# Create example file
cat > swiss_tourism.txt << 'EOF'
Willkommen in der Schweiz!
Die Schweiz hat vier Landessprachen: Deutsch, Französisch, Italienisch und Romansch.
Graubünden ist der einzige Kanton, wo Romansch gesprochen wird.
Es gibt sechs verschiedene Romansch-Dialekte.
Sursilvan ist der am weitesten verbreitete Dialekt.
Die Alpen bieten spektakuläre Landschaften.
Viele Touristen besuchen die Schweiz jedes Jahr.
Die lokale Küche ist sehr vielfältig.
Käsefondue ist ein traditionelles Schweizer Gericht.
Die Schweizer sind bekannt für ihre Pünktlichkeit und Präzision.
EOF
```

**4. Upload and Translate**
- In the Gradio interface, click **"Or upload .txt file"**
- Select your `swiss_tourism.txt` file
- Or paste the content directly into the text box
- Select **Source Language**: German
- Select **Target Language**: Romansh Sursilvan
- Click **"🌍 Translate All"**

**5. View Results**
The translation appears in the right panel, preserving the line structure:

```text
Beinvegni en Svizra!
La Svizra ha quatter linguas naziunalas: tudestg, franzos, talian e rumantsch.
Grischun è l'unic chantun nua che veng discurrì rumantsch.
I dat ses differents dialects rumantschs.
Sursilvan è il dialect il pli extensiv.
Las Alps purschivan cuntradas spectaculars.
Bler turissens visitan la Svizra mintga onn.
La cuschina locala è fitg multifaria.
Chaschiel fondieu è in maletg tradiziunal svizzer.
Ils Svizzers èn enconuschents per lur punctualitad e precisiun.
```

**6. Copy or Download Results**
- Copy the translated text directly
- Or save to a file by copying to your text editor

---

## Command-Line Batch Translation

### Method 1: Using batch_news_translator.py

**Basic Usage:**
```bash
# Syntax
python batch_news_translator.py --src SOURCE --tgt TARGET --input INPUT_FILE --output OUTPUT_FILE

# Example: German to Romansh
python batch_news_translator.py \
    --src de \
    --tgt rm-sursilv \
    --input swiss_tourism.txt \
    --output swiss_tourism_romansh.txt
```

**With Progress Display:**
```bash
# The script shows progress for each line
python batch_news_translator.py --src de --tgt rm-sursilv --input input.txt --output output.txt

# Output:
# Translating line 1/10...
# Translating line 2/10...
# ...
# ✅ Translation complete! Output saved to output.txt
```

### Method 2: Using Shell Script Loop

**Simple Line-by-Line Translation:**
```bash
#!/bin/bash
# batch_translate.sh

INPUT_FILE="$1"
OUTPUT_FILE="$2"
SRC_LANG="$3"
TGT_LANG="$4"

echo "Batch translation: $SRC_LANG → $TGT_LANG"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "---"

# Clear output file
> "$OUTPUT_FILE"

# Read and translate each line
line_num=0
total_lines=$(wc -l < "$INPUT_FILE")

while IFS= read -r line; do
    ((line_num++))
    echo "[$line_num/$total_lines] Translating..."

    if [ -z "$line" ]; then
        echo "" >> "$OUTPUT_FILE"
    else
        translation=$(./translate_enhanced.sh "$SRC_LANG" "$TGT_LANG" "$line")
        echo "$translation" >> "$OUTPUT_FILE"
    fi
done < "$INPUT_FILE"

echo "✅ Done! Translated $line_num lines."
```

**Usage:**
```bash
chmod +x batch_translate.sh
./batch_translate.sh input.txt output.txt de rm-sursilv
```

### Method 3: Direct Pipeline

**Quick One-Liner:**
```bash
# Translate each line and save to file
while IFS= read -r line; do
    ./translate_enhanced.sh en fr "$line"
done < input.txt > output.txt
```

---

## Python API Batch Translation

### Simple Batch Translator

```python
#!/usr/bin/env python3
"""
Simple batch translator for TraductAL
Usage: python simple_batch.py input.txt output.txt en fr
"""

import sys
from nllb_translator import EnhancedOfflineTranslator

def batch_translate(input_file, output_file, src_lang, tgt_lang):
    """Translate a file line by line."""

    # Initialize translator
    print(f"Initializing translator...")
    translator = EnhancedOfflineTranslator()

    # Read input
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    print(f"Found {total} lines to translate")
    print(f"Translating {src_lang} → {tgt_lang}")
    print("---")

    # Translate each line
    translations = []
    for i, line in enumerate(lines, 1):
        line = line.strip()

        # Preserve empty lines
        if not line:
            translations.append("")
            continue

        # Translate
        print(f"[{i}/{total}] Translating: {line[:50]}...")
        result = translator.translate(line, src_lang, tgt_lang)

        if "error" in result:
            print(f"  ⚠️  Error: {result['error']}")
            translations.append(f"[ERROR: {result['error']}]")
        else:
            translation = result["translation"]
            print(f"  ✓ {translation[:50]}...")
            translations.append(translation)

    # Write output
    print(f"\nWriting results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(translations))

    print(f"✅ Done! Translated {total} lines.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python simple_batch.py INPUT OUTPUT SRC_LANG TGT_LANG")
        print("Example: python simple_batch.py input.txt output.txt en fr")
        sys.exit(1)

    batch_translate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
```

**Usage:**
```bash
python simple_batch.py swiss_tourism.txt swiss_tourism_romansh.txt de rm-sursilv
```

### Advanced: With Progress Bar and Statistics

```python
#!/usr/bin/env python3
"""
Advanced batch translator with progress tracking
"""

import sys
import time
from pathlib import Path
from nllb_translator import EnhancedOfflineTranslator

def batch_translate_advanced(input_file, output_file, src_lang, tgt_lang):
    """Batch translate with statistics."""

    # Initialize
    print("="*60)
    print("TraductAL Batch Translator")
    print("="*60)

    translator = EnhancedOfflineTranslator()

    # Read input
    input_path = Path(input_file)
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    total_chars = sum(len(line.strip()) for line in lines)

    print(f"📄 Input file: {input_file}")
    print(f"📊 Statistics:")
    print(f"   - Total lines: {total_lines}")
    print(f"   - Total characters: {total_chars}")
    print(f"   - Average chars/line: {total_chars//total_lines if total_lines > 0 else 0}")
    print(f"🌍 Translation: {src_lang} → {tgt_lang}")
    print("="*60)

    # Translate with timing
    start_time = time.time()
    translations = []
    successful = 0
    errors = 0

    for i, line in enumerate(lines, 1):
        line = line.strip()

        # Progress indicator
        progress = (i / total_lines) * 100
        print(f"\r[{progress:5.1f}%] Line {i}/{total_lines}", end='', flush=True)

        if not line:
            translations.append("")
            continue

        # Translate
        result = translator.translate(line, src_lang, tgt_lang)

        if "error" in result:
            translations.append(f"[ERROR: {result['error']}]")
            errors += 1
        else:
            translations.append(result["translation"])
            successful += 1

    print()  # New line after progress

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(translations))

    # Final statistics
    elapsed_time = time.time() - start_time
    print("="*60)
    print("✅ Translation Complete!")
    print(f"📊 Results:")
    print(f"   - Successful: {successful}/{total_lines}")
    print(f"   - Errors: {errors}")
    print(f"   - Time: {elapsed_time:.2f}s")
    print(f"   - Speed: {total_lines/elapsed_time:.1f} lines/second")
    print(f"💾 Output saved to: {output_file}")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python advanced_batch.py INPUT OUTPUT SRC_LANG TGT_LANG")
        sys.exit(1)

    batch_translate_advanced(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
```

---

## Real-World Use Cases

### Use Case 1: Translating News Articles

**Input: `news_article.txt` (German)**
```text
Neue Entwicklungen in der Schweizer Politik
Die Bundesversammlung hat heute wichtige Entscheidungen getroffen.
Die Diskussionen konzentrierten sich auf Umweltfragen.
Vertreter aller Kantone nahmen an der Sitzung teil.
Die Ergebnisse werden morgen veröffentlicht.
```

**Command:**
```bash
python batch_news_translator.py --src de --tgt rm-sursilv --input news_article.txt --output news_romansh.txt
```

**Output: `news_romansh.txt`**
```text
Novas svilups en la politica svizra
L'Assamblea federala ha oz fatg decisiuns impurtantas.
Las discussiuns sa concentreschan sin dumondas d'ambient.
Represchentants da tut ils chantuns han partecipà a la sesida.
Ils resultats vegnan publitgads damaun.
```

### Use Case 2: Translating Educational Material

**Input: `lesson.txt` (English to French)**
```text
Welcome to Swiss Geography
Switzerland is located in Central Europe.
It borders five countries: Germany, France, Italy, Austria, and Liechtenstein.
The country has three main geographical regions.
The Alps cover approximately 60% of the territory.
```

**Command:**
```bash
python simple_batch.py lesson.txt lesson_fr.txt en fr
```

### Use Case 3: Translating Tourist Information

**Input: Multiple files**
```bash
# Translate all .txt files in a directory
for file in tourist_info/*.txt; do
    basename=$(basename "$file" .txt)
    python batch_news_translator.py \
        --src de \
        --tgt rm-sursilv \
        --input "$file" \
        --output "romansh/${basename}_rm.txt"
done
```

---

## Tips and Best Practices

### 1. **Optimize Line Length**
- Keep lines under 400-500 words for best results
- One sentence or paragraph per line works well
- Empty lines are preserved in output

### 2. **Handle Special Characters**
```bash
# Ensure UTF-8 encoding
iconv -f ISO-8859-1 -t UTF-8 input.txt > input_utf8.txt
python batch_news_translator.py --src de --tgt rm-sursilv --input input_utf8.txt --output output.txt
```

### 3. **Process Large Files**
```python
# For very large files (1000+ lines), process in batches
def batch_translate_large(input_file, output_file, src_lang, tgt_lang, batch_size=100):
    translator = EnhancedOfflineTranslator()

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        batch = []
        for line in infile:
            batch.append(line.strip())

            if len(batch) >= batch_size:
                # Translate batch
                for text in batch:
                    if text:
                        result = translator.translate(text, src_lang, tgt_lang)
                        outfile.write(result["translation"] + '\n')
                    else:
                        outfile.write('\n')
                batch = []

        # Process remaining lines
        for text in batch:
            if text:
                result = translator.translate(text, src_lang, tgt_lang)
                outfile.write(result["translation"] + '\n')
            else:
                outfile.write('\n')
```

### 4. **Quality Check**
```bash
# Compare line counts
wc -l input.txt output.txt

# Should be equal - if not, check for errors
```

---

## Troubleshooting

**Problem: Empty output**
```bash
# Check file encoding
file -bi input.txt

# Convert if needed
iconv -f ISO-8859-1 -t UTF-8 input.txt > input_fixed.txt
```

**Problem: Some lines not translated**
- Check for very long lines (>500 words)
- Check for special characters that might cause errors
- Review error messages in console output

**Problem: Slow translation**
- Normal speed: 0.5-1 second per line with NLLB-1.3B
- For faster processing: Ensure models are downloaded locally
- For Apertus-8B: Use GPU if available (5-10x faster)

---

## Summary

| Method | Best For | Complexity | Speed |
|--------|----------|------------|-------|
| **Gradio GUI** | Small-medium files, non-technical users | Easy | Fast |
| **batch_news_translator.py** | Medium-large files, automated workflows | Medium | Fast |
| **Python API** | Custom processing, integration | Advanced | Fastest |
| **Shell scripts** | System integration, pipelines | Medium | Medium |

**Recommendation:** Start with the Gradio GUI for testing, then use Python API for production workflows.
