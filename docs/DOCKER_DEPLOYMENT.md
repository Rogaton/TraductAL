# Docker Space Deployment - Professional Setup

Clean, efficient deployment for NLLB-200 fine-tuning on HF Spaces with T4 GPU.

## Architecture

- **Storage**: Checkpoints → HuggingFace Hub (every 500 steps, ~10 min)
- **Runtime**: Docker SDK (no Gradio timeout)
- **Resume**: Automatic from last Hub checkpoint if interrupted
- **Duration**: 2-3 hours for 3 language pairs × 50k samples

## Prerequisites

1. HuggingFace Pro account with T4 access
2. HF token with write permissions: https://huggingface.co/settings/tokens

## Deployment

### 1. Create Space

```
URL: https://huggingface.co/spaces
Configuration:
  - Name: nllb-training-docker
  - SDK: Docker
  - Hardware: T4 medium
  - Visibility: Private
```

### 2. Upload Files

Via git or web interface:

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/nllb-training-docker
cd nllb-training-docker

# Copy files
cp Dockerfile .
cp train_nllb_hf_spaces.py .
cp requirements_training.txt .
cp run_training.sh .

git add .
git commit -m "Initial training setup"
git push
```

Or via web UI: Files tab → Upload files

### 3. Configure Training

Edit `run_training.sh` and set:

```bash
HF_USERNAME="your-actual-username"
LANGUAGE_PAIRS="en-fr en-de en-es"  # Customize
MAX_SAMPLES="50000"
EPOCHS="3"
REPO_NAME="fine-tuned-nllb-600M"
```

### 4. Set Secrets

Space Settings → Repository Secrets:

```
Name: HF_TOKEN
Value: <your-token-here>
```

Alternatively, set in `run_training.sh`:
```bash
export HF_TOKEN="your-token"
```

### 5. Deploy

```bash
git add run_training.sh
git commit -m "Configure training parameters"
git push
```

Space will automatically build and start training.

## Monitoring

### Check Logs

Space → Logs tab shows real-time progress:
```
Loading model: facebook/nllb-200-distilled-600M
Model loaded. Parameters: 615,000,000
Loading opus-100 dataset...
Starting training...
Step 100: loss=2.45
Step 500: Saving checkpoint → Hub
...
```

### Check Hub Repo

Monitor checkpoints at:
```
https://huggingface.co/YOUR_USERNAME/fine-tuned-nllb-600M
```

Expected structure:
```
├── checkpoint-500/
├── checkpoint-1000/
├── checkpoint-1500/
└── ...
```

First checkpoint appears in ~10-15 minutes.

## Training Parameters

### Quick Test (45 min)
```bash
LANGUAGE_PAIRS="en-fr en-de"
MAX_SAMPLES="20000"
EPOCHS="1"
```

### Production (2-3 hrs)
```bash
LANGUAGE_PAIRS="en-fr en-de en-es"
MAX_SAMPLES="50000"
EPOCHS="3"
```

### Extended (4-6 hrs)
```bash
LANGUAGE_PAIRS="en-fr en-de en-es en-it en-pt"
MAX_SAMPLES="100000"
EPOCHS="3"
```

## Resume Training

If Space crashes or you stop training:

Edit `run_training.sh`:
```bash
RESUME_FROM="your-username/fine-tuned-nllb-600M"
```

Commit and push. Training resumes from last checkpoint.

## Download Model

After training completes:

```bash
python download_finetuned_model.py \
    --model_name YOUR_USERNAME/fine-tuned-nllb-600M \
    --output_dir ./models/deployed_models/nllb-finetuned \
    --test
```

## Troubleshooting

### OOM Error
```bash
BATCH_SIZE="2"  # Reduce from 4
```

### Training Too Slow
```bash
LANGUAGE_PAIRS="en-fr en-de"  # Fewer pairs
MAX_SAMPLES="20000"  # Fewer samples
```

### Space Timeout/Crash
No action needed. Checkpoints on Hub. Set `RESUME_FROM` and restart.

### No Checkpoints Appearing
- Check Space logs for errors
- Verify HF_TOKEN is set correctly
- Verify HF_USERNAME is correct
- Check Hub repo permissions

## Cost

HF Pro: $9/month includes T4 GPU quota.
Check usage: https://huggingface.co/settings/billing

## Performance

| Config | Time | Checkpoints | Cost |
|--------|------|-------------|------|
| Test (2 pairs, 20k) | 45 min | 6 | Included |
| Standard (3 pairs, 50k) | 2-3 hrs | 18 | Included |
| Extended (5 pairs, 100k) | 4-6 hrs | 30 | Included |

## Integration

Update your translator to use fine-tuned model:

```python
# nllb_translator.py
model_path = "./models/deployed_models/nllb-finetuned"
```

Or specify at runtime:
```bash
python nllb_translator.py \
    --model ./models/deployed_models/nllb-finetuned \
    --source en --target fr \
    --text "Your text here"
```

## Key Advantages

1. **No data loss**: Checkpoints on Hub, not ephemeral storage
2. **No timeout**: Docker SDK supports long-running jobs
3. **Resume capability**: Continue from last checkpoint
4. **Professional**: Clean setup, no Gradio overhead

## Support

- HF Spaces: https://huggingface.co/docs/hub/spaces-overview
- Docker SDK: https://huggingface.co/docs/hub/spaces-sdks-docker
- Issues: Check Space logs first, then HF community forums
