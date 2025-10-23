#!/usr/bin/env python3
"""
AI Studio Dependency Fix Script - Wangchuk Mind
快速修复AI Studio环境中的依赖问题
"""
import subprocess
import sys
import os

def run_command(cmd, timeout=300):
    """运行命令并返回结果"""
    print(f"🔧 执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True, result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False, e
    except subprocess.TimeoutExpired:
        print(f"⏰ 命令执行超时: {cmd}")
        return False, None

def fix_dependencies():
    """修复依赖问题"""
    print("🚀 开始修复AI Studio依赖问题...")
    print("=" * 50)
    
    # 关键依赖列表
    critical_deps = [
        "django==4.2.11",
        "django-cors-headers==4.3.1",
        "pillow",
        "numpy",
        "requests",
        "paddlepaddle-gpu==2.6.2",
        "ppdiffusers==0.29.0"
    ]
    
    print("📦 安装关键依赖...")
    failed_deps = []
    
    for dep in critical_deps:
        print(f"\n🔧 安装 {dep}...")
        success, _ = run_command(f"pip install {dep}", timeout=180)
        if success:
            print(f"✅ {dep} 安装成功")
        else:
            print(f"❌ {dep} 安装失败")
            failed_deps.append(dep)
    
    if failed_deps:
        print(f"\n⚠️ 以下依赖安装失败: {failed_deps}")
        print("尝试使用conda安装...")
        
        # 尝试使用conda安装失败的依赖
        for dep in failed_deps:
            if dep.startswith("django"):
                success, _ = run_command(f"conda install -c conda-forge django-cors-headers -y", timeout=120)
            elif dep == "pillow":
                success, _ = run_command(f"conda install pillow -y", timeout=120)
            elif dep == "numpy":
                success, _ = run_command(f"conda install numpy -y", timeout=120)
            
            if success:
                print(f"✅ {dep} 通过conda安装成功")
            else:
                print(f"❌ {dep} conda安装也失败")
    
    print("\n🔍 验证关键依赖...")
    test_imports = [
        ("django", "import django"),
        ("corsheaders", "import corsheaders"),
        ("PIL", "from PIL import Image"),
        ("numpy", "import numpy"),
        ("paddle", "import paddle")
    ]
    
    missing_deps = []
    for name, import_cmd in test_imports:
        try:
            exec(import_cmd)
            print(f"✅ {name} 可用")
        except ImportError:
            print(f"❌ {name} 不可用")
            missing_deps.append(name)
    
    if missing_deps:
        print(f"\n❌ 仍有依赖缺失: {missing_deps}")
        print("请手动安装这些依赖:")
        for dep in missing_deps:
            if dep == "corsheaders":
                print("pip install django-cors-headers==4.3.1")
            elif dep == "PIL":
                print("pip install pillow")
            else:
                print(f"pip install {dep}")
        return False
    else:
        print("\n🎉 所有关键依赖都已正确安装!")
        return True

def test_django_startup():
    """测试Django启动"""
    print("\n🧪 测试Django启动...")
    
    # 设置环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    
    try:
        import django
        from django.core.management import execute_from_command_line
        
        print("✅ Django导入成功")
        
        # 尝试Django设置
        django.setup()
        print("✅ Django设置成功")
        
        return True
    except Exception as e:
        print(f"❌ Django启动测试失败: {e}")
        return False

if __name__ == '__main__':
    print("🎨 Thangka AI Studio 依赖修复工具")
    print("=" * 50)
    
    # 修复依赖
    if fix_dependencies():
        print("\n🚀 依赖修复完成，测试Django启动...")
        if test_django_startup():
            print("\n🎉 修复成功! 现在可以启动Django服务器了")
            print("运行命令: python start_server.py runserver 0.0.0.0:8080")
        else:
            print("\n⚠️ Django启动测试失败，请检查错误信息")
    else:
        print("\n❌ 依赖修复失败，请手动安装缺失的依赖")
    
    print("\n" + "=" * 50)



