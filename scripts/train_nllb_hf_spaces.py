#!/usr/bin/env python3
"""
Fine-tune NLLB-200-distilled-600M on HuggingFace Spaces with T4 GPU
Dataset: Helsinki-NLP/opus-100
Optimized for T4 Medium (16GB VRAM)
"""

import os
import sys
import argparse
from pathlib import Path
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from huggingface_hub import login
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NLLBFineTuner:
    """Fine-tune NLLB-200-distilled-600M on opus-100 dataset."""

    def __init__(
        self,
        model_name="facebook/nllb-200-distilled-600M",
        language_pairs=None,
        output_dir="./fine-tuned-nllb",
        max_samples=50000,
        hf_token=None
    ):
        """
        Initialize the fine-tuner.

        Args:
            model_name: HuggingFace model ID
            language_pairs: List of language pairs (e.g., ['en-fr', 'en-de'])
            output_dir: Directory to save fine-tuned model
            max_samples: Maximum samples per language pair
            hf_token: HuggingFace API token
        """
        self.model_name = model_name
        self.language_pairs = language_pairs or ['en-fr', 'en-de', 'en-es']
        self.output_dir = Path(output_dir)
        self.max_samples = max_samples
        self.hf_token = hf_token

        # NLLB language code mapping (opus-100 uses ISO codes)
        self.nllb_lang_codes = {
            'en': 'eng_Latn', 'fr': 'fra_Latn', 'de': 'deu_Latn',
            'es': 'spa_Latn', 'it': 'ita_Latn', 'pt': 'por_Latn',
            'ru': 'rus_Cyrl', 'zh': 'zho_Hans', 'ja': 'jpn_Jpan',
            'ko': 'kor_Hang', 'ar': 'arb_Arab', 'hi': 'hin_Deva',
            'tr': 'tur_Latn', 'pl': 'pol_Latn', 'nl': 'nld_Latn',
            'sv': 'swe_Latn', 'da': 'dan_Latn', 'no': 'nob_Latn',
            'fi': 'fin_Latn', 'cs': 'ces_Latn', 'hu': 'hun_Latn',
            'ro': 'ron_Latn', 'bg': 'bul_Cyrl', 'el': 'ell_Grek',
            'he': 'heb_Hebr', 'th': 'tha_Thai', 'vi': 'vie_Latn',
            'id': 'ind_Latn', 'af': 'afr_Latn', 'et': 'est_Latn',
            'lv': 'lav_Latn', 'lt': 'lit_Latn', 'sk': 'slk_Latn',
        }

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

        # Login to HuggingFace if token provided
        if self.hf_token:
            login(token=self.hf_token)
            logger.info("Logged in to HuggingFace")

    def load_model_and_tokenizer(self):
        """Load the base NLLB model and tokenizer."""
        logger.info(f"Loading model: {self.model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            src_lang="eng_Latn",
            tgt_lang="fra_Latn"
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,  # Use FP16 to save memory
        ).to(self.device)

        logger.info(f"Model loaded. Parameters: {self.model.num_parameters():,}")
        logger.info(f"Memory allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")

    def load_dataset_pairs(self):
        """Load opus-100 dataset for specified language pairs."""
        logger.info(f"Loading opus-100 dataset for pairs: {self.language_pairs}")

        self.datasets = {}

        for pair in self.language_pairs:
            try:
                # Load specific language pair
                dataset = load_dataset(
                    "Helsinki-NLP/opus-100",
                    pair,
                    trust_remote_code=True
                )

                # Limit samples to avoid overwhelming T4
                if 'train' in dataset:
                    if len(dataset['train']) > self.max_samples:
                        dataset['train'] = dataset['train'].select(range(self.max_samples))

                self.datasets[pair] = dataset
                logger.info(f"Loaded {pair}: {len(dataset['train'])} training samples")

            except Exception as e:
                logger.error(f"Failed to load {pair}: {e}")

        if not self.datasets:
            raise ValueError("No datasets loaded successfully")

    def preprocess_function(self, examples, src_lang, tgt_lang):
        """
        Preprocess translation pairs for NLLB format.

        Args:
            examples: Batch of examples from dataset
            src_lang: Source language code (e.g., 'en')
            tgt_lang: Target language code (e.g., 'fr')
        """
        # Get NLLB language codes
        src_nllb = self.nllb_lang_codes.get(src_lang, src_lang)
        tgt_nllb = self.nllb_lang_codes.get(tgt_lang, tgt_lang)

        # opus-100 format: examples['translation'] = [{'en': '...', 'fr': '...'}, ...]
        sources = [item[src_lang] for item in examples['translation']]
        targets = [item[tgt_lang] for item in examples['translation']]

        # Tokenize sources
        self.tokenizer.src_lang = src_nllb
        model_inputs = self.tokenizer(
            sources,
            max_length=512,
            truncation=True,
            padding="max_length"
        )

        # Tokenize targets
        self.tokenizer.tgt_lang = tgt_nllb
        labels = self.tokenizer(
            targets,
            max_length=512,
            truncation=True,
            padding="max_length"
        )

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    def prepare_datasets(self):
        """Preprocess all loaded datasets."""
        logger.info("Preprocessing datasets...")

        self.processed_datasets = {}

        for pair, dataset in self.datasets.items():
            src_lang, tgt_lang = pair.split('-')

            # Preprocess train split
            if 'train' in dataset:
                train_dataset = dataset['train'].map(
                    lambda examples: self.preprocess_function(examples, src_lang, tgt_lang),
                    batched=True,
                    remove_columns=dataset['train'].column_names
                )

                # Preprocess validation split if available
                val_dataset = None
                if 'validation' in dataset:
                    val_dataset = dataset['validation'].map(
                        lambda examples: self.preprocess_function(examples, src_lang, tgt_lang),
                        batched=True,
                        remove_columns=dataset['validation'].column_names
                    )

                self.processed_datasets[pair] = {
                    'train': train_dataset,
                    'validation': val_dataset
                }

                logger.info(f"Preprocessed {pair}: {len(train_dataset)} train samples")

    def combine_datasets(self):
        """Combine all language pairs into single training dataset."""
        from datasets import concatenate_datasets

        train_datasets = []
        val_datasets = []

        for pair, datasets in self.processed_datasets.items():
            train_datasets.append(datasets['train'])
            if datasets['validation']:
                val_datasets.append(datasets['validation'])

        self.combined_train = concatenate_datasets(train_datasets)
        self.combined_val = concatenate_datasets(val_datasets) if val_datasets else None

        logger.info(f"Combined dataset: {len(self.combined_train)} train samples")
        if self.combined_val:
            logger.info(f"Validation samples: {len(self.combined_val)}")

    def train(self, epochs=3, batch_size=4, learning_rate=5e-5, hub_model_id=None, resume_from_checkpoint=None):
        """
        Fine-tune the model.

        Args:
            epochs: Number of training epochs
            batch_size: Training batch size (keep small for T4)
            learning_rate: Learning rate
            hub_model_id: HuggingFace Hub model ID to push checkpoints (e.g., 'username/model-name')
            resume_from_checkpoint: Path or Hub ID to resume training from
        """
        logger.info("Starting training...")

        # Training arguments optimized for T4 with Hub checkpointing
        training_args = Seq2SeqTrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            gradient_accumulation_steps=4,  # Effective batch size = 4 * 4 = 16
            learning_rate=learning_rate,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir=str(self.output_dir / "logs"),
            logging_steps=100,
            save_steps=500,  # Save checkpoints every 500 steps (more frequent)
            eval_steps=500,
            evaluation_strategy="steps" if self.combined_val else "no",
            save_total_limit=2,  # Keep only 2 checkpoints locally (saves space)
            fp16=True,  # Use mixed precision for T4
            gradient_checkpointing=True,  # Save memory
            predict_with_generate=True,
            generation_max_length=512,
            load_best_model_at_end=True if self.combined_val else False,
            metric_for_best_model="eval_loss" if self.combined_val else None,
            push_to_hub=True if hub_model_id else False,  # Push to Hub automatically
            hub_model_id=hub_model_id,  # Hub repo for checkpoints
            hub_strategy="checkpoint",  # Push every checkpoint to Hub
            hub_token=self.hf_token,
            report_to=["tensorboard"],
        )

        # Data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model,
            padding=True
        )

        # Initialize trainer
        trainer = Seq2SeqTrainer(
            model=self.model,
            args=training_args,
            train_dataset=self.combined_train,
            eval_dataset=self.combined_val,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
        )

        # Train! (with optional resume from checkpoint)
        logger.info("🚀 Starting training...")
        if resume_from_checkpoint:
            logger.info(f"Resuming from checkpoint: {resume_from_checkpoint}")
            trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        else:
            trainer.train()

        # Save final model
        logger.info(f"Saving final model to {self.output_dir}")
        trainer.save_model(str(self.output_dir / "final_model"))
        self.tokenizer.save_pretrained(str(self.output_dir / "final_model"))

        # Push final model to Hub if configured
        if hub_model_id:
            logger.info(f"Pushing final model to Hub: {hub_model_id}")
            trainer.push_to_hub(commit_message="Training completed")
            logger.info(f"✅ Final model pushed to: https://huggingface.co/{hub_model_id}")

        logger.info("✅ Training completed!")

    def push_to_hub(self, repo_name, hf_username=None):
        """
        Push fine-tuned model to HuggingFace Hub.

        Args:
            repo_name: Repository name (e.g., 'my-fine-tuned-nllb')
            hf_username: Your HuggingFace username
        """
        if not self.hf_token:
            logger.error("HuggingFace token required to push to hub")
            return

        full_repo_name = f"{hf_username}/{repo_name}" if hf_username else repo_name

        logger.info(f"Pushing model to hub: {full_repo_name}")

        self.model.push_to_hub(full_repo_name, token=self.hf_token)
        self.tokenizer.push_to_hub(full_repo_name, token=self.hf_token)

        logger.info(f"✅ Model pushed to: https://huggingface.co/{full_repo_name}")

