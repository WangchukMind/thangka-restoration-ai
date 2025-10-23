# 唐卡修复系统依赖库分析报告

## 📊 依赖库分类分析

### ✅ **核心必需库 (Core Essential)**

| 包名 | 用途 | 代码位置 | 必要性 |
|------|------|----------|--------|
| **paddlepaddle-gpu** | 深度学习框架 | diffusion_paddle.py | ✅ 必需 |
| **paddlenlp** | PaddlePaddle NLP | 可能用于文本处理 | ⚠️ 可能必需 |
| **ppdiffusers** | PaddlePaddle扩散模型 | diffusion_paddle.py | ✅ 必需 |
| **numpy** | 数值计算 | diffusion_paddle.py, images_paddle.py | ✅ 必需 |
| **PIL (pillow)** | 图像处理 | diffusion_paddle.py, images_paddle.py | ✅ 必需 |
| **opencv-python** | 计算机视觉 | diffusion_paddle.py, images_paddle.py | ✅ 必需 |
| **scikit-image** | 图像处理 | diffusion_paddle.py | ✅ 必需 |
| **Django** | Web框架 | 所有Django文件 | ✅ 必需 |
| **django-cors-headers** | CORS支持 | settings.py | ✅ 必需 |
| **erniebot** | 文心一言API | ernie_bot_paddle.py | ✅ 必需 |

### ⚠️ **可能必需库 (Possibly Essential)**

| 包名 | 用途 | 代码位置 | 必要性 |
|------|------|----------|--------|
| **torch** | PyTorch框架 | diffusion.py, images.py | ⚠️ 备用版本 |
| **torchvision** | PyTorch视觉 | 可能用于图像变换 | ⚠️ 备用版本 |
| **diffusers** | Hugging Face扩散模型 | diffusion.py | ⚠️ 备用版本 |
| **transformers** | 预训练模型 | 可能用于文本处理 | ⚠️ 可能必需 |
| **accelerate** | 模型加速 | 可能用于模型优化 | ⚠️ 可能必需 |
| **peft** | 参数高效微调 | 可能用于LoRA | ⚠️ 可能必需 |

### ❌ **非必需库 (Non-Essential)**

| 包名 | 用途 | 必要性 | 建议 |
|------|------|--------|------|
| **pandas** | 数据分析 | ❌ 未使用 | 可删除 |
| **datasets** | 数据集处理 | ❌ 未使用 | 可删除 |
| **pyarrow** | 数据序列化 | ❌ 未使用 | 可删除 |
| **scipy** | 科学计算 | ❌ 未使用 | 可删除 |
| **scikit-learn** | 机器学习 | ❌ 未使用 | 可删除 |
| **matplotlib** | 绘图 | ❌ 未使用 | 可删除 |
| **bokeh** | 交互式绘图 | ❌ 未使用 | 可删除 |
| **wandb** | 实验跟踪 | ❌ 未使用 | 可删除 |
| **tqdm** | 进度条 | ❌ 未使用 | 可删除 |
| **click** | 命令行工具 | ❌ 未使用 | 可删除 |
| **colorama** | 彩色输出 | ❌ 未使用 | 可删除 |
| **rich** | 富文本显示 | ❌ 未使用 | 可删除 |
| **filelock** | 文件锁定 | ❌ 未使用 | 可删除 |
| **fsspec** | 文件系统 | ❌ 未使用 | 可删除 |
| **h11** | HTTP协议 | ❌ 未使用 | 可删除 |
| **packaging** | 包管理 | ❌ 未使用 | 可删除 |
| **typing-extensions** | 类型提示 | ❌ 未使用 | 可删除 |
| **certifi** | SSL证书 | ❌ 未使用 | 可删除 |
| **urllib3** | HTTP客户端 | ❌ 未使用 | 可删除 |
| **charset-normalizer** | 字符编码 | ❌ 未使用 | 可删除 |
| **idna** | 国际化域名 | ❌ 未使用 | 可删除 |
| **aistudio-sdk** | AI Studio SDK | ❌ 未使用 | 可删除 |
| **bce-python-sdk** | 百度云SDK | ❌ 未使用 | 可删除 |
| **erniebot-agent** | 文心一言代理 | ❌ 未使用 | 可删除 |
| **regex** | 正则表达式 | ❌ 未使用 | 可删除 |
| **ftfy** | 文本修复 | ❌ 未使用 | 可删除 |
| **jieba** | 中文分词 | ❌ 未使用 | 可删除 |
| **asgiref** | ASGI支持 | ❌ 未使用 | 可删除 |
| **gunicorn** | WSGI服务器 | ❌ 未使用 | 可删除 |
| **Werkzeug** | WSGI工具 | ❌ 未使用 | 可删除 |
| **starlette** | ASGI框架 | ❌ 未使用 | 可删除 |
| **paddle2onnx** | 模型转换 | ❌ 未使用 | 可删除 |
| **paddlefsl** | 少样本学习 | ❌ 未使用 | 可删除 |
| **paddlesde** | 随机微分方程 | ❌ 未使用 | 可删除 |
| **pillow-avif-plugin** | AVIF支持 | ❌ 未使用 | 可删除 |
| **matplotlib-inline** | 内联绘图 | ❌ 未使用 | 可删除 |
| **numpydoc** | NumPy文档 | ❌ 未使用 | 可删除 |
| **open-clip-torch** | CLIP模型 | ❌ 未使用 | 可删除 |
| **pytorch-lightning** | PyTorch框架 | ❌ 未使用 | 可删除 |
| **torchdiffeq** | 微分方程 | ❌ 未使用 | 可删除 |
| **torchmetrics** | 评估指标 | ❌ 未使用 | 可删除 |
| **torchsde** | 随机微分方程 | ❌ 未使用 | 可删除 |
| **requests-file** | 文件请求 | ❌ 未使用 | 可删除 |
| **requests-mock** | 请求模拟 | ❌ 未使用 | 可删除 |
| **requests-toolbelt** | 请求工具 | ❌ 未使用 | 可删除 |
| **ruamel.yaml** | YAML处理 | ❌ 未使用 | 可删除 |
| **pydantic_core** | 数据验证 | ❌ 未使用 | 可删除 |
| **flask-babel** | Flask国际化 | ❌ 未使用 | 可删除 |

