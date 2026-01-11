#!/bin/bash
set -e

# Training configuration for NLLB-200-distilled-600M
# Checkpoints auto-saved to HF Hub every 500 steps

# === CONFIGURE THESE ===
HF_USERNAME="${HF_USERNAME:-YOUR_USERNAME}"  # Set in Space secrets or here
LANGUAGE_PAIRS="${LANGUAGE_PAIRS:-en-fr en-de en-es}"
MAX_SAMPLES="${MAX_SAMPLES:-50000}"
EPOCHS="${EPOCHS:-3}"
BATCH_SIZE="${BATCH_SIZE:-4}"
REPO_NAME="${REPO_NAME:-fine-tuned-nllb-600M}"

# Resume from checkpoint if needed (optional)
RESUME_FROM="${RESUME_FROM:-}"

# === EXECUTION ===
echo "=================================================="
echo "NLLB-200 Fine-tuning on Docker Space"
echo "=================================================="
echo "Language pairs: $LANGUAGE_PAIRS"
echo "Max samples: $MAX_SAMPLES per pair"
echo "Epochs: $EPOCHS"
echo "Hub repo: $HF_USERNAME/$REPO_NAME"
echo "Checkpoints: Every 500 steps → Hub"
echo "=================================================="

# Build command
CMD="python3 train_nllb_hf_spaces.py \
    --language_pairs $LANGUAGE_PAIRS \
    --max_samples $MAX_SAMPLES \
    --epochs $EPOCHS \
    --batch_size $BATCH_SIZE \
    --push_to_hub \
    --hub_repo_name $REPO_NAME \
    --hf_username $HF_USERNAME"

# Add resume if specified
if [ -n "$RESUME_FROM" ]; then
    CMD="$CMD --resume_from_checkpoint $RESUME_FROM"
    echo "Resuming from: $RESUME_FROM"
fi

# Execute
echo "Starting training..."
exec $CMD
