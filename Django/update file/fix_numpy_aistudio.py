#!/usr/bin/env python3
"""
NumPy Compatibility Fix for AI Studio
专门用于修复AI Studio环境中的NumPy兼容性问题
"""
import subprocess
import sys

def run_command(cmd, timeout=300):
    """Run command with timeout"""
    print(f"🔧 Executing: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ Command timeout: {cmd}")
        return False
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return False

def fix_numpy_compatibility():
    """Fix NumPy compatibility issues"""
    print("🔧 Fixing NumPy compatibility issues in AI Studio...")
    print("=" * 60)
    
    # Step 1: Check current NumPy version
    print("\n📋 Step 1: Checking current NumPy version")
    try:
        import numpy as np
        print(f"Current NumPy version: {np.__version__}")
        if not np.__version__.startswith('2.'):
            print("✅ NumPy version is already compatible")
            return True
    except ImportError:
        print("⚠️ NumPy not installed")
    except Exception as e:
        print(f"⚠️ Error checking NumPy: {e}")
    
    # Step 2: Uninstall incompatible packages
    print("\n📋 Step 2: Uninstalling incompatible packages")
    packages_to_remove = [
        "numpy", "scikit-image", "opencv-python", "imageio", 
        "albumentations", "matplotlib", "seaborn"
    ]
    
    for package in packages_to_remove:
        print(f"Removing {package}...")
        run_command(f"pip uninstall {package} -y", timeout=60)
    
    # Step 3: Install compatible NumPy 1.x
    print("\n📋 Step 3: Installing compatible NumPy 1.x")
    if not run_command("pip install 'numpy>=1.21.2,<2.0.0'", timeout=300):
        print("❌ NumPy installation failed")
        return False
    
    # Step 4: Install compatible image processing packages
    print("\n📋 Step 4: Installing compatible image processing packages")
    compatible_packages = [
        "scikit-image==0.21.0",
        "opencv-python==4.8.1.78", 
        "imageio==2.31.1",
        "albumentations==2.0.8",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0"
    ]
    
    for package in compatible_packages:
        print(f"Installing {package}...")
        if not run_command(f"pip install {package}", timeout=180):
            print(f"⚠️ {package} installation failed, continuing...")
    
    # Step 5: Verify compatibility
    print("\n📋 Step 5: Verifying compatibility")
    try:
        import numpy as np
        from skimage.feature import canny
        import cv2
        print(f"✅ NumPy {np.__version__} import successful")
        print("✅ scikit-image import successful")
        print("✅ OpenCV import successful")
        print("✅ All compatibility checks passed!")
        return True
    except Exception as e:
        print(f"❌ Compatibility verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AI Studio NumPy Compatibility Fix")
    print("=" * 50)
    
    if fix_numpy_compatibility():
        print("\n🎉 NumPy compatibility fix completed successfully!")
        print("✅ You can now run: python start_server_aistudio.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ NumPy compatibility fix failed!")
        print("💡 Please check the error messages above and try again")
        sys.exit(1)



