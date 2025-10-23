#!/usr/bin/env python3
"""
唐卡修复大师MVP产品启动脚本
商业化产品，专注用户体验和唐卡互动
Developed by Wangchuk Mind
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """打印产品启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              🎨 唐卡修复大师 MVP产品 🎨                        ║
    ║                                                              ║
    ║        让AI守护千年唐卡艺术 - 商业化产品版本                    ║
    ║                                                              ║
    ║  ✨ 一键修复  🎨 文化互动  🤖 AI智能  📱 简单易用              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求...")
    
    # 检查Python版本
    if sys.version_info < (3, 9):
        print("❌ 需要Python 3.9或更高版本")
        return False
    
    # 检查必要的包
    required_packages = ['django', 'paddlepaddle', 'pillow', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少必要的包: {', '.join(missing_packages)}")
        print("请运行: pip install -r Django/requirements_paddle.txt")
        return False
    
    print("✅ 系统要求检查通过")
    return True

def setup_environment():
    """设置环境变量"""
    print("🔧 设置环境变量...")
    
    # 设置Django环境
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    
    # 设置PaddlePaddle环境
    os.environ['PADDLE_FRAMEWORK'] = 'paddle'
    os.environ['PADDLE_DEVICE'] = 'gpu' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu'
    
    # 设置MVP产品模式
    os.environ['MVP_MODE'] = 'true'
    os.environ['SIMPLIFIED_UI'] = 'true'
    
    print("✅ 环境变量设置完成")

def create_directories():
    """创建必要的目录"""
    print("📁 创建必要目录...")
    
    directories = [
        'Django/server/media/mvp_uploads',
        'Django/server/media/mvp_results',
        'Django/server/static/mvp',
        'client/build/mvp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ 创建目录: {directory}")

def start_backend(port=8000):
    """启动后端服务"""
    print("🚀 启动后端服务...")
    
    try:
        # 切换到Django目录
        os.chdir('Django')
        
        # 启动Django服务器
        cmd = [sys.executable, 'start_server.py', 'runserver', f'0.0.0.0:{port}']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务器启动
        time.sleep(3)
        
        if process.poll() is None:
            print(f"✅ 后端服务启动成功 (http://localhost:{port})")
            return process
        else:
            print("❌ 后端服务启动失败")
            return None
            
    except Exception as e:
        print(f"❌ 启动后端服务时出错: {e}")
        return None

def start_frontend(port=3000):
    """启动前端服务"""
    print("🎨 启动前端服务...")
    
    try:
        # 切换到client目录
        os.chdir('../client')
        
        # 检查是否已安装依赖
        if not os.path.exists('node_modules'):
            print("📦 安装前端依赖...")
            subprocess.run(['npm', 'install'], check=True)
        
        # 设置端口环境变量
        env = os.environ.copy()
        env['PORT'] = str(port)
        
        # 启动React开发服务器
        cmd = ['npm', 'start']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        
        # 等待服务器启动
        time.sleep(5)
        
        if process.poll() is None:
            print(f"✅ 前端服务启动成功 (http://localhost:{port})")
            return process
        else:
            print("❌ 前端服务启动失败")
            return None
            
    except Exception as e:
        print(f"❌ 启动前端服务时出错: {e}")
        return None

def show_product_info(frontend_port=3000, backend_port=8000):
    """显示产品信息"""
    print("\n" + "="*60)
    print("🎨 唐卡修复大师 MVP产品已启动！")
    print("="*60)
    print()
    print("🌐 访问地址:")
    print(f"  前端界面: http://localhost:{frontend_port}")
    print(f"  后端API:  http://localhost:{backend_port}")
    print(f"  API文档:  http://localhost:{backend_port}/api/mvp/")
    print()
    print("📱 产品功能:")
    print("  ✨ 一键修复 - 上传图片即可开始修复")
    print("  🎨 文化互动 - 学习唐卡文化知识")
    print("  🤖 AI智能 - 自动识别和修复")
    print("  📊 修复历史 - 查看修复记录")
    print()
    print("🔧 技术特性:")
    print("  • 简化的用户界面")
    print("  • 预设修复模式")
    print("  • 实时进度更新")
    print("  • 文化知识集成")
    print()
    print("📞 技术支持: Wangchuk Mind")
    print("="*60)

def main():
    """主函数"""
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='唐卡修复大师MVP产品启动脚本')
    parser.add_argument('--kiosk-mode', action='store_true', help='启动终端模式')
    parser.add_argument('--production', action='store_true', help='生产模式启动')
    parser.add_argument('--port', type=int, default=3000, help='前端端口')
    parser.add_argument('--api-port', type=int, default=8000, help='后端API端口')
    args = parser.parse_args()
    
    print_banner()
    
    # 检查系统要求
    if not check_requirements():
        sys.exit(1)
    
    # 设置环境
    setup_environment()
    
    # 设置生产模式
    if args.production:
        os.environ['NODE_ENV'] = 'production'
        os.environ['DJANGO_DEBUG'] = 'False'
        print("🏭 生产模式启动")
    
    # 设置终端模式
    if args.kiosk_mode:
        os.environ['KIOSK_MODE'] = 'true'
        os.environ['FULLSCREEN'] = 'true'
        print("🖥️ 终端模式启动")
    
    # 创建目录
    create_directories()
    
    # 启动后端
    backend_process = start_backend(args.api_port)
    if not backend_process:
        print("❌ 无法启动后端服务，请检查配置")
        sys.exit(1)
    
    # 启动前端
    frontend_process = start_frontend(args.port)
    if not frontend_process:
        print("❌ 无法启动前端服务，请检查配置")
        backend_process.terminate()
        sys.exit(1)
    
    # 显示产品信息
    show_product_info(args.port, args.api_port)
    
    try:
        # 保持服务运行
        print("\n🔄 服务正在运行中... (按 Ctrl+C 停止)")
        while True:
            time.sleep(1)
            
            # 检查进程状态
            if backend_process.poll() is not None:
                print("❌ 后端服务意外停止")
                break
                
            if frontend_process.poll() is not None:
                print("❌ 前端服务意外停止")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        
        # 停止进程
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        print("✅ 服务已停止")
        print("感谢使用唐卡修复大师！")

if __name__ == "__main__":
    main()
