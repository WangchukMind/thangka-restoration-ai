#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
先进唐卡系统启动脚本 - wangchukMind
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path

def signal_handler(sig, frame):
    print('\n🛑 收到停止信号，正在关闭系统...')
    sys.exit(0)

def check_gpu():
    """检查GPU状态"""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU状态正常")
            return True
        else:
            print("⚠️ GPU状态异常")
            return False
    except Exception as e:
        print(f"❌ GPU检查失败: {e}")
        return False

def check_dependencies():
    """检查依赖"""
    try:
        import paddle
        import torch
        import diffusers
        print("✅ 核心依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 依赖检查失败: {e}")
        return False

def start_system():
    """启动系统"""
    try:
        print("🚀 启动先进唐卡系统...")
        
        # 检查GPU
        if not check_gpu():
            print("⚠️ GPU不可用，将使用CPU模式")
        
        # 检查依赖
        if not check_dependencies():
            print("❌ 依赖检查失败，请安装所需依赖")
            return False
        
        # 导入并启动系统
        from advanced_thangka_models import AdvancedThangkaSystem
        
        system = AdvancedThangkaSystem()
        if system.initialize():
            print("✅ 系统启动成功")
            
            # 保持运行
            while True:
                time.sleep(1)
        else:
            print("❌ 系统启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        return False

if __name__ == "__main__":
    # 设置信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动系统
    start_system()
