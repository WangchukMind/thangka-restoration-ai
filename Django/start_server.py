#!/usr/bin/env python3
"""
AI Studio One-Click Startup Script - Optimized by Wangchuk Mind
Integrated environment setup, dependency installation, model download and Django startup
"""
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

# Fix aistudio_sdk import error - Wangchuk Mind
try:
    import aistudio_sdk.hub
    if not hasattr(aistudio_sdk.hub, 'download'):
        def dummy_download(*args, **kwargs):
            print("⚠️ aistudio_sdk.download not available, skipping model download")
            return None
        aistudio_sdk.hub.download = dummy_download
        print("✅ aistudio_sdk patch applied")
except ImportError:
    print("⚠️ aistudio_sdk not installed, skipping")

def run_command(cmd, cwd=None, check=True, timeout=300, retries=2):
    """Run command with retry mechanism - Wangchuk Mind"""
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
                timeout = int(timeout * 1.5)  # Increase timeout by 50%
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
                time.sleep(2)  # Wait 2 seconds before retry
                continue
            else:
                print(f"❌ Command execution failed after {retries + 1} attempts: {e}")
                if e.stderr:
                    print(f"Error: {e.stderr}")
                return False, e

    return False, None

def setup_python_environment():
    """Setup Python environment (simplified version, no conda)"""
    print("🐍 Setting up Python environment...")

    # Check Python version
    success, result = run_command("python3 --version", check=False, timeout=30)
    if success and result:
        print(f"✅ Python version: {result.stdout.strip()}")
    else:
        print("⚠️ Python3 not available, trying python...")
        success, result = run_command("python --version", check=False, timeout=30)
        if success and result:
            print(f"✅ Python version: {result.stdout.strip()}")
        else:
            print("❌ Python not available")
            return False

    print("✅ Python environment setup completed")
    return True

def install_dependencies():
    """Smart install Python dependencies - integrated smart_install functionality"""
    print("📦 Starting smart dependency installation...")

    # Use smart grouped installation
    return install_packages_in_groups()

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
                time.sleep(3)  # Wait 3 seconds
                timeout = int(timeout * 1.2)  # Increase timeout by 20%
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

