import gradio as gr
import os
import time
from pathlib import Path
from multi_model_translator import MultiModelTranslator
import PyPDF2
import docx
import json

# Global translator and state
translator = MultiModelTranslator()
translation_history = []

def translate_text_with_progress(text, src_lang, tgt_lang, model_choice, progress=gr.Progress()):
    if not text.strip():
        return "Please enter text to translate", ""
    
    progress(0.1, desc="Initializing...")
    
    try:
        progress(0.3, desc=f"Loading {model_choice}...")
        result = translator.translate(text, src_lang, tgt_lang, model_choice)
        
        progress(0.8, desc="Generating translation...")
        time.sleep(0.5)  # Brief pause for UX
        
        if "error" in result:
            progress(1.0, desc="Error occurred")
            return f"Error: {result['error']}", ""
        
        translation = f"[{result.get('model', 'Unknown')}] {result['translation']}"
        
        # Add to history
        translation_history.append({
            "source": text,
            "target": translation,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang,
            "model": model_choice,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        progress(1.0, desc="Translation complete!")
        return translation, create_history_display()
        
    except Exception as e:
        progress(1.0, desc="Translation failed")
        return f"Translation error: {str(e)}", ""

def extract_text_from_file(file):
    if file is None:
        return "No file uploaded"
    
    file_path = Path(file.name)
    
    try:
        if file_path.suffix.lower() == '.pdf':
            with open(file.name, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        
        elif file_path.suffix.lower() == '.docx':
            doc = docx.Document(file.name)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file_path.suffix.lower() == '.txt':
            with open(file.name, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            return "Unsupported file format. Please use PDF, DOCX, or TXT files."
            
    except Exception as e:
        return f"Error reading file: {str(e)}"

def clear_all():
    return "", "", "", ""

def create_history_display():
    if not translation_history:
        return "No translations yet"
    
    history_text = "## Translation History\n\n"
    for i, entry in enumerate(reversed(translation_history[-5:]), 1):  # Last 5 entries
        history_text += f"**{i}.** [{entry['timestamp']}] {entry['src_lang']}→{entry['tgt_lang']} ({entry['model']})\n"
        history_text += f"*Source:* {entry['source'][:100]}{'...' if len(entry['source']) > 100 else ''}\n"
        history_text += f"*Translation:* {entry['target'][:100]}{'...' if len(entry['target']) > 100 else ''}\n\n"
    
    return history_text

def export_history():
    if not translation_history:
        return None
    
    export_data = {
        "export_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_translations": len(translation_history),
        "translations": translation_history
    }
    
    filename = f"translation_history_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return filename

def save_translation_as_file(translation_text):
    if not translation_text:
        return None
    
    filename = f"translation_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(translation_text)
    
    return filename

# Language mapping
lang_map = {
    "English": "en", "French": "fr", "German": "de", "Spanish": "es",
    "Italian": "it", "Portuguese": "pt", "Russian": "ru", "Chinese": "zh",
    "Japanese": "ja", "Korean": "ko", "Arabic": "ar", "Hindi": "hi"
}

# Create professional interface
with gr.Blocks(title="TraductAL Professional", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌐 TraductAL Professional - Multi-Model Translation Suite")
    gr.Markdown("*Professional neural machine translation with multiple open-source models*")
    
    with gr.Tab("Translation"):
        with gr.Row():
            model_choice = gr.Dropdown(
                choices=translator.get_available_models(),
                value="nllb-200-1.3B",
                label="🤖 Translation Model",
                info="Select your preferred translation model"
            )
            
        with gr.Row():
            src_lang = gr.Dropdown(
                choices=list(lang_map.keys()),
                value="English",
                label="📝 Source Language"
            )
            tgt_lang = gr.Dropdown(
                choices=list(lang_map.keys()),
                value="French",
                label="🎯 Target Language"
            )
        
        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(
                    label="📄 Text to translate",
                    placeholder="Enter your text here or upload a file...",
                    lines=6,
                    max_lines=10
                )
                
                with gr.Row():
                    file_upload = gr.File(
                        label="📎 Upload File (PDF, DOCX, TXT)",
                        file_types=[".pdf", ".docx", ".txt"]
                    )
            
            with gr.Column(scale=2):
                output = gr.Textbox(
                    label="🔄 Translation",
                    interactive=False,
                    lines=6,
                    max_lines=10
                )
        
        with gr.Row():
            translate_btn = gr.Button("🚀 Translate", variant="primary", size="lg")
            clear_btn = gr.Button("🗑️ Clear All", variant="secondary")
            download_btn = gr.Button("💾 Download Translation", variant="secondary")
        
        # File upload handler
        file_upload.change(
            fn=extract_text_from_file,
            inputs=[file_upload],
            outputs=[text_input]
        )
        
        # Translation with progress
        translate_btn.click(
            fn=translate_text_with_progress,
            inputs=[text_input, src_lang, tgt_lang, model_choice],
            outputs=[output, gr.State()]
        )
        
        # Clear function
        clear_btn.click(
            fn=clear_all,
            outputs=[text_input, output, file_upload, gr.State()]
        )
        
        # Download translation
        download_btn.click(
            fn=save_translation_as_file,
            inputs=[output],
            outputs=[gr.File()]
        )
    
    with gr.Tab("History & Export"):
        history_display = gr.Markdown("No translations yet")
        
        with gr.Row():
            refresh_history_btn = gr.Button("🔄 Refresh History")
            export_btn = gr.Button("📤 Export History (JSON)")
        
        refresh_history_btn.click(
            fn=create_history_display,
            outputs=[history_display]
        )
        
        export_btn.click(
            fn=export_history,
            outputs=[gr.File()]
        )
    
    with gr.Tab("Model Information"):
        gr.Markdown("""
        ## 🔧 Available Translation Models
        
        | Model | Size | Languages | Best For |
        |-------|------|-----------|----------|
        | **NLLB-200-1.3B** | 1.3B | 200+ | Multilingual, balanced quality/speed |
        | **NLLB-200-3.3B** | 3.3B | 200+ | High quality, slower |
        | **mBART-50** | 610M | 50 | European/Asian languages |
        | **T5-Base** | 220M | Major languages | Fast, general purpose |
        | **OPUS-MT** | 300M | European languages | Specialized pairs |
        
        ## 📋 Supported File Formats
        - **PDF**: Automatic text extraction
        - **DOCX**: Microsoft Word documents  
        - **TXT**: Plain text files
        
        ## 💡 Tips
        - Start with smaller models for faster loading
        - Use NLLB for rare language pairs
        - Export history for translation memory
        - Upload files up to 10MB
        """)
    
    with gr.Tab("Settings"):
        gr.Markdown("## ⚙️ Application Settings")
        
        with gr.Row():
            max_length = gr.Slider(
                minimum=128,
                maximum=2048,
                value=512,
                step=128,
                label="Max Translation Length"
            )
            
            beam_size = gr.Slider(
                minimum=1,
                maximum=8,
                value=4,
                step=1,
                label="Beam Search Size (Quality vs Speed)"
            )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7861,
        share=False,
        show_error=True
    )
