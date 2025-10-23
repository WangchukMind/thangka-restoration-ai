#!/usr/bin/env python3
"""
AI Studio 一键启动脚本 - 修复版本
集成环境设置、依赖安装、模型下载和Django启动
"""
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

# 修复aistudio_sdk导入错误
try:
    import aistudio_sdk.hub
    if not hasattr(aistudio_sdk.hub, 'download'):
        def dummy_download(*args, **kwargs):
            print("⚠️ aistudio_sdk.download 不可用，跳过模型下载")
            return None
        aistudio_sdk.hub.download = dummy_download
        print("✅ aistudio_sdk补丁已应用")
except ImportError:
    print("⚠️ aistudio_sdk 未安装，跳过")

def run_command(cmd, cwd=None, check=True, timeout=300):
    """运行命令并返回结果"""
    print(f"🔧 执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True, result
    except subprocess.TimeoutExpired:
        print(f"⏰ 命令执行超时: {cmd}")
        return False, None
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False, e

def check_critical_dependencies():
    """检查关键依赖是否安装"""
    print("🔍 检查关键依赖...")
    
    critical_deps = [
        'django',
        'corsheaders',
        'paddle',
        'PIL'  # Pillow
    ]
    
    missing_deps = []
    for dep in critical_deps:
        try:
            if dep == 'PIL':
                import PIL
            else:
                __import__(dep)
            print(f"✅ {dep} 可用")
        except ImportError:
            print(f"❌ {dep} 不可用")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"❌ 缺失关键依赖: {missing_deps}")
        print("🔧 尝试安装缺失的依赖...")
        
        # 尝试安装缺失的依赖
        for dep in missing_deps:
            if dep == 'corsheaders':
                success, _ = run_command("pip install django-cors-headers==4.3.1", timeout=60)
            elif dep == 'PIL':
                success, _ = run_command("pip install pillow", timeout=60)
            elif dep == 'django':
                success, _ = run_command("pip install django==4.2.11", timeout=60)
            elif dep == 'paddle':
                success, _ = run_command("pip install paddlepaddle-gpu==2.6.2", timeout=120)
            
            if success:
                print(f"✅ {dep} 安装成功")
            else:
                print(f"❌ {dep} 安装失败")
        
        return len(missing_deps) == 0
    
    return True

def setup_python_environment():
    """设置Python环境（简化版本，不使用conda）"""
    print("🐍 设置Python环境...")
    
    # 检查Python版本
    success, result = run_command("python3 --version", check=False, timeout=30)
    if success and result:
        print(f"✅ Python版本: {result.stdout.strip()}")
    else:
        print("⚠️ Python3不可用，尝试使用python...")
        success, result = run_command("python --version", check=False, timeout=30)
        if success and result:
            print(f"✅ Python版本: {result.stdout.strip()}")
        else:
            print("❌ Python不可用")
            return False
    
    print("✅ Python环境设置完成")
    return True

def install_dependencies():
    """使用pip安装Python依赖"""
    print("📦 开始使用pip安装Python依赖...")
    
    # 优先使用 requirements_paddle.txt
    requirements_file = "/home/aistudio/work/wangchukthangka/Thangka/Django/requirements_paddle.txt"
    if not os.path.exists(requirements_file):
        requirements_file = "/home/aistudio/work/wangchukthangka/Thangka/Django/requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ 依赖文件不存在: {requirements_file}")
        return False
    
    # 检查pip是否可用
    success, result = run_command("pip3 --version", check=False, timeout=30)
    if not success:
        print("⚠️ pip3不可用，尝试使用pip...")
        success, result = run_command("pip --version", check=False, timeout=30)
        if not success:
            print("❌ pip不可用")
            return False
    
    print(f"✅ pip可用: {result.stdout.strip() if result else 'Unknown version'}")
    
    # 升级pip
    print("🔧 升级pip...")
    pip_cmd = "pip3" if "pip3" in result.stdout else "pip"
    run_command(f"{pip_cmd} install --upgrade pip", timeout=120)
    
    # 安装基础依赖（包含CORS支持）
    print("📦 安装基础依赖...")
    basic_deps = [
        "paddlepaddle-gpu==2.6.2",
        "ppdiffusers==0.29.0", 
        "django==4.2.11",
        "django-cors-headers==4.3.1",  # 添加CORS支持
        "pillow",
        "numpy",
        "requests"
    ]
    
    failed_deps = []
    for dep in basic_deps:
        print(f"📦 安装 {dep}...")
        success, _ = run_command(f"{pip_cmd} install {dep}", timeout=180)
        if not success:
            print(f"⚠️ {dep} 安装失败，继续执行")
            failed_deps.append(dep)
    
    if failed_deps:
        print(f"❌ 关键依赖安装失败: {failed_deps}")
        print("⚠️ 服务器可能无法正常启动")
    
    # 尝试安装完整依赖文件
    print("📦 安装完整依赖文件...")
    success, _ = run_command(f"{pip_cmd} install -r {requirements_file}", timeout=600)
    if success:
        print("✅ 完整依赖安装成功")
    else:
        print("⚠️ 完整依赖安装失败，但基础依赖已安装")
    
    print("✅ 依赖安装完成")
    return True

