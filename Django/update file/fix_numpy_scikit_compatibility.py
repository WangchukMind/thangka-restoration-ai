#!/usr/bin/env python3
"""
NumPy + scikit-image Compatibility Fix Script - Wangchuk Mind
解决NumPy和scikit-image的二进制兼容性问题
"""
import subprocess
import sys
import os
import time
import shutil
import glob

def run_command(cmd, timeout=300):
    """运行命令并返回结果"""
    print(f"🔧 Executing command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                              capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"✅ Success: {result.stdout.strip()}")
        return True, result
    except subprocess.TimeoutExpired:
        print(f"⏰ Command execution timeout: {cmd}")
        return False, None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command execution failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False, e

def fix_numpy_scikit_compatibility():
    """修复NumPy和scikit-image的兼容性问题"""
    print("🚀 Starting NumPy + scikit-image compatibility fix...")
    print("=" * 60)

    # Step 1: 完全卸载冲突的包
    print("🗑️ Step 1: Uninstalling conflicting packages...")
    packages_to_remove = [
        "numpy", "scikit-image", "opencv-python", "imageio", 
        "scipy", "pillow", "paddlepaddle-gpu"
    ]
    
    for package in packages_to_remove:
        print(f"Removing {package}...")
        run_command(f"pip uninstall {package} -y", timeout=120)
    
    # Step 2: 清理所有相关缓存
    print("🧹 Step 2: Clearing all related caches...")
    cache_patterns = [
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/numpy*/__pycache__",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/skimage*/__pycache__",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/cv2*/__pycache__",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddle*/__pycache__",
        "/home/aistudio/.cache/pip/**/numpy*",
        "/home/aistudio/.cache/pip/**/scikit*",
        "/tmp/pip-*"
    ]
    
    for pattern in cache_patterns:
        cache_dirs = glob.glob(pattern)
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    shutil.rmtree(cache_dir)
                    print(f"Cleared: {cache_dir}")
                except Exception as e:
                    print(f"Could not clear {cache_dir}: {e}")
    
    # Step 3: 清理Python模块缓存
    print("🧹 Step 3: Clearing Python module cache...")
    import sys
    modules_to_clear = [name for name in sys.modules.keys() 
                       if any(keyword in name.lower() for keyword in ['numpy', 'skimage', 'cv2', 'paddle'])]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    print(f"Cleared {len(modules_to_clear)} related modules from cache")
    
    # Step 4: 按照正确的顺序安装兼容版本
    print("📦 Step 4: Installing compatible versions in correct order...")
    
    # 4.1: 首先安装兼容的NumPy版本
    numpy_version = "numpy==1.24.3"  # 使用与scikit-image兼容的版本
    print(f"Installing {numpy_version}...")
    success, _ = run_command(f"pip install {numpy_version} --no-cache-dir", timeout=300)
    if not success:
        print(f"❌ Failed to install {numpy_version}")
        return False
    
    # 4.2: 安装scikit-image
    scikit_version = "scikit-image==0.21.0"
    print(f"Installing {scikit_version}...")
    success, _ = run_command(f"pip install {scikit_version} --no-cache-dir", timeout=300)
    if not success:
        print(f"❌ Failed to install {scikit_version}")
        return False
    
    # 4.3: 安装其他图像处理包
    image_packages = [
        "opencv-python==4.8.1.78",
        "pillow==11.3.0",
        "imageio==2.31.1",
        "scipy==1.15.3"
    ]
    
    for package in image_packages:
        print(f"Installing {package}...")
        success, _ = run_command(f"pip install {package} --no-cache-dir", timeout=300)
        if not success:
            print(f"❌ Failed to install {package}")
            return False
    
    # 4.4: 最后安装PaddlePaddle（使用CPU版本避免GPU相关冲突）
    print("Installing PaddlePaddle CPU version...")
    paddle_strategies = [
        "pip install paddlepaddle==2.6.2 --no-cache-dir",
        "pip install paddlepaddle-gpu==2.6.2 --no-cache-dir"
    ]
    
    paddle_success = False
    for strategy in paddle_strategies:
        print(f"Trying: {strategy}")
        success, _ = run_command(strategy, timeout=300)
        if success:
            print(f"✅ PaddlePaddle installed successfully")
            paddle_success = True
            break
        else:
            print(f"❌ Failed with: {strategy}")
    
    if not paddle_success:
        print("❌ All PaddlePaddle installation strategies failed")
        return False
    
    # Step 5: 验证安装
    print("🧪 Step 5: Verifying installation...")
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} imported successfully")
        
        from skimage.feature import canny
        print("✅ scikit-image imported successfully")
        
        import cv2
        print(f"✅ OpenCV {cv2.__version__} imported successfully")
        
        import PIL
        print(f"✅ Pillow {PIL.__version__} imported successfully")
        
        import paddle
        print(f"✅ PaddlePaddle {paddle.__version__} imported successfully")
        
        # 测试基本功能
        x = np.array([1, 2, 3])
        print("✅ NumPy array creation successful")
        
        x_paddle = paddle.to_tensor([1.0, 2.0, 3.0])
        print("✅ PaddlePaddle tensor creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    success = fix_numpy_scikit_compatibility()
    if success:
        print("\n🎉 NumPy + scikit-image compatibility fix completed successfully!")
        print("🚀 You can now run: python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ Compatibility fix failed. Please check the logs above.")
        sys.exit(1)



