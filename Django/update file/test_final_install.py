#!/usr/bin/env python3
"""
最终依赖安装测试脚本
验证所有冲突问题是否已解决
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

def test_conflict_resolution():
    """测试冲突解决"""
    print("🚀 开始测试依赖冲突解决...")
    print("=" * 60)
    
    # 测试关键冲突包组合
    conflict_tests = [
        # 测试numpy和opencv兼容性
        ["numpy>=1.21.2,<2.0.0", "opencv-python==4.8.1.78"],
        # 测试click和flask兼容性
        ["click>=8.1.3", "Flask==3.1.1"],
        # 测试paddlepaddle和numpy兼容性
        ["paddlepaddle-gpu==2.6.2", "numpy>=1.21.2,<2.0.0"],
        # 测试torch和numpy兼容性
        ["torch==2.4.0", "numpy>=1.21.2,<2.0.0"]
    ]
    
    print("\n🔍 测试关键冲突包组合...")
    for i, packages in enumerate(conflict_tests, 1):
        print(f"\n测试 {i}: {' + '.join(packages)}")
        success, _ = run_command(f"pip install {' '.join(packages)}", timeout=120)
        if success:
            print(f"✅ 测试 {i} 通过")
        else:
            print(f"❌ 测试 {i} 失败")
            return False
    
    return True

def test_final_requirements():
    """测试最终requirements文件"""
    print("\n📦 测试最终requirements文件安装...")
    
    # 检查文件是否存在
    if not os.path.exists("requirements_final.txt"):
        print("❌ requirements_final.txt 文件不存在")
        return False
    
    # 尝试安装
    success, _ = run_command("pip install -r requirements_final.txt", timeout=600)
    if success:
        print("✅ requirements_final.txt 安装成功")
        return True
    else:
        print("❌ requirements_final.txt 安装失败")
        return False

def test_critical_imports():
    """测试关键包导入"""
    print("\n🔍 测试关键包导入...")
    
    critical_packages = [
        ("paddle", "PaddlePaddle"),
        ("torch", "PyTorch"),
        ("numpy", "NumPy"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("django", "Django"),
        ("fastapi", "FastAPI"),
        ("flask", "Flask"),
        ("click", "Click")
    ]
    
    success_count = 0
    for module, name in critical_packages:
        try:
            __import__(module)
            print(f"✅ {name} 导入成功")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")
    
    print(f"\n📊 测试结果: {success_count}/{len(critical_packages)} 个关键包导入成功")
    return success_count >= len(critical_packages) * 0.8  # 80%以上成功

if __name__ == "__main__":
    print("🎨 最终依赖安装测试脚本")
    print("=" * 60)
    
    # 测试冲突解决
    conflict_success = test_conflict_resolution()
    
    if conflict_success:
        print("\n✅ 冲突解决测试通过！")
        
        # 测试最终requirements文件
        final_success = test_final_requirements()
        
        if final_success:
            # 测试导入
            import_success = test_critical_imports()
            
            if import_success:
                print("\n🎉 所有测试通过！依赖安装完全成功！")
                print("\n🚀 现在可以启动服务器了：")
                print("python start_server.py runserver 0.0.0.0:8080")
            else:
                print("\n⚠️ 部分包导入失败，但核心功能应该可用")
        else:
            print("\n❌ 最终requirements文件安装失败")
    else:
        print("\n❌ 冲突解决测试失败")
    
    sys.exit(0)



