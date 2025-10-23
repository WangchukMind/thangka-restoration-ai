#!/usr/bin/env python3
"""
Quick PaddlePaddle Fix Script - Wangchuk Mind
Quickly fix PaddlePaddle circular import issues
"""
import subprocess
import sys
import os
import shutil
import glob

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

def quick_fix_paddle():
    """Quick fix for PaddlePaddle circular import issues"""
    print("🔧 Quick PaddlePaddle fix...")
    print("=" * 40)
    
    # Step 1: Uninstall PaddlePaddle
    print("📦 Step 1: Uninstalling PaddlePaddle...")
    run_command("pip uninstall paddlepaddle paddlepaddle-gpu -y", timeout=120)
    
    # Step 2: Clear cache
    print("📦 Step 2: Clearing Python cache...")
    cache_dirs = glob.glob("/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddle*/__pycache__")
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"Cleared: {cache_dir}")
    
    # Step 3: Reinstall PaddlePaddle
    print("📦 Step 3: Reinstalling PaddlePaddle...")
    success, _ = run_command("pip install paddlepaddle-gpu==2.6.2", timeout=300)
    
    if not success:
        print("❌ PaddlePaddle installation failed")
        return False
    
    # Step 4: Test import
    print("📦 Step 4: Testing import...")
    try:
        import paddle
        print(f"✅ PaddlePaddle import successful: {paddle.__version__}")
        
        # Test basic functionality
        x = paddle.to_tensor([1.0, 2.0])
        print(f"✅ PaddlePaddle tensor creation successful")
        
        return True
    except Exception as e:
        print(f"❌ PaddlePaddle import test failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Quick PaddlePaddle Fix Script")
    print("=" * 40)
    print("This script quickly fixes PaddlePaddle circular import issues")
    print("")
    
    if quick_fix_paddle():
        print("\n🎉 PaddlePaddle fix completed successfully!")
        print("You can now run the Django server:")
        print("python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ PaddlePaddle fix failed!")
        print("Please check the error messages above")
        sys.exit(1)

if __name__ == "__main__":
    main()



