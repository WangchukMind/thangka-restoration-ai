#!/usr/bin/env python3
"""
快速修复h11版本兼容性问题
解决PaddlePaddle导入失败的问题
"""
import subprocess
import sys

def run_command(cmd, timeout=120):
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

def fix_h11_issue():
    """修复h11版本问题"""
    print("🔧 开始修复h11版本兼容性问题...")
    print("=" * 50)
    
    # 1. 升级h11到兼容版本
    print("\n📦 升级h11到兼容版本...")
    success, _ = run_command("pip install --upgrade 'h11>=0.14.0'", timeout=120)
    if not success:
        print("⚠️ h11升级失败，尝试强制安装...")
        run_command("pip install --force-reinstall 'h11>=0.14.0'", timeout=120)
    
    # 2. 重新安装httpx确保兼容性
    print("\n🔄 重新安装httpx确保兼容性...")
    success, _ = run_command("pip install --upgrade httpx==0.24.1", timeout=120)
    if not success:
        print("⚠️ httpx重新安装失败，尝试强制安装...")
        run_command("pip install --force-reinstall httpx==0.24.1", timeout=120)
    
    # 3. 重新安装httpcore
    print("\n🔄 重新安装httpcore...")
    run_command("pip install --upgrade httpcore", timeout=120)
    
    # 4. 测试PaddlePaddle导入
    print("\n🧪 测试PaddlePaddle导入...")
    try:
        import paddle
        print("✅ PaddlePaddle导入成功！")
        return True
    except Exception as e:
        print(f"❌ PaddlePaddle导入仍然失败: {e}")
        
        # 尝试其他解决方案
        print("\n🔧 尝试其他解决方案...")
        
        # 方案1: 重新安装PaddlePaddle
        print("方案1: 重新安装PaddlePaddle...")
        run_command("pip install --force-reinstall paddlepaddle-gpu==2.6.2", timeout=300)
        
        # 方案2: 安装兼容的h11版本
        print("方案2: 安装特定h11版本...")
        run_command("pip install h11==0.14.0", timeout=120)
        
        # 再次测试
        try:
            import paddle
            print("✅ 修复成功！PaddlePaddle现在可以导入了！")
            return True
        except Exception as e2:
            print(f"❌ 修复失败: {e2}")
            return False

def test_other_imports():
    """测试其他关键包导入"""
    print("\n🔍 测试其他关键包导入...")
    
    test_packages = [
        ("numpy", "NumPy"),
        ("torch", "PyTorch"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("django", "Django"),
        ("fastapi", "FastAPI")
    ]
    
    success_count = 0
    for module, name in test_packages:
        try:
            __import__(module)
            print(f"✅ {name} 导入成功")
            success_count += 1
        except Exception as e:
            print(f"❌ {name} 导入失败: {e}")
    
    print(f"\n📊 其他包测试结果: {success_count}/{len(test_packages)} 个包导入成功")
    return success_count >= len(test_packages) * 0.8

if __name__ == "__main__":
    print("🎨 h11版本兼容性修复脚本")
    print("=" * 50)
    
    # 修复h11问题
    fix_success = fix_h11_issue()
    
    if fix_success:
        print("\n🎉 h11问题修复成功！")
        
        # 测试其他包
        other_success = test_other_imports()
        
        if other_success:
            print("\n🎉 所有问题已解决！可以启动服务器了！")
            print("\n🚀 启动命令:")
            print("python start_server.py runserver 0.0.0.0:8080")
        else:
            print("\n⚠️ h11问题已修复，但其他包可能有问题")
    else:
        print("\n❌ h11问题修复失败，请手动检查")
        print("\n💡 手动修复命令:")
        print("pip install --upgrade 'h11>=0.14.0' httpx httpcore")
    
    sys.exit(0)



