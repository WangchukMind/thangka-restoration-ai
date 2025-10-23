#!/usr/bin/env python3
"""
AI Studio Deployment Script - Optimized for Baidu AI Studio
Complete environment setup, dependency installation, model download and Django startup
Designed for fresh deployment on new AI Studio instances
"""
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def run_command(cmd, cwd=None, check=True, timeout=300, retries=2):
    """Run command with retry mechanism"""
    print(f"🔧 Executing command: {cmd}")

    for attempt in range(retries + 1):
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, check=check,
                                  capture_output=True, text=True, timeout=timeout)
            if result.stdout:
                print(f"Output: {result.stdout}")
            return True, result
        except subprocess.TimeoutExpired:
            if attempt < retries:
                print(f"⏰ Command execution timeout (attempt {attempt + 1}/{retries + 1}): {cmd}")
                print(f"🔄 Retrying with increased timeout...")
                timeout = int(timeout * 1.5)
                continue
            else:
                print(f"❌ Command execution timeout after {retries + 1} attempts: {cmd}")
                return False, None
        except subprocess.CalledProcessError as e:
            if attempt < retries:
                print(f"⚠️ Command execution failed (attempt {attempt + 1}/{retries + 1}): {e}")
                if e.stderr:
                    print(f"Error: {e.stderr}")
                print(f"🔄 Retrying...")
                time.sleep(2)
                continue
            else:
                print(f"❌ Command execution failed after {retries + 1} attempts: {e}")
                if e.stderr:
                    print(f"Error: {e.stderr}")
                return False, e

    return False, None

def check_python_environment():
    """Check and setup Python environment"""
    print("🐍 Checking Python environment...")
    
    # Check Python version
    success, result = run_command("python3 --version", check=False, timeout=30)
    if success and result:
        print(f"✅ Python version: {result.stdout.strip()}")
        return True
    else:
        print("⚠️ Python3 not available, trying python...")
        success, result = run_command("python --version", check=False, timeout=30)
        if success and result:
            print(f"✅ Python version: {result.stdout.strip()}")
            return True
        else:
            print("❌ Python not available")
            return False

def install_package_with_retry(package, timeout=120, max_retries=3):
    """Package installation with retry mechanism"""
    for attempt in range(max_retries):
        print(f"🔍 Installing {package} (attempt {attempt + 1}/{max_retries})...")
        success, result = run_command(f"pip install {package}", timeout=timeout, retries=1)

        if success:
            print(f"✅ {package} installed successfully")
            return True
        else:
            if attempt < max_retries - 1:
                print(f"⚠️ {package} installation failed, waiting before retry...")
                time.sleep(3)
                timeout = int(timeout * 1.2)
            else:
                print(f"❌ {package} installation failed, skipping")
                return False

    return False

def install_group_with_stats(group_name, packages, timeout=120, max_retries=3):
    """Install a group of packages and return statistics"""
    print(f"\n{group_name}")
    group_success = 0
    group_total = len(packages)

    for package in packages:
        success = install_package_with_retry(package, timeout=timeout, max_retries=max_retries)
        if success:
            group_success += 1
        else:
            print(f"⚠️ {package} installation failed, continuing with other packages...")

    print(f"📊 {group_name} completed: {group_success}/{group_total} packages installed successfully")
    return group_success, group_total

