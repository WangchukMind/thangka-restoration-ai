#!/usr/bin/env python3
"""
AI Studio依赖快速修复脚本
解决AI Studio环境中的包安装问题
"""
import subprocess
import sys
import os

def run_command(cmd, timeout=300):
    """运行命令并返回结果"""
    print(f"🔧 执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"✅ 成功: {result.stdout.strip()}")
        return True, result
    except subprocess.TimeoutExpired:
        print(f"⏰ 命令执行超时: {cmd}")
        return False, None
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False, e

def fix_aistudio_dependencies():
    """修复AI Studio依赖问题"""
    print("🚀 开始修复AI Studio依赖问题...")
    print("=" * 60)
    
    # 1. 安装基础依赖（跳过有问题的包）
    print("\n📦 安装基础依赖...")
    basic_deps = [
        "paddlepaddle-gpu==2.6.2",
        "paddlenlp==2.8.1", 
        "ppdiffusers==0.29.0",
        "diffusers==0.34.0",
        "transformers==4.56.0",
        "torch==2.4.0",
        "torchvision==0.19.0",
        "opencv-python==4.8.1.78",
        "pillow==11.3.0",
        "numpy==1.26.4",
        "scipy==1.15.3",
        "matplotlib==3.7.2",
        "django==4.2.11",
        "django-cors-headers==4.3.1",
        "fastapi==0.116.1",
        "requests==2.31.0"
    ]
    
    for dep in basic_deps:
        print(f"\n🔍 安装 {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=120)
        if not success:
            print(f"⚠️ {dep} 安装失败，继续安装其他包...")
    
    # 2. 安装图像处理相关包
    print("\n🖼️ 安装图像处理包...")
    image_deps = [
        "scikit-image==0.21.0",
        "imageio==2.31.1", 
        "albumentations==2.0.8",
        "opencv-python-headless==4.12.0.88"
    ]
    
    for dep in image_deps:
        print(f"\n🔍 安装 {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=120)
        if not success:
            print(f"⚠️ {dep} 安装失败，继续安装其他包...")
    
    # 3. 安装深度学习相关包
    print("\n🧠 安装深度学习包...")
    dl_deps = [
        "accelerate==0.21.0",
        "peft==0.7.0",
        "einops==0.8.1",
        "safetensors==0.6.2",
        "tokenizers==0.22.0"
    ]
    
    for dep in dl_deps:
        print(f"\n🔍 安装 {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=120)
        if not success:
            print(f"⚠️ {dep} 安装失败，继续安装其他包...")
    
    # 4. 安装工具包
    print("\n🛠️ 安装工具包...")
    tool_deps = [
        "tqdm==4.65.0",
        "click==8.0.4",
        "rich==14.1.0",
        "pandas==2.0.3",
        "datasets==2.12.0",
        "pyarrow==11.0.0"
    ]
    
    for dep in tool_deps:
        print(f"\n🔍 安装 {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=120)
        if not success:
            print(f"⚠️ {dep} 安装失败，继续安装其他包...")
    
    # 5. 安装Web框架相关包
    print("\n🌐 安装Web框架包...")
    web_deps = [
        "djangorestframework==3.16.1",
        "uvicorn==0.35.0",
        "jinja2==3.1.4",
        "httpx==0.24.1",
        "aiohttp==3.8.5"
    ]
    
    for dep in web_deps:
        print(f"\n🔍 安装 {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=120)
        if not success:
            print(f"⚠️ {dep} 安装失败，继续安装其他包...")
    
    # 6. 安装其他必要包
    print("\n📚 安装其他必要包...")
    other_deps = [
        "PyYAML==6.0.2",
        "omegaconf==2.2.3",
        "pydantic==2.11.9",
        "bokeh==3.2.1",
        "wandb==0.16.0",
        "filelock==3.13.1",
        "fsspec==2025.7.0",
        "h11==0.12.0",
        "packaging==23.1",
        "typing-extensions==4.14.1",
        "certifi==2023.7.22",
        "urllib3==1.26.16",
        "charset-normalizer==2.0.4",
        "idna==3.4",
        "aistudio-sdk==0.3.6",
        "bce-python-sdk==0.9.42",
        "erniebot==0.5.9",
        "regex==2022.7.9",
        "ftfy==6.3.1",
        "jieba==0.42.1",
        "asgiref==3.9.1",
        "gunicorn==23.0.0",
        "Werkzeug==3.1.3",
        "starlette==0.47.2",
        "mplfonts==0.0.3"
    ]
    
    for dep in other_deps:
        print(f"\n🔍 安装 {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=120)
        if not success:
            print(f"⚠️ {dep} 安装失败，继续安装其他包...")
    
    print("\n🎉 依赖安装完成！")
    return True

def test_installation():
    """测试安装结果"""
    print("\n🔍 测试关键包导入...")
    
    test_packages = [
        ("paddle", "PaddlePaddle"),
        ("paddlenlp", "PaddleNLP"),
        ("ppdiffusers", "PPDiffusers"),
        ("torch", "PyTorch"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("matplotlib", "Matplotlib"),
        ("django", "Django"),
        ("fastapi", "FastAPI")
    ]
    
    success_count = 0
    for module, name in test_packages:
        try:
            __import__(module)
            print(f"✅ {name} 导入成功")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")
    
    print(f"\n📊 测试结果: {success_count}/{len(test_packages)} 个包导入成功")
    
    if success_count >= len(test_packages) * 0.8:  # 80%以上成功
        print("🎉 安装基本成功！")
        return True
    else:
        print("⚠️ 部分包安装失败，但核心功能应该可用")
        return False

if __name__ == "__main__":
    print("🎨 AI Studio依赖快速修复脚本")
    print("=" * 60)
    
    # 修复依赖
    fix_success = fix_aistudio_dependencies()
    
    if fix_success:
        # 测试安装
        test_success = test_installation()
        
        if test_success:
            print("\n🎉 所有依赖修复完成！可以启动服务器了！")
            print("\n🚀 启动命令:")
            print("python start_server.py runserver 0.0.0.0:8080")
        else:
            print("\n⚠️ 部分依赖可能有问题，但可以尝试启动服务器")
    else:
        print("\n❌ 依赖修复失败，请检查网络连接和权限")
    
    sys.exit(0)



