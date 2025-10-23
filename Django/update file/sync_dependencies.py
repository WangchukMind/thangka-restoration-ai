#!/usr/bin/env python3
"""
Dependency Sync Script - Wangchuk Mind
Sync local environment with requirements.txt
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

def check_current_versions():
    """Check current package versions"""
    print("🔍 Checking current package versions...")
    
    packages_to_check = [
        "paddlepaddle-gpu", "paddlenlp", "ppdiffusers", "Django", 
        "Flask", "scikit-learn", "numpy", "scipy", "torch"
    ]
    
    current_versions = {}
    for package in packages_to_check:
        try:
            if package == "paddlepaddle-gpu":
                import paddle
                current_versions[package] = paddle.__version__
            elif package == "paddlenlp":
                import paddlenlp
                current_versions[package] = paddlenlp.__version__
            elif package == "ppdiffusers":
                import ppdiffusers
                current_versions[package] = ppdiffusers.__version__
            elif package == "Django":
                import django
                current_versions[package] = django.__version__
            elif package == "Flask":
                import flask
                current_versions[package] = flask.__version__
            elif package == "scikit-learn":
                import sklearn
                current_versions[package] = sklearn.__version__
            elif package == "numpy":
                import numpy
                current_versions[package] = numpy.__version__
            elif package == "scipy":
                import scipy
                current_versions[package] = scipy.__version__
            elif package == "torch":
                import torch
                current_versions[package] = torch.__version__
        except ImportError:
            current_versions[package] = "Not installed"
    
    return current_versions

def sync_to_requirements():
    """Sync local environment to requirements.txt versions"""
    print("🔄 Syncing local environment to requirements.txt versions...")
    print("=" * 60)
    
    # Key packages that need version adjustment
    key_packages = [
        "paddlepaddle-gpu==2.6.2",
        "paddlenlp==2.8.1", 
        "ppdiffusers==0.29.0",
        "Django==4.2.11",
        "Flask==3.1.1",
        "scikit-learn==1.7.1"
    ]
    
    print("📦 Installing/updating key packages...")
    for package in key_packages:
        print(f"\n🔧 Installing {package}...")
        success, _ = run_command(f"pip install {package}", timeout=300)
        if success:
            print(f"✅ {package} installed successfully")
        else:
            print(f"❌ Failed to install {package}")
    
    print("\n📦 Installing all requirements...")
    success, _ = run_command("pip install -r requirements.txt", timeout=600)
    if success:
        print("✅ All requirements installed successfully")
        return True
    else:
        print("❌ Some requirements failed to install")
        return False

def verify_sync():
    """Verify that sync was successful"""
    print("\n🧪 Verifying sync results...")
    
    current_versions = check_current_versions()
    
    print("\n📊 Current versions after sync:")
    for package, version in current_versions.items():
        print(f"  {package}: {version}")
    
    # Check if key packages are working
    print("\n🔍 Testing key imports...")
    test_imports = [
        ("paddle", "PaddlePaddle"),
        ("paddlenlp", "PaddleNLP"),
        ("ppdiffusers", "PPDiffusers"),
        ("django", "Django"),
        ("flask", "Flask"),
        ("sklearn", "Scikit-learn"),
        ("numpy", "NumPy"),
        ("torch", "PyTorch")
    ]
    
    all_passed = True
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} import successful")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Main function"""
    print("🔄 Dependency Sync Script")
    print("=" * 60)
    print("This script syncs your local environment with requirements.txt")
    print("")
    
    # Check current versions
    print("📊 Current package versions:")
    current_versions = check_current_versions()
    for package, version in current_versions.items():
        print(f"  {package}: {version}")
    
    print("\n" + "=" * 60)
    
    # Ask user for confirmation
    response = input("Do you want to sync to requirements.txt versions? (y/N): ")
    if response.lower() != 'y':
        print("❌ Sync cancelled by user")
        return
    
    # Perform sync
    if sync_to_requirements():
        print("\n🎉 Sync completed successfully!")
        
        # Verify sync
        if verify_sync():
            print("✅ All packages are working correctly")
            print("\n🚀 You can now run the Django server:")
            print("python start_server.py runserver 0.0.0.0:8080")
        else:
            print("⚠️ Some packages may have issues, please check the logs above")
    else:
        print("❌ Sync failed, please check the error messages above")
        print("\n💡 Manual sync commands:")
        print("pip install paddlepaddle-gpu==2.6.2")
        print("pip install paddlenlp==2.8.1")
        print("pip install ppdiffusers==0.29.0")
        print("pip install Django==4.2.11")
        print("pip install Flask==3.1.1")
        print("pip install scikit-learn==1.7.1")

if __name__ == "__main__":
    main()



