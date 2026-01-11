import gradio as gr
import torch
import gc
import psutil
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import time

class DiagnosticTranslator:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.loading_status = {}
    
    def check_system_resources(self):
        """Check available system resources"""
        memory = psutil.virtual_memory()
        return {
            "total_ram": f"{memory.total / (1024**3):.1f} GB",
            "available_ram": f"{memory.available / (1024**3):.1f} GB",
            "used_ram": f"{memory.used / (1024**3):.1f} GB",
            "cpu_count": psutil.cpu_count(),
            "gpu_available": torch.cuda.is_available(),
            "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
        }
    
    def load_model_with_diagnostics(self, model_name="facebook/nllb-200-1.3B"):
        """Load model with detailed diagnostics"""
        if model_name in self.models:
            return f"✅ {model_name} already loaded"
        
        try:
            # Clear memory first
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            resources_before = self.check_system_resources()
            start_time = time.time()
            
            # Step 1: Load tokenizer
            yield f"🔄 Loading tokenizer for {model_name}..."
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            yield f"✅ Tokenizer loaded ({time.time() - start_time:.1f}s)"
            
            # Step 2: Load model with specific settings
            yield f"🔄 Loading model weights (this may take 5-15 minutes)..."
            
            # Try different loading strategies
            try:
                # Strategy 1: Auto device map
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    low_cpu_mem_usage=True
                )
                yield f"✅ Model loaded with auto device mapping"
            except Exception as e1:
                yield f"⚠️ Auto device mapping failed: {str(e1)[:100]}"
                try:
                    # Strategy 2: CPU only
                    model = AutoModelForSeq2SeqLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float32,
                        device_map="cpu",
                        low_cpu_mem_usage=True
                    )
                    yield f"✅ Model loaded on CPU"
                except Exception as e2:
                    yield f"❌ CPU loading failed: {str(e2)[:100]}"
                    return
            
            # Store model and tokenizer
            self.models[model_name] = model
            self.tokenizers[model_name] = tokenizer
            
            resources_after = self.check_system_resources()
            total_time = time.time() - start_time
            
            yield f"""✅ Model loaded successfully!
            
**Loading Summary:**
- Time taken: {total_time:.1f} seconds
- RAM before: {resources_before['used_ram']}
- RAM after: {resources_after['used_ram']}
- Model location: {'GPU' if next(model.parameters()).is_cuda else 'CPU'}
- Ready for translation!"""
            
        except Exception as e:
            yield f"❌ Loading failed: {str(e)}"
    
    def translate_simple(self, text, src_lang="en", tgt_lang="fr", model_name="facebook/nllb-200-1.3B"):
        """Simple translation with error handling"""
        if model_name not in self.models:
            return "❌ Model not loaded. Please load model first."
        
        if not text.strip():
            return "Please enter text to translate"
        
        try:
            model = self.models[model_name]
            tokenizer = self.tokenizers[model_name]
            
            # NLLB language codes
            lang_codes = {
                'en': 'eng_Latn', 'fr': 'fra_Latn', 'de': 'deu_Latn', 
                'es': 'spa_Latn', 'it': 'ita_Latn', 'pt': 'por_Latn'
            }
            
            src_code = lang_codes.get(src_lang, 'eng_Latn')
            tgt_code = lang_codes.get(tgt_lang, 'fra_Latn')
            
            tokenizer.src_lang = src_code
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
            
            # Move inputs to same device as model
            device = next(model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    forced_bos_token_id=tokenizer.lang_code_to_id[tgt_code],
                    max_length=256,
                    num_beams=2,  # Reduced for speed
                    early_stopping=True
                )
            
            translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return f"✅ Translation: {translation}"
            
        except Exception as e:
            return f"❌ Translation error: {str(e)}"

# Initialize diagnostic translator
diagnostic = DiagnosticTranslator()

# Create diagnostic interface
with gr.Blocks(title="TraductAL Diagnostics") as demo:
    gr.Markdown("# 🔧 TraductAL Model Diagnostics")
    gr.Markdown("*Diagnose and fix model loading issues*")
    
    with gr.Tab("System Check"):
        system_info = gr.Textbox(label="System Information", lines=10)
        check_btn = gr.Button("🔍 Check System Resources")
        
        def show_system_info():
            info = diagnostic.check_system_resources()
            return f"""**System Resources:**
- Total RAM: {info['total_ram']}
- Available RAM: {info['available_ram']}
- Used RAM: {info['used_ram']}
- CPU Cores: {info['cpu_count']}
- GPU Available: {info['gpu_available']}
- GPU Count: {info['gpu_count']}

**Recommendations:**
- Minimum 16GB RAM for NLLB-1.3B
- 32GB+ RAM recommended for multiple models
- GPU optional but speeds up inference"""
        
        check_btn.click(fn=show_system_info, outputs=[system_info])
    
    with gr.Tab("Model Loading"):
        loading_output = gr.Textbox(label="Loading Progress", lines=15)
        load_btn = gr.Button("🚀 Load NLLB-200-1.3B Model", variant="primary")
        
        load_btn.click(
            fn=diagnostic.load_model_with_diagnostics,
            outputs=[loading_output]
        )
    
    with gr.Tab("Quick Test"):
        with gr.Row():
            test_input = gr.Textbox(label="Test Text", value="Hello, how are you?")
            test_output = gr.Textbox(label="Translation Result")
        
        with gr.Row():
            src_lang = gr.Dropdown(choices=["en", "fr", "de", "es"], value="en", label="Source")
            tgt_lang = gr.Dropdown(choices=["en", "fr", "de", "es"], value="fr", label="Target")
        
        test_btn = gr.Button("🧪 Test Translation")
        
        test_btn.click(
            fn=diagnostic.translate_simple,
            inputs=[test_input, src_lang, tgt_lang],
            outputs=[test_output]
        )
    
    with gr.Tab("Troubleshooting"):
        gr.Markdown("""
        ## 🛠️ Common Issues & Solutions
        
        **Model loading stalls at 100%:**
        - Insufficient RAM (need 16GB+ for 1.3B model)
        - Try CPU-only loading
        - Close other applications
        - Restart the application
        
        **Out of Memory errors:**
        - Reduce batch size
        - Use torch.float16 instead of float32
        - Enable low_cpu_mem_usage=True
        
        **Slow performance:**
        - Model loaded on CPU instead of GPU
        - Large input text (try shorter segments)
        - Multiple models loaded simultaneously
        
        **Quick fixes:**
        1. Restart Python kernel
        2. Clear GPU cache: `torch.cuda.empty_cache()`
        3. Use smaller model first (T5-base)
        4. Check available disk space
        """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7862)
