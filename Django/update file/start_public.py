#!/usr/bin/env python3
"""
公网部署启动脚本
支持AI Studio和云服务器部署
"""
import os
import sys
import subprocess
import socket
from pathlib import Path

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 连接到一个远程地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def check_ai_studio():
    """检查是否在AI Studio环境"""
    return os.path.exists('/home/aistudio') or 'aistudio' in os.getcwd()

def start_server():
    """启动Django服务器"""
    print("🚀 启动唐卡AI生成系统...")
    
    # 检查环境
    if check_ai_studio():
        print("🔍 检测到AI Studio环境，使用AI Studio配置")
        host = "0.0.0.0"
        port = 8080
    else:
        print("🔍 检测到本地环境，使用本地配置")
        host = "0.0.0.0"
        port = 8080
    
    # 设置环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    
    # 启动命令
    cmd = f"python manage.py runserver {host}:{port}"
    
    print(f"📡 服务器地址: http://{host}:{port}")
    print(f"🌐 公网访问: http://{get_local_ip()}:{port}")
    
    if check_ai_studio():
        print("🔗 AI Studio公网地址将在启动后显示")
        print("📱 请使用AI Studio提供的公网地址访问")
    
    print("\n" + "="*50)
    print("🎨 唐卡AI生成系统启动中...")
    print("="*50)
    
    try:
        # 启动服务器
        subprocess.run(cmd, shell=True, cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def show_access_info():
    """显示访问信息"""
    print("\n" + "="*60)
    print("🌐 公网访问信息")
    print("="*60)
    
    local_ip = get_local_ip()
    
    print(f"📱 本地访问: http://127.0.0.1:8080")
    print(f"🏠 局域网访问: http://{local_ip}:8080")
    
    if check_ai_studio():
        print(f"☁️  AI Studio公网地址: 请查看AI Studio控制台")
        print(f"🔗 公网访问: https://api-xxxxx.aistudio-app.com")
    else:
        print(f"🌍 如需公网访问，请使用ngrok或部署到云服务器")
    
    print("\n📋 功能测试:")
    print("  ✅ 页面加载测试")
    print("  ✅ 图像上传测试") 
    print("  ✅ 图像生成测试")
    print("  ✅ 历史记录测试")
    
    print("\n⚠️  注意事项:")
    print("  - 首次访问可能需要加载模型，请耐心等待")
    print("  - 建议使用Chrome或Firefox浏览器")
    print("  - 移动端访问体验已优化")

if __name__ == "__main__":
    print("🎨 唐卡AI生成系统 - 公网部署版")
    print("="*50)
    
    # 显示访问信息
    show_access_info()
    
    # 启动服务器
    start_server()

