#!/usr/bin/env python3
"""
Numpy Compatibility Fix Script - Wangchuk Mind
Fix numpy version compatibility issues with scikit-image
"""
import subprocess
import sys

def run_command(cmd, timeout=120):
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

def fix_numpy_compatibility():
    """Fix numpy compatibility issues"""
    print("🔧 Starting numpy compatibility fix...")
    print("=" * 50)
    
    # Step 1: Uninstall conflicting packages
    print("\n📦 Step 1: Uninstalling conflicting packages...")
    packages_to_uninstall = [
        "scikit-image",
        "numpy"
    ]
    
    for package in packages_to_uninstall:
        print(f"Uninstalling {package}...")
        run_command(f"pip uninstall {package} -y", timeout=60)
    
    # Step 2: Install compatible numpy version
    print("\n📦 Step 2: Installing compatible numpy version...")
    success, _ = run_command("pip install numpy==1.24.3", timeout=120)
    if not success:
        print("❌ Failed to install numpy==1.24.3")
        return False
    
    # Step 3: Install compatible scikit-image version
    print("\n📦 Step 3: Installing compatible scikit-image version...")
    success, _ = run_command("pip install scikit-image==0.21.0", timeout=120)
    if not success:
        print("❌ Failed to install scikit-image==0.21.0")
        return False
    
    # Step 4: Verify installation
    print("\n🧪 Step 4: Verifying installation...")
    try:
        import numpy as np
        import skimage
        print(f"✅ NumPy version: {np.__version__}")
        print(f"✅ Scikit-image version: {skimage.__version__}")
        print("✅ Compatibility fix successful!")
        return True
    except ImportError as e:
        print(f"❌ Import verification failed: {e}")
        return False

def main():
    """Main function"""
    print("🎨 Numpy Compatibility Fix Script")
    print("=" * 50)
    print("This script fixes numpy version compatibility issues with scikit-image")
    print("")
    
    if fix_numpy_compatibility():
        print("\n🎉 Numpy compatibility fix completed successfully!")
        print("You can now run the Django server without numpy compatibility issues.")
    else:
        print("\n❌ Numpy compatibility fix failed!")
        print("Please check the error messages above and try manual installation:")
        print("pip install numpy==1.24.3 scikit-image==0.21.0")
        sys.exit(1)

if __name__ == "__main__":
    main()