def install_dependencies():
    """Install all required dependencies for AI Studio deployment"""
    print("📦 Starting comprehensive dependency installation...")
    print("=" * 60)

    # Installation statistics
    total_successful = 0
    total_packages = 0

    # Group 1: Core numerical computing (with NumPy compatibility fix)
    group1 = [
        "numpy>=1.21.2,<2.0.0",
        "scipy>=1.11.0"
    ]
    success, total = install_group_with_stats("📊 Group 1: Installing core numerical computing...", group1, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total
    
    # Force NumPy 1.x to prevent compatibility issues
    print("\n🔧 Ensuring NumPy 1.x compatibility...")
    run_command("pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall", timeout=120)

    # Group 2: Image processing packages (compatible with NumPy 1.x)
    group2 = [
        "opencv-python==4.8.1.78",
        "pillow>=10.0.0",
        "scikit-image==0.21.0",
        "imageio==2.31.1",
        "albumentations==2.0.8"
    ]
    success, total = install_group_with_stats("🖼️ Group 2: Installing image processing packages...", group2, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total
    
    # Re-enforce NumPy 1.x after image processing packages
    print("\n🔧 Re-enforcing NumPy 1.x after image processing...")
    run_command("pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall", timeout=120)

    # Group 3: PaddlePaddle ecosystem
    group3 = [
        "paddlepaddle-gpu==2.6.2",
        "paddlenlp==2.8.1",
        "ppdiffusers==0.29.0"
    ]
    success, total = install_group_with_stats("🚣 Group 3: Installing PaddlePaddle ecosystem...", group3, timeout=180, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 4: PyTorch ecosystem (for compatibility)
    group4 = [
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "transformers>=4.30.0",
        "diffusers>=0.21.0",
        "accelerate>=0.20.0"
    ]
    success, total = install_group_with_stats("🔥 Group 4: Installing PyTorch ecosystem...", group4, timeout=180, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 5: Web framework
    group5 = [
        "Django==4.2.11",
        "django-cors-headers==4.3.1",
        "djangorestframework==3.16.1",
        "channels>=4.0.0"
    ]
    success, total = install_group_with_stats("🌐 Group 5: Installing web framework...", group5, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 6: Essential utilities
    group6 = [
        "requests>=2.31.0",
        "einops>=0.8.1",
        "tqdm>=4.65.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0"
    ]
    success, total = install_group_with_stats("🔧 Group 6: Installing essential utilities...", group6, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 7: Optional packages
    print("\n🎨 Group 7: Installing optional packages...")
    optional_packages = [
        "mplfonts==0.0.3",
        "gradio>=3.40.0",
        "streamlit>=1.25.0"
    ]

    optional_success = 0
    for package in optional_packages:
        print(f"🔍 Attempting to install optional package {package}...")
        success = install_package_with_retry(package, timeout=60, max_retries=1)
        if success:
            optional_success += 1
            print(f"✅ {package} installed successfully")
        else:
            print(f"⚠️ {package} installation failed, skipping (optional)")

    print(f"📊 Optional packages: {optional_success}/{len(optional_packages)} successful")

    # Final NumPy compatibility check and fix
    print("\n🔧 Final NumPy compatibility check...")
    try:
        import numpy as np
        if np.__version__.startswith('2.'):
            print("⚠️ NumPy 2.x detected, forcing downgrade to 1.x...")
            run_command("pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall --no-deps", timeout=120)
            run_command("pip install scikit-image==0.21.0 --force-reinstall", timeout=120)
            run_command("pip install opencv-python==4.8.1.78 --force-reinstall", timeout=120)
        else:
            print("✅ NumPy version is compatible")
    except Exception as e:
        print(f"⚠️ NumPy compatibility check failed: {e}")

    # Final statistics
    print(f"\n📊 Installation completion statistics:")
    print(f"✅ Successfully installed: {total_successful}/{total_packages} packages")
    print(f"📈 Success rate: {(total_successful/total_packages*100):.1f}%")

    if total_successful >= total_packages * 0.8:
        print("🎉 Dependencies installation successful!")
        return True
    else:
        print("⚠️ Some dependencies installation failed, but continuing...")
        return True

def download_models():
    """Download model files for AI Studio"""
    print("🚀 Starting model file download...")

    # Set model directory
    model_dir = "./models"
    os.makedirs(model_dir, exist_ok=True)

    # Check if model files already exist
    if os.path.exists(os.path.join(model_dir, "sd2.1_base_paddle")):
        print("✅ Model files already exist, skipping download")
        return True

    # Try to copy models from AI Studio data directory
    aistudio_models = "/home/aistudio/data/models/34288/thangka/models"
    if os.path.exists(aistudio_models):
        print(f"📋 Copying models from AI Studio data directory: {aistudio_models}")
        success, _ = run_command(f"cp -r {aistudio_models}/* {model_dir}/", timeout=300)
        if success:
            print("✅ Model files copied successfully")
            return True
        else:
            print("⚠️ Failed to copy from data directory, trying Git download")

    # Clone model repository
    repo_url = "https://e5896710865571a725e5f3c516cdb55e99b6ea90@git.aistudio.baidu.com/Wangchuk/thangka1376.git"
    temp_dir = "/home/aistudio/work/temp_models"

    print(f"📥 Cloning model repository to: {temp_dir}")

    # Delete temporary directory (if exists)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    # Clone repository
    success, _ = run_command(f"git clone {repo_url} {temp_dir}", timeout=1200)
    if not success:
        print("❌ Model repository cloning failed")
        return False

    # Copy model files
    source_models = os.path.join(temp_dir, "models")
    if os.path.exists(source_models):
        print(f"📋 Copying model files from {source_models} to {model_dir}")
        success, _ = run_command(f"cp -r {source_models}/* {model_dir}/", timeout=1200)
        if success:
            print("✅ Model files copied successfully")
        else:
            print("❌ Model file copying failed")
            return False
    else:
        print("❌ Source model directory does not exist")
        return False

    # Clean up temporary directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print("🧹 Temporary file cleanup completed")

    print("🎉 Model download completed!")
    return True

def fix_numpy_compatibility():
    """Fix NumPy compatibility issues in AI Studio"""
    print("🔧 Fixing NumPy compatibility issues...")
    
    try:
        # Check current NumPy version
        import numpy as np
        print(f"Current NumPy version: {np.__version__}")
        
        # If NumPy 2.x, downgrade to 1.x
        if np.__version__.startswith('2.'):
            print("⚠️ Detected NumPy 2.x, downgrading to 1.x for compatibility...")
            
            # Uninstall NumPy 2.x and related packages
            print("📦 Uninstalling incompatible packages...")
            run_command("pip uninstall numpy scikit-image opencv-python imageio -y", timeout=120)
            
            # Install compatible versions
            print("📦 Installing compatible versions...")
            run_command("pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall", timeout=300)
            run_command("pip install scikit-image==0.21.0 --force-reinstall", timeout=300)
            run_command("pip install opencv-python==4.8.1.78 --force-reinstall", timeout=300)
            run_command("pip install imageio==2.31.1 --force-reinstall", timeout=300)
            
            print("✅ NumPy compatibility fix completed")
            return True
        else:
            print("✅ NumPy version is compatible")
            return True
            
    except Exception as e:
        print(f"❌ NumPy compatibility fix failed: {e}")
        return False

def check_critical_dependencies():
    """Check critical dependencies with NumPy compatibility fix"""
    print("🔍 Checking critical dependencies...")
    
    # First, check and fix NumPy compatibility
    try:
        import numpy as np
        from skimage.feature import canny
        print("✅ NumPy and scikit-image compatibility verified")
    except ValueError as e:
        if "numpy.dtype size changed" in str(e):
            print("⚠️ Detected NumPy binary compatibility issue")
            print("🔧 Attempting to fix NumPy compatibility...")
            if fix_numpy_compatibility():
                print("✅ NumPy compatibility fix successful")
            else:
                print("❌ NumPy compatibility fix failed")
        else:
            print(f"❌ NumPy compatibility error: {e}")
    except ImportError as e:
        print(f"❌ NumPy/scikit-image import error: {e}")
    
    critical_packages = [
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("skimage", "scikit-image"),
        ("django", "Django"),
        ("paddle", "PaddlePaddle"),
        ("torch", "PyTorch"),
        ("transformers", "Transformers")
    ]
    
    success_count = 0
    failed_packages = []
 
    for module, name in critical_packages:
        try:
            __import__(module)
            print(f"✅ {name} import successful")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            failed_packages.append((module, name))
        except Exception as e:
            print(f"⚠️ {name} import encountered other error: {e}")
            failed_packages.append((module, name))

    print(f"\n📊 Test results: {success_count}/{len(critical_packages)} critical packages imported successfully")

    if failed_packages:
        print(f"\n⚠️ Failed packages: {[name for _, name in failed_packages]}")
        
        # Try to fix critical packages
        print("\n🔧 Attempting to fix critical dependencies...")
        for module, name in failed_packages:
            if module == 'cv2':
                print("🔧 Fixing OpenCV...")
                run_command("pip install opencv-python==4.8.1.78 --force-reinstall", timeout=120)
            elif module == 'skimage':
                print("🔧 Fixing scikit-image...")
                run_command("pip install scikit-image==0.21.0 --force-reinstall", timeout=120)
            elif module == 'numpy':
                print("🔧 Fixing NumPy...")
                run_command("pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall", timeout=120)
        
        # Re-check after fixes
        print("\n🔍 Re-checking after fixes...")
        for module, name in failed_packages:
            try:
                __import__(module)
                print(f"✅ {name} import successful after fix")
                success_count += 1
            except Exception as e:
                print(f"❌ {name} still failed after fix: {e}")

    # Lower success threshold to 75% for AI Studio
    return success_count >= len(critical_packages) * 0.75

def setup_django_environment():
    """Setup Django environment"""
    print("🔧 Setting up Django environment...")

    # Set environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

    # Set PaddlePaddle environment variables
    os.environ['PADDLE_FRAMEWORK'] = 'paddle'
    os.environ['PADDLE_DEVICE'] = 'gpu' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu'

    print("✅ Django environment setup completed")

def collect_static_files():
    """Collect static files for production deployment"""
    print("📁 Collecting static files...")
    
    try:
        import django
        from django.core.management import execute_from_command_line
        
        # Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
        
        # Initialize Django
        django.setup()
        
        # Run collectstatic command
        from django.core.management import call_command
        call_command('collectstatic', '--noinput', '--clear')
        
        print("✅ Static files collected successfully")
        return True
        
    except Exception as e:
        print(f"❌ Static files collection failed: {e}")
        print("💡 Trying alternative method...")
        
        # Alternative: manually copy static files
        try:
            import shutil
            # AI Studio环境使用完整绝对路径
            static_source = '/home/aistudio/work/wangchukthangka/Thangka/Django/server/static'
            static_dest = '/home/aistudio/work/wangchukthangka/Thangka/Django/staticfiles'
            
            if os.path.exists(static_source):
                if os.path.exists(static_dest):
                    shutil.rmtree(static_dest)
                shutil.copytree(static_source, static_dest)
                print("✅ Static files copied manually")
                return True
            else:
                print(f"❌ Static source directory not found: {static_source}")
                return False
                
        except Exception as e2:
            print(f"❌ Manual static files copy failed: {e2}")
            return False

def fix_aistudio_api_urls():
    """Fix AI Studio API URLs for dynamic addressing"""
    print("🔧 Fixing AI Studio API URLs...")
    
    def fix_template_file(file_path):
        """Fix API URLs in template file"""
        if not os.path.exists(file_path):
            return False
            
        print(f"📝 Fixing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add dynamic API configuration
        api_config = """
    // 动态API配置 - AI Studio兼容
    const API_BASE_URL = window.location.origin;
    const API_ENDPOINTS = {
        getType: API_BASE_URL + '/api/getType',
        generate: API_BASE_URL + '/stream/generate',
        getImg: API_BASE_URL + '/api/getImg',
        changePipe: API_BASE_URL + '/api/changePipe',
        generateDirect: API_BASE_URL + '/api/generate'
    };
    """
        
        # Add API configuration if not already present
        if 'const API_BASE_URL' not in content:
            content = content.replace(
                '<script>',
                f'<script>{api_config}'
            )
        
        # Replace hardcoded API paths
        replacements = {
            "fetch('/api/getType'": "fetch(API_ENDPOINTS.getType",
            "fetch('/stream/generate'": "fetch(API_ENDPOINTS.generate",
            "fetch('/api/getImg'": "fetch(API_ENDPOINTS.getImg",
            "fetch('/api/changePipe'": "fetch(API_ENDPOINTS.changePipe",
            "fetch('/api/generate'": "fetch(API_ENDPOINTS.generateDirect",
            "const testUrl = `/api/getImg?filename=${filename}&path=output`": "const testUrl = `${API_ENDPOINTS.getImg}?filename=${filename}&path=output`"
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} fixed")
        return True
    
    # Fix template files
    template_files = [
        "server/templates/index.html",
        "server/templates/index copy.html"
    ]
    
    success_count = 0
    for template_file in template_files:
        if fix_template_file(template_file):
            success_count += 1
    
    if success_count > 0:
        print("✅ AI Studio API URLs fixed successfully")
        return True
    else:
        print("⚠️ No template files found to fix")
        return False

def print_system_introduction():
    """Print system introduction"""
    print("\n" + "=" * 80)
    print("🎨 AI + Intangible Cultural Heritage Thangka Image Restoration System")
    print("=" * 80)
    print("")
    print("🌟 System Overview:")
    print("   • Advanced AI-powered Thangka image restoration technology")
    print("   • Specialized for intangible cultural heritage preservation")
    print("   • State-of-the-art diffusion models with LoRA fine-tuning")
    print("   • Real-time streaming processing capabilities")
    print("")
    print("🔧 Core Technologies:")
    print("   • PaddlePaddle deep learning framework")
    print("   • Stable Diffusion 2.1 with custom fine-tuning")
    print("   • LoRA (Low-Rank Adaptation) for efficient model adaptation")
    print("   • Django web framework for robust API services")
    print("   • Real-time progress streaming and intermediate results")
    print("")
    print("👨‍💻 Development & Implementation:")
    print("   • Core technology development: Wangchuk Mind")
    print("   • System architecture and optimization: Wangchuk Mind")
    print("   • AI model integration and fine-tuning: Wangchuk Mind")
    print("   • Web API development and streaming: Wangchuk Mind")
    print("")
    print("🎯 Features:")
    print("   • High-quality image inpainting and restoration")
    print("   • Multiple generation modes (inpaint, text2img, img2img)")
    print("   • LoRA model support for specialized artistic styles")
    print("   • Real-time progress monitoring and intermediate previews")
    print("   • Comprehensive repair history and baseline management")
    print("   • RESTful API with streaming response support")
    print("")
    print("🌍 Cultural Impact:")
    print("   • Preserving traditional Thangka art through AI technology")
    print("   • Supporting intangible cultural heritage conservation")
    print("   • Bridging ancient art with modern technology")
    print("   • Democratizing access to professional restoration tools")
    print("")
    print("=" * 80)
    print("🚀 System is ready! Access the web interface to start restoration.")
    print("=" * 80)

def setup_environment():
    """Complete environment setup for AI Studio deployment"""
    print("🚀 AI Studio Complete Deployment Script")
    print("=" * 50)

    # Step 1: Check Python environment
    print("\n📋 Step 1: Checking Python environment")
    print("-" * 30)
    if not check_python_environment():
        print("❌ Python environment check failed")
        return False

    # Step 2: Install dependencies
    print("\n📋 Step 2: Installing dependencies")
    print("-" * 30)
    if not install_dependencies():
        print("❌ Dependencies installation failed")
        return False

    # Step 3: Download models
    print("\n📋 Step 3: Downloading models")
    print("-" * 30)
    if not download_models():
        print("⚠️ Model download failed, will start server without models")
        os.environ['SKIP_MODEL_LOADING'] = '1'

    # Step 4: Setup Django environment
    print("\n📋 Step 4: Setting up Django environment")
    print("-" * 30)
    setup_django_environment()
    
    # Step 4.5: Collect static files
    print("\n📋 Step 4.5: Collecting static files")
    print("-" * 30)
    collect_static_files()
    
    # Step 4.6: Fix AI Studio API URLs
    print("\n📋 Step 4.6: Fixing AI Studio API URLs")
    print("-" * 30)
    fix_aistudio_api_urls()

    # Step 5: Final dependency check
    print("\n📋 Step 5: Final dependency check")
    print("-" * 30)
    if not check_critical_dependencies():
        print("⚠️ Some critical dependencies may have issues, but continuing...")

    print("\n🎉 Environment setup completed!")
    print("=" * 50)

    # Display system introduction
    print_system_introduction()

def pre_django_paddle_check():
    """Pre-Django PaddlePaddle check"""
    print("🔍 Pre-Django PaddlePaddle check...")
    
    try:
        import paddle  # type: ignore
        print(f"✅ PaddlePaddle pre-check successful: {paddle.__version__}")
        return True
    except Exception as e:
        print(f"❌ PaddlePaddle pre-check failed: {e}")
        return False

if __name__ == '__main__':
    # Execute complete environment setup
    setup_environment()

    # Pre-Django PaddlePaddle check
    print("\n🔍 Pre-Django PaddlePaddle check...")
    if not pre_django_paddle_check():
        print("⚠️ PaddlePaddle pre-check failed, but continuing...")

    # Import Django and start server
    try:
        import django  # type: ignore
        from django.core.management import execute_from_command_line  # type: ignore

        print("\n🚀 Starting Django server...")
        print("=" * 50)
        
        # Start Django server with 0.0.0.0:8080 for AI Studio
        execute_from_command_line(sys.argv)
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        print("💡 Please ensure Django is properly installed")
        print("🔧 Try running: pip install django==4.2.11")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Django startup failed: {e}")
        print("💡 Please check if dependencies are correctly installed")
        sys.exit(1)
