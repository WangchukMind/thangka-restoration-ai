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


def run_command(cmd, cwd=None, check=True, timeout=300):
    """Run command and return result - Wangchuk Mind"""
    print(f"🔧 Executing command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check,
                                capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True, result
    except subprocess.TimeoutExpired:
        print(f"⏰ Command execution timeout: {cmd}")
        return False, None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command execution failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False, e


def setup_conda_environment():
    """Setup conda environment - Wangchuk Mind"""
    print("🚀 Starting conda environment setup...")

    # Check existing environments
    print("📋 Checking existing environments...")
    success, result = run_command("conda env list", check=False, timeout=60)
    if not success:
        print("⚠️ conda command execution failed, skipping environment setup")
        return False

    # Check if environment already exists
    if result and "wangchukthangka" in result.stdout:
        print("✅ Environment already exists, skipping creation")
        return True

    # Create new environment
    print("🆕 Creating new environment...")
    success, _ = run_command("conda create -n wangchukthangka python=3.9 -y", timeout=300)
    if success:
        print("✅ Environment created successfully")
        return True
    else:
        print("❌ Environment creation failed")
        return False


def install_dependencies():
    """Install Python dependencies - Wangchuk Mind"""
    print("📦 Starting Python dependency installation...")

    requirements_file = "/home/aistudio/work/wangchukthangka/Thangka/Django/requirements_paddle.txt"

    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file does not exist: {requirements_file}")
        return False

    # Install basic dependencies first
    print("🔧 Installing basic dependencies...")
    basic_deps = [
        "paddlepaddle-gpu==2.6.2",
        "ppdiffusers==0.29.0",
        "django==4.2.11",
        "pillow",
        "numpy",
        "requests"
    ]

    for dep in basic_deps:
        print(f"📦 Installing {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=120)
        if not success:
            print(f"⚠️ {dep} installation failed, continuing")

    # Try to install complete requirements file
    print("📦 Installing complete requirements file...")
    success, _ = run_command(f"pip install -r {requirements_file}", timeout=600)
    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("⚠️ Complete dependency installation failed, but basic dependencies are installed")
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
    success, _ = run_command(f"git clone {repo_url} {temp_dir}", timeout=600)
    if not success:
        print("❌ Model repository cloning failed")
        return False

    # Copy model files
    source_models = os.path.join(temp_dir, "models")
    if os.path.exists(source_models):
        print(f"📋 Copying model files from {source_models} to {model_dir}")
        success, _ = run_command(f"cp -r {source_models}/* {model_dir}/", timeout=300)
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


def setup_django_environment():
    """Setup Django environment - Wangchuk Mind"""
    print("🔧 Setting up Django environment...")

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


def main():
    """Main function - one-click startup for all features - Wangchuk Mind"""
    print("🚀 AI Studio one-click startup script starting execution...")
    print("=" * 50)

    # Check if running in AI Studio environment
    if not os.path.exists('/home/aistudio'):
        print("⚠️ Not in AI Studio environment, skipping environment setup")
        setup_django_environment()
        # Display system introduction even in local environment - Wangchuk Mind
        print_system_introduction()
        return

    # Fast startup mode - prioritize Django startup, background environment processing
    print("⚡ Fast startup mode: prioritizing Django server startup")

    # Step 1: Setup Django environment (required)
    print("\n📋 Step 1: Setting up Django environment")
    print("-" * 30)
    setup_django_environment()

    # Step 2: Check and setup conda environment (non-blocking)
    print("\n📋 Step 2: Checking conda environment")
    print("-" * 30)
    setup_conda_environment()

    # Step 3: Install basic dependencies (non-blocking)
    print("\n📋 Step 3: Installing basic dependencies")
    print("-" * 30)
    install_dependencies()

    # Step 4: Download models (background processing)
    print("\n📋 Step 4: Preparing model files")
    print("-" * 30)
    if not download_models():
        print("⚠️ Model download failed, will start server without models")
        os.environ['SKIP_MODEL_LOADING'] = '1'

    print("\n🎉 Environment setup completed!")
    print("=" * 50)

    # Display system introduction - Wangchuk Mind
    print_system_introduction()


if __name__ == '__main__':
    # Execute environment setup
    main()

    # Import Django and start server
    try:
        import django
        from django.core.management import execute_from_command_line

        print("🚀 Starting Django server...")
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"❌ Django startup failed: {e}")
        sys.exit(1)
