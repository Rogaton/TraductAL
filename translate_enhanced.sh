#!/bin/bash
# Enhanced Translation Shell Wrapper
# Supports both MT5 and NLLB-200 models

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSLATOR="$SCRIPT_DIR/nllb_translator.py"

# Check if translator exists
if [ ! -f "$TRANSLATOR" ]; then
    echo "❌ Translator script not found: $TRANSLATOR"
    exit 1
fi

# Function to show help
show_help() {
    echo "🌍 Enhanced Offline Neural Machine Translation"
    echo "Usage: $0 [OPTIONS] <src_lang> <tgt_lang> <text>"
    echo ""
    echo "Options:"
    echo "  clean              - Output only translation"
    echo "  interactive        - Interactive translation mode"
    echo "  list-models        - Show available models"
    echo "  list-languages     - Show supported languages"
    echo "  check              - System health check"
    echo "  help               - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 en fr "Hello world""
    echo "  $0 clean en de "Good morning""
    echo "  $0 list-models"
    echo "  $0 interactive en fr"
}

# Function for interactive mode
interactive_mode() {
    local src_lang="$1"
    local tgt_lang="$2"
    
    echo "🔄 Interactive Translation Mode"
    echo "Source: $src_lang → Target: $tgt_lang"
    echo "Type 'quit' to exit"
    echo ""
    
    while true; do
        echo -n "Enter text to translate: "
        read -r text
        
        if [ "$text" = "quit" ] || [ "$text" = "exit" ]; then
            echo "👋 Goodbye!"
            break
        fi
        
        if [ -n "$text" ]; then
            python3 "$TRANSLATOR" "$src_lang" "$tgt_lang" "$text" --clean
            echo ""
        fi
    done
}

# Function for system check
system_check() {
    echo "🔍 System Health Check"
    echo "====================="
    
    # Check Python and packages
    if python3 -c "import torch, transformers" 2>/dev/null; then
        echo "✅ Python packages: OK"
    else
        echo "❌ Python packages: Missing dependencies"
    fi
    
    # Check models
    python3 "$TRANSLATOR" --list-models
    
    # Check disk space
    echo ""
    echo "💾 Disk Usage:"
    du -sh "$SCRIPT_DIR/models" 2>/dev/null || echo "No models directory found"
    
    # Check memory
    echo ""
    echo "🧠 System Memory:"
    free -h | head -2
}

# Main logic
case "$1" in
    "help"|"-h"|"--help")
        show_help
        ;;
    "check")
        system_check
        ;;
    "list-models")
        python3 "$TRANSLATOR" --list-models
        ;;
    "list-languages")
        python3 "$TRANSLATOR" --list-languages
        ;;
    "interactive")
        if [ $# -lt 3 ]; then
            echo "❌ Usage: $0 interactive <src_lang> <tgt_lang>"
            exit 1
        fi
        interactive_mode "$2" "$3"
        ;;
    "clean")
        if [ $# -lt 4 ]; then
            echo "❌ Usage: $0 clean <src_lang> <tgt_lang> <text>"
            exit 1
        fi
        python3 "$TRANSLATOR" "$2" "$3" "$4" --clean
        ;;
    *)
        if [ $# -lt 3 ]; then
            echo "❌ Usage: $0 <src_lang> <tgt_lang> <text>"
            echo "Run '$0 help' for more information"
            exit 1
        fi
        python3 "$TRANSLATOR" "$1" "$2" "$3"
        ;;
esac
