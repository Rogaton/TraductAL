#!/usr/bin/env python3
"""
Multi-Model Translation System - Fixed Version
Supports NLLB, BART, mBART, T5, and other open-source translation models
"""

import os
import torch
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM, 
    MBartForConditionalGeneration, MBart50TokenizerFast,
    T5ForConditionalGeneration, T5Tokenizer,
    pipeline
)
from pathlib import Path

class MultiModelTranslator:
    def __init__(self, models_dir="./models"):
        self.models_dir = Path(models_dir)
        self.models = {}
        self.tokenizers = {}
        
        # Available models configuration
        self.available_models = {
            "nllb-200-1.3B": {
                "model_name": "facebook/nllb-200-1.3B",
                "type": "nllb",
                "languages": self._get_nllb_languages()
            },
            "nllb-200-3.3B": {
                "model_name": "facebook/nllb-200-3.3B", 
                "type": "nllb",
                "languages": self._get_nllb_languages()
            },
            "mbart-large-50": {
                "model_name": "facebook/mbart-large-50-many-to-many-mmt",
                "type": "mbart",
                "languages": self._get_mbart_languages()
            },
            "t5-base": {
                "model_name": "t5-base",
                "type": "t5",
                "languages": {"en": "en", "fr": "fr", "de": "de", "es": "es"}
            },
            "opus-mt": {
                "model_name": "Helsinki-NLP/opus-mt-en-mul",
                "type": "opus",
                "languages": {"en": "en", "fr": "fr", "de": "de", "es": "es", "it": "it"}
            }
        }
    
    def _get_nllb_languages(self):
        return {
            'en': 'eng_Latn', 'fr': 'fra_Latn', 'de': 'deu_Latn', 'es': 'spa_Latn',
            'it': 'ita_Latn', 'pt': 'por_Latn', 'ru': 'rus_Cyrl', 'zh': 'zho_Hans',
            'ja': 'jpn_Jpan', 'ko': 'kor_Hang', 'ar': 'arb_Arab', 'hi': 'hin_Deva'
        }
    
    def _get_mbart_languages(self):
        return {
            'en': 'en_XX', 'fr': 'fr_XX', 'de': 'de_DE', 'es': 'es_XX',
            'it': 'it_IT', 'pt': 'pt_XX', 'ru': 'ru_RU', 'zh': 'zh_CN',
            'ja': 'ja_XX', 'ko': 'ko_KR', 'ar': 'ar_AR', 'hi': 'hi_IN'
        }
    
    def load_model(self, model_key):
        """Load specified model"""
        if model_key in self.models:
            return True
            
        if model_key not in self.available_models:
            raise ValueError(f"Model {model_key} not available")
        
        config = self.available_models[model_key]
        model_name = config["model_name"]
        
        try:
            if config["type"] == "nllb":
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.float16)
            
            elif config["type"] == "mbart":
                tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
                model = MBartForConditionalGeneration.from_pretrained(model_name, torch_dtype=torch.float16)
            
            elif config["type"] == "t5":
                tokenizer = T5Tokenizer.from_pretrained(model_name)
                model = T5ForConditionalGeneration.from_pretrained(model_name, torch_dtype=torch.float16)
            
            elif config["type"] == "opus":
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.float16)
            
            self.models[model_key] = model
            self.tokenizers[model_key] = tokenizer
            print(f"✅ Loaded {model_key}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load {model_key}: {e}")
            return False
    
    def translate(self, text, src_lang, tgt_lang, model_key="nllb-200-1.3B"):
        """Translate text using specified model"""
        if not self.load_model(model_key):
            return {"error": f"Failed to load {model_key}"}
        
        config = self.available_models[model_key]
        model = self.models[model_key]
        tokenizer = self.tokenizers[model_key]
        
        try:
            if config["type"] == "nllb":
                return self._translate_nllb_fixed(text, src_lang, tgt_lang, model, tokenizer, config)
            elif config["type"] == "mbart":
                return self._translate_mbart(text, src_lang, tgt_lang, model, tokenizer, config)
            elif config["type"] == "t5":
                return self._translate_t5(text, src_lang, tgt_lang, model, tokenizer)
            elif config["type"] == "opus":
                return self._translate_opus(text, src_lang, tgt_lang, model, tokenizer)
                
        except Exception as e:
            return {"error": str(e)}
    
    def _translate_nllb_fixed(self, text, src_lang, tgt_lang, model, tokenizer, config):
        """Fixed NLLB translation method"""
        src_code = config["languages"].get(src_lang, src_lang)
        tgt_code = config["languages"].get(tgt_lang, tgt_lang)
        
        # Set source language
        tokenizer.src_lang = src_code
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Get target language token ID - fixed method
        try:
            # Method 1: Try lang_code_to_id (older versions)
            if hasattr(tokenizer, 'lang_code_to_id'):
                forced_bos_token_id = tokenizer.lang_code_to_id[tgt_code]
            # Method 2: Try convert_tokens_to_ids (newer versions)
            elif hasattr(tokenizer, 'convert_tokens_to_ids'):
                forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_code)
            # Method 3: Manual lookup
            else:
                # Get the token ID for target language
                forced_bos_token_id = tokenizer.get_vocab().get(tgt_code, tokenizer.eos_token_id)
        except:
            # Fallback: use a default approach
            forced_bos_token_id = tokenizer.eos_token_id
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_length=512,
                num_beams=4,
                early_stopping=True
            )
        
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"translation": translation, "model": "NLLB"}
    
    def _translate_mbart(self, text, src_lang, tgt_lang, model, tokenizer, config):
        src_code = config["languages"].get(src_lang, f"{src_lang}_XX")
        tgt_code = config["languages"].get(tgt_lang, f"{tgt_lang}_XX")
        
        tokenizer.src_lang = src_code
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.lang_code_to_id[tgt_code],
                max_length=512,
                num_beams=4
            )
        
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"translation": translation, "model": "mBART"}
    
    def _translate_t5(self, text, src_lang, tgt_lang, model, tokenizer):
        # T5 uses task prefixes
        input_text = f"translate {src_lang} to {tgt_lang}: {text}"
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=512, num_beams=4)
        
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"translation": translation, "model": "T5"}
    
    def _translate_opus(self, text, src_lang, tgt_lang, model, tokenizer):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=512, num_beams=4)
        
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"translation": translation, "model": "OPUS-MT"}
    
    def get_available_models(self):
        """Return list of available models"""
        return list(self.available_models.keys())
    
    def get_supported_languages(self, model_key):
        """Get supported languages for a model"""
        if model_key in self.available_models:
            return list(self.available_models[model_key]["languages"].keys())
        return []
