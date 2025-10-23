# 📦 Model Files Download Guide

## Overview

Due to GitHub's file size limitations, model files (approximately 80GB) are not included in this repository. 

## 🔗 Download Options

### Option 1: AI Studio (Recommended for PaddlePaddle)
```bash
# Download from AI Studio
# Repository: https://aistudio.baidu.com/datasetdetail/...
```

### Option 2: Hugging Face Hub
```bash
# Download from Hugging Face
huggingface-cli download WangchukMind/thangka-restoration-models
```

### Option 3: Direct Download
Large model files are available via:
- **Stable Diffusion 2.1 Base**: [Download Link]
- **LoRA Fine-tuned Models**: [Download Link]
- **Training Dataset**: [Download Link]

## 📁 Required Model Structure

After downloading, place the models in the following structure:

```
Django/
├── models/
│   ├── sd2.1_base_paddle/
│   │   ├── text_encoder/
│   │   │   ├── model.pdparams
│   │   │   ├── model.safetensors
│   │   │   └── config.json
│   │   ├── unet/
│   │   │   ├── model.pdparams
│   │   │   ├── diffusion_pytorch_model.safetensors
│   │   │   └── config.json
│   │   ├── vae/
│   │   │   ├── model.pdparams
│   │   │   ├── diffusion_pytorch_model.safetensors
│   │   │   └── config.json
│   │   └── model_index.json
│   └── finetuned/
│       ├── thangka_21_Status_140/
│       │   └── model.pdparams
│       └── thangka_21_ACD_250/
│           └── model.pdparams
```

## 🚀 Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/WangchukMind/thangka-restoration-ai.git
cd thangka-restoration-ai

# 2. Create models directory
mkdir -p Django/models

# 3. Download and extract models
# [Add specific download commands here]

# 4. Verify installation
python Django/start_server.py check
```

## 📊 Model Specifications

| Model | Size | Format | Purpose |
|-------|------|--------|---------|
| SD 2.1 Base (Text Encoder) | ~2.5GB | .pdparams | Text encoding |
| SD 2.1 Base (UNet) | ~6.5GB | .pdparams | Diffusion model |
| SD 2.1 Base (VAE) | ~638MB | .pdparams | Image encoding/decoding |
| LoRA Fine-tuned (Status) | ~50MB | .pdparams | Thangka style adaptation |
| LoRA Fine-tuned (ACD) | ~50MB | .pdparams | Thangka style adaptation |

## 🔧 Alternative: Use Pre-converted Models

If you prefer to use PyTorch models and convert them:

```bash
# Download PyTorch models
git lfs install
git clone https://huggingface.co/stabilityai/stable-diffusion-2-1-base

# Convert to PaddlePaddle format
python code/bin2ckpt.py --input ./stable-diffusion-2-1-base --output ./Django/models/sd2.1_base_paddle
```

## 📞 Support

For model download issues or questions:
- **Developer**: Wangchuk Mind
- **Issues**: [GitHub Issues](https://github.com/WangchukMind/thangka-restoration-ai/issues)

---

**Note**: Model files are continuously being optimized. Check back for updates on smaller, more efficient versions.
