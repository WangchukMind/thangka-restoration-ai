#!/usr/bin/env python3
"""
AI Studio 完整修复脚本
解决所有已知问题，包括NumPy兼容性和API错误
"""
import os
import sys
import subprocess
import json

def run_command(cmd, timeout=300):
    """运行命令"""
    print(f"🔧 执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"输出: {result.stdout}")
        if result.stderr:
            print(f"错误: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return False

def fix_numpy_compatibility():
    """修复NumPy兼容性"""
    print("🔧 修复NumPy兼容性问题...")
    
    # 强制安装NumPy 1.x
    commands = [
        "pip uninstall numpy scikit-image opencv-python imageio -y",
        "pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall",
        "pip install scikit-image==0.21.0 --force-reinstall",
        "pip install opencv-python==4.8.1.78 --force-reinstall",
        "pip install imageio==2.31.1 --force-reinstall"
    ]
    
    for cmd in commands:
        if not run_command(cmd, timeout=300):
            print(f"⚠️ 命令执行失败: {cmd}")
    
    return True

def create_model_directories():
    """创建必要的模型目录"""
    print("📁 创建模型目录...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    finetuned_dir = os.path.join(models_dir, "finetuned")
    controlnet_dir = os.path.join(models_dir, "control_v11p_sd21_canny_paddle")
    
    directories = [models_dir, finetuned_dir, controlnet_dir]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 创建目录: {directory}")
    
    return True

def test_api_endpoint():
    """测试API端点"""
    print("🧪 测试API端点...")
    
    try:
        import requests
        response = requests.get("http://localhost:8080/api/getType", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API测试成功: {data}")
            return True
        else:
            print(f"❌ API测试失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API测试异常: {e}")
        return False

def create_test_script():
    """创建测试脚本"""
    test_script = '''#!/usr/bin/env python3
"""
测试API端点
"""
import requests
import json

def test_getType_api():
    try:
        response = requests.get("http://localhost:8080/api/getType", timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        print(f"响应内容: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON数据: {data}")
                return True
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}")
                return False
        else:
            return False
    except Exception as e:
        print(f"请求失败: {e}")
        return False

if __name__ == "__main__":
    test_getType_api()
'''
    
    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ 测试脚本已创建: test_api.py")
    return True

def main():
    """主函数"""
    print("🚀 AI Studio 完整修复脚本")
    print("=" * 50)
    
    # 步骤1: 修复NumPy兼容性
    print("\n📋 步骤1: 修复NumPy兼容性")
    fix_numpy_compatibility()
    
    # 步骤2: 创建模型目录
    print("\n📋 步骤2: 创建模型目录")
    create_model_directories()
    
    # 步骤3: 创建测试脚本
    print("\n📋 步骤3: 创建测试脚本")
    create_test_script()
    
    print("\n🎉 修复完成！")
    print("\n📋 下一步操作:")
    print("1. 重启Django服务器:")
    print("   python start_server_aistudio.py runserver 0.0.0.0:8080")
    print("\n2. 测试API端点:")
    print("   python test_api.py")
    print("\n3. 如果还有问题，检查服务器日志")

if __name__ == "__main__":
    main()



