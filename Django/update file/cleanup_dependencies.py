#!/usr/bin/env python3
"""
Dependency Cleanup Script - Wangchuk Mind
Remove unnecessary dependencies from the Thangka restoration system
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

def get_installed_packages():
    """Get list of currently installed packages"""
    try:
        result = subprocess.run("pip list --format=freeze", shell=True, 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            packages = {}
            for line in result.stdout.strip().split('\n'):
                if '==' in line:
                    name, version = line.split('==', 1)
                    packages[name.lower()] = version
            return packages
        return {}
    except Exception as e:
        print(f"❌ Failed to get installed packages: {e}")
        return {}

def identify_unnecessary_packages():
    """Identify packages that are not used in the Thangka system"""
    
    # Core packages that ARE used
    essential_packages = {
        'paddlepaddle-gpu', 'paddlenlp', 'ppdiffusers',
        'opencv-python', 'pillow', 'scikit-image', 'imageio', 'albumentations',
        'numpy', 'django', 'django-cors-headers', 'djangorestframework',
        'requests', 'erniebot', 'einops'
    }
    
    # Packages that are NOT used (based on code analysis)
    unnecessary_packages = {
        # Data processing
        'pandas', 'datasets', 'pyarrow',
        
        # Scientific computing
        'scipy', 'scikit-learn',
        
        # Visualization
        'matplotlib', 'bokeh', 'wandb',
        
        # Tools
        'tqdm', 'click', 'colorama', 'rich',
        
        # File handling
        'filelock', 'fsspec',
        
        # HTTP/Network
        'h11', 'httpx', 'aiohttp',
        
        # Configuration
        'packaging', 'typing-extensions', 'certifi', 'urllib3', 
        'charset-normalizer', 'idna',
        
        # AI Studio specific
        'aistudio-sdk', 'bce-python-sdk',
        
        # ErnieBot extensions
        'erniebot-agent',
        
        # Text processing
        'regex', 'ftfy', 'jieba',
        
        # Web frameworks
        'asgiref', 'gunicorn', 'werkzeug', 'starlette',
        'fastapi', 'flask', 'uvicorn', 'jinja2',
        
        # PaddlePaddle extensions
        'paddle2onnx', 'paddlefsl', 'paddlesde',
        
        # Image extensions
        'pillow-avif-plugin', 'matplotlib-inline', 'numpydoc',
        
        # PyTorch ecosystem
        'open-clip-torch', 'pytorch-lightning', 'torchdiffeq',
        'torchmetrics', 'torchsde',
        
        # Request extensions
        'requests-file', 'requests-mock', 'requests-toolbelt',
        
        # YAML processing
        'ruamel.yaml', 'ruamel-yaml-conda',
        
        # Data validation
        'pydantic', 'pydantic_core',
        
        # Flask extensions
        'flask-babel',
        
        # Configuration management
        'pyyaml', 'omegaconf'
    }
    
    return essential_packages, unnecessary_packages

def cleanup_packages():
    """Remove unnecessary packages"""
    print("🧹 Starting dependency cleanup...")
    print("=" * 50)
    
    # Get installed packages
    installed = get_installed_packages()
    if not installed:
        print("❌ Could not get installed packages list")
        return False
    
    # Identify unnecessary packages
    essential, unnecessary = identify_unnecessary_packages()
    
    # Find packages to remove
    to_remove = []
    for package in unnecessary:
        if package in installed:
            to_remove.append(package)
    
    print(f"📊 Found {len(to_remove)} unnecessary packages to remove:")
    for package in to_remove:
        print(f"  - {package} ({installed[package]})")
    
    if not to_remove:
        print("✅ No unnecessary packages found!")
        return True
    
    # Ask for confirmation
    print(f"\n⚠️ This will remove {len(to_remove)} packages.")
    response = input("Do you want to continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cleanup cancelled by user")
        return False
    
    # Remove packages
    print("\n🗑️ Removing unnecessary packages...")
    removed_count = 0
    failed_packages = []
    
    for package in to_remove:
        print(f"Removing {package}...")
        success, _ = run_command(f"pip uninstall {package} -y", timeout=120)
        if success:
            removed_count += 1
            print(f"✅ {package} removed successfully")
        else:
            failed_packages.append(package)
            print(f"❌ Failed to remove {package}")
    
    # Report results
    print(f"\n📊 Cleanup results:")
    print(f"✅ Successfully removed: {removed_count}/{len(to_remove)} packages")
    if failed_packages:
        print(f"❌ Failed to remove: {failed_packages}")
    
    return len(failed_packages) == 0

def create_minimal_requirements():
    """Create minimal requirements.txt"""
    print("\n📝 Creating minimal requirements.txt...")
    
    minimal_content = """# 唐卡修复系统核心依赖 - 精简版
# 基于实际代码使用情况分析

# 深度学习框架
paddlepaddle-gpu==2.6.2
paddlenlp==2.8.1
ppdiffusers==0.29.0

# 图像处理
opencv-python==4.8.1.78
pillow==11.3.0
scikit-image==0.21.0
imageio==2.31.1
albumentations==2.0.8

# 数值计算
numpy>=1.21.2,<2.0.0

# Web框架
Django==4.2.11
django-cors-headers==4.3.1
djangorestframework==3.16.1

# HTTP客户端
requests==2.31.0

# 文心一言API
erniebot==0.5.9

# 基础依赖
einops==0.8.1

# 备用深度学习框架 (可选)
# torch==2.4.0
# torchvision==0.19.0
# diffusers==0.34.0
# transformers==4.56.0
# accelerate==0.21.0
# peft==0.7.0
"""
    
    with open('requirements_minimal.txt', 'w') as f:
        f.write(minimal_content)
    
    print("✅ Created requirements_minimal.txt")

def main():
    """Main function"""
    print("🧹 Dependency Cleanup Script")
    print("=" * 50)
    print("This script removes unnecessary dependencies from the Thangka system")
    print("")
    
    # Show current package count
    installed = get_installed_packages()
    print(f"📊 Current installed packages: {len(installed)}")
    
    # Cleanup packages
    if cleanup_packages():
        print("\n🎉 Cleanup completed successfully!")
        
        # Create minimal requirements
        create_minimal_requirements()
        
        print("\n📋 Next steps:")
        print("1. Test the system with: python start_server.py runserver 0.0.0.0:8080")
        print("2. If everything works, replace requirements.txt with requirements_minimal.txt")
        print("3. Update deployment scripts to use the minimal requirements")
    else:
        print("\n❌ Cleanup failed or was cancelled")
        print("Please check the error messages above")

if __name__ == "__main__":
    main()



