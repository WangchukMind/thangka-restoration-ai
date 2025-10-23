# AI Studio 部署指南

## 快速部署步骤

### 1. 上传文件到 AI Studio
将以下文件上传到 AI Studio 项目根目录：
- `start_server_aistudio.py` (新创建的部署脚本)
- `Django/` 目录下的所有文件
- `models/` 目录 (如果已有模型文件)

### 2. 运行部署脚本
在 AI Studio 终端中执行：

```bash
cd /home/aistudio/work/your_project_name
python start_server_aistudio.py runserver 0.0.0.0:8080
```

### 3. 访问系统
部署完成后，访问：
- 主界面：`http://localhost:8080`
- 或通过 AI Studio 提供的公网地址访问

## 部署脚本功能

### 自动安装的依赖包
- **核心计算**: numpy, scipy
- **图像处理**: opencv-python, pillow, scikit-image, imageio, albumentations
- **深度学习**: paddlepaddle-gpu, paddlenlp, ppdiffusers, torch, torchvision, transformers, diffusers
- **Web框架**: Django, django-cors-headers, djangorestframework, channels
- **工具库**: requests, einops, tqdm, matplotlib, seaborn
- **可选包**: mplfonts, gradio, streamlit

### 自动配置
- 设置 Django 环境变量
- 配置 PaddlePaddle 设备 (GPU/CPU)
- 下载或复制模型文件
- 检查依赖兼容性

### 错误处理
- 自动重试失败的安装
- 兼容性检查和修复
- 详细的错误报告

## 注意事项

1. **首次部署**: 脚本会自动安装所有依赖，可能需要 10-15 分钟
2. **模型文件**: 如果模型文件不存在，脚本会尝试从 AI Studio 数据目录复制或从 Git 仓库下载
3. **GPU 支持**: 在 AI Studio 环境中会自动检测并使用 GPU
4. **内存要求**: 建议至少 8GB 内存用于模型加载

## 故障排除

### 如果依赖安装失败
```bash
pip install --upgrade pip
python start_server_aistudio.py runserver 0.0.0.0:8080
```

### 如果模型加载失败
检查 `models/` 目录是否存在，如果不存在：
```bash
mkdir -p models
# 手动上传模型文件到 models/ 目录
```

### 如果端口被占用
```bash
python start_server_aistudio.py runserver 0.0.0.0:8081
```

## 系统要求

- Python 3.8+
- CUDA 11.2+ (推荐)
- 至少 8GB 内存
- 至少 10GB 存储空间

## 成功部署标志

看到以下输出表示部署成功：
```
🎉 Environment setup completed!
🚀 System is ready! Access the web interface to start restoration.
Starting development server at http://0.0.0.0:8080/
```

## 技术支持

如有问题，请检查：
1. Python 版本是否符合要求
2. 网络连接是否正常
3. 存储空间是否充足
4. 查看终端输出的详细错误信息



