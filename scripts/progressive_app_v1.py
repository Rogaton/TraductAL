import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5Tokenizer, T5ForConditionalGeneration

class MultiModelTranslator:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        
        self.available_models = {
            "nllb-200-1.3B": {
                "model_name": "facebook/nllb-200-1.3B",
                "type": "nllb"
            },
            "nllb-200-3.3B": {
                "model_name": "facebook/nllb-200-3.3B", 
                "type": "nllb"
            },
            "t5-base": {
                "model_name": "t5-base",
                "type": "t5"
            }
        }
    
    def load_model(self, model_key):
        if model_key in self.models:
            return f"✅ {model_key} already loaded"
        
        if model_key not in self.available_models:
            return f"❌ Model {model_key} not available"
        
        try:
            config = self.available_models[model_key]
            model_name = config["model_name"]
            
            if config["type"] == "nllb":
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    model_name, 
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
            elif config["type"] == "t5":
                tokenizer = T5Tokenizer.from_pretrained(model_name)
                model = T5ForConditionalGeneration.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
            
            self.models[model_key] = model
            self.tokenizers[model_key] = tokenizer
            return f"✅ {model_key} loaded successfully"
            
        except Exception as e:
            return f"❌ Error loading {model_key}: {str(e)}"
    
    def translate_text(self, text, src_lang, tgt_lang, model_key):
        if not text or not text.strip():
            return "Please enter text to translate"
        
        # Load model if needed
        load_result = self.load_model(model_key)
        if "Error" in load_result:
            return load_result
        
        model = self.models[model_key]
        tokenizer = self.tokenizers[model_key]
        config = self.available_models[model_key]
        
        try:
            if config["type"] == "nllb":
                return self._translate_nllb(text, src_lang, tgt_lang, model, tokenizer)
            elif config["type"] == "t5":
                return self._translate_t5(text, src_lang, tgt_lang, model, tokenizer)
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def _translate_nllb(self, text, src_lang, tgt_lang, model, tokenizer):
        lang_codes = {
            'English': 'eng_Latn', 'French': 'fra_Latn', 'German': 'deu_Latn', 
            'Spanish': 'spa_Latn', 'Italian': 'ita_Latn', 'Portuguese': 'por_Latn'
        }
        
        src_code = lang_codes.get(src_lang, 'eng_Latn')
        tgt_code = lang_codes.get(tgt_lang, 'fra_Latn')
        
        tokenizer.src_lang = src_code
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
        
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            tgt_lang_id = tokenizer.convert_tokens_to_ids(tgt_code)
            generated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=tgt_lang_id,
                max_new_tokens=256,
                num_beams=3,
                early_stopping=True
            )
        
        translation = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        
        # Clean up duplication
        if translation.startswith(text):
            translation = translation[len(text):].strip()
        
        return f"[NLLB] {translation}" if translation else "Translation failed"
    
    def _translate_t5(self, text, src_lang, tgt_lang, model, tokenizer):
        # T5 uses task prefixes
        input_text = f"translate {src_lang.lower()} to {tgt_lang.lower()}: {text}"
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=256, num_beams=3)
        
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return f"[T5] {translation}"

# Initialize translator
translator = MultiModelTranslator()

# Create interface with model selection
with gr.Blocks(title="TraductAL Progressive v1", theme=gr.themes.Default()) as demo:
    gr.Markdown("# 🌐 TraductAL - Multi-Model Translation (Progressive v1)")
    
    with gr.Row():
        model_choice = gr.Dropdown(
            choices=list(translator.available_models.keys()),
            value="nllb-200-1.3B",
            label="🤖 Translation Model"
        )
    
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
        inputs=[text_input, src_lang, tgt_lang, model_choice],
        outputs=[output]
    )
    
    # Clear function
    def clear_fields():
        return "", ""
    
    clear_btn.click(
        fn=clear_fields,
        outputs=[text_input, output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7865)
