# 🚀 Deployment Guide

## AI + Intangible Cultural Heritage Thangka Image Restoration System

This guide will help you deploy the system to various platforms including GitHub, Hugging Face, and cloud services.

## 📋 Prerequisites

- Git installed and configured
- Python 3.9+ installed
- Docker installed (optional)
- GitHub account
- Hugging Face account (optional)

## 🔧 Quick Deployment

### 1. GitHub Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "🎨 Initial commit: AI + Intangible Cultural Heritage Thangka Image Restoration System"

# Add remote repository
git remote add origin https://github.com/yourusername/thangka-restoration-ai.git

# Push to GitHub
git push -u origin main
```

### 2. Hugging Face Hub

```bash
# Install Hugging Face Hub
pip install huggingface_hub

# Set your token
export HF_TOKEN=your_huggingface_token_here

# Upload to Hugging Face
python -c "
from huggingface_hub import HfApi
api = HfApi()
api.create_repo(repo_id='yourusername/thangka-restoration-ai', exist_ok=True)
api.upload_folder(folder_path='.', repo_id='yourusername/thangka-restoration-ai')
"
```

### 3. Docker Deployment

```bash
# Build Docker image
docker build -t thangka-restoration-ai:latest .

# Run container
docker run -d \
  --name thangka-restoration \
  --gpus all \
  -p 8000:8000 \
  -v $(pwd)/Django/server/media:/app/Django/server/media \
  thangka-restoration-ai:latest
```

### 4. Automated Deployment

```bash
# Run the automated deployment script
python deploy_to_platforms.py
```

## 🌐 Platform-Specific Instructions

### GitHub

1. Create a new repository on GitHub
2. Update the repository URL in `setup.py` and `README.md`
3. Push your code using the commands above
4. Enable GitHub Actions for CI/CD

### Hugging Face Hub

1. Create a new model repository on Hugging Face
2. Set your HF_TOKEN environment variable
3. Run the upload script
4. Update the model card with your specific details

### Docker Hub

```bash
# Tag your image
docker tag thangka-restoration-ai:latest yourusername/thangka-restoration-ai:latest

# Push to Docker Hub
docker push yourusername/thangka-restoration-ai:latest
```

### Cloud Platforms

#### AWS

```bash
# Build for AWS
docker build -t thangka-restoration-ai .

# Tag for ECR
docker tag thangka-restoration-ai:latest your-account.dkr.ecr.region.amazonaws.com/thangka-restoration-ai:latest

# Push to ECR
aws ecr get-login-password --region region | docker login --username AWS --password-stdin your-account.dkr.ecr.region.amazonaws.com
docker push your-account.dkr.ecr.region.amazonaws.com/thangka-restoration-ai:latest
```

#### Google Cloud

```bash
# Build for GCP
docker build -t gcr.io/your-project/thangka-restoration-ai .

# Push to GCR
docker push gcr.io/your-project/thangka-restoration-ai
```

#### Azure

```bash
# Build for Azure
docker build -t your-registry.azurecr.io/thangka-restoration-ai:latest .

# Push to ACR
docker push your-registry.azurecr.io/thangka-restoration-ai:latest
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
PADDLE_FRAMEWORK=paddle
PADDLE_DEVICE=gpu  # or cpu
CUDA_VISIBLE_DEVICES=0

# Optional
DJANGO_SETTINGS_MODULE=server.settings
SKIP_MODEL_LOADING=0
```

### Model Files

Ensure model files are properly configured:

```bash
# Create model directories
mkdir -p Django/models/sd2.1_base_paddle
mkdir -p Django/models/finetuned

# Download or place your model files
# - Stable Diffusion 2.1 base model
# - LoRA fine-tuned models
# - Preprocessor configurations
```

## 📊 Monitoring and Logging

### Health Checks

```bash
# Check if the service is running
curl http://localhost:8000/api/test/

# Check model loading status
curl http://localhost:8000/api/getType/
```

### Logs

```bash
# View application logs
docker logs thangka-restoration

# View specific logs
docker logs thangka-restoration 2>&1 | grep ERROR
```

## 🚨 Troubleshooting

### Common Issues

1. **GPU not detected**
   ```bash
   # Check GPU availability
   nvidia-smi
   
   # Ensure Docker has GPU support
   docker run --rm --gpus all nvidia/cuda:11.2-base-ubuntu20.04 nvidia-smi
   ```

2. **Model loading failed**
   ```bash
   # Check model files
   ls -la Django/models/
   
   # Verify model paths in configuration
   python -c "import server.models.diffusion_paddle as d; print(d.getModelType())"
   ```

3. **Port already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   
   # Kill the process
   kill -9 <PID>
   ```

## 📈 Performance Optimization

### GPU Optimization

```bash
# Set optimal GPU memory allocation
export PADDLE_FRAMEWORK=paddle
export PADDLE_DEVICE=gpu
export CUDA_VISIBLE_DEVICES=0
```

### Memory Optimization

```bash
# Reduce memory usage
export PADDLE_MEMORY_FRACTION=0.8
export PADDLE_MEMORY_GROWTH=true
```

## 🔒 Security Considerations

1. **API Security**
   - Implement rate limiting
   - Add authentication if needed
   - Use HTTPS in production

2. **Model Security**
   - Keep model files secure
   - Implement access controls
   - Regular security updates

## 📞 Support

For deployment issues or questions:

- **Developer**: Wangchuk Mind
- **Project**: AI + Intangible Cultural Heritage Thangka Restoration
- **Issues**: GitHub Issues
- **Documentation**: Project Wiki

---

**Made with ❤️ for cultural heritage preservation**
