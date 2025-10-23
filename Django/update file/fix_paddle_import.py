#!/usr/bin/env python3
"""
PaddlePaddle Import Fix Script - Wangchuk Mind
Fix PaddlePaddle circular import issues
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

def check_paddle_installation():
    """Check PaddlePaddle installation status"""
    print("🔍 Checking PaddlePaddle installation...")
    
    try:
        import paddle
        version = paddle.__version__
        print(f"✅ PaddlePaddle version: {version}")
        return True, version
    except ImportError as e:
        print(f"❌ PaddlePaddle not installed: {e}")
        return False, None
    except Exception as e:
        print(f"⚠️ PaddlePaddle import error: {e}")
        return False, None

def fix_paddle_import_issue():
    """Fix PaddlePaddle import issues"""
    print("🔧 Fixing PaddlePaddle import issues...")
    print("=" * 50)
    
    # Step 1: Uninstall current PaddlePaddle
    print("📦 Step 1: Uninstalling current PaddlePaddle...")
    run_command("pip uninstall paddlepaddle paddlepaddle-gpu -y", timeout=120)
    
    # Step 2: Clear Python cache
    print("📦 Step 2: Clearing Python cache...")
    import shutil
    import glob
    
    # Clear __pycache__ directories
    cache_dirs = glob.glob("/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddle*/__pycache__")
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"Cleared cache: {cache_dir}")
    
    # Step 3: Install compatible PaddlePaddle version
    print("📦 Step 3: Installing compatible PaddlePaddle version...")
    
    # Try different PaddlePaddle versions
    paddle_versions = [
        "paddlepaddle-gpu==2.6.2",
        "paddlepaddle-gpu==2.5.2", 
        "paddlepaddle==2.6.2",
        "paddlepaddle==2.5.2"
    ]
    
    for version in paddle_versions:
        print(f"Trying {version}...")
        success, _ = run_command(f"pip install {version}", timeout=300)
        if success:
            print(f"✅ Successfully installed {version}")
            break
        else:
            print(f"❌ Failed to install {version}")
    
    if not success:
        print("❌ All PaddlePaddle versions failed to install")
        return False
    
    # Step 4: Test import
    print("📦 Step 4: Testing PaddlePaddle import...")
    try:
        import paddle
        print(f"✅ PaddlePaddle import successful: {paddle.__version__}")
        
        # Test basic functionality
        x = paddle.to_tensor([1.0, 2.0])
        print(f"✅ PaddlePaddle tensor creation successful: {x}")
        
        return True
    except Exception as e:
        print(f"❌ PaddlePaddle import test failed: {e}")
        return False

def install_paddlenlp_compatible():
    """Install compatible PaddleNLP version"""
    print("📦 Installing compatible PaddleNLP...")
    
    # Try different PaddleNLP versions
    paddlenlp_versions = [
        "paddlenlp==2.8.1",
        "paddlenlp==2.7.0",
        "paddlenlp==2.6.0"
    ]
    
    for version in paddlenlp_versions:
        print(f"Trying PaddleNLP {version}...")
        success, _ = run_command(f"pip install {version}", timeout=180)
        if success:
            print(f"✅ Successfully installed PaddleNLP {version}")
            return True
        else:
            print(f"❌ Failed to install PaddleNLP {version}")
    
    return False

def install_ppdiffusers_compatible():
    """Install compatible PPDiffusers version"""
    print("📦 Installing compatible PPDiffusers...")
    
    # Try different PPDiffusers versions
    ppdiffusers_versions = [
        "ppdiffusers==0.29.0",
        "ppdiffusers==0.28.0",
        "ppdiffusers==0.27.0"
    ]
    
    for version in ppdiffusers_versions:
        print(f"Trying PPDiffusers {version}...")
        success, _ = run_command(f"pip install {version}", timeout=180)
        if success:
            print(f"✅ Successfully installed PPDiffusers {version}")
            return True
        else:
            print(f"❌ Failed to install PPDiffusers {version}")
    
    return False

def test_django_import():
    """Test Django import after PaddlePaddle fix"""
    print("🧪 Testing Django import...")
    
    try:
        # Test the specific import that was failing
        import paddle
        from server.models import thangka_paddle as thangka
        print("✅ Django import with PaddlePaddle successful")
        return True
    except Exception as e:
        print(f"❌ Django import test failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 PaddlePaddle Import Fix Script")
    print("=" * 50)
    print("This script fixes PaddlePaddle circular import issues")
    print("")
    
    # Check current installation
    installed, version = check_paddle_installation()
    if installed:
        print(f"Current PaddlePaddle version: {version}")
    
    # Fix PaddlePaddle import issues
    if fix_paddle_import_issue():
        print("\n✅ PaddlePaddle import fix completed!")
        
        # Install compatible PaddleNLP
        if install_paddlenlp_compatible():
            print("✅ PaddleNLP installed successfully")
        else:
            print("⚠️ PaddleNLP installation failed")
        
        # Install compatible PPDiffusers
        if install_ppdiffusers_compatible():
            print("✅ PPDiffusers installed successfully")
        else:
            print("⚠️ PPDiffusers installation failed")
        
        # Test Django import
        if test_django_import():
            print("\n🎉 All tests passed!")
            print("You can now run the Django server:")
            print("python start_server.py runserver 0.0.0.0:8080")
        else:
            print("\n⚠️ Django import test failed, but PaddlePaddle is fixed")
    else:
        print("\n❌ PaddlePaddle import fix failed!")
        print("Please check the error messages above")
        sys.exit(1)

if __name__ == "__main__":
    main()
