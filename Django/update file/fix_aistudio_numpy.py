#!/usr/bin/env python3
"""
AI Studio NumPy Compatibility Fix Script - Wangchuk Mind
Fix numpy version compatibility issues in AI Studio environment
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

def fix_numpy_compatibility():
    """Fix numpy compatibility issues for AI Studio"""
    print("🔧 Starting AI Studio NumPy compatibility fix...")
    print("=" * 60)
    
    # Check current numpy version
    current_version = check_numpy_version()
    if current_version and current_version.startswith('2.'):
        print("⚠️ Detected NumPy 2.x, which is incompatible with scikit-image")
        print("🔧 Downgrading to NumPy 1.24.3 for compatibility...")
        
        # Step 1: Uninstall current numpy and related packages
        print("\n📦 Step 1: Uninstalling incompatible packages...")
        packages_to_uninstall = [
            "numpy",
            "scikit-image",
            "opencv-python"
        ]
        
        for package in packages_to_uninstall:
            print(f"Uninstalling {package}...")
            run_command(f"pip uninstall {package} -y", timeout=120)
        
        # Step 2: Install compatible numpy version
        print("\n📦 Step 2: Installing compatible NumPy 1.24.3...")
        success, _ = run_command("pip install numpy==1.24.3", timeout=300)
        if not success:
            print("❌ Failed to install numpy==1.24.3")
            return False
        
        # Step 3: Install compatible scikit-image
        print("\n📦 Step 3: Installing compatible scikit-image...")
        success, _ = run_command("pip install scikit-image==0.21.0", timeout=300)
        if not success:
            print("❌ Failed to install scikit-image==0.21.0")
            return False
        
        # Step 4: Reinstall opencv-python
        print("\n📦 Step 4: Reinstalling OpenCV...")
        success, _ = run_command("pip install opencv-python==4.8.1.78", timeout=300)
        if not success:
            print("❌ Failed to install opencv-python")
            return False
        
        # Step 5: Verify installation
        print("\n🧪 Step 5: Verifying installation...")
        try:
            import numpy as np
            import skimage
            import cv2
            print(f"✅ NumPy version: {np.__version__}")
            print(f"✅ Scikit-image version: {skimage.__version__}")
            print(f"✅ OpenCV version: {cv2.__version__}")
            
            # Test the specific import that was failing
            from skimage.feature import canny
            print("✅ Canny import successful!")
            
            print("🎉 NumPy compatibility fix successful!")
            return True
            
        except ImportError as e:
            print(f"❌ Import verification failed: {e}")
            return False
        except ValueError as e:
            print(f"❌ Binary compatibility error still exists: {e}")
            return False
    
    elif current_version and current_version.startswith('1.'):
        print("✅ NumPy 1.x detected, checking scikit-image compatibility...")
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

def main():
    """Main function"""
    print("🎨 AI Studio NumPy Compatibility Fix Script")
    print("=" * 60)
    print("This script fixes numpy version compatibility issues in AI Studio")
    print("")
    
    if fix_numpy_compatibility():
        print("\n🎉 NumPy compatibility fix completed successfully!")
        print("You can now run the Django server without numpy compatibility issues.")
        print("\n🚀 Next steps:")
        print("python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ NumPy compatibility fix failed!")
        print("Please check the error messages above and try manual installation:")
        print("pip uninstall numpy scikit-image opencv-python -y")
        print("pip install numpy==1.24.3 scikit-image==0.21.0 opencv-python==4.8.1.78")
        sys.exit(1)

if __name__ == "__main__":
    main()