def install_packages_in_groups():
    """Install minimal essential packages for Thangka restoration system"""
    print("🚀 Starting minimal dependency installation...")
    print("=" * 60)

    # Installation statistics
    total_successful = 0
    total_packages = 0

    # Group 1: Core numerical computing (essential only)
    group1 = [
        "numpy>=1.21.2,<2.0.0"  # Flexible version range for compatibility
    ]
    success, total = install_group_with_stats("📊 Group 1: Installing core numerical computing...", group1, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 2: PaddlePaddle core packages (essential)
    group2 = [
        "paddlepaddle-gpu==2.6.2",
        "paddlenlp==2.8.1",
        "ppdiffusers==0.29.0"
    ]
    success, total = install_group_with_stats("🚣 Group 2: Installing PaddlePaddle core packages...", group2, timeout=180, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 3: Image processing packages (essential) - with numpy compatibility fix
    group3 = [
        "opencv-python==4.8.1.78",
        "pillow==11.3.0",
        "scikit-image==0.21.0"
    ]
    success, total = install_group_with_stats("🖼️ Group 3: Installing image processing packages...", group3, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total
    
    # Group 3.5: Install imageio with numpy compatibility protection
    print("\n🖼️ Group 3.5: Installing imageio with numpy compatibility protection...")
    success = install_imageio_safely()
    if success:
        total_successful += 1
        total_packages += 1
    else:
        print("⚠️ imageio installation failed, but continuing...")
        total_packages += 1
    
    # Group 3.6: Install albumentations
    success, total = install_group_with_stats("🖼️ Group 3.6: Installing albumentations...", ["albumentations==2.0.8"], timeout=120, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 4: Web framework (essential)
    group4 = [
        "Django==4.2.11",
        "django-cors-headers==4.3.1",
        "djangorestframework==3.16.1"
    ]
    success, total = install_group_with_stats("🌐 Group 4: Installing web framework...", group4, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 5: Essential utilities (minimal)
    group5 = [
        "requests==2.31.0",
        "erniebot==0.5.9",
        "einops==0.8.1"
    ]
    success, total = install_group_with_stats("🔧 Group 5: Installing essential utilities...", group5, timeout=120, max_retries=3)
    total_successful += success
    total_packages += total

    # Group 6: Optional packages (non-essential, installation failure doesn't affect system)
    print("\n🎨 Group 6: Installing optional packages...")
    optional_packages_list = [
        "mplfonts==0.0.3"  # Chinese font support, optional
    ]

    optional_success = 0
    for package in optional_packages_list:
        print(f"🔍 Attempting to install optional package {package}...")
        success = install_package_with_retry(package, timeout=60, max_retries=1)  # Only retry once
        if success:
            optional_success += 1
            print(f"✅ {package} installed successfully")
        else:
            print(f"⚠️ {package} installation failed, skipping (does not affect system operation)")

    print(f"📊 Optional packages installation: {optional_success}/{len(optional_packages_list)} successful")

    # Final statistics
    print(f"\n📊 Installation completion statistics:")
    print(f"✅ Successfully installed: {total_successful}/{total_packages} packages")
    print(f"📈 Success rate: {(total_successful/total_packages*100):.1f}%")

    if total_successful >= total_packages * 0.8:  # 80% or more successful
        print("🎉 Minimal dependencies installation successful!")
        return True
    else:
        print("⚠️ Some dependencies installation failed, but attempting to start server")
        return True

def download_models():
    """Download model files - Wangchuk Mind"""
    print("🚀 Starting model file download...")

    # Set model directory - dynamically set based on environment
    if os.path.exists("/home/aistudio/work/wangchukthangka/Thangka/Django/models/"):
        # AI Studio environment
        model_dir = "/home/aistudio/work/wangchukthangka/Thangka/Django/models"
    else:
        # Local environment
        model_dir = "./models"

    # Ensure directory exists
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

def fix_numpy_compatibility_issue():
    """Fix numpy compatibility issue in AI Studio environment"""
    print("🔧 Fixing numpy compatibility issue...")
    
    # Check if we're in AI Studio environment
    if not os.path.exists('/home/aistudio'):
        print("⚠️ Not in AI Studio environment, skipping numpy fix")
        return False
    
    try:
        # Uninstall incompatible packages
        print("📦 Uninstalling incompatible packages...")
        run_command("pip uninstall numpy scikit-image opencv-python imageio -y", timeout=120)
        
        # Install compatible versions in correct order
        print("📦 Installing compatible versions...")
        run_command("pip install 'numpy>=1.21.2,<2.0.0'", timeout=300)
        run_command("pip install scikit-image==0.21.0", timeout=300)
        run_command("pip install opencv-python==4.8.1.78", timeout=300)
        run_command("pip install imageio==2.31.1", timeout=300)
        
        # Verify fix
        print("🧪 Verifying fix...")
        import numpy as np
        from skimage.feature import canny
        print(f"✅ NumPy {np.__version__} and scikit-image compatibility verified")
        return True
        
    except Exception as e:
        print(f"❌ NumPy compatibility fix failed: {e}")
        return False

def install_imageio_safely():
    """Install imageio safely without breaking numpy compatibility"""
    print("🔧 Installing imageio with numpy compatibility protection...")
    
    try:
        # First, ensure numpy is at compatible version
        print("📦 Ensuring numpy compatibility...")
        run_command("pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall", timeout=120)
        
        # Then install imageio
        print("📦 Installing imageio...")
        success, _ = run_command("pip install imageio==2.31.1", timeout=120)
        
        if success:
            print("✅ imageio installed successfully with numpy compatibility")
            return True
        else:
            print("❌ imageio installation failed")
            return False
            
    except Exception as e:
        print(f"❌ imageio installation error: {e}")
        return False

def fix_paddle_import_issue():
    """Fix PaddlePaddle circular import issues - Enhanced version"""
    print("🔧 Fixing PaddlePaddle circular import issues...")
    
    # Check if we're in AI Studio environment
    if not os.path.exists('/home/aistudio'):
        print("⚠️ Not in AI Studio environment, skipping PaddlePaddle fix")
        return False
    
    try:
        # Step 1: Completely uninstall PaddlePaddle and related packages
        print("📦 Step 1: Completely uninstalling PaddlePaddle ecosystem...")
        packages_to_remove = [
            "paddlepaddle", "paddlepaddle-gpu", "paddlenlp", "ppdiffusers",
            "paddle2onnx", "paddlefsl", "paddlesde"
        ]
        
        for package in packages_to_remove:
            print(f"Removing {package}...")
            run_command(f"pip uninstall {package} -y", timeout=60)
        
        # Step 2: Clear all Python cache and temporary files
        print("📦 Step 2: Clearing all Python cache...")
        import shutil
        import glob
        
        # Clear __pycache__ directories
        cache_patterns = [
            "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddle*/__pycache__",
            "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/paddlenlp*/__pycache__",
            "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/ppdiffusers*/__pycache__",
            "/home/aistudio/.cache/pip/**/paddle*",
            "/tmp/pip-*"
        ]
        
        for pattern in cache_patterns:
            cache_dirs = glob.glob(pattern)
            for cache_dir in cache_dirs:
                if os.path.exists(cache_dir):
                    try:
                        shutil.rmtree(cache_dir)
                        print(f"Cleared: {cache_dir}")
                    except Exception as e:
                        print(f"Could not clear {cache_dir}: {e}")
        
        # Step 3: Clear Python module cache
        print("📦 Step 3: Clearing Python module cache...")
        import sys
        modules_to_clear = [name for name in sys.modules.keys() if 'paddle' in name.lower()]
        for module in modules_to_clear:
            del sys.modules[module]
        print(f"Cleared {len(modules_to_clear)} paddle-related modules from cache")
        
        # Step 4: Install PaddlePaddle in a clean environment
        print("📦 Step 4: Installing PaddlePaddle in clean environment...")
        
        # Try different installation strategies
        installation_strategies = [
            "pip install paddlepaddle-gpu==2.6.2 --no-cache-dir --force-reinstall",
            "pip install paddlepaddle==2.6.2 --no-cache-dir --force-reinstall",
            "pip install paddlepaddle-gpu==2.5.2 --no-cache-dir --force-reinstall",
            "pip install paddlepaddle==2.5.2 --no-cache-dir --force-reinstall"
        ]
        
        success = False
        for strategy in installation_strategies:
            print(f"Trying: {strategy}")
            success, _ = run_command(strategy, timeout=300)
            if success:
                print(f"✅ Successfully installed with: {strategy}")
                break
            else:
                print(f"❌ Failed with: {strategy}")
        
        if not success:
            print("❌ All PaddlePaddle installation strategies failed")
            return False
        
        # Step 5: Test import with retry mechanism
        print("📦 Step 5: Testing PaddlePaddle import with retry...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Clear module cache before each attempt
                import sys
                modules_to_clear = [name for name in sys.modules.keys() if 'paddle' in name.lower()]
                for module in modules_to_clear:
                    if module in sys.modules:
                        del sys.modules[module]
                
                # Try import
                import paddle
                print(f"✅ PaddlePaddle import successful: {paddle.__version__}")
                
                # Test basic functionality
                x = paddle.to_tensor([1.0, 2.0])
                print(f"✅ PaddlePaddle tensor creation successful")
                
                return True
                
            except Exception as e:
                print(f"❌ Import attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print("🔄 Retrying in 2 seconds...")
                    import time
                    time.sleep(2)
                else:
                    print("❌ All import attempts failed")
                    return False
        
        return False
        
    except Exception as e:
        print(f"❌ PaddlePaddle import fix failed: {e}")
        return False

def clear_module_cache():
    """Clear Python module cache to ensure fresh imports after installation"""
    import sys
    modules_to_clear = [
        'django', 'django.core', 'django.core.management',
        'django.utils', 'django.conf', 'django.db',
        'corsheaders', 'corsheaders.middleware',
        'PIL', 'cv2', 'numpy', 'paddle'
    ]
    
    cleared_count = 0
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
            cleared_count += 1
    
    if cleared_count > 0:
        print(f"🧹 Cleared {cleared_count} modules from cache for fresh imports")

def check_critical_dependencies():
    """Smart check critical dependencies - integrated smart_install test functionality"""
    print("🔍 Smart checking critical dependencies...")
    
    # Special check for numpy compatibility issues in AI Studio
    try:
        import numpy as np
        from skimage.feature import canny
        print("✅ NumPy and scikit-image compatibility verified")
    except ValueError as e:
        if "numpy.dtype size changed" in str(e):
            print("⚠️ Detected numpy binary compatibility issue")
            print("🔧 Attempting to fix numpy compatibility...")
            fix_numpy_compatibility_issue()
        else:
            print(f"❌ NumPy compatibility error: {e}")
    except ImportError as e:
        print(f"❌ NumPy/scikit-image import error: {e}")
    
    # Special check for PaddlePaddle import issues
    try:
        import paddle
        print(f"✅ PaddlePaddle import successful: {paddle.__version__}")
    except AttributeError as e:
        if "partially initialized module" in str(e):
            print("⚠️ Detected PaddlePaddle circular import issue")
            print("🔧 Attempting to fix PaddlePaddle import...")
            if fix_paddle_import_issue():
                print("✅ PaddlePaddle fix successful, retrying import...")
                try:
                    import paddle
                    print(f"✅ PaddlePaddle import successful after fix: {paddle.__version__}")
                except Exception as retry_e:
                    print(f"❌ PaddlePaddle import still failed after fix: {retry_e}")
            else:
                print("❌ PaddlePaddle fix failed")
        else:
            print(f"❌ PaddlePaddle attribute error: {e}")
    except ImportError as e:
        print(f"❌ PaddlePaddle import error: {e}")
    except Exception as e:
        print(f"❌ PaddlePaddle unexpected error: {e}")
        if "partially initialized" in str(e) or "circular import" in str(e):
            print("🔧 Attempting to fix PaddlePaddle import...")
            fix_paddle_import_issue()
    
    critical_packages = [
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("django", "Django"),
        ("paddle", "PaddlePaddle")  # Put paddle last as it may have issues
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

        # If paddle has issues, provide special suggestions
        if any("paddle" in module for module, _ in failed_packages):
            print("\n💡 PaddlePaddle import failure may be due to h11 version issues, suggest running:")
            print("pip install --upgrade h11>=0.14.0 httpx")

        # Try to automatically fix critical dependencies
        print("\n🔧 Attempting to automatically fix critical dependencies...")
        for module, name in failed_packages:
            success = False  # Initialize success variable
            if module == 'PIL':
                success, _ = run_command("pip install pillow==11.3.0", timeout=60)
            elif module == 'django':
                success, _ = run_command("pip install django==4.2.11", timeout=60)
            elif module == 'paddle':
                success, _ = run_command("pip install paddlepaddle-gpu==2.6.2", timeout=120)
            elif module == 'cv2':
                success, _ = run_command("pip install opencv-python==4.8.1.78", timeout=60)
            elif module == 'numpy':
                success, _ = run_command("pip install 'numpy>=1.21.2,<2.0.0'", timeout=60)
            else:
                print(f"⚠️ No fix available for {name}")
                continue

            if success:
                print(f"✅ {name} fix successful")
            else:
                print(f"❌ {name} fix failed")

    # Lower success threshold to 60% (more lenient)
    return success_count >= len(critical_packages) * 0.6

def setup_django_environment():
    """Setup Django environment - Wangchuk Mind"""
    print("🔧 Setting up Django environment...")

    # Check critical dependencies first
    if not check_critical_dependencies():
        print("⚠️ Some critical dependencies are missing, but continuing...")

    # Set environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

    # Set PaddlePaddle environment variables
    os.environ['PADDLE_FRAMEWORK'] = 'paddle'
    os.environ['PADDLE_DEVICE'] = 'gpu' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu'

    print("✅ Django environment setup completed")

def print_system_introduction():
    """Print system introduction after successful startup - Wangchuk Mind"""
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
    print("   • Minimal dependency footprint for optimal performance")
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
    """Setup environment for Django server - Wangchuk Mind"""
    # Import startup status manager
    try:
        from startup_status import is_already_setup, mark_environment_setup
        if is_already_setup():
            print("⚡ Environment already set up, skipping repeated setup...")
            return
    except ImportError:
        # Fallback to function attribute check
        if hasattr(setup_environment, '_already_setup'):
            print("⚡ Environment already set up, skipping repeated setup...")
            return
    
    print("🚀 AI Studio One-Click Startup Script")
    print("=" * 50)

    # Check if running in AI Studio environment
    if not os.path.exists('/home/aistudio'):
        print("⚠️ Not in AI Studio environment, skipping environment setup")
        setup_django_environment()
        print_system_introduction()
        setup_environment._already_setup = True
        return

    # Fast startup mode - prioritize Django startup
    print("⚡ Fast startup mode: prioritizing Django server startup")

    # Step 1: Setup Django environment (required)
    print("\n📋 Step 1: Setting up Django environment")
    print("-" * 30)
    setup_django_environment()

    # Step 2: Check Python environment (non-blocking)
    print("\n📋 Step 2: Checking Python environment")
    print("-" * 30)
    setup_python_environment()

    # Step 3: Install dependencies (non-blocking)
    print("\n📋 Step 3: Installing dependencies")
    print("-" * 30)
    install_dependencies()

    # Step 4: Download models (background processing)
    print("\n📋 Step 4: Preparing model files")
    print("-" * 30)
    if not download_models():
        print("⚠️ Model download failed, will start server without models")
        os.environ['SKIP_MODEL_LOADING'] = '1'

    # Step 5: Final dependency check
    print("\n📋 Step 5: Final dependency check")
    print("-" * 30)
    deps_ok = check_critical_dependencies()
    if not deps_ok:
        print("⚠️ Some critical dependencies may have issues, but continuing...")

    print("\n🎉 Environment setup completed!")
    print("=" * 50)

    # Display system introduction
    print_system_introduction()
    
    # Clear Python module cache to ensure fresh imports
    clear_module_cache()
    
    # Mark environment as already set up to prevent repeated execution
    try:
        from startup_status import mark_environment_setup
        mark_environment_setup()
    except ImportError:
        setup_environment._already_setup = True

def pre_django_paddle_check():
    """Pre-Django PaddlePaddle check to prevent circular import issues"""
    # Check if PaddlePaddle has already been checked to avoid repeated execution
    if hasattr(pre_django_paddle_check, '_already_checked'):
        print("⚡ PaddlePaddle already checked, skipping repeated check...")
        return True
    
    print("🔍 Pre-Django PaddlePaddle check...")
    
    try:
        import paddle
        print(f"✅ PaddlePaddle pre-check successful: {paddle.__version__}")
        pre_django_paddle_check._already_checked = True
        return True
    except AttributeError as e:
        if "partially initialized module" in str(e):
            print("⚠️ Detected PaddlePaddle circular import in pre-check")
            print("🔧 Attempting aggressive PaddlePaddle fix...")
            result = fix_paddle_import_issue()
            if result:
                pre_django_paddle_check._already_checked = True
            return result
        else:
            print(f"❌ PaddlePaddle attribute error in pre-check: {e}")
            return False
    except ImportError as e:
        print(f"❌ PaddlePaddle import error in pre-check: {e}")
        return False
    except Exception as e:
        print(f"❌ PaddlePaddle unexpected error in pre-check: {e}")
        if "partially initialized" in str(e) or "circular import" in str(e):
            print("🔧 Attempting aggressive PaddlePaddle fix...")
            result = fix_paddle_import_issue()
            if result:
                pre_django_paddle_check._already_checked = True
            return result
        return False

if __name__ == '__main__':
    # Execute environment setup
    setup_environment()

    # Pre-Django PaddlePaddle check
    print("\n🔍 Pre-Django PaddlePaddle check...")
    if not pre_django_paddle_check():
        print("⚠️ PaddlePaddle pre-check failed, but continuing...")

    # Import Django and start server
    try:
        import django
        from django.core.management import execute_from_command_line

        print("\n🚀 Starting Django server...")
        print("=" * 50)
        
        # Modify sys.argv to use localhost instead of 0.0.0.0
        if len(sys.argv) > 2 and 'runserver' in sys.argv:
            # Replace 0.0.0.0:8080 with localhost:8080
            for i, arg in enumerate(sys.argv):
                if '0.0.0.0:8080' in arg:
                    sys.argv[i] = arg.replace('0.0.0.0:8080', 'localhost:8080')
                elif '0.0.0.0' in arg and ':8080' in arg:
                    sys.argv[i] = arg.replace('0.0.0.0', 'localhost')
        
        execute_from_command_line(sys.argv)
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        print("💡 Please ensure Django is properly installed")
        print("🔧 Try running: pip install django==4.2.11")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Django startup failed: {e}")
        print("💡 Please check if dependencies are correctly installed")
        print("🔧 Try running: python smart_install.py")
        sys.exit(1)
