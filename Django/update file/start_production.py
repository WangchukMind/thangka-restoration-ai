#!/usr/bin/env python3
"""
Production Startup Script - Wangchuk Mind
Simplified startup script without repeated environment setup
"""
import os
import sys

def start_django_server():
    """Start Django server without repeated environment setup"""
    print("🚀 Starting Django Server (Production Mode)")
    print("=" * 50)
    
    # Set environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    os.environ['PADDLE_FRAMEWORK'] = 'paddle'
    os.environ['PADDLE_DEVICE'] = 'gpu' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu'
    
    # Import Django and start server
    try:
        import django
        from django.core.management import execute_from_command_line
        
        print("✅ Django server starting...")
        execute_from_command_line(sys.argv)
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        print("💡 Please run the full setup first:")
        print("python start_server.py runserver 0.0.0.0:8080")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Django startup failed: {e}")
        print("💡 Please check if dependencies are correctly installed")
        sys.exit(1)

if __name__ == '__main__':
    start_django_server()



