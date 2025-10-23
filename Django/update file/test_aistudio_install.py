#!/usr/bin/env python3
"""
AI Studio环境依赖安装测试脚本
测试requirements_aistudio.txt中的包是否都能正确安装
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

def test_package_installation():
    """测试包安装"""
    print("🚀 开始测试AI Studio环境依赖安装...")
    print("=" * 60)
    
    # 检查Python版本
    success, result = run_command("python --version", timeout=30)
    if success and result:
        print(f"✅ Python版本: {result.stdout.strip()}")
    else:
        print("❌ 无法获取Python版本")
        return False
    
    # 检查pip版本
    success, result = run_command("pip --version", timeout=30)
    if success and result:
        print(f"✅ pip版本: {result.stdout.strip()}")
    else:
        print("❌ 无法获取pip版本")
        return False
    
    # 测试关键包的安装
    critical_packages = [
        "scipy==1.15.3",
        "scikit-image==0.21.0", 
        "imageio==2.31.1",
        "paddlepaddle-gpu==2.6.2",
        "paddlenlp==2.8.1",
        "ppdiffusers==0.29.0"
    ]
    
    print("\n📦 测试关键包安装...")
    for package in critical_packages:
        print(f"\n🔍 测试安装 {package}...")
        success, result = run_command(f"pip install {package}", timeout=120)
        if success:
            print(f"✅ {package} 安装成功")
        else:
            print(f"❌ {package} 安装失败")
            return False
    
    print("\n🎉 所有关键包安装测试通过！")
    return True

def test_imports():
    """测试包导入"""
    print("\n🔍 测试包导入...")
    
    test_imports = [
        ("paddle", "PaddlePaddle"),
        ("paddlenlp", "PaddleNLP"),
        ("ppdiffusers", "PPDiffusers"),
        ("diffusers", "Diffusers"),
        ("transformers", "Transformers"),
        ("torch", "PyTorch"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("matplotlib", "Matplotlib"),
        ("django", "Django"),
        ("fastapi", "FastAPI")
    ]
    
    failed_imports = []
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} 导入成功")
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")
            failed_imports.append((module, name))
    
    if failed_imports:
        print(f"\n⚠️ 有 {len(failed_imports)} 个包导入失败:")
        for module, name in failed_imports:
            print(f"  - {name} ({module})")
        return False
    else:
        print("\n🎉 所有包导入测试通过！")
        return True

if __name__ == "__main__":
    print("🎨 AI Studio环境依赖测试脚本")
    print("=" * 60)
    
    # 测试安装
    install_success = test_package_installation()
    
    if install_success:
        # 测试导入
        import_success = test_imports()
        
        if import_success:
            print("\n🎉 所有测试通过！AI Studio环境配置成功！")
            sys.exit(0)
        else:
            print("\n⚠️ 包安装成功但导入失败，请检查环境配置")
            sys.exit(1)
    else:
        print("\n❌ 包安装失败，请检查requirements_aistudio.txt文件")
        sys.exit(1)



