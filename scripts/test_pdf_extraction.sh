#!/bin/bash
# Quick test script for PDF glossary extraction

echo "📚 PDF Glossary Extraction - Quick Test"
echo "========================================"
echo ""

# Check if PDF file provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <path_to_pdf> [dialect_name]"
    echo ""
    echo "Example:"
    echo "  $0 glossaire_vaudois_1861.pdf vaud"
    echo ""
    exit 1
fi

PDF_FILE="$1"
DIALECT="${2:-vaud}"

# Check if file exists
if [ ! -f "$PDF_FILE" ]; then
    echo "❌ Error: File not found: $PDF_FILE"
    exit 1
fi

echo "📄 PDF file: $PDF_FILE"
echo "🗣️  Dialect: $DIALECT"
echo ""

# Step 1: Check if PDF libraries are installed
echo "Step 1: Checking PDF libraries..."
echo "-----------------------------------"

has_library=false

if python3 -c "import PyPDF2" 2>/dev/null; then
    echo "✅ PyPDF2 installed"
    has_library=true
else
    echo "❌ PyPDF2 not installed (pip install PyPDF2)"
fi

if python3 -c "import pdfplumber" 2>/dev/null; then
    echo "✅ pdfplumber installed"
    has_library=true
else
    echo "❌ pdfplumber not installed (pip install pdfplumber)"
fi

if python3 -c "import fitz" 2>/dev/null; then
    echo "✅ pymupdf installed"
    has_library=true
else
    echo "❌ pymupdf not installed (pip install pymupdf)"
fi

if [ "$has_library" = false ]; then
    echo ""
    echo "❌ No PDF library installed!"
    echo ""
    echo "Install at least one:"
    echo "  pip install PyPDF2          # Simplest"
    echo "  pip install pdfplumber      # Best for layouts"
    echo "  pip install pymupdf         # Best for scanned PDFs"
    echo ""
    echo "Or install all:"
    echo "  pip install PyPDF2 pdfplumber pymupdf"
    exit 1
fi

echo ""

# Step 2: Test extraction (first 10 pages)
echo "Step 2: Testing extraction (first 10 pages)..."
echo "------------------------------------------------"

TEST_RAW="test_extraction_${DIALECT}.txt"

python3 glossary_extractor.py \
    --pdf "$PDF_FILE" \
    --save-raw "$TEST_RAW" \
    --dialect "$DIALECT" 2>&1 | head -50

if [ ! -f "$TEST_RAW" ]; then
    echo ""
    echo "❌ Extraction failed - no text file created"
    exit 1
fi

echo ""
echo "✅ Raw text saved to: $TEST_RAW"
echo ""

# Step 3: Show sample of extracted text
echo "Step 3: Sample of extracted text (first 30 lines):"
echo "---------------------------------------------------"
head -30 "$TEST_RAW"
echo ""
echo "[... more lines in $TEST_RAW ...]"
echo ""

# Step 4: Analyze text
echo "Step 4: Quick analysis:"
echo "------------------------"

total_chars=$(wc -c < "$TEST_RAW")
total_lines=$(wc -l < "$TEST_RAW")

echo "Total characters: $total_chars"
echo "Total lines: $total_lines"

if [ "$total_chars" -lt 100 ]; then
    echo ""
    echo "⚠️  WARNING: Very little text extracted!"
    echo ""
    echo "Possible reasons:"
    echo "  1. PDF is image-based (scanned) - needs OCR"
    echo "  2. PDF has security restrictions"
    echo "  3. Wrong file format"
    echo ""
    echo "Solutions:"
    echo "  1. Run OCR: ocrmypdf $PDF_FILE ${PDF_FILE%.pdf}_ocr.pdf --language fra"
    echo "  2. Try online OCR: https://www.onlineocr.net/"
    echo "  3. Convert with Google Drive: Upload → Open with Google Docs → Download as PDF"
else
    echo "✅ Extraction looks good!"
fi

echo ""

# Step 5: Check for glossary patterns
echo "Step 5: Looking for glossary patterns..."
echo "----------------------------------------"

# Look for uppercase words (typical glossary entries)
uppercase_words=$(grep -c '^[A-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÆŒÇ]' "$TEST_RAW" || echo "0")
echo "Lines starting with uppercase: $uppercase_words"

# Look for common patterns
echo ""
echo "Pattern detection:"
grep -E '^[A-Z]+.*\b(m\.|f\.|n\.|adj\.|v\.)\b' "$TEST_RAW" | head -5 || echo "  No entries found with gender markers"

echo ""

# Step 6: Recommendations
echo "Step 6: Recommendations:"
echo "------------------------"

if [ "$total_chars" -lt 100 ]; then
    echo "❌ Need to run OCR first"
    echo "   Command: ocrmypdf $PDF_FILE ${PDF_FILE%.pdf}_ocr.pdf --language fra"
elif [ "$uppercase_words" -lt 10 ]; then
    echo "⚠️  Few uppercase words found - check if glossary starts later in PDF"
    echo "   Review $TEST_RAW and find where glossary actually starts"
    echo "   Look for patterns like 'A.', 'ABAISER', etc."
else
    echo "✅ Ready for full extraction!"
    echo ""
    echo "Run full extraction with:"
    echo "  python3 glossary_extractor.py \\"
    echo "    --pdf $PDF_FILE \\"
    echo "    --dialect $DIALECT"
fi

echo ""
echo "================================================================"
echo "Test complete! Review $TEST_RAW to verify quality"
echo "================================================================"
