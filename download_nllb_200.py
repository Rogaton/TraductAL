#!/usr/bin/env python3
"""
Download NLLB-200 models for offline neural machine translation
Optimized for professional translator use with 64GB RAM system
"""

import os
import sys
import json
import time
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    from huggingface_hub import snapshot_download
    print("✅ Required packages loaded successfully")
except ImportError as e:
    print("❌ Error: Required packages not installed")
    print("Please install: pip install transformers torch huggingface_hub")
    sys.exit(1)

class NLLBDownloader:
    """Download and setup NLLB-200 models for offline translation."""
    
    def __init__(self, models_dir="./models/deployed_models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # NLLB model configurations
        self.nllb_models = {
            "nllb-200-1.3B": {
                "model_id": "facebook/nllb-200-1.3B",
                "size": "~2.6GB",
                "description": "High quality, good balance",
                "recommended": True
            },
            "nllb-200-3.3B": {
                "model_id": "facebook/nllb-200-3.3B", 
                "size": "~6.6GB",
                "description": "Maximum quality, slower",
                "recommended": False
            },
            "nllb-200-distilled-1.3B": {
                "model_id": "facebook/nllb-200-distilled-1.3B",
                "size": "~2.6GB", 
                "description": "Faster inference, slightly lower quality",
                "recommended": False
            }
        }
        
        print("🌍 NLLB-200 Model Downloader")
        print("📍 Supporting 200+ languages for professional translation")
        print(f"📁 Target directory: {self.models_dir}")
    
    def check_disk_space(self, required_gb=10):
        """Check available disk space."""
        statvfs = os.statvfs(self.models_dir)
        free_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
        
        print(f"💾 Available disk space: {free_gb:.1f}GB")
        if free_gb < required_gb:
            print(f"⚠️  Warning: Less than {required_gb}GB available")
            return False
        return True
    
    def check_ram(self):
        """Check system RAM."""
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            for line in meminfo.split('\n'):
                if 'MemTotal:' in line:
                    total_kb = int(line.split()[1])
                    total_gb = total_kb / (1024**2)
                    print(f"🧠 System RAM: {total_gb:.1f}GB")
                    
                    if total_gb >= 32:
                        print("✅ Excellent RAM for NLLB-200-3.3B")
                        return "3.3B"
                    elif total_gb >= 16:
                        print("✅ Good RAM for NLLB-200-1.3B")
                        return "1.3B"
                    else:
                        print("⚠️  Limited RAM - consider distilled model")
                        return "distilled"
        except:
            print("❓ Could not detect RAM, assuming sufficient")
            return "1.3B"
    
    def download_model(self, model_key="nllb-200-1.3B"):
        """Download specified NLLB model."""
        if model_key not in self.nllb_models:
            print(f"❌ Unknown model: {model_key}")
            return False
        
        model_info = self.nllb_models[model_key]
        model_id = model_info["model_id"]
        local_dir = self.models_dir / model_key.replace("-", "_").lower()
        
        print(f"\n🔄 Downloading {model_key}")
        print(f"📦 Model: {model_id}")
        print(f"💾 Size: {model_info['size']}")
        print(f"📁 Local path: {local_dir}")
        print(f"📝 Description: {model_info['description']}")
        
        if local_dir.exists() and any(local_dir.iterdir()):
            print("✅ Model already exists, skipping download")
            return True
        
        try:
            print("⏳ Starting download... (this may take 10-30 minutes)")
            start_time = time.time()
            
            # Download model files
            snapshot_download(
                repo_id=model_id,
                local_dir=local_dir,
                local_dir_use_symlinks=False,
                resume_download=True
            )
            
            download_time = time.time() - start_time
            print(f"✅ Download completed in {download_time/60:.1f} minutes")
            
            # Test model loading
            print("🧪 Testing model loading...")
            tokenizer = AutoTokenizer.from_pretrained(local_dir)
            model = AutoModelForSeq2SeqLM.from_pretrained(local_dir)
            
            print("✅ Model loaded successfully")
            print(f"📊 Model parameters: {model.num_parameters():,}")
            
            # Clean up test objects
            del model, tokenizer
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {str(e)}")
            return False
    
    def list_available_models(self):
        """List all available NLLB models."""
        print("\n📋 Available NLLB-200 Models:")
        print("=" * 60)
        
        for key, info in self.nllb_models.items():
            status = "⭐ RECOMMENDED" if info.get("recommended") else ""
            print(f"🔹 {key}")
            print(f"   Size: {info['size']}")
            print(f"   Description: {info['description']} {status}")
            print()
    
    def create_model_info(self, model_key):
        """Create model information file."""
        info_file = self.models_dir / f"{model_key.replace('-', '_').lower()}_info.json"
        
        model_info = {
            "model_name": model_key,
            "model_id": self.nllb_models[model_key]["model_id"],
            "download_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "languages_supported": 200,
            "model_type": "NLLB-200",
            "use_case": "Professional multilingual translation",
            "quality": "High" if "3.3B" in model_key else "Very Good",
            "recommended_for": [
                "Professional translators",
                "Sensitive document translation", 
                "Multilingual content creation",
                "Cross-language research"
            ]
        }
        
        with open(info_file, 'w') as f:
            json.dump(model_info, f, indent=2)
        
        print(f"📄 Model info saved: {info_file}")

def main():
    """Main download function."""
    downloader = NLLBDownloader()
    
    print("🚀 NLLB-200 Setup for Professional Translation")
    print("=" * 50)
    
    # System checks
    if not downloader.check_disk_space(10):
        print("❌ Insufficient disk space")
        return
    
    ram_recommendation = downloader.check_ram()
    
    # Show available models
    downloader.list_available_models()
    
    # Get user choice
    print("💡 Recommendations based on your 64GB RAM system:")
    print("   1. nllb-200-1.3B (recommended for testing)")
    print("   2. nllb-200-3.3B (maximum quality)")
    print("   3. Both models (for flexibility)")
    print()
    
    choice = input("Enter your choice (1/2/3) or model name: ").strip()
    
    models_to_download = []
    if choice == "1":
        models_to_download = ["nllb-200-1.3B"]
    elif choice == "2":
        models_to_download = ["nllb-200-3.3B"]
    elif choice == "3":
        models_to_download = ["nllb-200-1.3B", "nllb-200-3.3B"]
    elif choice in downloader.nllb_models:
        models_to_download = [choice]
    else:
        print("❌ Invalid choice, defaulting to nllb-200-1.3B")
        models_to_download = ["nllb-200-1.3B"]
    
    # Download selected models
    success_count = 0
    for model_key in models_to_download:
        if downloader.download_model(model_key):
            downloader.create_model_info(model_key)
            success_count += 1
        print("-" * 50)
    
    # Summary
    print(f"\n🎉 Download Summary:")
    print(f"✅ Successfully downloaded: {success_count}/{len(models_to_download)} models")
    
    if success_count > 0:
        print("\n🔄 Next Steps:")
        print("1. Update your translation script to use NLLB-200")
        print("2. Test translations with the new model")
        print("3. Compare quality with your current MT5 setup")
        print("\n📖 Run the updated translation script to start using NLLB-200!")

if __name__ == "__main__":
    main()
