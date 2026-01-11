#!/bin/bash
# Start Gradio Web Interface for TraductAL Romansh Translation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"

echo "============================================================"
echo "🇨🇭 TraductAL Romansh Translation System"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Activate virtual environment
echo "⏳ Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Check if gradio is installed
if ! python -c "import gradio" 2>/dev/null; then
    echo "❌ Gradio not installed"
    echo "   Run: pip install gradio librosa"
    exit 1
fi

echo "✅ Environment ready"
echo ""
echo "📡 Starting Gradio interface..."
echo "   Server will be available at: http://localhost:7860"
echo "   Press Ctrl+C to stop"
echo ""
echo "============================================================"
echo ""

# Start Gradio app
cd "$SCRIPT_DIR"
python gradio_app.py