def main():
    parser = argparse.ArgumentParser(description="Fine-tune NLLB-200 on opus-100")
    parser.add_argument(
        "--language_pairs",
        nargs="+",
        default=["en-fr", "en-de", "en-es"],
        help="Language pairs to train on (e.g., en-fr en-de)"
    )
    parser.add_argument(
        "--output_dir",
        default="./fine-tuned-nllb",
        help="Output directory for fine-tuned model"
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        default=50000,
        help="Maximum samples per language pair"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=4,
        help="Training batch size per device"
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=5e-5,
        help="Learning rate"
    )
    parser.add_argument(
        "--hf_token",
        default=None,
        help="HuggingFace API token (or use HF_TOKEN env var)"
    )
    parser.add_argument(
        "--push_to_hub",
        action="store_true",
        help="Push fine-tuned model to HuggingFace Hub"
    )
    parser.add_argument(
        "--hub_repo_name",
        default="fine-tuned-nllb-600M",
        help="Repository name for HuggingFace Hub"
    )
    parser.add_argument(
        "--hf_username",
        default=None,
        help="Your HuggingFace username"
    )
    parser.add_argument(
        "--resume_from_checkpoint",
        default=None,
        help="Resume training from checkpoint (local path or Hub ID)"
    )

    args = parser.parse_args()

    # Get HF token from args or environment
    hf_token = args.hf_token or os.environ.get("HF_TOKEN")

    # Prepare hub_model_id if push_to_hub is requested
    hub_model_id = None
    if args.push_to_hub:
        if args.hf_username:
            hub_model_id = f"{args.hf_username}/{args.hub_repo_name}"
        else:
            logger.error("--hf_username required when using --push_to_hub")
            sys.exit(1)

    # Initialize fine-tuner
    tuner = NLLBFineTuner(
        language_pairs=args.language_pairs,
        output_dir=args.output_dir,
        max_samples=args.max_samples,
        hf_token=hf_token
    )

    # Load model and datasets
    tuner.load_model_and_tokenizer()
    tuner.load_dataset_pairs()
    tuner.prepare_datasets()
    tuner.combine_datasets()

    # Train with automatic Hub checkpointing
    tuner.train(
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        hub_model_id=hub_model_id,
        resume_from_checkpoint=args.resume_from_checkpoint
    )

    logger.info("All done! 🎉")

if __name__ == "__main__":
    main()
