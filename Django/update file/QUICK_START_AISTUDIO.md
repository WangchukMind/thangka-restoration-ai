# AI Studio 快速部署指南

## 方法一：一键部署（推荐）

```bash
python start_server_aistudio.py runserver 0.0.0.0:8080
```

## 方法二：分步部署（如果遇到NumPy兼容性问题）

### 步骤1：修复NumPy兼容性
```bash
python fix_numpy_aistudio.py
```

### 步骤2：启动服务器
```bash
python start_server_aistudio.py runserver 0.0.0.0:8080
```

## 部署流程

1. **自动环境检查** - 检查 Python 版本
2. **依赖安装** - 自动安装所有必需的包
3. **模型下载** - 下载或复制模型文件
4. **Django 配置** - 设置 Web 服务器
5. **启动服务** - 在 0.0.0.0:8080 启动

## 预期输出

```
🚀 AI Studio Complete Deployment Script
==================================================

📋 Step 1: Checking Python environment
✅ Python version: Python 3.10.x

📋 Step 2: Installing dependencies
📊 Group 1: Installing core numerical computing...
✅ numpy>=1.21.2,<2.0.0 installed successfully
...

📋 Step 3: Downloading models
✅ Model files copied successfully

📋 Step 4: Setting up Django environment
✅ Django environment setup completed

📋 Step 5: Final dependency check
✅ NumPy import successful
✅ OpenCV import successful
...

🎉 Environment setup completed!
🚀 System is ready! Access the web interface to start restoration.

🚀 Starting Django server...
Starting development server at http://0.0.0.0:8080/
```

## 访问系统

部署成功后，访问：
- **本地访问**: http://localhost:8080
- **公网访问**: 使用 AI Studio 提供的公网地址

## 故障排除

### 如果遇到NumPy兼容性错误
```bash
# 运行NumPy修复脚本
python fix_numpy_aistudio.py

# 然后重新启动
python start_server_aistudio.py runserver 0.0.0.0:8080
```

### 如果安装失败
```bash
pip install --upgrade pip setuptools wheel
python start_server_aistudio.py runserver 0.0.0.0:8080
```

### 如果端口被占用
```bash
python start_server_aistudio.py runserver 0.0.0.0:8081
```

### 如果模型加载失败
检查 models 目录是否存在，手动创建：
```bash
mkdir -p models
```

### 如果OpenCV导入失败
```bash
pip uninstall opencv-python -y
pip install opencv-python==4.8.1.78
```

### 如果scikit-image导入失败
```bash
pip uninstall scikit-image -y
pip install scikit-image==0.21.0
```

## 系统要求

- Python 3.8+
- 至少 8GB 内存
- 至少 10GB 存储空间
- CUDA 11.2+ (推荐，用于 GPU 加速)

## 注意事项

- 首次部署需要 10-15 分钟安装依赖
- 确保网络连接稳定
- 如果遇到权限问题，可能需要使用 `sudo`
