# Docker-based HuggingFace Space Setup

This setup uses **Docker SDK** instead of Gradio, which solves both issues:
- ✅ **No timeout issues** - Docker Spaces can run for extended periods
- ✅ **Checkpoint to Hub** - Every 500 steps saved to HuggingFace Hub (not ephemeral storage)

## Setup Instructions

### 1. Create HuggingFace Space with Docker SDK

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Configure:
   - **Space name**: `nllb-training-docker`
   - **SDK**: **Docker** (NOT Gradio!)
   - **Hardware**: **T4 medium**
   - **Visibility**: Private

### 2. Upload Files to Space

Upload these files to your Space:
- `Dockerfile`
- `train_nllb_hf_spaces.py`
- `requirements_training.txt`

### 3. Create Configuration File

Create a file named `run_training.sh` in your Space:

```bash
#!/bin/bash

python3 train_nllb_hf_spaces.py \
    --language_pairs en-fr en-de en-es \
    --max_samples 50000 \
    --epochs 3 \
    --batch_size 4 \
    --push_to_hub \
    --hub_repo_name fine-tuned-nllb-600M \
    --hf_username YOUR_HF_USERNAME \
    --hf_token $HF_TOKEN
```

**Replace `YOUR_HF_USERNAME`** with your actual HuggingFace username!

### 4. Update Dockerfile CMD

Edit the last line of `Dockerfile` to:

```dockerfile
# Entry point - run training
CMD ["bash", "run_training.sh"]
```

### 5. Set HuggingFace Token

1. Go to your Space Settings → **Repository secrets**
2. Add secret:
   - **Name**: `HF_TOKEN`
   - **Value**: Your HuggingFace token

### 6. Start Training

1. Commit all files to your Space
2. The Space will automatically build and start training
3. Monitor progress in the Logs tab

## Key Advantages

### 1. Checkpoints Saved to Hub Every 500 Steps

Your model checkpoints are automatically pushed to HuggingFace Hub:
```
https://huggingface.co/YOUR_USERNAME/fine-tuned-nllb-600M
```

This means:
- **If training crashes**: You don't lose progress!
- **Resume training**: Use `--resume_from_checkpoint YOUR_USERNAME/fine-tuned-nllb-600M`
- **No ephemeral storage issues**: Everything saved to Hub, not local disk

### 2. No Gradio Timeout

Docker Spaces can run for extended periods without timeout issues. Your 2-3 hour training will complete successfully.

### 3. Resume from Checkpoint

If training is interrupted, resume from the last checkpoint:

```bash
python3 train_nllb_hf_spaces.py \
    --resume_from_checkpoint YOUR_USERNAME/fine-tuned-nllb-600M \
    --language_pairs en-fr en-de en-es \
    --max_samples 50000 \
    --epochs 3 \
    --push_to_hub \
    --hub_repo_name fine-tuned-nllb-600M \
    --hf_username YOUR_HF_USERNAME
```

## Monitoring Training

Check your Hub repository to see checkpoints being saved:
```
https://huggingface.co/YOUR_USERNAME/fine-tuned-nllb-600M
```

You should see:
- `checkpoint-500/` (after 500 steps)
- `checkpoint-1000/` (after 1000 steps)
- `checkpoint-1500/` (after 1500 steps)
- etc.

## Expected Timeline

With 3 language pairs × 50k samples:
- **Total steps**: ~9,000 steps
- **Checkpoints saved**: Every 500 steps (18 checkpoints)
- **Training time**: 2-3 hours
- **First checkpoint**: ~10-15 minutes

## Download Final Model

After training completes:

```bash
python download_finetuned_model.py \
    --model_name YOUR_USERNAME/fine-tuned-nllb-600M \
    --test
```

## Troubleshooting

### Space Crashes During Training

**Solution**: Resume from last checkpoint
```bash
--resume_from_checkpoint YOUR_USERNAME/fine-tuned-nllb-600M
```

The training will automatically continue from where it left off!

### Out of Memory

**Solution**: Reduce batch size in `run_training.sh`
```bash
--batch_size 2  # Instead of 4
```

### Training Too Slow

**Solution**: Reduce samples or language pairs
```bash
--language_pairs en-fr en-de  # Just 2 pairs
--max_samples 20000
```

## Cost

Docker Spaces with T4 GPU are included in HuggingFace Pro ($9/month).
Check your quota at: https://huggingface.co/settings/billing
