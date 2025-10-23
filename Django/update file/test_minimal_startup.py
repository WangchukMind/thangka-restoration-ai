#!/usr/bin/env python3
"""
Test Minimal Startup Script - Wangchuk Mind
Test the optimized start_server.py with minimal dependencies
"""
import subprocess
import sys
import os

def run_command(cmd, timeout=60):
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

def test_minimal_requirements():
    """Test installation of minimal requirements"""
    print("🧪 Testing minimal requirements installation...")
    
    # Install minimal requirements
    success, _ = run_command("pip install -r requirements_minimal.txt", timeout=300)
    if not success:
        print("❌ Failed to install minimal requirements")
        return False
    
    print("✅ Minimal requirements installed successfully")
    return True

def test_core_imports():
    """Test core package imports"""
    print("🧪 Testing core package imports...")
    
    core_packages = [
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("django", "Django"),
        ("paddle", "PaddlePaddle")
    ]
    
    all_passed = True
    for module, name in core_packages:
        try:
            __import__(module)
            print(f"✅ {name} import successful")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            all_passed = False
        except Exception as e:
            print(f"⚠️ {name} import error: {e}")
            all_passed = False
    
    return all_passed

def test_startup_script():
    """Test the startup script syntax"""
    print("🧪 Testing startup script syntax...")
    
    try:
        # Check Python syntax
        with open('start_server.py', 'r') as f:
            code = f.read()
        
        compile(code, 'start_server.py', 'exec')
        print("✅ Startup script syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in startup script: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking startup script: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Minimal Startup Test Script")
    print("=" * 50)
    print("Testing the optimized start_server.py with minimal dependencies")
    print("")
    
    # Test 1: Syntax check
    if not test_startup_script():
        print("❌ Startup script syntax test failed")
        return False
    
    # Test 2: Install minimal requirements
    if not test_minimal_requirements():
        print("❌ Minimal requirements installation test failed")
        return False
    
    # Test 3: Core imports
    if not test_core_imports():
        print("❌ Core imports test failed")
        return False
    
    print("\n🎉 All tests passed!")
    print("✅ The optimized start_server.py is ready to use")
    print("\n🚀 You can now run:")
    print("python start_server.py runserver 0.0.0.0:8080")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



