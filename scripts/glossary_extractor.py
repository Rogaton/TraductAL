#!/usr/bin/env python3
"""
Historical Glossary PDF Extractor

Extracts lexical data from historical Swiss French dialect glossaries (PDF format).
Handles OCR, structure parsing, and conversion to CSV for dataset import.

Supports formats like:
- Glossaire vaudois (1861)
- GPSR entries
- Other historical dictionaries
"""

import re
import csv
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse


class GlossaryExtractor:
    """Extract and structure glossary data from PDF text."""

    # Common patterns in historical glossaries
    ENTRY_PATTERNS = [
        # Pattern 1: "WORD, genre. Definition"
        r'^([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][a-zàâäéèêëïîôöùûüÿæœç\-]+),?\s+(m\.|f\.|n\.|adj\.|v\.|adv\.)\s+(.+)$',

        # Pattern 2: "WORD (genre) Definition"
        r'^([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][a-zàâäéèêëïîôöùûüÿæœç\-]+)\s+\((m\.|f\.|n\.|adj\.|v\.|adv\.)\)\s+(.+)$',

        # Pattern 3: "WORD. — Definition" (no gender)
        r'^([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][a-zàâäéèêëïîôöùûüÿæœç\-]+)\.?\s*[—–-]\s*(.+)$',

        # Pattern 4: "word, Definition" (lowercase start, likely continuation)
        r'^([a-zàâäéèêëïîôöùûüÿæœç\-]+),?\s+(.+)$',
    ]

    # Gender/Part of speech abbreviations
    POS_MAPPING = {
        'm.': 'masculine noun',
        'f.': 'feminine noun',
        'n.': 'neuter noun',
        'adj.': 'adjective',
        'v.': 'verb',
        'adv.': 'adverb',
        's.m.': 'masculine noun',
        's.f.': 'feminine noun',
        'v.a.': 'active verb',
        'v.n.': 'neutral verb',
    }

    def __init__(self, pdf_path: str, dialect: str = "vaud"):
        """Initialize extractor."""
        self.pdf_path = Path(pdf_path)
        self.dialect = dialect
        self.entries = []
        self.raw_text = ""

    def extract_text_from_pdf(self) -> str:
        """Extract text from PDF using available libraries."""
        print(f"📄 Extracting text from: {self.pdf_path}")

        # Try PyPDF2 first (most common)
        try:
            import PyPDF2
            return self._extract_with_pypdf2()
        except ImportError:
            print("   PyPDF2 not available, trying pdfplumber...")

        # Try pdfplumber (better for complex layouts)
        try:
            import pdfplumber
            return self._extract_with_pdfplumber()
        except ImportError:
            print("   pdfplumber not available, trying pymupdf...")

        # Try pymupdf/fitz (good for OCR'd PDFs)
        try:
            import fitz  # pymupdf
            return self._extract_with_pymupdf()
        except ImportError:
            print("   pymupdf not available")

        print("\n❌ No PDF library available!")
        print("Install one of:")
        print("  pip install PyPDF2")
        print("  pip install pdfplumber")
        print("  pip install pymupdf")
        return ""

    def _extract_with_pypdf2(self) -> str:
        """Extract using PyPDF2."""
        import PyPDF2

        text = ""
        with open(self.pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"   Pages: {len(reader.pages)}")

            for i, page in enumerate(reader.pages, 1):
                if i % 10 == 0:
                    print(f"   Processing page {i}...")
                text += page.extract_text() + "\n"

        print(f"   ✅ Extracted {len(text)} characters")
        return text

    def _extract_with_pdfplumber(self) -> str:
        """Extract using pdfplumber."""
        import pdfplumber

        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            print(f"   Pages: {len(pdf.pages)}")

            for i, page in enumerate(pdf.pages, 1):
                if i % 10 == 0:
                    print(f"   Processing page {i}...")
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        print(f"   ✅ Extracted {len(text)} characters")
        return text

    def _extract_with_pymupdf(self) -> str:
        """Extract using PyMuPDF."""
        import fitz

        text = ""
        doc = fitz.open(self.pdf_path)
        print(f"   Pages: {len(doc)}")

        for i, page in enumerate(doc, 1):
            if i % 10 == 0:
                print(f"   Processing page {i}...")
            text += page.get_text() + "\n"

        doc.close()
        print(f"   ✅ Extracted {len(text)} characters")
        return text

    def save_raw_text(self, output_path: str):
        """Save raw extracted text for manual review."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w', encoding='utf-8') as f:
            f.write(self.raw_text)

        print(f"📝 Raw text saved to: {output}")

    def clean_text(self, text: str) -> List[str]:
        """Clean and normalize extracted text."""
        print("\n🧹 Cleaning text...")

        # Split into lines
        lines = text.split('\n')

        # Clean each line
        cleaned = []
        for line in lines:
            # Remove extra whitespace
            line = ' '.join(line.split())

            # Skip empty lines
            if not line.strip():
                continue

            # Skip page numbers (common pattern: just numbers)
            if re.match(r'^\d+$', line.strip()):
                continue

            # Skip headers/footers (adjust based on your PDF)
            if any(keyword in line.lower() for keyword in ['glossaire', 'vaudois', 'table des matières', 'préface']):
                if len(line) < 50:  # Short lines are likely headers
                    continue

            cleaned.append(line)

        print(f"   Cleaned {len(cleaned)} lines from {len(lines)} total")
        return cleaned

    def identify_glossary_start(self, lines: List[str]) -> int:
        """Find where the actual glossary starts (after preface, etc.)."""
        print("\n🔍 Identifying glossary start...")

        # Look for first entry (usually starts with 'A')
        for i, line in enumerate(lines):
            # Check if line looks like a glossary entry
            if re.match(r'^A[A-Z]', line):  # "ABAISER", "ABONDER", etc.
                print(f"   Found glossary start at line {i}: {line[:50]}...")
                return i

            # Alternative: look for "A." as section marker
            if re.match(r'^A\.\s*$', line):
                print(f"   Found section marker at line {i}: {line}")
                return i + 1

        print("   ⚠️  Could not auto-detect start, using line 0")
        return 0

    def parse_entries(self, lines: List[str], start_idx: int = 0) -> List[Dict]:
        """Parse glossary entries from cleaned lines."""
        print(f"\n📖 Parsing entries from line {start_idx}...")

        entries = []
        current_entry = None

        for i, line in enumerate(lines[start_idx:], start_idx):
            # Try each pattern
            matched = False

            for pattern in self.ENTRY_PATTERNS:
                match = re.match(pattern, line)
                if match:
                    matched = True

                    # Save previous entry if exists
                    if current_entry:
                        entries.append(current_entry)

                    # Parse new entry
                    groups = match.groups()

                    if len(groups) == 3:
                        word, pos, definition = groups
                        current_entry = {
                            'word': word.strip(),
                            'pos': self.POS_MAPPING.get(pos.strip(), pos.strip()),
                            'definition': definition.strip(),
                            'line_number': i
                        }
                    elif len(groups) == 2:
                        word, definition = groups
                        current_entry = {
                            'word': word.strip(),
                            'pos': 'unknown',
                            'definition': definition.strip(),
                            'line_number': i
                        }

                    break

            # If no match and we have current entry, might be continuation
            if not matched and current_entry:
                # Check if line looks like a continuation (lowercase start, short)
                if line and not line[0].isupper() and len(line) < 100:
                    current_entry['definition'] += ' ' + line.strip()

        # Don't forget last entry
        if current_entry:
            entries.append(current_entry)

        print(f"   ✅ Parsed {len(entries)} entries")
        return entries

    def extract_standard_french(self, definition: str) -> Optional[str]:
        """Extract standard French equivalent from definition."""
        # Common patterns in definitions
        patterns = [
            r'(?:même que|synonyme de|équivalent à|français)\s+[«"]?([^.»"]+)[»"]?',
            r'V\.\s+([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][a-zàâäéèêëïîôöùûüÿæœç\-]+)',  # "V. Word"
            r'\(([^)]+)\)',  # Text in parentheses
        ]

        for pattern in patterns:
            match = re.search(pattern, definition, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # If no explicit match, try to extract a simple translation
        # (this is heuristic and may need adjustment)
        words = definition.split()
        if len(words) <= 3:
            return definition.strip('.,;:')

        return None

    def enrich_entries(self):
        """Enrich entries with additional information."""
        print("\n✨ Enriching entries...")

        for entry in self.entries:
            # Extract standard French equivalent
            std_french = self.extract_standard_french(entry['definition'])
            if std_french:
                entry['standard_french'] = std_french
            else:
                entry['standard_french'] = ''

            # Add dialect
            entry['dialect'] = self.dialect

            # Add source
            entry['source'] = f"Glossaire {self.dialect} (1861)"

        print(f"   ✅ Enriched {len(self.entries)} entries")

    def save_to_csv(self, output_path: str):
        """Save entries to CSV for import."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        print(f"\n💾 Saving to CSV: {output}")

        with open(output, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)

            # Header matching swiss_french_dataset_builder.py format
            writer.writerow([
                'swiss_french',
                'standard_french',
                'dialect',
                'part_of_speech',
                'definition',
                'source',
                'notes'
            ])

            for entry in self.entries:
                writer.writerow([
                    entry.get('word', ''),
                    entry.get('standard_french', ''),
                    entry.get('dialect', self.dialect),
                    entry.get('pos', 'unknown'),
                    entry.get('definition', ''),
                    entry.get('source', 'Glossaire (1861)'),
                    f"Line {entry.get('line_number', 0)}"
                ])

        print(f"   ✅ Saved {len(self.entries)} entries")
        print(f"\n📝 Next step:")
        print(f"   python3 swiss_french_dataset_builder.py --dialect {self.dialect} --import-csv {output}")

    def save_to_json(self, output_path: str):
        """Save entries to JSON for review."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

        print(f"📄 JSON saved to: {output}")

    def generate_statistics(self):
        """Generate extraction statistics."""
        print("\n" + "="*60)
        print("📊 EXTRACTION STATISTICS")
        print("="*60)

        print(f"PDF file: {self.pdf_path.name}")
        print(f"Dialect: {self.dialect}")
        print(f"Total entries extracted: {len(self.entries)}")

        if self.entries:
            # POS distribution
            pos_counts = {}
            for entry in self.entries:
                pos = entry.get('pos', 'unknown')
                pos_counts[pos] = pos_counts.get(pos, 0) + 1

            print(f"\nPart of speech distribution:")
            for pos, count in sorted(pos_counts.items(), key=lambda x: -x[1]):
                print(f"   {pos}: {count}")

            # Entries with standard French
            with_std = sum(1 for e in self.entries if e.get('standard_french'))
            print(f"\nEntries with standard French: {with_std} ({with_std/len(self.entries)*100:.1f}%)")

            # Sample entries
            print(f"\nSample entries:")
            for entry in self.entries[:5]:
                print(f"   {entry['word']} ({entry.get('pos', 'unknown')}): {entry['definition'][:60]}...")

    def process(self, skip_extraction: bool = False, raw_text_path: Optional[str] = None):
        """Complete extraction process."""
        if skip_extraction and raw_text_path:
            # Load pre-extracted text
            print(f"📥 Loading pre-extracted text from: {raw_text_path}")
            with open(raw_text_path, 'r', encoding='utf-8') as f:
                self.raw_text = f.read()
        else:
            # Extract from PDF
            self.raw_text = self.extract_text_from_pdf()

            if not self.raw_text:
                print("❌ Text extraction failed")
                return False

        # Clean text
        lines = self.clean_text(self.raw_text)

        # Find glossary start
        start_idx = self.identify_glossary_start(lines)

        # Parse entries
        self.entries = self.parse_entries(lines, start_idx)

        if not self.entries:
            print("⚠️  No entries found!")
            print("Try manual review of raw text and adjust patterns")
            return False

        # Enrich entries
        self.enrich_entries()

        # Generate statistics
        self.generate_statistics()

        return True


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Extract lexical data from historical Swiss French glossaries (PDF)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from PDF
  %(prog)s --pdf glossaire_vaudois_1861.pdf --dialect vaud

  # Save raw text for manual review
  %(prog)s --pdf glossaire_vaudois_1861.pdf --save-raw raw_text.txt

  # Process pre-extracted text
  %(prog)s --raw-text raw_text.txt --dialect vaud --output vaud_glossary.csv

  # Adjust glossary start manually
  %(prog)s --pdf glossaire.pdf --start-line 50 --output output.csv

Required libraries (install at least one):
  pip install PyPDF2          # Basic PDF extraction
  pip install pdfplumber      # Better layout handling
  pip install pymupdf         # Good for OCR'd PDFs
        """
    )

    parser.add_argument("--pdf", type=str,
                       help="Path to PDF file")
    parser.add_argument("--raw-text", type=str,
                       help="Path to pre-extracted text file")
    parser.add_argument("--dialect", default="vaud",
                       help="Dialect name (default: vaud)")
    parser.add_argument("--output", type=str,
                       help="Output CSV path (default: auto-generated)")
    parser.add_argument("--save-raw", type=str,
                       help="Save raw extracted text to file")
    parser.add_argument("--json", type=str,
                       help="Also save as JSON for review")
    parser.add_argument("--start-line", type=int,
                       help="Manual glossary start line (for fine-tuning)")

    args = parser.parse_args()

    # Validate inputs
    if not args.pdf and not args.raw_text:
        parser.error("Either --pdf or --raw-text must be provided")

    # Initialize extractor
    pdf_path = args.pdf if args.pdf else "dummy.pdf"
    extractor = GlossaryExtractor(pdf_path, args.dialect)

    # Process
    skip_extraction = bool(args.raw_text)
    success = extractor.process(skip_extraction, args.raw_text)

    if not success:
        print("\n❌ Extraction failed")

        # Save raw text for manual review
        if extractor.raw_text and args.save_raw:
            extractor.save_raw_text(args.save_raw)
            print(f"\n💡 Try reviewing raw text and adjusting patterns")

        return

    # Save raw text if requested
    if args.save_raw and extractor.raw_text:
        extractor.save_raw_text(args.save_raw)

    # Save outputs
    if args.output:
        output_csv = args.output
    else:
        output_csv = f"datasets/swiss_french/Raw_Data/extracted_{args.dialect}_glossary.csv"

    extractor.save_to_csv(output_csv)

    # Save JSON if requested
    if args.json:
        extractor.save_to_json(args.json)

    print("\n✅ Extraction complete!")
    print(f"\n📊 Results:")
    print(f"   Entries extracted: {len(extractor.entries)}")
    print(f"   CSV output: {output_csv}")
    if args.json:
        print(f"   JSON output: {args.json}")


if __name__ == "__main__":
    main()
