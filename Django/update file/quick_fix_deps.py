#!/usr/bin/env python3
"""
Quick Dependency Fix Script - Wangchuk Mind
Fix missing critical dependencies quickly
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

def fix_critical_dependencies():
    """Fix critical missing dependencies"""
    print("🔧 Starting quick dependency fix...")
    print("=" * 50)
    
    # Critical dependencies that are missing
    critical_deps = [
        ("django==4.2.11", "Django"),
        ("torch==2.4.0", "PyTorch"),
        ("django-cors-headers==4.3.1", "Django CORS")
    ]
    
    success_count = 0
    for package, name in critical_deps:
        print(f"\n📦 Installing {name}...")
        success, _ = run_command(f"pip install {package}", timeout=180)
        if success:
            print(f"✅ {name} installed successfully")
            success_count += 1
        else:
            print(f"❌ {name} installation failed")
    
    print(f"\n📊 Fix results: {success_count}/{len(critical_deps)} packages installed successfully")
    
    if success_count >= len(critical_deps) * 0.8:  # 80% success
        print("🎉 Critical dependencies fix completed!")
        return True
    else:
        print("⚠️ Some critical dependencies failed to install")
        return False

def test_imports():
    """Test if critical packages can be imported"""
    print("\n🧪 Testing package imports...")
    
    test_packages = [
        ("django", "Django"),
        ("torch", "PyTorch"),
        ("corsheaders", "Django CORS")
    ]
    
    success_count = 0
    for module, name in test_packages:
        try:
            __import__(module)
            print(f"✅ {name} import successful")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
    
    print(f"\n📊 Import test: {success_count}/{len(test_packages)} packages imported successfully")
    return success_count >= len(test_packages) * 0.8

def main():
    """Main function"""
    print("🚀 Quick Dependency Fix Script")
    print("=" * 50)
    print("This script fixes the most critical missing dependencies")
    print("")
    
    # Fix dependencies
    if fix_critical_dependencies():
        print("\n✅ Dependencies fix completed!")
        
        # Test imports
        if test_imports():
            print("\n🎉 All critical dependencies are working!")
            print("You can now run the Django server:")
            print("python start_server.py runserver 0.0.0.0:8080")
        else:
            print("\n⚠️ Some packages still have import issues")
            print("Try running the full installation:")
            print("python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ Dependency fix failed!")
        print("Please check the error messages above")
        sys.exit(1)

if __name__ == "__main__":
    main()



