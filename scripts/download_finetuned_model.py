#!/usr/bin/env python3
"""
Download fine-tuned NLLB model from HuggingFace Hub to local machine
"""

import os
import sys
import argparse
import json
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from huggingface_hub import login
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_disk_space(output_dir, required_gb=10):
    """Check if sufficient disk space is available."""
    import shutil

    stat = shutil.disk_usage(output_dir.parent)
    free_gb = stat.free / (1024**3)

    logger.info(f"Available disk space: {free_gb:.2f} GB")

    if free_gb < required_gb:
        logger.warning(f"Low disk space! Required: {required_gb} GB, Available: {free_gb:.2f} GB")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

    return True

def download_model(model_name, output_dir, hf_token=None):
    """
    Download model and tokenizer from HuggingFace Hub.

    Args:
        model_name: HuggingFace model ID (e.g., 'username/fine-tuned-nllb-600M')
        output_dir: Local directory to save model
        hf_token: HuggingFace API token (optional for public models)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading model: {model_name}")
    logger.info(f"Output directory: {output_dir}")

    # Login to HuggingFace if token provided
    if hf_token:
        login(token=hf_token)
        logger.info("Logged in to HuggingFace")

    # Check disk space
    check_disk_space(output_dir, required_gb=10)

    try:
        # Download tokenizer
        logger.info("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(output_dir)
        logger.info("✅ Tokenizer downloaded")

        # Download model
        logger.info("Downloading model (this may take a few minutes)...")
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16  # Save space
        )
        model.save_pretrained(output_dir)
        logger.info("✅ Model downloaded")

        # Get model info
        model_size_mb = sum(
            os.path.getsize(output_dir / f)
            for f in os.listdir(output_dir)
            if os.path.isfile(output_dir / f)
        ) / (1024**2)

        logger.info(f"Model size: {model_size_mb:.2f} MB")
        logger.info(f"Parameters: {model.num_parameters():,}")

        # Create model info file
        model_info = {
            "model_name": model_name,
            "model_type": "nllb-200-distilled-600M-finetuned",
            "size_mb": round(model_size_mb, 2),
            "parameters": model.num_parameters(),
            "downloaded_from": f"https://huggingface.co/{model_name}",
            "local_path": str(output_dir.absolute()),
            "languages": 200,
            "description": "Fine-tuned NLLB-200 model on opus-100 dataset",
            "use_case": "Multilingual translation (improved on training pairs)"
        }

        info_file = output_dir / "model_info.json"
        with open(info_file, 'w') as f:
            json.dump(model_info, f, indent=2)

        logger.info(f"Model info saved to: {info_file}")

    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        sys.exit(1)

def test_model(model_dir):
    """
    Test the downloaded model with a sample translation.

    Args:
        model_dir: Directory containing the model
    """
    model_dir = Path(model_dir)

    logger.info("Testing model...")

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

        # Move to GPU if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        logger.info(f"Using device: {device}")

        # Test translation (English to French)
        test_text = "Hello, how are you today?"
        logger.info(f"Test input: '{test_text}'")

        # Set language codes for NLLB
        tokenizer.src_lang = "eng_Latn"
        inputs = tokenizer(test_text, return_tensors="pt").to(device)

        # Generate translation
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id["fra_Latn"],
            max_length=512,
            num_beams=5
        )

        translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        logger.info(f"Test output (French): '{translation}'")
        logger.info("✅ Model test successful!")

        return True

    except Exception as e:
        logger.error(f"Model test failed: {e}")
        return False

def integrate_with_translator(model_dir, translator_file="nllb_translator.py"):
    """
    Provide instructions for integrating with existing translator.

    Args:
        model_dir: Directory containing the fine-tuned model
        translator_file: Path to translator script
    """
    model_dir = Path(model_dir)

    logger.info("\n" + "="*60)
    logger.info("INTEGRATION INSTRUCTIONS")
    logger.info("="*60)

    logger.info(f"""
To use your fine-tuned model with {translator_file}:

Option 1: Use directly with model path
--------------------------------------
python {translator_file} \\
    --model {model_dir} \\
    --source en \\
    --target fr \\
    --text "Your text here"

Option 2: Update default model in code
---------------------------------------
Edit {translator_file} and change the model path:

    model_path = "{model_dir}"

Option 3: Use in your app
--------------------------
from nllb_translator import EnhancedOfflineTranslator

translator = EnhancedOfflineTranslator(models_dir="{model_dir.parent}")
result = translator.translate(
    text="Hello, world!",
    source_lang="en",
    target_lang="fr"
)
print(result['translation'])

Note: Your fine-tuned model will perform better on the language
pairs it was trained on (e.g., en-fr, en-de, en-es from opus-100).
    """)

def main():
    parser = argparse.ArgumentParser(
        description="Download fine-tuned NLLB model from HuggingFace Hub"
    )
    parser.add_argument(
        "--model_name",
        required=True,
        help="HuggingFace model ID (e.g., 'username/fine-tuned-nllb-600M')"
    )
    parser.add_argument(
        "--output_dir",
        default="./models/deployed_models/nllb-200-distilled-600M-finetuned",
        help="Local directory to save model"
    )
    parser.add_argument(
        "--hf_token",
        default=None,
        help="HuggingFace API token (required for private models)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test model after downloading"
    )
    parser.add_argument(
        "--skip_integration_help",
        action="store_true",
        help="Skip showing integration instructions"
    )

    args = parser.parse_args()

    # Get HF token from args or environment
    hf_token = args.hf_token or os.environ.get("HF_TOKEN")

    # Download model
    download_model(args.model_name, args.output_dir, hf_token)

    # Test model if requested
    if args.test:
        test_model(args.output_dir)

    # Show integration instructions
    if not args.skip_integration_help:
        integrate_with_translator(args.output_dir)

    logger.info("\n✅ All done! Your fine-tuned model is ready to use.")

if __name__ == "__main__":
    main()
