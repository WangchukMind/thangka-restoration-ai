#!/usr/bin/env python3
"""
Quick AI Studio Fix Script - Wangchuk Mind
Quickly fix AI Studio specific issues
"""
import subprocess
import sys
import os

def run_command(cmd, timeout=300):
    """Run command and return result"""
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

def fix_aistudio_issues():
    """Fix AI Studio specific issues"""
    print("🔧 Starting AI Studio quick fix...")
    print("=" * 50)
    
    # Check if we're in AI Studio
    if not os.path.exists('/home/aistudio'):
        print("⚠️ Not in AI Studio environment, skipping AI Studio specific fixes")
        return True
    
    print("🎯 Detected AI Studio environment")
    
    # Step 1: Fix numpy compatibility
    print("\n📦 Step 1: Fixing NumPy compatibility...")
    print("Current NumPy version check...")
    
    try:
        import numpy as np
        print(f"Current NumPy version: {np.__version__}")
        
        if np.__version__.startswith('2.'):
            print("⚠️ NumPy 2.x detected, downgrading to 1.24.3...")
            
            # Uninstall incompatible packages
            packages_to_uninstall = ["numpy", "scikit-image", "opencv-python"]
            for package in packages_to_uninstall:
                print(f"Uninstalling {package}...")
                run_command(f"pip uninstall {package} -y", timeout=120)
            
            # Install compatible versions
            compatible_packages = [
                "numpy==1.24.3",
                "scikit-image==0.21.0", 
                "opencv-python==4.8.1.78"
            ]
            
            for package in compatible_packages:
                print(f"Installing {package}...")
                success, _ = run_command(f"pip install {package}", timeout=300)
                if not success:
                    print(f"❌ Failed to install {package}")
                    return False
            
            print("✅ NumPy compatibility fix completed")
        else:
            print("✅ NumPy version is compatible")
            
    except ImportError:
        print("❌ NumPy not installed, installing compatible version...")
        run_command("pip install numpy==1.24.3", timeout=300)
        run_command("pip install scikit-image==0.21.0", timeout=300)
        run_command("pip install opencv-python==4.8.1.78", timeout=300)
    
    # Step 2: Verify fix
    print("\n🧪 Step 2: Verifying fix...")
    try:
        import numpy as np
        from skimage.feature import canny
        import cv2
        print(f"✅ NumPy {np.__version__} - Compatible")
        print(f"✅ Scikit-image - Compatible")
        print(f"✅ OpenCV {cv2.__version__} - Compatible")
        print("✅ Canny import test - Successful")
        return True
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 AI Studio Quick Fix Script")
    print("=" * 50)
    print("This script fixes AI Studio specific compatibility issues")
    print("")
    
    if fix_aistudio_issues():
        print("\n🎉 AI Studio issues fixed successfully!")
        print("You can now run the Django server:")
        print("python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ AI Studio fix failed!")
        print("Please check the error messages above")
        print("\nManual fix commands:")
        print("pip uninstall numpy scikit-image opencv-python -y")
        print("pip install numpy==1.24.3 scikit-image==0.21.0 opencv-python==4.8.1.78")
        sys.exit(1)

if __name__ == "__main__":
    main()



