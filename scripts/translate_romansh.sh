#!/bin/bash
# TraductAL Unified Translator - Shell Wrapper
# Combines NLLB-200 + Apertus8B for Romansh translation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"

# Activate virtual environment
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "❌ Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Run unified translator
python "$SCRIPT_DIR/unified_translator.py" "$@"
