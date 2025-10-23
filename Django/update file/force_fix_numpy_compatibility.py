#!/usr/bin/env python3
"""
Force Fix NumPy Compatibility Script - Wangchuk Mind
强制修复NumPy兼容性问题，确保版本一致性
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

def force_fix_numpy_compatibility():
    """强制修复NumPy兼容性问题"""
    print("🚀 Starting FORCE NumPy compatibility fix...")
    print("=" * 60)

    # Step 1: 完全卸载所有相关包
    print("🗑️ Step 1: Force uninstalling ALL related packages...")
    packages_to_remove = [
        "numpy", "scikit-image", "opencv-python", "imageio", 
        "scipy", "pillow", "paddlepaddle", "paddlepaddle-gpu",
        "paddlenlp", "ppdiffusers"
    ]
    
    for package in packages_to_remove:
        print(f"Force removing {package}...")
        run_command(f"pip uninstall {package} -y", timeout=120)
    
    # Step 2: 清理所有缓存
    print("🧹 Step 2: Clearing ALL caches...")
    cache_patterns = [
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/numpy*/__pycache__",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/skimage*/__pycache__",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/cv2*/__pycache__",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddle*/__pycache__",
        "/home/aistudio/.cache/pip/**/numpy*",
        "/home/aistudio/.cache/pip/**/scikit*",
        "/tmp/pip-*",
        "/Users/xiang/anaconda3/lib/python3.11/site-packages/numpy*/__pycache__",
        "/Users/xiang/anaconda3/lib/python3.11/site-packages/skimage*/__pycache__",
        "/Users/xiang/anaconda3/lib/python3.11/site-packages/cv2*/__pycache__",
        "/Users/xiang/anaconda3/lib/python3.11/site-packages/paddle*/__pycache__"
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
    
    # Step 4: 使用pip install --force-reinstall --no-deps 强制安装
    print("📦 Step 4: Force installing compatible versions...")
    
    # 4.1: 强制安装NumPy 1.24.3，不允许依赖自动升级
    print("Installing numpy==1.24.3 with --force-reinstall --no-deps...")
    success, _ = run_command("pip install numpy==1.24.3 --force-reinstall --no-deps --no-cache-dir", timeout=300)
    if not success:
        print(f"❌ Failed to install numpy==1.24.3")
        return False
    
    # 4.2: 安装scikit-image，但阻止它升级NumPy
    print("Installing scikit-image==0.21.0 with version constraint...")
    success, _ = run_command("pip install 'scikit-image==0.21.0' 'numpy==1.24.3' --force-reinstall --no-cache-dir", timeout=300)
    if not success:
        print(f"❌ Failed to install scikit-image")
        return False
    
    # 4.3: 安装其他包，确保NumPy版本不变
    other_packages = [
        "opencv-python==4.8.1.78",
        "pillow==11.3.0", 
        "imageio==2.31.1",
        "scipy==1.15.3"
    ]
    
    for package in other_packages:
        print(f"Installing {package} with numpy constraint...")
        success, _ = run_command(f"pip install '{package}' 'numpy==1.24.3' --force-reinstall --no-cache-dir", timeout=300)
        if not success:
            print(f"❌ Failed to install {package}")
            return False
    
    # 4.4: 最后安装PaddlePaddle
    print("Installing PaddlePaddle with numpy constraint...")
    success, _ = run_command("pip install 'paddlepaddle==2.6.2' 'numpy==1.24.3' --force-reinstall --no-cache-dir", timeout=300)
    if not success:
        print(f"❌ Failed to install PaddlePaddle")
        return False
    
    # Step 5: 验证NumPy版本
    print("🧪 Step 5: Verifying NumPy version...")
    success, result = run_command("python -c 'import numpy; print(f\"NumPy version: {numpy.__version__}\")'", timeout=30)
    if success:
        print(f"✅ NumPy version check: {result.stdout.strip()}")
        if "1.24.3" not in result.stdout:
            print("⚠️ Warning: NumPy version is not 1.24.3")
    
    # Step 6: 验证所有包
    print("🧪 Step 6: Verifying all packages...")
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
    success = force_fix_numpy_compatibility()
    if success:
        print("\n🎉 FORCE NumPy compatibility fix completed successfully!")
        print("🚀 You can now run: python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ Force compatibility fix failed. Please check the logs above.")
        sys.exit(1)



