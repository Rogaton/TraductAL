import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class SimpleTranslator:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
    
    def load_nllb_model(self):
        if self.model_loaded:
            return "Model already loaded"
        
        try:
            model_name = "facebook/nllb-200-1.3B"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name, 
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self.model_loaded = True
            return "✅ NLLB model loaded successfully"
        except Exception as e:
            return f"❌ Error loading model: {str(e)}"
    
    def translate_text(self, text, src_lang, tgt_lang):
        if not self.model_loaded:
            load_result = self.load_nllb_model()
            if "Error" in load_result:
                return load_result
        
        if not text or not text.strip():
            return "Please enter text to translate"
        
        # Language codes for NLLB
        lang_codes = {
            'English': 'eng_Latn', 'French': 'fra_Latn', 'German': 'deu_Latn', 
            'Spanish': 'spa_Latn', 'Italian': 'ita_Latn', 'Portuguese': 'por_Latn',
            'Russian': 'rus_Cyrl', 'Chinese': 'zho_Hans', 'Japanese': 'jpn_Jpan',
            'Korean': 'kor_Hang', 'Arabic': 'arb_Arab', 'Hindi': 'hin_Deva'
        }
        
        src_code = lang_codes.get(src_lang, 'eng_Latn')
        tgt_code = lang_codes.get(tgt_lang, 'fra_Latn')
        
        try:
            # Set source language
            self.tokenizer.src_lang = src_code
            
            # Tokenize input
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=256
            )
            
            # Move to same device as model
            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Generate translation
            with torch.no_grad():
                # Get target language token ID
                tgt_lang_id = self.tokenizer.convert_tokens_to_ids(tgt_code)
                
                generated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=tgt_lang_id,
                    max_new_tokens=256,
                    num_beams=3,
                    early_stopping=True,
                    do_sample=False
                )
            
            # Decode translation
            translation = self.tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
            
            # Clean up the translation (remove source text if duplicated)
            if translation.startswith(text):
                translation = translation[len(text):].strip()
            
            return translation if translation else "Translation failed - please try again"
            
        except Exception as e:
            return f"Translation error: {str(e)}"

# Initialize translator
translator = SimpleTranslator()

# Create simple interface
with gr.Blocks(title="TraductAL Simple", theme=gr.themes.Default()) as demo:
    gr.Markdown("# 🌐 TraductAL - Simple NLLB Translation")
    
    with gr.Row():
        src_lang = gr.Dropdown(
            choices=["English", "French", "German", "Spanish", "Italian", "Portuguese"],
            value="English",
            label="Source Language"
        )
        tgt_lang = gr.Dropdown(
            choices=["English", "French", "German", "Spanish", "Italian", "Portuguese"],
            value="French",
            label="Target Language"
        )
    
    text_input = gr.Textbox(
        label="Text to translate",
        placeholder="Enter your text here...",
        lines=4
    )
    
    translate_btn = gr.Button("Translate", variant="primary")
    
    output = gr.Textbox(
        label="Translation",
        lines=4,
        interactive=False
    )
    
    clear_btn = gr.Button("Clear", variant="secondary")
    
    # Translation function
    translate_btn.click(
        fn=translator.translate_text,
        inputs=[text_input, src_lang, tgt_lang],
        outputs=[output]
    )
    
    # Clear function - properly return empty strings
    def clear_fields():
        return "", ""
    
    clear_btn.click(
        fn=clear_fields,
        outputs=[text_input, output]
    )
    
    # Load model on startup
    demo.load(
        fn=translator.load_nllb_model,
        outputs=[gr.Textbox(visible=False)]  # Hidden status
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7864)
