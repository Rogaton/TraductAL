#!/bin/bash
# Setup script for Janus-SWI-Prolog interface
# Checks installation and provides guidance

echo "🔧 Janus-SWI-Prolog Setup Checker"
echo "=================================="
echo ""

# Check SWI-Prolog
echo "1. Checking SWI-Prolog..."
if command -v swipl &> /dev/null; then
    VERSION=$(swipl --version | head -1)
    echo "   ✅ Found: $VERSION"

    # Check if version is 9.0+
    MAJOR=$(swipl --version | grep -oP '\d+\.\d+' | head -1 | cut -d'.' -f1)
    if [ "$MAJOR" -ge 9 ]; then
        echo "   ✅ Version 9.0+ (Janus compatible)"
    else
        echo "   ⚠️  Version $MAJOR (need 9.0+ for Janus)"
        echo ""
        echo "   Install newer version:"
        echo "   sudo apt-add-repository ppa:swi-prolog/stable"
        echo "   sudo apt-get update"
        echo "   sudo apt-get install swi-prolog"
    fi
else
    echo "   ❌ SWI-Prolog not found"
    echo ""
    echo "   Install with:"
    echo "   sudo apt-add-repository ppa:swi-prolog/stable"
    echo "   sudo apt-get update"
    echo "   sudo apt-get install swi-prolog"
fi

echo ""

# Check Janus Python module
echo "2. Checking Janus Python module..."
if python3 -c "from janus_swi import *" 2>/dev/null; then
    echo "   ✅ Janus Python module installed"
else
    echo "   ❌ Janus Python module not found"
    echo ""
    echo "   Install with:"
    echo "   pip install janus-swi"
    echo ""
    echo "   Or if using venv:"
    echo "   source /home/aldn/Apertus8B/alvenv/bin/activate"
    echo "   pip install janus-swi"
fi

echo ""

# Test Janus
echo "3. Testing Janus integration..."
python3 << 'EOF'
try:
    from janus_swi import *

    # Test simple query
    result = query_once("member(X, [1,2,3])")
    if result:
        print("   ✅ Janus works! Test query successful")
        print(f"      Result: {result}")
    else:
        print("   ⚠️  Janus loaded but query failed")
except ImportError:
    print("   ❌ Cannot import janus_swi")
except Exception as e:
    print(f"   ❌ Janus error: {e}")
EOF

echo ""

# Check if Prolog files exist
echo "4. Checking Prolog grammar files..."
if [ -f "grammar.pl" ]; then
    echo "   ✅ grammar.pl found"
else
    echo "   ❌ grammar.pl not found"
fi

if [ -f "lexicon.pl" ]; then
    echo "   ✅ lexicon.pl found"
else
    echo "   ❌ lexicon.pl not found"
fi

echo ""

# Summary
echo "=================================="
echo "📊 Summary"
echo "=================================="

ALL_OK=true

if command -v swipl &> /dev/null; then
    echo "✅ SWI-Prolog: OK"
else
    echo "❌ SWI-Prolog: MISSING"
    ALL_OK=false
fi

if python3 -c "from janus_swi import *" 2>/dev/null; then
    echo "✅ Janus Python: OK"
else
    echo "❌ Janus Python: MISSING"
    ALL_OK=false
fi

if [ -f "grammar.pl" ] && [ -f "lexicon.pl" ]; then
    echo "✅ Prolog files: OK"
else
    echo "❌ Prolog files: MISSING"
    ALL_OK=false
fi

echo ""

if [ "$ALL_OK" = true ]; then
    echo "🎉 All dependencies installed!"
    echo ""
    echo "Ready to run:"
    echo "  python3 janus_interface.py --input ../raw_glossaire_vaud.txt --output output.csv"
else
    echo "⚠️  Some dependencies missing. Follow instructions above."
fi

echo ""
