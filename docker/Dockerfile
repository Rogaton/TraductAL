# Dockerfile for HuggingFace Spaces - Docker SDK
# Optimized for long-running training jobs with checkpoint-to-hub

FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_training.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements_training.txt

# Copy training files
COPY train_nllb_hf_spaces.py .
COPY run_training.sh .
RUN chmod +x run_training.sh

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/tmp/cache \
    HF_HOME=/tmp/cache \
    TOKENIZERS_PARALLELISM=false

# Execute training
CMD ["bash", "run_training.sh"]
