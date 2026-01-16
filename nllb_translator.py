#!/usr/bin/env python3
"""
Enhanced Offline Neural Machine Translation System
Supports both MT5 and NLLB-200 models for professional translation
Optimized for linguists and translators working with sensitive documents
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    print("✅ Required packages loaded successfully")
except ImportError as e:
    print("❌ Error: Required packages not installed")
    print("Please activate conda environment: conda activate neural_mt_offline")
    sys.exit(1)

try:
    from text_chunker import SmartTextChunker
except ImportError:
    # Chunker not available, will use basic sentence splitting
    SmartTextChunker = None

class EnhancedOfflineTranslator:
    """Enhanced offline neural machine translator supporting MT5 and NLLB-200."""
    
    def __init__(self, models_dir="./models/deployed_models"):
        self.models_dir = Path(models_dir)
        self.models = {}
        self.tokenizers = {}
        self.current_model = None
        self.current_model_name = None
        
        # NLLB-200 language codes (subset of most common ones)
        self.nllb_languages = {
            'en': 'eng_Latn',    # English
            'fr': 'fra_Latn',    # French  
            'de': 'deu_Latn',    # German
            'es': 'spa_Latn',    # Spanish
            'it': 'ita_Latn',    # Italian
            'pt': 'por_Latn',    # Portuguese
            'ru': 'rus_Cyrl',    # Russian
            'zh': 'zho_Hans',    # Chinese (Simplified)
            'ja': 'jpn_Jpan',    # Japanese
            'ko': 'kor_Hang',    # Korean
            'ar': 'arb_Arab',    # Arabic
            'hi': 'hin_Deva',    # Hindi
            'tr': 'tur_Latn',    # Turkish
            'pl': 'pol_Latn',    # Polish
            'nl': 'nld_Latn',    # Dutch
            'sv': 'swe_Latn',    # Swedish
            'da': 'dan_Latn',    # Danish
            'no': 'nor_Latn',    # Norwegian
            'fi': 'fin_Latn',    # Finnish
            'cs': 'ces_Latn',    # Czech
            'hu': 'hun_Latn',    # Hungarian
            'ro': 'ron_Latn',    # Romanian
            'bg': 'bul_Cyrl',    # Bulgarian
            'hr': 'hrv_Latn',    # Croatian
            'sk': 'slk_Latn',    # Slovak
            'sl': 'slv_Latn',    # Slovenian
            'et': 'est_Latn',    # Estonian
            'lv': 'lav_Latn',    # Latvian
            'lt': 'lit_Latn',    # Lithuanian
            'el': 'ell_Grek',    # Greek
            'he': 'heb_Hebr',    # Hebrew
            'th': 'tha_Thai',    # Thai
            'vi': 'vie_Latn',    # Vietnamese
            'id': 'ind_Latn',    # Indonesian
            'ms': 'zsm_Latn',    # Malay
            'tl': 'tgl_Latn',    # Filipino
            'sw': 'swh_Latn',    # Swahili
            'am': 'amh_Ethi',    # Amharic
            'yo': 'yor_Latn',    # Yoruba
            'ig': 'ibo_Latn',    # Igbo
            'ha': 'hau_Latn',    # Hausa
            'zu': 'zul_Latn',    # Zulu
            'af': 'afr_Latn',    # Afrikaans
            'is': 'isl_Latn',    # Icelandic
            'mt': 'mlt_Latn',    # Maltese
            'cy': 'cym_Latn',    # Welsh
            'ga': 'gle_Latn',    # Irish
            'eu': 'eus_Latn',    # Basque
            'ca': 'cat_Latn',    # Catalan
            'gl': 'glg_Latn',    # Galician
        }
        
        # Language names for display
        self.language_names = {
            'en': 'English', 'fr': 'French', 'de': 'German', 'es': 'Spanish',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh': 'Chinese',
            'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi',
            'tr': 'Turkish', 'pl': 'Polish', 'nl': 'Dutch', 'sv': 'Swedish',
            'da': 'Danish', 'no': 'Norwegian', 'fi': 'Finnish', 'cs': 'Czech',
            'hu': 'Hungarian', 'ro': 'Romanian', 'bg': 'Bulgarian', 'hr': 'Croatian',
            'sk': 'Slovak', 'sl': 'Slovenian', 'et': 'Estonian', 'lv': 'Latvian',
            'lt': 'Lithuanian', 'el': 'Greek', 'he': 'Hebrew', 'th': 'Thai',
            'vi': 'Vietnamese', 'id': 'Indonesian', 'ms': 'Malay', 'tl': 'Filipino',
            'sw': 'Swahili', 'am': 'Amharic', 'yo': 'Yoruba', 'ig': 'Igbo',
            'ha': 'Hausa', 'zu': 'Zulu', 'af': 'Afrikaans', 'is': 'Icelandic',
            'mt': 'Maltese', 'cy': 'Welsh', 'ga': 'Irish', 'eu': 'Basque',
            'ca': 'Catalan', 'gl': 'Galician'
        }
        
        print("🌍 Enhanced Offline Neural MT System")
        print("🔒 Complete privacy - all processing happens locally")
        print(f"📁 Models directory: {self.models_dir}")
        
        # Detect available models
        self.detect_available_models()
    
    def detect_available_models(self):
        """Detect which models are available."""
        self.available_models = {}
        
        # Check for NLLB models with correct naming
        nllb_models = [
            "nllb_200_1.3b", "nllb_200_3.3b", "nllb_200_distilled_1.3b"
        ]
        
        for model_name in nllb_models:
            model_path = self.models_dir / model_name
            if model_path.exists() and any(model_path.iterdir()):
                self.available_models[model_name] = {
                    "path": model_path,
                    "type": "NLLB-200",
                    "languages": len(self.nllb_languages),
                    "quality": "High" if "3.3b" in model_name else "Very Good"
                }
        
        # Check for MT5 models
        mt5_models = ["mt5_small", "mt5_base", "t5_small", "t5_base"]
        
        for model_name in mt5_models:
            model_path = self.models_dir / model_name
            if model_path.exists() and any(model_path.iterdir()):
                self.available_models[model_name] = {
                    "path": model_path,
                    "type": "MT5/T5",
                    "languages": 101 if "mt5" in model_name else 50,
                    "quality": "Good" if "small" in model_name else "Very Good"
                }
        
        print(f"🔍 Found {len(self.available_models)} available models:")
        for name, info in self.available_models.items():
            print(f"  ✅ {name} ({info['type']}) - {info['languages']} languages")
    
    def load_model(self, model_name):
        """Load a translation model."""
        if model_name not in self.available_models:
            print(f"❌ Model not found: {model_name}")
            return False
        
        if model_name in self.models:
            self.current_model = self.models[model_name]
            self.current_model_name = model_name
            print(f"✅ Switched to cached model: {model_name}")
            return True
        
        model_path = self.available_models[model_name]["path"]
        
        try:
            print(f"⏳ Loading model: {model_name}")
            start_time = time.time()
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            
            # Move to GPU if available
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = model.to(device)
            
            load_time = time.time() - start_time
            
            # Cache the model
            self.models[model_name] = model
            self.tokenizers[model_name] = tokenizer
            self.current_model = model
            self.current_model_name = model_name
            
            print(f"✅ Model loaded in {load_time:.1f}s")
            print(f"📊 Parameters: {model.num_parameters():,}")
            print(f"💾 Device: {device}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model {model_name}: {str(e)}")
            return False
    
    def translate_nllb(self, text, src_lang, tgt_lang):
        """Translate using NLLB-200 model with smart chunking for long texts."""
        if src_lang not in self.nllb_languages or tgt_lang not in self.nllb_languages:
            return f"❌ Language not supported. Available: {list(self.nllb_languages.keys())}"

        tokenizer = self.tokenizers[self.current_model_name]
        tokenizer.src_lang = self.nllb_languages[src_lang]

        # Use smart chunking if available
        if SmartTextChunker:
            chunker = SmartTextChunker(max_tokens=400, tokenizer=tokenizer)
            chunks = chunker.chunk_text(text)

            # If text was chunked, show info
            if len(chunks) > 1:
                print(f"📝 Long text detected: splitting into {len(chunks)} chunks for optimal translation")
        else:
            # Fallback to basic sentence splitting
            import re
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            chunks = [(s, 'sentence') for s in sentences if s.strip()]

        translations = []
        device = next(self.current_model.parameters()).device
        tgt_lang_code = self.nllb_languages[tgt_lang]
        forced_bos_token_id = getattr(tokenizer, 'lang_code_to_id', {}).get(tgt_lang_code) or tokenizer.convert_tokens_to_ids(tgt_lang_code)

        for i, (chunk, chunk_type) in enumerate(chunks, 1):
            if not chunk.strip():
                continue

            # Show progress for long texts
            if len(chunks) > 5 and i % 5 == 0:
                print(f"   Progress: {i}/{len(chunks)} chunks translated...")

            inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                generated_tokens = self.current_model.generate(
                    **inputs,
                    forced_bos_token_id=forced_bos_token_id,
                    max_length=512,
                    num_beams=5,
                    early_stopping=True,
                    no_repeat_ngram_size=2
                )

            translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            translations.append(translation)

        if len(chunks) > 1:
            print(f"✅ Translation complete: {len(chunks)} chunks processed")

        # Join translations, preserving paragraph breaks for paragraph-level chunks
        if SmartTextChunker and any(ct == 'paragraph' for _, ct in chunks):
            # Preserve paragraph structure
            result = []
            for translation, (_, chunk_type) in zip(translations, chunks):
                result.append(translation)
                if chunk_type == 'paragraph':
                    result.append('\n\n')
            return ''.join(result).strip()
        else:
            # Standard sentence joining
            return ' '.join(translations)
    
    def translate_mt5(self, text, src_lang, tgt_lang):
        """Translate using MT5/T5 model."""
        tokenizer = self.tokenizers[self.current_model_name]
        
        # Format prompt for T5/MT5
        src_name = self.language_names.get(src_lang, src_lang)
        tgt_name = self.language_names.get(tgt_lang, tgt_lang)
        prompt = f"translate {src_name} to {tgt_name}: {text}"
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Move to same device as model
        device = next(self.current_model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate translation
        with torch.no_grad():
            generated_tokens = self.current_model.generate(
                **inputs,
                max_length=512,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
        
        # Decode translation
        translation = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        return translation
    
    def translate(self, text, src_lang, tgt_lang, model_name=None):
        """Main translation function."""
        if not text.strip():
            return "❌ Empty text provided"
        
        # Load model if specified or use current
        if model_name and model_name != self.current_model_name:
            if not self.load_model(model_name):
                return f"❌ Failed to load model: {model_name}"
        
        if not self.current_model:
            # Auto-select best available model
            # Priority: nllb_200_3.3b > nllb_200_1.3b > nllb_200_distilled_1.3b > others
            if any("nllb" in name for name in self.available_models):
                # Prefer 3.3B model for best quality
                if "nllb_200_3.3b" in self.available_models:
                    best_model = "nllb_200_3.3b"
                elif "nllb_200_1.3b" in self.available_models:
                    best_model = "nllb_200_1.3b"
                elif "nllb_200_distilled_1.3b" in self.available_models:
                    best_model = "nllb_200_distilled_1.3b"
                else:
                    best_model = next(name for name in self.available_models if "nllb" in name)
            else:
                best_model = next(iter(self.available_models))

            if not self.load_model(best_model):
                return "❌ No models available"
        
        # Validate languages
        if src_lang not in self.language_names or tgt_lang not in self.language_names:
            return f"❌ Unsupported language. Available: {list(self.language_names.keys())}"
        
        try:
            start_time = time.time()
            
            # Choose translation method based on model type
            model_type = self.available_models[self.current_model_name]["type"]
            
            if "NLLB" in model_type:
                translation = self.translate_nllb(text, src_lang, tgt_lang)
            else:
                translation = self.translate_mt5(text, src_lang, tgt_lang)
            
            translation_time = time.time() - start_time
            
            return {
                "translation": translation,
                "model": self.current_model_name,
                "model_type": model_type,
                "time": f"{translation_time:.2f}s",
                "src_lang": f"{src_lang} ({self.language_names[src_lang]})",
                "tgt_lang": f"{tgt_lang} ({self.language_names[tgt_lang]})"
            }
            
        except Exception as e:
            return f"❌ Translation failed: {str(e)}"
    
    def list_models(self):
        """List all available models."""
        if not self.available_models:
            print("❌ No models found")
            return
        
        print("\n📋 Available Models:")
        print("=" * 60)
        
        for name, info in self.available_models.items():
            status = "🟢 LOADED" if name == self.current_model_name else "⚪ Available"
            print(f"{status} {name}")
            print(f"   Type: {info['type']}")
            print(f"   Languages: {info['languages']}")
            print(f"   Quality: {info['quality']}")
            print()
    
    def list_languages(self):
        """List supported languages."""
        print("\n🌍 Supported Languages:")
        print("=" * 40)
        
        for code, name in sorted(self.language_names.items()):
            nllb_support = "✅" if code in self.nllb_languages else "⚠️ "
            print(f"{nllb_support} {code}: {name}")
        
        print(f"\n✅ = Full NLLB-200 support")
        print(f"⚠️  = MT5/T5 support only")

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Enhanced Offline Neural Machine Translation")
    parser.add_argument("src_lang", nargs="?", help="Source language code (e.g., en, fr, de)")
    parser.add_argument("tgt_lang", nargs="?", help="Target language code (e.g., en, fr, de)")
    parser.add_argument("text", nargs="?", help="Text to translate")
    parser.add_argument("--model", help="Specific model to use")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--list-languages", action="store_true", help="List supported languages")
    parser.add_argument("--clean", action="store_true", help="Output only translation")
    
    args = parser.parse_args()
    
    # Initialize translator
    translator = EnhancedOfflineTranslator()
    
    # Handle list commands
    if args.list_models:
        translator.list_models()
        return
    
    if args.list_languages:
        translator.list_languages()
        return
    
    # Check required arguments for translation
    if not all([args.src_lang, args.tgt_lang, args.text]):
        parser.error("src_lang, tgt_lang, and text are required for translation")
    
    # Perform translation
    result = translator.translate(args.text, args.src_lang, args.tgt_lang, args.model)
    
    if args.clean:
        if isinstance(result, dict):
            print(result["translation"])
        else:
            print(result)
    else:
        if isinstance(result, dict):
            print(f"🔤 Original ({result['src_lang']}): {args.text}")
            print(f"🌍 Translation ({result['tgt_lang']}): {result['translation']}")
            print(f"🤖 Model: {result['model']} ({result['model_type']})")
            print(f"⏱️  Time: {result['time']}")
        else:
            print(result)

if __name__ == "__main__":
    main()
