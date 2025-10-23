#!/usr/bin/env python3
"""
Ultimate PaddlePaddle Fix Script - Wangchuk Mind
Completely resolve PaddlePaddle circular import issues
"""
import subprocess
import sys
import os
import shutil
import glob
import time

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

def ultimate_paddle_fix():
    """Ultimate PaddlePaddle fix - nuclear option"""
    print("🚀 Ultimate PaddlePaddle Fix - Nuclear Option")
    print("=" * 60)
    print("This will completely remove and reinstall PaddlePaddle ecosystem")
    print("")
    
    # Step 1: Complete removal
    print("💥 Step 1: Complete PaddlePaddle ecosystem removal...")
    packages_to_remove = [
        "paddlepaddle", "paddlepaddle-gpu", "paddlenlp", "ppdiffusers",
        "paddle2onnx", "paddlefsl", "paddlesde", "paddlehub"
    ]
    
    for package in packages_to_remove:
        print(f"Removing {package}...")
        run_command(f"pip uninstall {package} -y", timeout=60)
    
    # Step 2: Nuclear cache clearing
    print("💥 Step 2: Nuclear cache clearing...")
    
    # Clear all Python cache
    cache_patterns = [
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddle*",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddlenlp*",
        "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/ppdiffusers*",
        "/home/aistudio/.cache/pip/**/paddle*",
        "/tmp/pip-*",
        "/home/aistudio/.local/lib/python3.10/site-packages/paddle*"
    ]
    
    for pattern in cache_patterns:
        cache_dirs = glob.glob(pattern)
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    shutil.rmtree(cache_dir)
                    print(f"💥 Nuked: {cache_dir}")
                except Exception as e:
                    print(f"Could not remove {cache_dir}: {e}")
    
    # Clear Python module cache
    import sys
    modules_to_clear = [name for name in sys.modules.keys() if 'paddle' in name.lower()]
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    print(f"💥 Cleared {len(modules_to_clear)} paddle modules from memory")
    
    # Step 3: Clean pip cache
    print("💥 Step 3: Cleaning pip cache...")
    run_command("pip cache purge", timeout=60)
    
    # Step 4: Fresh installation
    print("💥 Step 4: Fresh PaddlePaddle installation...")
    
    # Try different installation strategies
    strategies = [
        {
            "name": "GPU version with no cache",
            "cmd": "pip install paddlepaddle-gpu==2.6.2 --no-cache-dir --force-reinstall --no-deps"
        },
        {
            "name": "CPU version with no cache", 
            "cmd": "pip install paddlepaddle==2.6.2 --no-cache-dir --force-reinstall --no-deps"
        },
        {
            "name": "GPU version 2.5.2",
            "cmd": "pip install paddlepaddle-gpu==2.5.2 --no-cache-dir --force-reinstall --no-deps"
        },
        {
            "name": "CPU version 2.5.2",
            "cmd": "pip install paddlepaddle==2.5.2 --no-cache-dir --force-reinstall --no-deps"
        }
    ]
    
    success = False
    for strategy in strategies:
        print(f"Trying strategy: {strategy['name']}")
        success, _ = run_command(strategy['cmd'], timeout=300)
        if success:
            print(f"✅ Success with: {strategy['name']}")
            break
        else:
            print(f"❌ Failed with: {strategy['name']}")
    
    if not success:
        print("❌ All installation strategies failed")
        return False
    
    # Step 5: Install dependencies
    print("💥 Step 5: Installing PaddlePaddle dependencies...")
    dependencies = [
        "numpy>=1.21.2,<2.0.0",
        "protobuf>=3.20.0",
        "six>=1.15.0",
        "decorator>=4.4.0",
        "astor>=0.8.0",
        "gast>=0.3.0",
        "pillow>=8.0.0",
        "opencv-python>=4.5.0"
    ]
    
    for dep in dependencies:
        print(f"Installing dependency: {dep}")
        run_command(f"pip install {dep}", timeout=120)
    
    # Step 6: Test import with multiple attempts
    print("💥 Step 6: Testing PaddlePaddle import...")
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            # Clear module cache before each attempt
            import sys
            modules_to_clear = [name for name in sys.modules.keys() if 'paddle' in name.lower()]
            for module in modules_to_clear:
                if module in sys.modules:
                    del sys.modules[module]
            
            # Wait a bit
            time.sleep(1)
            
            # Try import
            import paddle
            print(f"✅ PaddlePaddle import successful: {paddle.__version__}")
            
            # Test basic functionality
            x = paddle.to_tensor([1.0, 2.0])
            print(f"✅ PaddlePaddle tensor creation successful: {x}")
            
            # Test more complex functionality
            y = paddle.nn.Linear(2, 1)
            print(f"✅ PaddlePaddle neural network creation successful")
            
            return True
            
        except Exception as e:
            print(f"❌ Import attempt {attempt + 1} failed: {e}")
            if attempt < max_attempts - 1:
                print("🔄 Waiting 3 seconds before retry...")
                time.sleep(3)
            else:
                print("❌ All import attempts failed")
                return False
    
    return False

def install_paddle_ecosystem():
    """Install PaddlePaddle ecosystem after successful core installation"""
    print("💥 Step 7: Installing PaddlePaddle ecosystem...")
    
    ecosystem_packages = [
        "paddlenlp==2.8.1",
        "ppdiffusers==0.29.0"
    ]
    
    for package in ecosystem_packages:
        print(f"Installing {package}...")
        success, _ = run_command(f"pip install {package}", timeout=180)
        if success:
            print(f"✅ {package} installed successfully")
        else:
            print(f"⚠️ {package} installation failed, but continuing...")

def main():
    """Main function"""
    print("🚀 Ultimate PaddlePaddle Fix Script")
    print("=" * 60)
    print("This script will completely remove and reinstall PaddlePaddle")
    print("WARNING: This is a nuclear option that will remove all PaddlePaddle packages")
    print("")
    
    # Ask for confirmation
    response = input("Do you want to proceed with the nuclear option? (y/N): ")
    if response.lower() != 'y':
        print("❌ Operation cancelled by user")
        return
    
    if ultimate_paddle_fix():
        print("\n🎉 Ultimate PaddlePaddle fix completed!")
        
        # Install ecosystem
        install_paddle_ecosystem()
        
        print("\n✅ PaddlePaddle is now working correctly!")
        print("You can now run the Django server:")
        print("python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ Ultimate PaddlePaddle fix failed!")
        print("Please check the error messages above")
        print("\nManual recovery commands:")
        print("pip uninstall paddlepaddle paddlepaddle-gpu -y")
        print("pip install paddlepaddle-gpu==2.6.2 --no-cache-dir --force-reinstall")
        sys.exit(1)

if __name__ == "__main__":
    main()



