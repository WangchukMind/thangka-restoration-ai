#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
先进唐卡系统部署脚本 - wangchukMind
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

class AdvancedThangkaDeployer:
    """先进唐卡系统部署器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.models_dir = self.project_root / "models"
        self.config_dir = self.project_root / "configs"
        self.logs_dir = self.project_root / "logs"
        
    def create_directories(self):
        """创建必要的目录"""
        print("🔧 创建系统目录...")
        
        directories = [
            self.models_dir,
            self.models_dir / "sd3",
            self.models_dir / "controlnet",
            self.models_dir / "lora",
            self.models_dir / "llm",
            self.config_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建目录: {directory}")
    
    def create_model_config(self):
        """创建模型配置文件"""
        print("🔧 创建模型配置...")
        
        config = {
            "diffusion": {
                "base_model": "stabilityai/stable-diffusion-3-medium",
                "inpaint_model": "stabilityai/stable-diffusion-3-inpainting",
                "scheduler": "FlowMatchEulerDiscreteScheduler",
                "dtype": "bfloat16",
                "resolution": 1024,
                "batch_size": 1,
                "num_inference_steps": 50,
                "guidance_scale": 15.0,
                "strength": 0.8
            },
            "controlnet": {
                "canny": "lllyasviel/control_v11p_sd15_canny",
                "depth": "lllyasviel/control_v11f1p_sd15_depth",
                "pose": "lllyasviel/control_v11p_sd15_openpose",
                "seg": "lllyasviel/control_v11p_sd15_seg"
            },
            "llm": {
                "primary": "Qwen/Qwen2-VL-72B-Instruct",
                "backup": "liuhaotian/LLaVA-NeXT-72B",
                "specialized": "OpenGVLab/InternVL2-40B",
                "max_tokens": 2048,
                "temperature": 0.7,
                "top_p": 0.9
            },
            "lora": {
                "artistic": "thangka_artistic_v2.0.safetensors",
                "colors": "thangka_colors_v1.5.safetensors",
                "patterns": "thangka_patterns_v1.8.safetensors",
                "details": "thangka_details_v2.1.safetensors"
            },
            "optimization": {
                "memory": {
                    "attention_slicing": True,
                    "cpu_offload": True,
                    "sequential_cpu_offload": True,
                    "memory_efficient_attention": True
                },
                "inference": {
                    "compile_model": True,
                    "torch_compile": True,
                    "xformers": True,
                    "flash_attention": True
                },
                "distributed": {
                    "model_parallel": True,
                    "pipeline_parallel": True,
                    "tensor_parallel": True
                }
            }
        }
        
        config_path = self.config_dir / "model_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 模型配置已保存: {config_path}")
    
    def create_system_config(self):
        """创建系统配置文件"""
        print("🔧 创建系统配置...")
        
        config = {
            "system": {
                "name": "Advanced Thangka AI System",
                "version": "2.0.0",
                "description": "先进唐卡修复与大语言模型系统",
                "author": "wangchukMind"
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8080,
                "workers": 4,
                "timeout": 300,
                "max_requests": 1000
            },
            "gpu": {
                "enabled": True,
                "device_ids": [0, 1, 2, 3],
                "memory_fraction": 0.9,
                "allow_growth": True
            },
            "storage": {
                "models_path": "./models",
                "cache_path": "./cache",
                "logs_path": "./logs",
                "temp_path": "./temp"
            },
            "api": {
                "rate_limit": "100/minute",
                "max_file_size": "50MB",
                "allowed_formats": ["png", "jpg", "jpeg"],
                "timeout": 300
            }
        }
        
        config_path = self.config_dir / "system_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 系统配置已保存: {config_path}")
    
    def create_requirements(self):
        """创建依赖文件"""
        print("🔧 创建依赖文件...")
        
        requirements = [
            "paddlepaddle-gpu>=2.6.0",
            "diffusers>=0.24.0",
            "transformers>=4.35.0",
            "torch>=2.1.0",
            "torchvision>=0.16.0",
            "accelerate>=0.24.0",
            "xformers>=0.0.22",
            "opencv-python>=4.8.0",
            "Pillow>=10.0.0",
            "numpy>=1.24.0",
            "scikit-image>=0.21.0",
            "safetensors>=0.4.0",
            "Django>=4.2.0",
            "djangorestframework>=3.14.0",
            "channels>=4.0.0",
            "redis>=5.0.0",
            "celery>=5.3.0",
            "gunicorn>=21.2.0",
            "uvicorn>=0.24.0",
            "fastapi>=0.104.0",
            "websockets>=12.0",
            "aiofiles>=23.2.0",
            "python-multipart>=0.0.6",
            "httpx>=0.25.0",
            "pydantic>=2.5.0",
            "loguru>=0.7.0",
            "tqdm>=4.66.0",
            "wandb>=0.16.0",
            "tensorboard>=2.15.0"
        ]
        
        requirements_path = self.project_root / "requirements_advanced.txt"
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
        
        print(f"✅ 依赖文件已保存: {requirements_path}")
    
    def create_docker_config(self):
        """创建Docker配置"""
        print("🔧 创建Docker配置...")
        
        # Dockerfile
        dockerfile_content = """FROM nvidia/cuda:12.1-devel-ubuntu22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0,1,2,3

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    python3.10 \\
    python3.10-dev \\
    python3-pip \\
    git \\
    wget \\
    curl \\
    build-essential \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    && rm -rf /var/lib/apt/lists/*

# 设置Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements_advanced.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements_advanced.txt

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p models logs cache temp

# 设置权限
RUN chmod +x *.py

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "start_advanced_server.py"]
"""
        
        dockerfile_path = self.project_root / "Dockerfile.advanced"
        with open(dockerfile_path, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        # docker-compose.yml
        compose_content = """version: '3.8'

services:
  thangka-ai:
    build:
      context: .
      dockerfile: Dockerfile.advanced
    ports:
      - "8080:8080"
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
      - ./cache:/app/cache
      - ./temp:/app/temp
    environment:
      - CUDA_VISIBLE_DEVICES=0,1,2,3
      - PADDLE_CUDNN_DETERMINISTIC=1
      - PADDLE_CUDNN_BENCHMARK=1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 4
              capabilities: [gpu]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - thangka-ai
    restart: unless-stopped

volumes:
  redis_data:
"""
        
        compose_path = self.project_root / "docker-compose.advanced.yml"
        with open(compose_path, 'w', encoding='utf-8') as f:
            f.write(compose_content)
        
        print(f"✅ Docker配置已保存: {dockerfile_path}, {compose_path}")
    
    def create_startup_script(self):
        """创建启动脚本"""
        print("🔧 创建启动脚本...")
        
        startup_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
先进唐卡系统启动脚本 - wangchukMind
\"\"\"

import os
import sys
import time
import signal
import subprocess
from pathlib import Path

def signal_handler(sig, frame):
    print('\\n🛑 收到停止信号，正在关闭系统...')
    sys.exit(0)

def check_gpu():
    \"\"\"检查GPU状态\"\"\"
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU状态正常")
            return True
        else:
            print("⚠️ GPU状态异常")
            return False
    except Exception as e:
        print(f"❌ GPU检查失败: {e}")
        return False

def check_dependencies():
    \"\"\"检查依赖\"\"\"
    try:
        import paddle
        import torch
        import diffusers
        print("✅ 核心依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 依赖检查失败: {e}")
        return False

def start_system():
    \"\"\"启动系统\"\"\"
    try:
        print("🚀 启动先进唐卡系统...")
        
        # 检查GPU
        if not check_gpu():
            print("⚠️ GPU不可用，将使用CPU模式")
        
        # 检查依赖
        if not check_dependencies():
            print("❌ 依赖检查失败，请安装所需依赖")
            return False
        
        # 导入并启动系统
        from advanced_thangka_models import AdvancedThangkaSystem
        
        system = AdvancedThangkaSystem()
        if system.initialize():
            print("✅ 系统启动成功")
            
            # 保持运行
            while True:
                time.sleep(1)
        else:
            print("❌ 系统启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        return False

if __name__ == "__main__":
    # 设置信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动系统
    start_system()
"""
        
        startup_path = self.project_root / "start_advanced_server.py"
        with open(startup_path, 'w', encoding='utf-8') as f:
            f.write(startup_content)
        
        # 设置执行权限
        os.chmod(startup_path, 0o755)
        
        print(f"✅ 启动脚本已保存: {startup_path}")
    
    def create_nginx_config(self):
        """创建Nginx配置"""
        print("🔧 创建Nginx配置...")
        
        nginx_content = """events {
    worker_connections 1024;
}

http {
    upstream thangka_backend {
        server thangka-ai:8080;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        client_max_body_size 50M;
        
        location / {
            proxy_pass http://thangka_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            
            # 超时设置
            proxy_connect_timeout 300s;
            proxy_send_timeout 300s;
            proxy_read_timeout 300s;
        }
        
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        location /media/ {
            alias /app/media/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
"""
        
        nginx_path = self.project_root / "nginx.conf"
        with open(nginx_path, 'w', encoding='utf-8') as f:
            f.write(nginx_content)
        
        print(f"✅ Nginx配置已保存: {nginx_path}")
    
    def create_deployment_script(self):
        """创建部署脚本"""
        print("🔧 创建部署脚本...")
        
        deploy_content = """#!/bin/bash
# 先进唐卡系统部署脚本 - wangchukMind

set -e

echo "🚀 开始部署先进唐卡系统..."

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查NVIDIA Docker支持
if ! docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi &> /dev/null; then
    echo "⚠️ NVIDIA Docker支持未检测到，将使用CPU模式"
fi

# 创建必要目录
mkdir -p models logs cache temp ssl

# 构建镜像
echo "🔧 构建Docker镜像..."
docker-compose -f docker-compose.advanced.yml build

# 启动服务
echo "🚀 启动服务..."
docker-compose -f docker-compose.advanced.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.advanced.yml ps

# 检查健康状态
echo "🏥 检查健康状态..."
curl -f http://localhost:8080/health || echo "⚠️ 健康检查失败"

echo "✅ 部署完成！"
echo "🌐 访问地址: http://localhost:8080"
echo "📊 监控地址: http://localhost:8080/admin"
"""
        
        deploy_path = self.project_root / "deploy_advanced.sh"
        with open(deploy_path, 'w', encoding='utf-8') as f:
            f.write(deploy_content)
        
        # 设置执行权限
        os.chmod(deploy_path, 0o755)
        
        print(f"✅ 部署脚本已保存: {deploy_path}")
    
    def deploy(self):
        """执行部署"""
        print("🚀 开始部署先进唐卡系统...")
        
        try:
            # 1. 创建目录
            self.create_directories()
            
            # 2. 创建配置文件
            self.create_model_config()
            self.create_system_config()
            
            # 3. 创建依赖文件
            self.create_requirements()
            
            # 4. 创建Docker配置
            self.create_docker_config()
            
            # 5. 创建启动脚本
            self.create_startup_script()
            
            # 6. 创建Nginx配置
            self.create_nginx_config()
            
            # 7. 创建部署脚本
            self.create_deployment_script()
            
            print("✅ 先进唐卡系统部署配置完成！")
            print("\n📋 下一步操作:")
            print("  1. 安装依赖: pip install -r requirements_advanced.txt")
            print("  2. 下载模型: 将模型文件放入 models/ 目录")
            print("  3. 启动系统: python start_advanced_server.py")
            print("  4. 或使用Docker: ./deploy_advanced.sh")
            
        except Exception as e:
            print(f"❌ 部署失败: {e}")

def main():
    """主函数"""
    deployer = AdvancedThangkaDeployer()
    deployer.deploy()

if __name__ == "__main__":
    main()



