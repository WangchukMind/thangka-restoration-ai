#!/usr/bin/env python3
"""
NumPy Version Conflict Fix Script - Wangchuk Mind
Fix numpy version conflicts caused by imageio installation
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

def check_numpy_version():
    """Check current numpy version"""
    try:
        import numpy as np
        version = np.__version__
        print(f"📊 Current NumPy version: {version}")
        return version
    except ImportError:
        print("❌ NumPy not installed")
        return None

def fix_numpy_version_conflict():
    """Fix numpy version conflict caused by imageio"""
    print("🔧 Fixing NumPy version conflict...")
    print("=" * 50)
    
    # Check current numpy version
    current_version = check_numpy_version()
    if current_version and current_version.startswith('2.'):
        print("⚠️ Detected NumPy 2.x, which causes compatibility issues")
        print("🔧 Downgrading to NumPy 1.x for compatibility...")
        
        # Step 1: Uninstall conflicting packages
        print("\n📦 Step 1: Uninstalling conflicting packages...")
        packages_to_uninstall = [
            "numpy", "scikit-image", "opencv-python", "imageio", "albumentations"
        ]
        
        for package in packages_to_uninstall:
            print(f"Uninstalling {package}...")
            run_command(f"pip uninstall {package} -y", timeout=120)
        
        # Step 2: Install compatible numpy version first
        print("\n📦 Step 2: Installing compatible NumPy version...")
        success, _ = run_command("pip install 'numpy>=1.21.2,<2.0.0'", timeout=300)
        if not success:
            print("❌ Failed to install compatible numpy version")
            return False
        
        # Step 3: Install scikit-image (most sensitive to numpy version)
        print("\n📦 Step 3: Installing scikit-image...")
        success, _ = run_command("pip install scikit-image==0.21.0", timeout=300)
        if not success:
            print("❌ Failed to install scikit-image")
            return False
        
        # Step 4: Install opencv-python
        print("\n📦 Step 4: Installing OpenCV...")
        success, _ = run_command("pip install opencv-python==4.8.1.78", timeout=300)
        if not success:
            print("❌ Failed to install opencv-python")
            return False
        
        # Step 5: Install imageio (with numpy constraint)
        print("\n📦 Step 5: Installing imageio with numpy constraint...")
        success, _ = run_command("pip install 'imageio==2.31.1; numpy<2.0.0'", timeout=300)
        if not success:
            print("⚠️ imageio installation failed, trying without constraint...")
            success, _ = run_command("pip install imageio==2.31.1", timeout=300)
            if not success:
                print("❌ Failed to install imageio")
                return False
        
        # Step 6: Install albumentations
        print("\n📦 Step 6: Installing albumentations...")
        success, _ = run_command("pip install albumentations==2.0.8", timeout=300)
        if not success:
            print("❌ Failed to install albumentations")
            return False
        
        print("\n✅ All packages installed successfully!")
        return True
        
    elif current_version and current_version.startswith('1.'):
        print("✅ NumPy 1.x detected, checking compatibility...")
        try:
            from skimage.feature import canny
            print("✅ Scikit-image is compatible with current NumPy version")
            return True
        except (ImportError, ValueError) as e:
            print(f"⚠️ Scikit-image compatibility issue: {e}")
            print("🔧 Reinstalling scikit-image...")
            run_command("pip uninstall scikit-image -y", timeout=120)
            run_command("pip install scikit-image==0.21.0", timeout=300)
            return True
    else:
        print("❌ Unknown NumPy version or installation issue")
        return False

def verify_fix():
    """Verify that the fix worked"""
    print("\n🧪 Verifying fix...")
    
    try:
        import numpy as np
        from skimage.feature import canny
        import cv2
        import imageio
        import albumentations
        
        print(f"✅ NumPy version: {np.__version__}")
        print(f"✅ Scikit-image: Compatible")
        print(f"✅ OpenCV: {cv2.__version__}")
        print(f"✅ ImageIO: {imageio.__version__}")
        print(f"✅ Albumentations: {albumentations.__version__}")
        
        # Test the specific import that was failing
        from skimage.feature import canny
        print("✅ Canny import successful!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import verification failed: {e}")
        return False
    except ValueError as e:
        print(f"❌ Binary compatibility error still exists: {e}")
        return False

def main():
    """Main function"""
    print("🔧 NumPy Version Conflict Fix Script")
    print("=" * 50)
    print("This script fixes numpy version conflicts caused by imageio installation")
    print("")
    
    if fix_numpy_version_conflict():
        print("\n🎉 NumPy version conflict fix completed!")
        
        if verify_fix():
            print("✅ All packages are working correctly")
            print("You can now run the Django server:")
            print("python start_server.py runserver 0.0.0.0:8080")
        else:
            print("⚠️ Some packages may still have issues, please check the logs above")
    else:
        print("\n❌ NumPy version conflict fix failed!")
        print("Please check the error messages above")
        print("\nManual fix commands:")
        print("pip uninstall numpy scikit-image opencv-python imageio albumentations -y")
        print("pip install 'numpy>=1.21.2,<2.0.0'")
        print("pip install scikit-image==0.21.0 opencv-python==4.8.1.78")
        print("pip install imageio==2.31.1 albumentations==2.0.8")
        sys.exit(1)

if __name__ == "__main__":
    main()



