import gradio as gr
from multi_model_translator import MultiModelTranslator

# Global translator
translator = MultiModelTranslator()

def translate_text(text, src_lang, tgt_lang, model_choice):
    if not text.strip():
        return "Please enter text to translate"
    
    try:
        result = translator.translate(text, src_lang, tgt_lang, model_choice)
        if "error" in result:
            return f"Error: {result['error']}"
        return f"[{result.get('model', 'Unknown')}] {result['translation']}"
    except Exception as e:
        return f"Translation error: {str(e)}"

def update_languages(model_choice):
    """Update language options based on selected model"""
    supported_langs = translator.get_supported_languages(model_choice)
    lang_names = {
        'en': 'English', 'fr': 'French', 'de': 'German', 'es': 'Spanish',
        'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh': 'Chinese',
        'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi'
    }
    
    choices = [lang_names.get(code, code.upper()) for code in supported_langs]
    return gr.update(choices=choices), gr.update(choices=choices)

# Create interface
with gr.Blocks(title="TraductAL - Multi-Model Translation") as demo:
    gr.Markdown("# TraductAL - Multi-Model Neural Machine Translation")
    gr.Markdown("🚀 **Enhanced Version** - Multiple open-source translation models")
    
    with gr.Row():
        model_choice = gr.Dropdown(
            choices=translator.get_available_models(),
            value="nllb-200-1.3B",
            label="Translation Model"
        )
    
    with gr.Row():
        src_lang = gr.Dropdown(
            choices=["English", "French", "German", "Spanish", "Italian", "Portuguese", 
                    "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi"],
            value="English",
            label="Source Language"
        )
        tgt_lang = gr.Dropdown(
            choices=["English", "French", "German", "Spanish", "Italian", "Portuguese", 
                    "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi"],
            value="French",
            label="Target Language"
        )
    
    text_input = gr.Textbox(
        label="Text to translate", 
        placeholder="Enter text here...",
        lines=3
    )
    
    translate_btn = gr.Button("Translate", variant="primary")
    
    output = gr.Textbox(
        label="Translation", 
        interactive=False,
        lines=3
    )
    
    # Language mapping
    lang_map = {
        "English": "en", "French": "fr", "German": "de", "Spanish": "es",
        "Italian": "it", "Portuguese": "pt", "Russian": "ru", "Chinese": "zh",
        "Japanese": "ja", "Korean": "ko", "Arabic": "ar", "Hindi": "hi"
    }
    
    # Update languages when model changes
    model_choice.change(
        fn=update_languages,
        inputs=[model_choice],
        outputs=[src_lang, tgt_lang]
    )
    
    # Translation function
    translate_btn.click(
        fn=lambda text, src, tgt, model: translate_text(
            text, 
            lang_map.get(src, src.lower()), 
            lang_map.get(tgt, tgt.lower()), 
            model
        ),
        inputs=[text_input, src_lang, tgt_lang, model_choice],
        outputs=output
    )
    
    # Model information
    with gr.Accordion("Model Information", open=False):
        gr.Markdown("""
        **Available Models:**
        - **NLLB-200-1.3B/3.3B**: Facebook's No Language Left Behind - 200 languages
        - **mBART-50**: Multilingual BART - 50 languages  
        - **T5-Base**: Google's Text-to-Text Transfer Transformer
        - **OPUS-MT**: Helsinki-NLP's multilingual models
        
        **Note**: First use of each model requires download time.
        """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