### 🔄 **Web框架冗余 (Web Framework Redundancy)**

| 包名 | 用途 | 必要性 | 建议 |
|------|------|--------|------|
| **fastapi** | 现代Web框架 | ❌ 未使用 | 可删除 |
| **Flask** | 轻量级Web框架 | ❌ 未使用 | 可删除 |
| **uvicorn** | ASGI服务器 | ❌ 未使用 | 可删除 |
| **jinja2** | 模板引擎 | ❌ 未使用 | 可删除 |

### 🔄 **HTTP客户端冗余 (HTTP Client Redundancy)**

| 包名 | 用途 | 必要性 | 建议 |
|------|------|--------|------|
| **httpx** | 现代HTTP客户端 | ❌ 未使用 | 可删除 |
| **aiohttp** | 异步HTTP客户端 | ❌ 未使用 | 可删除 |

### 🔄 **配置处理冗余 (Configuration Redundancy)**

| 包名 | 用途 | 必要性 | 建议 |
|------|------|--------|------|
| **PyYAML** | YAML处理 | ❌ 未使用 | 可删除 |
| **omegaconf** | 配置管理 | ❌ 未使用 | 可删除 |
| **pydantic** | 数据验证 | ❌ 未使用 | 可删除 |

## 📋 **精简后的requirements.txt建议**

```txt
# 唐卡修复系统核心依赖
# 深度学习框架
paddlepaddle-gpu==2.6.2
paddlenlp==2.8.1
ppdiffusers==0.29.0

# 图像处理
opencv-python==4.8.1.78
pillow==11.3.0
scikit-image==0.21.0
imageio==2.31.1
albumentations==2.0.8

# 数值计算
numpy>=1.21.2,<2.0.0

# Web框架
Django==4.2.11
django-cors-headers==4.3.1
djangorestframework==3.16.1

# HTTP客户端
requests==2.31.0

# 文心一言API
erniebot==0.5.9

# 基础依赖
einops==0.8.1
```

## 🎯 **优化建议**

### **立即删除 (Immediate Removal)**
- 所有未使用的科学计算库 (pandas, scipy, scikit-learn等)
- 所有未使用的可视化库 (matplotlib, bokeh, wandb等)
- 所有未使用的工具库 (tqdm, click, rich等)
- 所有未使用的Web框架 (fastapi, flask等)
- 所有未使用的HTTP客户端 (httpx, aiohttp等)

### **保留备用 (Keep as Backup)**
- torch, torchvision, diffusers (备用PyTorch版本)
- transformers, accelerate, peft (可能用于高级功能)

### **监控使用 (Monitor Usage)**
- paddlenlp (检查是否实际使用)
- 各种PaddlePaddle扩展包

## 📊 **优化效果预估**

| 指标 | 当前 | 优化后 | 改善 |
|------|------|--------|------|
| **包数量** | 75+ | 15-20 | -70% |
| **安装时间** | 10-15分钟 | 3-5分钟 | -60% |
| **磁盘空间** | 2-3GB | 500MB-1GB | -70% |
| **内存占用** | 高 | 低 | -50% |
| **启动速度** | 慢 | 快 | +100% |

## 🚀 **实施步骤**

1. **创建精简版requirements.txt**
2. **测试核心功能**
3. **逐步删除非必需包**
4. **验证系统稳定性**
5. **更新部署脚本**



