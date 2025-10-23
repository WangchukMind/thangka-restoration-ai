#!/usr/bin/env python3
"""
快速启动脚本 - 简化版本
专门用于快速启动Django服务器
"""
import os
import sys
import subprocess

def run_command(cmd, timeout=60):
    """运行命令并返回结果"""
    print(f"🔧 执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"✅ 成功: {result.stdout.strip()}")
        return True, result
    except subprocess.TimeoutExpired:
        print(f"⏰ 命令执行超时: {cmd}")
        return False, None
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False, e

def quick_dependency_check():
    """快速检查关键依赖"""
    print("🔍 快速检查关键依赖...")
    
    critical_packages = [
        ("django", "Django"),
        ("corsheaders", "Django CORS"),
        ("paddle", "PaddlePaddle"),
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow")
    ]
    
    missing = []
    for module, name in critical_packages:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} 缺失")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️ 缺失关键依赖: {missing}")
        print("🔧 尝试快速安装...")
        
        # 快速安装缺失的依赖
        for name in missing:
            if name == "Django":
                run_command("pip install django==4.2.11", timeout=60)
            elif name == "Django CORS":
                run_command("pip install django-cors-headers==4.3.1", timeout=60)
            elif name == "PaddlePaddle":
                run_command("pip install paddlepaddle-gpu==2.6.2", timeout=120)
            elif name == "NumPy":
                run_command("pip install numpy>=1.21.2,<2.0.0", timeout=60)
            elif name == "OpenCV":
                run_command("pip install opencv-python==4.8.1.78", timeout=60)
            elif name == "Pillow":
                run_command("pip install pillow", timeout=60)
        
        return False
    
    print("✅ 所有关键依赖检查通过")
    return True

def main():
    """快速启动主函数"""
    print("🚀 快速启动唐卡修复系统...")
    print("=" * 50)
    
    # 快速依赖检查
    if not quick_dependency_check():
        print("⚠️ 依赖检查未完全通过，但尝试继续启动...")
    
    # 设置环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    os.environ['PADDLE_FRAMEWORK'] = 'paddle'
    os.environ['PADDLE_DEVICE'] = 'gpu' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu'
    
    print("\n🎨 AI + 非物质文化遗产唐卡图像修复系统")
    print("=" * 50)
    print("🌟 系统概述:")
    print("   • 先进的AI驱动唐卡图像修复技术")
    print("   • 专门用于非物质文化遗产保护")
    print("   • 最先进的扩散模型与LoRA微调")
    print("   • 实时流式处理能力")
    print("")
    print("👨‍💻 开发与实现: Wangchuk Mind")
    print("=" * 50)
    
    # 启动Django服务器
    try:
        import django
        from django.core.management import execute_from_command_line
        
        print("\n🚀 启动Django服务器...")
        execute_from_command_line(sys.argv)
    except ImportError as e:
        print(f"❌ Django导入失败: {e}")
        print("💡 请运行完整安装: python start_server.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Django启动失败: {e}")
        print("💡 请运行完整安装: python start_server.py")
        sys.exit(1)

if __name__ == '__main__':
    main()



