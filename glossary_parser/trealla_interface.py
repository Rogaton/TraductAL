#!/usr/bin/env python3
"""
Trealla Prolog Interface for Glossary Parser

Drop-in replacement for Janus interface that uses Trealla Prolog
via subprocess communication instead of Janus.

Author: Adapted for Trealla Prolog compatibility
Requires: Trealla Prolog installed (tpl command available)
"""

import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
import csv
import re


class TreallaGlossaryParser:
    """DCG-based glossary parser using Trealla Prolog via subprocess."""

    def __init__(self, grammar_file: str = "grammar.pl", lexicon_file: str = "lexicon.pl"):
        """Initialize Trealla interface."""
        self.grammar_file = Path(grammar_file)
        self.lexicon_file = Path(lexicon_file)

        # Check if Trealla is available
        if not self._check_trealla_available():
            raise RuntimeError("Trealla Prolog (tpl) not found in PATH")

        print("🔧 Trealla Prolog interface initialized")
        print(f"   Grammar: {self.grammar_file}")
        print(f"   Lexicon: {self.lexicon_file}")

    def _check_trealla_available(self) -> bool:
        """Check if tpl command is available."""
        try:
            result = subprocess.run(
                ['tpl', '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _query_trealla(self, query: str, consult_files: List[str] = None) -> Optional[Dict]:
        """
        Execute a Prolog query in Trealla and parse the result.

        Args:
            query: Prolog query to execute
            consult_files: List of .pl files to consult before query

        Returns:
            Dictionary with query results or None
        """
        try:
            # Build Prolog program
            prolog_code = ""

            # Add file consultations
            if consult_files:
                for file in consult_files:
                    prolog_code += f":- consult('{file}').\n"

            # Add query
            prolog_code += f":- {query}, halt(0).\n"
            prolog_code += ":- halt(1).\n"  # Fail case

            # Execute with Trealla
            result = subprocess.run(
                ['tpl'],
                input=prolog_code,
                capture_output=True,
                text=True,
                timeout=10
            )

            # Parse output
            if result.returncode == 0:
                return {'success': True, 'output': result.stdout}
            else:
                return {'success': False, 'error': result.stderr}

        except subprocess.TimeoutExpired:
            print("⚠️  Trealla query timeout")
            return None
        except Exception as e:
            print(f"⚠️  Trealla query error: {e}")
            return None

    def parse_entry(self, text: str) -> Optional[Dict]:
        """
        Parse a single glossary entry using DCG grammar.

        Note: This uses a simplified regex-based fallback since
        Trealla subprocess communication is less efficient for
        per-entry parsing. For full DCG parsing, use parse_file_with_trealla().
        """
        return self._fallback_parse_entry(text)

    def _fallback_parse_entry(self, text: str) -> Optional[Dict]:
        """Simple regex-based parsing (fast fallback)."""
        # Pattern 1: WORD, pos. Definition
        pattern1 = r'^([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇa-zàâäéèêëïîôöùûüÿæœç\-\s\(\)]*),\s*(s\.[mfn]\.|v\.[a-z]+\.|adj\.|adv\.)\s*(.+)$'
        match = re.match(pattern1, text)

        if match:
            return {
                'headword': match.group(1).strip(),
                'pos': match.group(2).strip(),
                'definition': match.group(3).strip(),
                'metadata': {}
            }

        # Pattern 2: WORD. Definition (no POS)
        pattern2 = r'^([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇa-zàâäéèêëïîôöùûüÿæœç\-\s\(\)]*)\.\s+(.+)$'
        match = re.match(pattern2, text)

        if match:
            return {
                'headword': match.group(1).strip(),
                'pos': 'unknown',
                'definition': match.group(2).strip(),
                'metadata': {}
            }

        return None

    def parse_file_with_trealla(self, input_file: str, output_file: str) -> List[Dict]:
        """
        Parse entire file using Trealla's standalone parser.
        This uses the parse_glossary.pl script directly.
        """
        print(f"\n📖 Parsing with Trealla: {input_file}")

        try:
            # Use the standalone Trealla parser script
            parser_script = Path(__file__).parent / "parse_glossary_trealla.pl"

            result = subprocess.run(
                ['tpl', str(parser_script), input_file, output_file],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print(f"   ✅ Trealla parsing complete")
                print(result.stdout)

                # Read back the parsed CSV
                return self._read_csv_results(output_file)
            else:
                print(f"   ❌ Trealla parsing failed: {result.stderr}")
                return []

        except subprocess.TimeoutExpired:
            print("   ⚠️  Trealla parsing timeout (>2 minutes)")
            return []
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []

    def _read_csv_results(self, csv_file: str) -> List[Dict]:
        """Read parsed results from CSV."""
        entries = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entries.append({
                        'headword': row.get('swiss_french', ''),
                        'pos': row.get('part_of_speech', 'unknown'),
                        'definition': row.get('definition', ''),
                        'standard_french': row.get('standard_french', ''),
                        'metadata': {
                            'dialect': row.get('dialect', ''),
                            'source': row.get('source', ''),
                            'notes': row.get('notes', '')
                        }
                    })
        except Exception as e:
            print(f"⚠️  Error reading CSV: {e}")

        return entries

    def parse_file(self, input_file: str) -> List[Dict]:
        """
        Parse entire glossary file.
        Uses fast regex-based parsing for compatibility.
        """
        print(f"\n📖 Parsing glossary file: {input_file}")

        entries = []
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total = len(lines)
        for i, line in enumerate(lines, 1):
            if i % 100 == 0:
                print(f"   Processing line {i}/{total}...")

            line = line.strip()
            if not line:
                continue

            entry = self.parse_entry(line)
            if entry:
                entries.append(entry)

        print(f"   ✅ Parsed {len(entries)} entries from {total} lines")
        return entries

    def parse_multiline_entries(self, text: str) -> List[Dict]:
        """
        Parse text with multi-line entries.
        Uses heuristics to group lines into complete entries.
        """
        lines = text.split('\n')
        entries = []
        current_entry_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line starts a new entry (uppercase word at start)
            if line and line[0].isupper() and current_entry_lines:
                # Process accumulated entry
                entry_text = ' '.join(current_entry_lines)
                entry = self.parse_entry(entry_text)
                if entry:
                    entries.append(entry)

                # Start new entry
                current_entry_lines = [line]
            else:
                # Continue current entry
                current_entry_lines.append(line)

        # Don't forget last entry
        if current_entry_lines:
            entry_text = ' '.join(current_entry_lines)
            entry = self.parse_entry(entry_text)
            if entry:
                entries.append(entry)

        return entries

    def get_lexicon_statistics(self) -> Dict:
        """Get statistics (simplified for Trealla)."""
        return {
            'backend': 'trealla',
            'note': 'Full lexicon statistics require DCG integration'
        }


class FallbackPythonParser:
    """
    Fallback parser when neither Janus nor Trealla are available.
    Uses simpler Python regex-based parsing.
    """

    def __init__(self):
        print("⚠️  Using fallback Python parser (no Prolog backend)")

    def parse_entry(self, text: str) -> Optional[Dict]:
        """Simple regex-based parsing."""
        import re

        # Pattern 1: WORD, pos. Definition
        pattern1 = r'^([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇa-zàâäéèêëïîôöùûüÿæœç\-\s\(\)]*),\s*(s\.[mfn]\.|v\.[a-z]+\.|adj\.|adv\.)\s*(.+)$'
        match = re.match(pattern1, text)

        if match:
            return {
                'headword': match.group(1).strip(),
                'pos': match.group(2).strip(),
                'definition': match.group(3).strip(),
                'metadata': {}
            }

        return None

    def parse_file(self, input_file: str) -> List[Dict]:
        """Parse file with fallback parser."""
        entries = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                entry = self.parse_entry(line.strip())
                if entry:
                    entries.append(entry)
        return entries


def main():
    """CLI interface for glossary parser."""
    import argparse

    parser = argparse.ArgumentParser(
        description="DCG-based glossary parser using Trealla Prolog"
    )

    parser.add_argument("--input", required=True,
                       help="Input text file (raw glossary text)")
    parser.add_argument("--output", required=True,
                       help="Output CSV file")
    parser.add_argument("--grammar", default="grammar.pl",
                       help="Grammar file (default: grammar.pl)")
    parser.add_argument("--lexicon", default="lexicon.pl",
                       help="Lexicon file (default: lexicon.pl)")
    parser.add_argument("--backend", choices=['trealla', 'fallback'], default='trealla',
                       help="Parser backend (default: trealla)")

    args = parser.parse_args()

    # Initialize parser
    if args.backend == 'trealla':
        try:
            parser_obj = TreallaGlossaryParser(args.grammar, args.lexicon)
        except RuntimeError as e:
            print(f"⚠️  {e}")
            print("   Falling back to Python parser")
            parser_obj = FallbackPythonParser()
    else:
        parser_obj = FallbackPythonParser()

    # Parse input
    entries = parser_obj.parse_file(args.input)

    # Save to CSV (remove metadata field for CSV output)
    with open(args.output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['headword', 'pos', 'definition'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(entries)

    print(f"\n✅ Saved {len(entries)} entries to {args.output}")
    print("✅ Parsing complete!")


if __name__ == "__main__":
    main()
