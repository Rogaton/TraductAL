#!/usr/bin/env python3
"""
Janus-SWI-Prolog Interface for Glossary Parser

Uses Janus (official Python-SWI-Prolog bridge) to interface with
the DCG-based glossary parser.

Author: Adapted for Swiss French Vaudois glossary extraction
Requires: SWI-Prolog 9.0+ with Janus support
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional
import csv
import json

try:
    from janus_swi import *
    JANUS_AVAILABLE = True
except ImportError:
    print("⚠️  Janus not available. Install SWI-Prolog 9.0+ with Janus support.")
    print("   Or use fallback Python parser.")
    JANUS_AVAILABLE = False


class JanusGlossaryParser:
    """DCG-based glossary parser using Janus-SWI-Prolog."""

    def __init__(self, grammar_file: str = "grammar.pl", lexicon_file: str = "lexicon.pl"):
        """Initialize Janus interface and load Prolog modules."""
        if not JANUS_AVAILABLE:
            raise ImportError("Janus not available. Install SWI-Prolog with Janus.")

        self.grammar_file = Path(grammar_file)
        self.lexicon_file = Path(lexicon_file)

        # Load Prolog modules
        print("🔧 Loading Prolog modules...")
        try:
            # Consult grammar
            query_once(f"consult('{self.grammar_file}')")
            print(f"   ✅ Loaded: {self.grammar_file}")

            # Consult lexicon
            query_once(f"consult('{self.lexicon_file}')")
            print(f"   ✅ Loaded: {self.lexicon_file}")

        except Exception as e:
            print(f"   ❌ Error loading Prolog modules: {e}")
            raise

    def parse_entry(self, text: str) -> Optional[Dict]:
        """Parse a single glossary entry using DCG grammar."""
        try:
            # Escape quotes in text
            text_escaped = text.replace("'", "\\'")

            # Query Prolog parser
            result = query_once(
                f"glossary_grammar:parse_entry_from_string('{text_escaped}', Entry)"
            )

            if result:
                return self._prolog_entry_to_dict(result.get('Entry'))
            return None

        except Exception as e:
            print(f"⚠️  Parse error: {e}")
            return None

    def _prolog_entry_to_dict(self, prolog_entry) -> Dict:
        """Convert Prolog entry structure to Python dict."""
        # Prolog entry format: entry(Headword, POS, Definition, Metadata)
        if not prolog_entry:
            return {}

        return {
            'headword': str(prolog_entry.args[0]),
            'pos': str(prolog_entry.args[1]),
            'definition': str(prolog_entry.args[2]),
            'metadata': str(prolog_entry.args[3])
        }

    def parse_file(self, input_file: str) -> List[Dict]:
        """Parse entire glossary file."""
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

    def add_to_lexicon(self, entry: Dict):
        """Add parsed entry to Prolog lexicon."""
        try:
            # Convert dict back to Prolog term
            headword = entry['headword']
            pos = entry['pos']
            definition = entry['definition']

            query_once(
                f"glossary_lexicon:add_lexeme(entry('{headword}', {pos}, '{definition}', metadata([], none, [])))"
            )
        except Exception as e:
            print(f"⚠️  Error adding to lexicon: {e}")

    def export_lexicon_to_csv(self, output_file: str):
        """Export Prolog lexicon to CSV."""
        print(f"\n💾 Exporting lexicon to CSV: {output_file}")

        try:
            query_once(f"glossary_lexicon:export_to_csv('{output_file}')")
            print(f"   ✅ Exported to: {output_file}")
        except Exception as e:
            print(f"   ❌ Export failed: {e}")

    def get_lexicon_statistics(self) -> Dict:
        """Get statistics from Prolog lexicon."""
        try:
            result = query_once("glossary_lexicon:lexicon_statistics(Stats)")
            if result:
                return result.get('Stats', {})
            return {}
        except Exception as e:
            print(f"⚠️  Error getting statistics: {e}")
            return {}

    def save_lexicon(self, filename: str):
        """Save Prolog lexicon to file."""
        try:
            query_once(f"glossary_lexicon:save_lexicon('{filename}')")
            print(f"✅ Lexicon saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving lexicon: {e}")

    def load_lexicon(self, filename: str):
        """Load Prolog lexicon from file."""
        try:
            query_once(f"glossary_lexicon:load_lexicon('{filename}')")
            print(f"✅ Lexicon loaded from: {filename}")
        except Exception as e:
            print(f"❌ Error loading lexicon: {e}")


class FallbackPythonParser:
    """
    Fallback parser when Janus is not available.
    Uses simpler Python regex-based parsing.
    """

    def __init__(self):
        print("⚠️  Using fallback Python parser (Janus not available)")

    def parse_entry(self, text: str) -> Optional[Dict]:
        """Simple regex-based parsing."""
        import re

        # Pattern 1: WORD, pos. Definition
        pattern1 = r'^([A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ][a-zàâäéèêëïîôöùûüÿæœç\-\s\(\)]+),\s*(s\.[mfn]\.|v\.[a-z]+\.|adj\.|adv\.)\s*(.+)$'
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
        description="DCG-based glossary parser using Janus-SWI-Prolog"
    )

    parser.add_argument("--input", required=True,
                       help="Input text file (raw glossary text)")
    parser.add_argument("--output", required=True,
                       help="Output CSV file")
    parser.add_argument("--grammar", default="grammar.pl",
                       help="Grammar file (default: grammar.pl)")
    parser.add_argument("--lexicon", default="lexicon.pl",
                       help="Lexicon file (default: lexicon.pl)")
    parser.add_argument("--save-prolog", type=str,
                       help="Save Prolog lexicon to file")
    parser.add_argument("--fallback", action="store_true",
                       help="Use fallback Python parser (no Janus)")

    args = parser.parse_args()

    # Initialize parser
    if args.fallback or not JANUS_AVAILABLE:
        parser = FallbackPythonParser()
    else:
        parser = JanusGlossaryParser(args.grammar, args.lexicon)

    # Parse input
    entries = parser.parse_file(args.input)

    # Add to lexicon (if using Janus)
    if isinstance(parser, JanusGlossaryParser):
        print("\n📚 Building lexicon...")
        for entry in entries:
            parser.add_to_lexicon(entry)

        # Get statistics
        stats = parser.get_lexicon_statistics()
        print(f"\n📊 Lexicon statistics:")
        print(f"   {stats}")

        # Save Prolog lexicon if requested
        if args.save_prolog:
            parser.save_lexicon(args.save_prolog)

        # Export to CSV
        parser.export_lexicon_to_csv(args.output)
    else:
        # Fallback: save directly to CSV
        with open(args.output, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['headword', 'pos', 'definition'])
            writer.writeheader()
            writer.writerows(entries)
        print(f"✅ Saved {len(entries)} entries to {args.output}")

    print("\n✅ Parsing complete!")


if __name__ == "__main__":
    main()
