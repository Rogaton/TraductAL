#!/usr/bin/env python3
"""
Batch News Translator for Graubünden News
Translate news articles from German to Romansh and vice versa
"""

import os
import sys
import argparse
from pathlib import Path
import time
import warnings
warnings.filterwarnings("ignore")

try:
    from unified_translator import UnifiedTranslator
    print("✅ Unified translator loaded")
except ImportError as e:
    print(f"❌ Error loading translator: {e}")
    sys.exit(1)


class NewsTranslator:
    """Batch translator for news articles."""

    def __init__(self):
        self.translator = UnifiedTranslator()

    def translate_file(self, input_file, output_file, src_lang, tgt_lang, preserve_structure=True):
        """
        Translate a text file line by line.

        Args:
            input_file: Path to input text file
            output_file: Path to output translation file
            src_lang: Source language code
            tgt_lang: Target language code
            preserve_structure: Keep empty lines and structure
        """
        input_path = Path(input_file)
        output_path = Path(output_file)

        if not input_path.exists():
            print(f"❌ Input file not found: {input_file}")
            return False

        print(f"📰 Translating: {input_path.name}")
        print(f"   {src_lang} → {tgt_lang}")
        print(f"   Output: {output_path}")
        print()

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            translations = []
            total_lines = len(lines)
            translated_count = 0
            start_time = time.time()

            for i, line in enumerate(lines, 1):
                # Progress indicator
                if i % 10 == 0 or i == total_lines:
                    print(f"  Progress: {i}/{total_lines} lines...", end='\r')

                # Handle empty lines
                if not line.strip():
                    if preserve_structure:
                        translations.append("")
                    continue

                # Translate
                result = self.translator.translate(
                    line.strip(),
                    src_lang,
                    tgt_lang
                )

                if "error" in result:
                    print(f"\n⚠️  Warning: Line {i} failed: {result['error']}")
                    translations.append(f"[TRANSLATION ERROR: {line.strip()}]")
                else:
                    translations.append(result.get("translation", ""))
                    translated_count += 1

            # Write output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(translations))

            elapsed_time = time.time() - start_time

            print(f"\n✅ Translation complete!")
            print(f"   Translated: {translated_count}/{total_lines} lines")
            print(f"   Time: {elapsed_time:.2f}s")
            print(f"   Output: {output_path}")

            return True

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def translate_directory(self, input_dir, output_dir, src_lang, tgt_lang, pattern="*.txt"):
        """
        Translate all files in a directory.

        Args:
            input_dir: Path to directory with input files
            output_dir: Path to output directory
            src_lang: Source language code
            tgt_lang: Target language code
            pattern: File pattern to match (default: *.txt)
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        if not input_path.exists():
            print(f"❌ Input directory not found: {input_dir}")
            return False

        files = list(input_path.glob(pattern))

        if not files:
            print(f"⚠️  No files matching '{pattern}' found in {input_dir}")
            return False

        print(f"📁 Found {len(files)} files to translate")
        print()

        output_path.mkdir(parents=True, exist_ok=True)

        success_count = 0
        for file_path in files:
            output_file = output_path / file_path.name

            if self.translate_file(file_path, output_file, src_lang, tgt_lang):
                success_count += 1
            print()

        print(f"🎉 Batch translation complete!")
        print(f"   Success: {success_count}/{len(files)} files")

        return True

    def translate_article(self, text, src_lang, tgt_lang, split_paragraphs=True):
        """
        Translate a full article with paragraph structure.

        Args:
            text: Article text
            src_lang: Source language code
            tgt_lang: Target language code
            split_paragraphs: Translate paragraph by paragraph

        Returns:
            Translated article text
        """
        if split_paragraphs:
            paragraphs = text.split('\n\n')
            translations = []

            for i, para in enumerate(paragraphs, 1):
                if not para.strip():
                    translations.append("")
                    continue

                print(f"  Translating paragraph {i}/{len(paragraphs)}...", end='\r')

                result = self.translator.translate(para.strip(), src_lang, tgt_lang)

                if "error" in result:
                    translations.append(f"[ERROR: {para.strip()}]")
                else:
                    translations.append(result.get("translation", ""))

            print()
            return '\n\n'.join(translations)
        else:
            # Translate entire article at once
            result = self.translator.translate(text, src_lang, tgt_lang)
            if "error" in result:
                return f"ERROR: {result['error']}"
            return result.get("translation", "")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Batch News Translator for Graubünden News",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate a single file
  %(prog)s --file article.txt --output article_rm.txt --src de --tgt rm-sursilv

  # Translate all .txt files in a directory
  %(prog)s --dir news/ --output-dir news_translated/ --src de --tgt rm-sursilv

  # Translate article text directly
  %(prog)s --text "Guten Tag" --src de --tgt rm-sursilv
        """
    )

    parser.add_argument("--file", help="Input file to translate")
    parser.add_argument("--dir", help="Input directory to translate")
    parser.add_argument("--output", help="Output file (for --file)")
    parser.add_argument("--output-dir", help="Output directory (for --dir)")
    parser.add_argument("--text", help="Text to translate directly")
    parser.add_argument("--src", required=True, help="Source language (de, en, fr, etc.)")
    parser.add_argument("--tgt", required=True, help="Target language (rm-sursilv, de, etc.)")
    parser.add_argument("--pattern", default="*.txt", help="File pattern for --dir (default: *.txt)")

    args = parser.parse_args()

    translator = NewsTranslator()

    # Translate single file
    if args.file:
        if not args.output:
            # Auto-generate output name
            input_path = Path(args.file)
            args.output = input_path.stem + f"_{args.tgt}" + input_path.suffix

        translator.translate_file(
            args.file,
            args.output,
            args.src,
            args.tgt
        )

    # Translate directory
    elif args.dir:
        if not args.output_dir:
            args.output_dir = Path(args.dir).name + "_translated"

        translator.translate_directory(
            args.dir,
            args.output_dir,
            args.src,
            args.tgt,
            args.pattern
        )

    # Translate text
    elif args.text:
        result = translator.translator.translate(
            args.text,
            args.src,
            args.tgt
        )

        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"Original ({args.src}): {args.text}")
            print(f"Translation ({args.tgt}): {result['translation']}")

    else:
        parser.error("Must specify --file, --dir, or --text")


if __name__ == "__main__":
    main()
