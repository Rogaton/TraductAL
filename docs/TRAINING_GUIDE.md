# Fine-tuning NLLB-200 on HuggingFace Spaces

This guide walks you through fine-tuning `facebook/nllb-200-distilled-600M` on the `Helsinki-NLP/opus-100` dataset using HuggingFace Spaces with T4 GPU.

## Why This Setup?

- **Model**: NLLB-200-distilled-600M (600M parameters) - Fits comfortably on T4 GPU
- **Dataset**: opus-100 - 100+ language pairs with high-quality parallel corpora
- **Hardware**: T4 Medium (16GB VRAM) - Available with HF Pro plan
- **Training Time**: ~2-6 hours depending on language pairs and samples

## Prerequisites

1. **HuggingFace Pro Account** with T4 GPU access
2. **HuggingFace Token** with write access
   - Go to https://huggingface.co/settings/tokens
   - Create a new token with "Write" permissions
   - Copy the token (you'll need it later)

## Step 1: Create HuggingFace Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Configure:
   - **Space name**: `nllb-finetuning` (or your choice)
   - **License**: Apache 2.0 (or your preference)
   - **SDK**: Gradio (or Docker)
   - **Hardware**: **T4 medium** (requires Pro plan)
   - **Visibility**: Private (recommended during training)

4. Click **"Create Space"**

## Step 2: Upload Training Files

Once your Space is created, upload these files:

### Option A: Via Web Interface

1. Click **"Files"** tab in your Space
2. Upload:
   - `train_nllb_hf_spaces.py`
   - `requirements_training.txt`

### Option B: Via Git (Recommended)

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR-USERNAME/nllb-finetuning
cd nllb-finetuning

# Copy training files
cp /home/aldn/TraductAL/TraductAL/train_nllb_hf_spaces.py .
cp /home/aldn/TraductAL/TraductAL/requirements_training.txt requirements.txt

# Commit and push
git add .
git commit -m "Add training script and requirements"
git push
```

## Step 3: Configure Environment

### Set HuggingFace Token as Secret

1. In your Space, go to **Settings** → **Repository secrets**
2. Add secret:
   - **Name**: `HF_TOKEN`
   - **Value**: Your HuggingFace token (from Prerequisites)
3. Click **"Add secret"**

## Step 4: Create App File

Create an `app.py` file in your Space to run the training:

```python
#!/usr/bin/env python3
import os
import subprocess
import sys

# Install requirements first
print("Installing dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Get HF token from environment
hf_token = os.environ.get("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN not found! Please add it to Space secrets.")

# Run training
print("Starting training...")
subprocess.run([
    sys.executable,
    "train_nllb_hf_spaces.py",
    "--language_pairs", "en-fr", "en-de", "en-es",  # Customize these!
    "--max_samples", "50000",
    "--epochs", "3",
    "--batch_size", "4",
    "--hf_token", hf_token,
    "--push_to_hub",  # Push to your HF account when done
    "--hub_repo_name", "fine-tuned-nllb-600M",  # Customize this!
    "--hf_username", "YOUR-USERNAME"  # Replace with your HF username
])
```

**Important**: Replace `YOUR-USERNAME` with your actual HuggingFace username!

## Step 5: Customize Training

Edit the training parameters in `app.py`:

### Language Pairs

Choose from 100+ available pairs:
```python
--language_pairs en-fr en-de en-es en-it en-pt en-ru en-zh en-ja en-ko en-ar
```

Common pairs: `en-fr`, `en-de`, `en-es`, `en-it`, `en-pt`, `en-ru`, `en-zh`, `en-ja`, `en-ko`, `en-ar`

Full list: https://huggingface.co/datasets/Helsinki-NLP/opus-100

### Training Parameters

```python
--max_samples 50000      # Samples per language pair (lower = faster)
--epochs 3               # Training epochs (3-5 recommended)
--batch_size 4           # Keep at 4 for T4 GPU
--learning_rate 5e-5     # Default works well
```

**Memory vs. Speed Trade-offs**:
- More language pairs = longer training
- More samples = better quality but slower
- More epochs = better convergence but diminishing returns after 3-5

**Recommended Configurations**:

| Goal | Language Pairs | Max Samples | Epochs | Time |
|------|---------------|-------------|---------|------|
| Quick test | 2-3 | 10,000 | 1 | ~30 min |
| Balanced | 3-5 | 50,000 | 3 | ~2-3 hours |
| High quality | 5-10 | 100,000 | 3 | ~4-6 hours |

## Step 6: Start Training

1. Commit `app.py` to your Space
2. The Space will automatically start building and training
3. Monitor progress in the **Logs** tab

**What to expect**:
```
Loading model: facebook/nllb-200-distilled-600M
Model loaded. Parameters: 615,000,000
Memory allocated: 2.34 GB
Loading opus-100 dataset for pairs: ['en-fr', 'en-de', 'en-es']
Loaded en-fr: 50000 training samples
Loaded en-de: 50000 training samples
Loaded en-es: 50000 training samples
Preprocessing datasets...
Combined dataset: 150000 train samples
Starting training...
🚀 Starting training...
[Training progress with loss values...]
✅ Training completed!
Pushing model to hub: your-username/fine-tuned-nllb-600M
✅ Model pushed to: https://huggingface.co/your-username/fine-tuned-nllb-600M
All done! 🎉
```

## Step 7: Download Fine-tuned Model

Once training completes, download your fine-tuned model to local machine:

```bash
# Use the provided download script
python download_finetuned_model.py \
    --model_name YOUR-USERNAME/fine-tuned-nllb-600M \
    --output_dir ./models/deployed_models/nllb-200-distilled-600M-finetuned
```

Or manually:
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "YOUR-USERNAME/fine-tuned-nllb-600M"
output_dir = "./models/deployed_models/nllb-200-distilled-600M-finetuned"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

tokenizer.save_pretrained(output_dir)
model.save_pretrained(output_dir)

print(f"✅ Model downloaded to {output_dir}")
```

## Step 8: Test Fine-tuned Model

Test your fine-tuned model locally:

```bash
# Update nllb_translator.py to use fine-tuned model
python nllb_translator.py \
    --model ./models/deployed_models/nllb-200-distilled-600M-finetuned \
    --source en \
    --target fr \
    --text "Hello, how are you today?"
```

Or use it in your app by updating the model path.

## Troubleshooting

### Out of Memory Error

**Solution**: Reduce batch size or max samples
```python
--batch_size 2
--max_samples 20000
```

### Training Too Slow

**Solution**: Reduce language pairs or samples
```python
--language_pairs en-fr en-de  # Just 2 pairs
--max_samples 10000
```

### Model Not Improving

**Solution**: Adjust learning rate or increase epochs
```python
--learning_rate 3e-5
--epochs 5
```

### Space Timeout

**Solution**: HF Spaces have 48-hour limit. For longer training:
1. Reduce max_samples
2. Use fewer language pairs
3. Save checkpoints frequently (done automatically every 1000 steps)

## Cost Considerations

**HuggingFace Pro Plan**:
- T4 Medium: Included in Pro subscription ($9/month)
- No additional compute charges for included hours
- Check your quota: https://huggingface.co/settings/billing

**Training Time Estimates**:
- 3 language pairs × 50k samples × 3 epochs ≈ 2-3 hours
- 10 language pairs × 100k samples × 3 epochs ≈ 6-8 hours

## Next Steps

1. **Evaluate quality**: Compare translations with base model
2. **Iterate**: Try different language pairs or hyperparameters
3. **Scale up**: Once satisfied, train on more data
4. **Production**: Deploy fine-tuned model in your app

## Advanced: Custom Datasets

To use your own translation data instead of opus-100:

1. Format data as parallel corpus (JSON Lines):
```json
{"translation": {"en": "Hello", "fr": "Bonjour"}}
{"translation": {"en": "Good morning", "fr": "Bon matin"}}
```

2. Modify `load_dataset_pairs()` in training script:
```python
dataset = load_dataset("json", data_files="my_data.jsonl")
```

3. Run training with custom data

## Resources

- NLLB-200 Paper: https://arxiv.org/abs/2207.04672
- opus-100 Dataset: https://huggingface.co/datasets/Helsinki-NLP/opus-100
- HuggingFace Spaces Docs: https://huggingface.co/docs/hub/spaces
- Transformers Training: https://huggingface.co/docs/transformers/training

## Support

Questions? Check:
1. HuggingFace Community: https://discuss.huggingface.co
2. NLLB GitHub: https://github.com/facebookresearch/fairseq/tree/nllb
3. This project's issues

Good luck with your training! 🚀
