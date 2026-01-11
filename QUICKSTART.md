# Quick Start - Docker Space Deployment

## Files to Upload

Required files for HF Space:
```
Dockerfile
train_nllb_hf_spaces.py
requirements_training.txt
run_training.sh
```

## 3-Step Setup

### 1. Create Space
- URL: https://huggingface.co/spaces
- SDK: **Docker** (not Gradio)
- Hardware: **T4 medium**

### 2. Configure
Edit `run_training.sh`:
```bash
HF_USERNAME="your-username"          # Your HF username
LANGUAGE_PAIRS="en-fr en-de en-es"   # Language pairs
MAX_SAMPLES="50000"                  # Samples per pair
EPOCHS="3"                           # Training epochs
```

Set secret in Space Settings → Repository Secrets:
```
HF_TOKEN = your-token-from-hf-settings
```

### 3. Deploy
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/your-space-name
cd your-space-name
cp /path/to/files/* .
git add .
git commit -m "Initial setup"
git push
```

## Monitoring

- **Logs**: Space → Logs tab (real-time)
- **Checkpoints**: https://huggingface.co/YOUR_USERNAME/fine-tuned-nllb-600M
- **First checkpoint**: ~10-15 minutes

## Time Estimates

| Config | Time |
|--------|------|
| 2 pairs × 20k (test) | 45 min |
| 3 pairs × 50k | 2-3 hrs |
| 5 pairs × 100k | 4-6 hrs |

## Resume After Crash

Edit `run_training.sh`:
```bash
RESUME_FROM="your-username/fine-tuned-nllb-600M"
```

Push changes. Training resumes from last checkpoint.

## Download Trained Model

```bash
python download_finetuned_model.py \
    --model_name YOUR_USERNAME/fine-tuned-nllb-600M \
    --test
```

## Key Points

- ✅ Checkpoints saved to Hub every 500 steps (~10 min)
- ✅ No ephemeral storage issues
- ✅ No Gradio timeout
- ✅ Resume from checkpoint if interrupted
- ✅ 2-3 hours for standard config (much faster than 8-12 hrs)

## Support

Full guide: `DOCKER_DEPLOYMENT.md`
