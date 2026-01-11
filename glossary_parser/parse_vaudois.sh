#!/bin/bash
# parse_vaudois.sh
# Wrapper script for parse_glossary.pl with user-friendly syntax

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
INPUT=""
OUTPUT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--input)
            INPUT="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 -i INPUT_FILE -o OUTPUT_FILE"
            echo ""
            echo "Options:"
            echo "  -i, --input FILE    Input text file (raw glossary)"
            echo "  -o, --output FILE   Output CSV file"
            echo "  -h, --help          Show this help"
            echo ""
            echo "Example:"
            echo "  $0 -i raw_glossaire_vaud.txt -o vaud-glossary.csv"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h for help"
            exit 1
            ;;
    esac
done

# Check required arguments
if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "Error: Both -i INPUT and -o OUTPUT are required"
    echo "Use -h for help"
    exit 1
fi

# Check input file exists
if [ ! -f "$INPUT" ]; then
    echo "Error: Input file not found: $INPUT"
    exit 1
fi

# Run the Prolog parser
echo "📖 Parsing glossary with DCG parser..."
echo "   Input:  $INPUT"
echo "   Output: $OUTPUT"
echo ""

swipl -s "$SCRIPT_DIR/parse_glossary.pl" \
      -g "main(['-i', '$INPUT', '-o', '$OUTPUT']), halt" \
      2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Success! Parsed entries saved to: $OUTPUT"
else
    echo ""
    echo "❌ Parsing failed with exit code: $EXIT_CODE"
    exit $EXIT_CODE
fi