def download_models():
    """下载模型文件"""
    print("🚀 开始下载模型文件...")
    
    # 设置模型目录
    model_dir = "/home/aistudio/work/wangchukthangka/Thangka/Django/models"
    
    # 确保目录存在
    os.makedirs(model_dir, exist_ok=True)
    
    # 检查是否已经存在模型文件
    if os.path.exists(os.path.join(model_dir, "sd2.1_base_paddle")):
        print("✅ 模型文件已存在，跳过下载")
        return True
    
    # 尝试从AI Studio数据目录复制模型
    aistudio_models = "/home/aistudio/data/models/34288/thangka/models"
    if os.path.exists(aistudio_models):
        print(f"📋 从AI Studio数据目录复制模型: {aistudio_models}")
        success, _ = run_command(f"cp -r {aistudio_models}/* {model_dir}/", timeout=300)
        if success:
            print("✅ 模型文件复制成功")
            return True
        else:
            print("⚠️ 从数据目录复制失败，尝试Git下载")
    
    # 克隆模型仓库
    repo_url = "https://e5896710865571a725e5f3c516cdb55e99b6ea90@git.aistudio.baidu.com/Wangchuk/thangka1376.git"
    temp_dir = "/home/aistudio/work/temp_models"
    
    print(f"📥 克隆模型仓库到: {temp_dir}")
    
    # 删除临时目录（如果存在）
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # 克隆仓库（带重试机制）
    max_retries = 3
    for attempt in range(max_retries):
        print(f"📥 克隆模型仓库 (尝试 {attempt + 1}/{max_retries})...")
        success, result = run_command(f"git clone {repo_url} {temp_dir}", timeout=600)
        if success:
            print("✅ 模型仓库克隆成功")
            break
        else:
            print(f"❌ 克隆失败 (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                print("⏳ 等待5秒后重试...")
                time.sleep(5)
                # 清理可能的部分下载
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            else:
                print("❌ 模型仓库克隆失败，已达到最大重试次数")
                return False
    
    # 复制模型文件
    source_models = os.path.join(temp_dir, "models")
    if os.path.exists(source_models):
        print(f"📋 复制模型文件从 {source_models} 到 {model_dir}")
        success, _ = run_command(f"cp -r {source_models}/* {model_dir}/", timeout=1200)
        if success:
            print("✅ 模型文件复制成功")
        else:
            print("❌ 模型文件复制失败")
            return False
    else:
        print("❌ 源模型目录不存在")
        return False
    
    # 清理临时目录
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print("🧹 清理临时文件完成")
    
    print("🎉 模型下载完成！")
    return True

def setup_django_environment():
    """设置Django环境"""
    print("🔧 设置Django环境...")
    
    # 检查关键依赖
    if not check_critical_dependencies():
        print("⚠️ 部分关键依赖缺失，但继续启动...")
    
    # 设置环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    
    # 设置PaddlePaddle环境变量
    os.environ['PADDLE_FRAMEWORK'] = 'paddle'
    os.environ['PADDLE_DEVICE'] = 'gpu' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu'
    
    print("✅ Django环境设置完成")

def main():
    """主函数 -启动所有功能"""
    print("🚀 AI Studio 启动脚本开始执行...")
    print("=" * 50)
    
    # 检查是否在AI Studio环境中
    if not os.path.exists('/home/aistudio'):
        print("⚠️ 不在AI Studio环境中，跳过环境设置")
        setup_django_environment()
        return
    
    # 快速启动模式 - 优先启动Django，后台处理环境
    print("⚡ 快速启动模式：优先启动Django服务器")
    
    # 步骤1: 设置Django环境（必须）
    print("\n📋 步骤1: 设置Django环境")
    print("-" * 30)
    setup_django_environment()
    
    # 步骤2: 设置Python环境
    print("\n📋 步骤2: 设置Python环境")
    print("-" * 30)
    setup_python_environment()
    
    # 步骤3: 安装依赖
    print("\n📋 步骤3: 安装依赖")
    print("-" * 30)
    install_dependencies()
    
    # 步骤4: 下载模型（后台进行）
    print("\n📋 步骤4: 准备模型文件")
    print("-" * 30)
    if not download_models():
        print("⚠️ 模型下载失败，将在没有模型的情况下启动服务器")
        os.environ['SKIP_MODEL_LOADING'] = '1'
    
    print("\n🎉 环境设置完成！")
    print("=" * 50)

if __name__ == '__main__':
    # 执行环境设置
    main()
    
    # 启动Django服务器
    try:
        import django
        from django.core.management import execute_from_command_line
        
        print("🚀 启动Django服务器...")
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"❌ Django启动失败: {e}")
        sys.exit(1)



