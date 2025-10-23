# 🚀 唐卡修复系统启动指南

## 📋 启动方式

### 方式1：完整智能启动（推荐）
```bash
cd /home/aistudio/work/wangchukthangka/Thangka/Django
python start_server.py runserver 0.0.0.0:8080
```

**特点：**
- ✅ 自动安装所有依赖
- ✅ 智能解决依赖冲突
- ✅ 自动下载模型文件
- ✅ 完整的错误处理和修复
- ✅ 适合首次启动或环境重置

### 方式2：快速启动
```bash
cd /home/aistudio/work/wangchukthangka/Thangka/Django
python quick_start.py runserver 0.0.0.0:8080
```

**特点：**
- ⚡ 快速启动
- 🔍 只检查关键依赖
- 🚀 适合依赖已安装的情况

### 方式3：仅依赖安装
```bash
cd /home/aistudio/work/wangchukthangka/Thangka/Django
python smart_install.py
```

**特点：**
- 📦 只安装依赖，不启动服务器
- 🔧 智能分组安装
- 🛠️ 适合依赖问题排查

## 🔧 故障排除

### 问题1：h11版本冲突
```bash
pip install --upgrade 'h11>=0.14.0' httpx
```

### 问题2：Django导入失败
```bash
pip install django==4.2.11 django-cors-headers==4.3.1
```

### 问题3：PaddlePaddle导入失败
```bash
pip install paddlepaddle-gpu==2.6.2
```

### 问题4：端口被占用
```bash
lsof -ti:8080 | xargs kill -9
```

## 📊 系统要求

### 环境要求
- Python 3.10+
- CUDA支持（推荐）
- 至少8GB内存
- 至少20GB存储空间

### 关键依赖
- PaddlePaddle 2.6.2
- Django 4.2.11
- OpenCV 4.8.1.78
- NumPy >=1.21.2,<2.0.0
- Pillow 11.3.0

## 🎯 功能特性

### 核心功能
- 🖼️ 高质量图像修复
- 🎨 多种生成模式（inpaint, text2img, img2img）
- 🔧 LoRA模型支持
- 📊 实时进度监控
- 📚 修复历史管理
- 🌐 RESTful API

### 技术栈
- **深度学习**: PaddlePaddle, PyTorch
- **Web框架**: Django, FastAPI
- **图像处理**: OpenCV, Pillow, Albumentations
- **AI模型**: Stable Diffusion 2.1, LoRA
- **前端**: React, Webpack

## 🌍 文化影响

- 🏛️ 通过AI技术保护传统唐卡艺术
- 🎭 支持非物质文化遗产保护
- 🌉 连接古代艺术与现代技术
- 🚀 普及专业修复工具

## 👨‍💻 开发信息

**核心开发**: Wangchuk Mind
**技术架构**: Wangchuk Mind
**AI模型集成**: Wangchuk Mind
**Web API开发**: Wangchuk Mind

---

## 🚀 快速开始

1. **首次启动**:
   ```bash
   python start_server.py runserver 0.0.0.0:8080
   ```

2. **访问系统**: 打开浏览器访问 `http://localhost:8080`

3. **开始修复**: 上传唐卡图像，选择修复模式，开始AI修复

---

*如有问题，请查看日志输出或联系开发团队。*



