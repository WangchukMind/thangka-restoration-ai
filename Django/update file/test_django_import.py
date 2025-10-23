#!/usr/bin/env python3
"""
Django Import Test Script - Wangchuk Mind
Test Django import after installation
"""
import sys
import subprocess

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

def clear_module_cache():
    """Clear Python module cache"""
    modules_to_clear = [
        'django', 'django.core', 'django.core.management',
        'django.utils', 'django.conf', 'django.db',
        'corsheaders', 'corsheaders.middleware'
    ]
    
    cleared_count = 0
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
            cleared_count += 1
    
    print(f"🧹 Cleared {cleared_count} modules from cache")

def test_django_import():
    """Test Django import after installation"""
    print("🧪 Testing Django import...")
    
    # Clear module cache first
    clear_module_cache()
    
    # Test Django import
    try:
        import django
        print(f"✅ Django import successful: {django.__version__}")
        
        # Test Django management
        from django.core.management import execute_from_command_line
        print("✅ Django management import successful")
        
        # Test CORS headers
        try:
            import corsheaders
            print("✅ CORS headers import successful")
        except ImportError:
            print("⚠️ CORS headers not available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Django import error: {e}")
        return False

def main():
    """Main function"""
    print("🧪 Django Import Test Script")
    print("=" * 40)
    
    # First, ensure Django is installed
    print("📦 Ensuring Django is installed...")
    success, _ = run_command("pip install django==4.2.11", timeout=120)
    if not success:
        print("❌ Failed to install Django")
        return
    
    # Test import
    if test_django_import():
        print("\n🎉 Django import test successful!")
        print("You can now run the Django server:")
        print("python start_server.py runserver 0.0.0.0:8080")
    else:
        print("\n❌ Django import test failed!")
        print("Please check the error messages above")

if __name__ == "__main__":
    main()



