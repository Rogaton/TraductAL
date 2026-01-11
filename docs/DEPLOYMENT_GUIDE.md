# TraductAL Deployment Guide

**Complete guide for deploying TraductAL in production environments**

Updated: January 2026
Version: 2.0.0

---

## Table of Contents

1. [Overview](#overview)
2. [Deployment Options](#deployment-options)
3. [HuggingFace Spaces Deployment](#huggingface-spaces-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Local Deployment](#local-deployment)
6. [Configuration & Optimization](#configuration--optimization)
7. [Troubleshooting](#troubleshooting)

---

## Overview

TraductAL can be deployed in three main ways:

| Method | Best For | Hardware | Difficulty |
|--------|----------|----------|------------|
| **HuggingFace Spaces** | Quick public demos, testing | Cloud GPU/CPU | Easy |
| **Docker** | Production servers, self-hosting | Own servers | Medium |
| **Local** | Development, customization | Local machine | Easy |

### System Requirements

**Minimum (CPU-only):**
- CPU: 4+ cores
- RAM: 16GB
- Storage: 30GB free
- Internet: For model downloads

**Recommended (GPU):**
- GPU: NVIDIA with 8GB+ VRAM (T4, RTX 3060+)
- CPU: 8+ cores
- RAM: 32GB
- Storage: 50GB free

---

## HuggingFace Spaces Deployment

Deploy TraductAL as a public or private HuggingFace Space.

### Step 1: Prepare Files

Required files:
- `gradio_app.py` (main application)
- `unified_translator.py` (translation engine)
- `apertus_translator.py` (Apertus integration)
- `nllb_translator.py` (NLLB integration)
- `tts_engine.py` (text-to-speech)
- `whisper_stt.py` (speech-to-text)
- `startup_check.py` (model verification)
- `requirements_hf.txt` (dependencies)
- `README_HF.md` (Space description)

### Step 2: Create HuggingFace Space

1. Go to https://huggingface.co/new-space
2. Configure:
   - **Name**: `traductal` (or your choice)
   - **SDK**: Gradio
   - **Hardware**:
     - CPU Basic (free, slower)
     - T4 Small/Medium (paid, recommended)
   - **Visibility**: Public or Private

### Step 3: Upload Files

**Option A: Git (Recommended)**

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/traductal
cd traductal

# Copy application files
cp gradio_app.py .
cp unified_translator.py .
cp apertus_translator.py .
cp nllb_translator.py .
cp tts_engine.py .
cp whisper_stt.py .
cp startup_check.py .
cp requirements_hf.txt requirements.txt  # HF Spaces uses requirements.txt
cp README_HF.md README.md  # HF Spaces uses README.md

# Commit and push
git add .
git commit -m "Initial TraductAL deployment"
git push
```

**Option B: Web Interface**

1. Go to your Space's "Files" tab
2. Click "Add file" → "Upload files"
3. Upload all required files
4. Rename `requirements_hf.txt` → `requirements.txt`
5. Rename `README_HF.md` → `README.md`

### Step 4: Configure Space

The `README.md` (formerly `README_HF.md`) contains YAML frontmatter that configures your Space:

```yaml
---
title: TraductAL - Swiss Languages Translator
emoji: 🇨🇭
sdk: gradio
sdk_version: 4.0.0
app_file: gradio_app.py
pinned: false
license: apache-2.0
---
```

### Step 5: Launch

Your Space will automatically build and launch. First run takes 10-15 minutes to:
1. Install dependencies
2. Download models (~20GB)
3. Initialize application

### Step 6: Monitor

- Check "Logs" tab for startup progress
- Models download automatically on first run
- Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/traductal`

### HuggingFace Spaces Tips

- **Free tier**: CPU-only, may be slow for Apertus-8B
- **T4 GPU**: Recommended for good performance (~$0.60/hour)
- **Persistent storage**: Models persist between restarts
- **Automatic updates**: Push to git = automatic rebuild

---

## Docker Deployment

Deploy TraductAL using Docker for production servers or local hosting.

### Prerequisites

- Docker 20.10+ installed
- Docker Compose 2.0+ (optional but recommended)
- NVIDIA Docker runtime (for GPU support)

### Quick Start with Docker Compose

**1. Basic CPU Deployment:**

```bash
# Start the service
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the service
docker-compose down
```

**2. GPU Deployment:**

Edit `docker-compose.yml` and uncomment the `traductal-gpu` service, then:

```bash
# Start GPU service
docker-compose up -d traductal-gpu

# Verify GPU is detected
docker-compose exec traductal-gpu nvidia-smi
```

### Manual Docker Build

**Build the image:**

```bash
docker build -f Dockerfile.production -t traductal:latest .
```

**Run CPU-only:**

```bash
docker run -d \
  --name traductal \
  -p 7860:7860 \
  -v traductal-models:/app/models \
  traductal:latest
```

**Run with GPU:**

```bash
docker run -d \
  --name traductal \
  --gpus all \
  -p 7860:7860 \
  -v traductal-models:/app/models \
  traductal:latest
```

### Docker Configuration

**Environment Variables:**

```bash
# Model cache location
-e TRANSFORMERS_CACHE=/app/models
-e HF_HOME=/app/models

# Performance tuning
-e OMP_NUM_THREADS=4
-e MKL_NUM_THREADS=4

# HuggingFace token (for private models)
-e HF_TOKEN=your_token_here
```

**Volume Mounts:**

```bash
# Persist models across restarts
-v traductal-models:/app/models

# Mount input audio files
-v ./audio_input:/app/audio_input:ro

# Mount output directory
-v ./audio_output:/app/audio_output
```

### Production Docker Setup

For production, use a reverse proxy (nginx/traefik) with SSL:

**docker-compose.production.yml:**

```yaml
version: '3.8'

services:
  traductal:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: traductal-app
    restart: always
    volumes:
      - traductal-models:/app/models
    environment:
      - TRANSFORMERS_CACHE=/app/models
      - HF_HOME=/app/models
    networks:
      - traductal-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traductal.rule=Host(`translate.yourdomain.com`)"
      - "traefik.http.services.traductal.loadbalancer.server.port=7860"

  traefik:
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.email=your@email.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik-certs:/letsencrypt
    networks:
      - traductal-network

volumes:
  traductal-models:
  traefik-certs:

networks:
  traductal-network:
    external: false
```

---

## Local Deployment

Run TraductAL directly on your machine for development or personal use.

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd TraductAL
```

### Step 2: Install Dependencies

**Using pip:**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_hf.txt
```

**Using conda:**

```bash
# Create conda environment
conda create -n traductal python=3.10
conda activate traductal

# Install dependencies
pip install -r requirements_hf.txt
```

### Step 3: Download Models

**Automatic (Recommended):**

```bash
# Run startup check interactively
python startup_check.py

# This will prompt you to download required models
```

**Manual:**

```bash
# Download specific models using Python
python -c "
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Download NLLB-200
AutoTokenizer.from_pretrained('facebook/nllb-200-1.3B')
AutoModelForSeq2SeqLM.from_pretrained('facebook/nllb-200-1.3B')

# Download Apertus-8B
AutoTokenizer.from_pretrained('swiss-ai/Apertus-8B-2509')
AutoModelForSeq2SeqLM.from_pretrained('swiss-ai/Apertus-8B-2509')
"
```

### Step 4: Run Application

```bash
# Start Gradio app
python gradio_app.py

# Access at: http://localhost:7860
```

### Step 5: Optional - Install Whisper

For speech-to-text support:

```bash
pip install openai-whisper
```

---

## Configuration & Optimization

### Model Selection

**CPU-only Systems:**
- Use NLLB-200 (faster, 1.3B parameters)
- Apertus-8B will work but be slower

**GPU Systems:**
- Both models work well
- T4 GPU: ~2s per translation
- RTX 3090: ~0.5s per translation

### Memory Optimization

**Reduce memory usage:**

```python
# In unified_translator.py, use smaller batch sizes
# or load models in 8-bit mode
model = AutoModelForSeq2SeqLM.from_pretrained(
    model_id,
    load_in_8bit=True,  # Requires bitsandbytes library
    device_map="auto"
)
```

### Performance Tuning

**Environment variables:**

```bash
# Increase parallel processing
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8

# Disable tokenizer warnings
export TOKENIZERS_PARALLELISM=false
```

### Language Selection

Disable unused languages to reduce UI clutter by editing `gradio_app.py`:

```python
# Comment out languages you don't need
NLLB_LANGUAGES = {
    "German": "de",
    "English": "en",
    "French": "fr",
    # "Italian": "it",  # Disabled
    # ...
}
```

---

## Troubleshooting

### Common Issues

**Issue: Out of Memory (OOM)**

```
Solution:
1. Close other applications
2. Use CPU instead of GPU (may be slower but uses system RAM)
3. Reduce batch size in translator code
4. Use 8-bit quantization
```

**Issue: Models not downloading**

```
Solution:
1. Check internet connection
2. Verify HuggingFace Hub access
3. Try manual download:
   python startup_check.py --force-download
4. Set HF_TOKEN if using private models
```

**Issue: Gradio port already in use**

```
Solution:
# Change port in gradio_app.py
demo.launch(server_port=7861)  # Use different port
```

**Issue: GPU not detected**

```
Solution:
# Check CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# If False:
1. Install correct CUDA version
2. Reinstall PyTorch with CUDA support:
   pip install torch --index-url https://download.pytorch.org/whl/cu118
```

**Issue: Slow translation (Apertus-8B)**

```
Solution:
1. Ensure GPU is being used
2. Use NLLB-200 for faster translations
3. Check system resources (htop/nvidia-smi)
4. Reduce input text length
```

### Logging & Debugging

**Enable verbose logging:**

```bash
# Set environment variable
export TRANSFORMERS_VERBOSITY=debug

# Run app
python gradio_app.py
```

**Check model status:**

```bash
# Run startup check
python startup_check.py --non-interactive
```

**Monitor GPU usage:**

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi
```

---

## Production Checklist

Before deploying to production:

- [ ] Models downloaded and verified (`python startup_check.py`)
- [ ] Application runs without errors locally
- [ ] Language list customized if needed
- [ ] Resource limits configured (CPU/memory/GPU)
- [ ] HTTPS/SSL configured (for public deployment)
- [ ] Monitoring set up (logs, health checks)
- [ ] Backup strategy for model cache
- [ ] Rate limiting configured (if public)
- [ ] Documentation updated with deployment URL
- [ ] Testing performed on target hardware

---

## Support & Resources

- **Documentation**: See project README.md and guides
- **Model Status**: `python startup_check.py --non-interactive`
- **Issues**: Report at project repository
- **HuggingFace Hub**: https://huggingface.co/
- **Docker Docs**: https://docs.docker.com/

---

**Last Updated**: January 2026
**Version**: 2.0.0
**License**: Apache 2.0
