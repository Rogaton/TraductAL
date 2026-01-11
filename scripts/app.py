import gradio as gr
import subprocess
import os
from nllb_translator import EnhancedOfflineTranslator

# Global translator variable
translator = None

def ensure_models_downloaded():
    """Download models if not present"""
    if not os.path.exists("models/deployed_models"):
        try:
            subprocess.run(["python3", "download_nllb_200.py"], check=True)
            return "Models downloaded successfully"
        except Exception as e:
            return f"Model download failed: {str(e)}"
    return "Models already available"

def translate_text(text, src_lang, tgt_lang):
    if not text.strip():
        return "Please enter text to translate"
    
    try:
        global translator
        if translator is None:
            # Ensure models are downloaded first
            download_status = ensure_models_downloaded()
            if "failed" in download_status:
                return download_status
            
            # Initialize translator
            translator = EnhancedOfflineTranslator()
        
        result = translator.translate(text, src_lang, tgt_lang)
        return result["translation"]
    except Exception as e:
        return f"Translation error: {str(e)}"

# Language options
languages = {
    "English": "en",
    "French": "fr", 
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Swedish": "sv",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar"
}

# Create interface
with gr.Blocks(title="TraductAL - Offline Neural Translation") as demo:
    gr.Markdown("# TraductAL - Offline Neural Machine Translation")
    gr.Markdown("⚠️ **Development Version** - Use at your own risk. Translations may be incomplete.")
    gr.Markdown("🔄 First translation may take several minutes while models download...")
    gr.Markdown("ℹ️ **Basic Interface** - 12 mainstream languages. For 65+ languages use `./start_gradio.sh`")
    
    with gr.Row():
        src_lang = gr.Dropdown(choices=list(languages.keys()), value="English", label="Source Language")
        tgt_lang = gr.Dropdown(choices=list(languages.keys()), value="French", label="Target Language")
    
    text_input = gr.Textbox(label="Text to translate", placeholder="Enter text here...")
    translate_btn = gr.Button("Translate", variant="primary")
    output = gr.Textbox(label="Translation", interactive=False)
    
    translate_btn.click(
        fn=lambda text, src, tgt: translate_text(text, languages[src], languages[tgt]),
        inputs=[text_input, src_lang, tgt_lang],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()
