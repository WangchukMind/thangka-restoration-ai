#!/usr/bin/env python3
"""
唐卡修复大师 - 数字终端部署脚本
用于在触摸屏终端上部署和运行产品
Developed by Wangchuk Mind
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def print_banner():
    """打印部署横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              🖥️ 唐卡修复大师 - 数字终端部署 🖥️                ║
    ║                                                              ║
    ║        现代化触摸屏终端，完美展示AI修复技术                    ║
    ║                                                              ║
    ║  🎨 大屏展示  📱 触摸交互  🎯 专业界面  🚀 一键部署            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_system_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求...")
    
    # 检查操作系统
    if sys.platform not in ['linux', 'darwin', 'win32']:
        print("❌ 不支持的操作系统")
        return False
    
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

def setup_kiosk_environment():
    """设置终端环境"""
    print("🔧 设置终端环境...")
    
    # 设置环境变量
    os.environ['KIOSK_MODE'] = 'true'
    os.environ['TOUCH_INTERFACE'] = 'true'
    os.environ['FULLSCREEN'] = 'true'
    os.environ['AUTO_START'] = 'true'
    
    # 创建终端配置
    kiosk_config = {
        'fullscreen': True,
        'touch_optimized': True,
        'auto_start': True,
        'display_mode': 'kiosk',
        'screen_resolution': '1920x1080',
        'touch_sensitivity': 'high',
        'ui_scale': 1.2
    }
    
    with open('kiosk_config.json', 'w', encoding='utf-8') as f:
        json.dump(kiosk_config, f, indent=2, ensure_ascii=False)
    
    print("✅ 终端环境设置完成")

def create_kiosk_startup_script():
    """创建终端启动脚本"""
    print("📝 创建终端启动脚本...")
    
    if sys.platform == 'win32':
        startup_script = """@echo off
title 唐卡修复大师 - 数字终端
cd /d "%~dp0"
python start_mvp_product.py --kiosk-mode
pause
"""
        with open('start_kiosk.bat', 'w', encoding='utf-8') as f:
            f.write(startup_script)
    else:
        startup_script = """#!/bin/bash
# 唐卡修复大师 - 数字终端启动脚本
cd "$(dirname "$0")"
python3 start_mvp_product.py --kiosk-mode
"""
        with open('start_kiosk.sh', 'w', encoding='utf-8') as f:
            f.write(startup_script)
        os.chmod('start_kiosk.sh', 0o755)
    
    print("✅ 启动脚本创建完成")

def create_kiosk_desktop_file():
    """创建桌面快捷方式（Linux）"""
    if sys.platform == 'linux':
        print("🖥️ 创建桌面快捷方式...")
        
        desktop_file = """[Desktop Entry]
Version=1.0
Type=Application
Name=唐卡修复大师
Comment=AI智能唐卡修复系统
Exec=python3 start_mvp_product.py --kiosk-mode
Icon=thangka-icon.png
Terminal=false
Categories=Graphics;Education;
StartupWMClass=唐卡修复大师
"""
        
        desktop_path = os.path.expanduser('~/.local/share/applications/thangka-repair.desktop')
        os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
        
        with open(desktop_path, 'w', encoding='utf-8') as f:
            f.write(desktop_file)
        
        print("✅ 桌面快捷方式创建完成")

def optimize_for_touch():
    """优化触摸体验"""
    print("👆 优化触摸体验...")
    
    # 创建触摸优化配置
    touch_config = {
        'min_touch_target': 44,  # 最小触摸目标尺寸
        'touch_feedback': True,  # 触摸反馈
        'gesture_support': True, # 手势支持
        'double_tap_zoom': True, # 双击缩放
        'swipe_navigation': True, # 滑动手势
        'haptic_feedback': False # 触觉反馈（需要硬件支持）
    }
    
    with open('touch_config.json', 'w', encoding='utf-8') as f:
        json.dump(touch_config, f, indent=2, ensure_ascii=False)
    
    print("✅ 触摸体验优化完成")

def create_fullscreen_launcher():
    """创建全屏启动器"""
    print("🖥️ 创建全屏启动器...")
    
    launcher_script = """#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from pathlib import Path

def launch_fullscreen():
    # 设置全屏环境
    os.environ['FULLSCREEN'] = 'true'
    os.environ['KIOSK_MODE'] = 'true'
    
    # 启动应用
    try:
        # 启动后端
        backend_process = subprocess.Popen([
            sys.executable, 'start_mvp_product.py', '--kiosk-mode'
        ])
        
        # 等待启动
        time.sleep(5)
        
        # 打开浏览器到全屏模式
        if sys.platform == 'win32':
            subprocess.run([
                'start', 'msedge', '--kiosk', '--fullscreen', 
                'http://localhost:3000'
            ], shell=True)
        elif sys.platform == 'darwin':
            subprocess.run([
                'open', '-a', 'Safari', '--args', '--kiosk',
                'http://localhost:3000'
            ])
        else:
            subprocess.run([
                'xdg-open', '--kiosk', 'http://localhost:3000'
            ])
        
        # 保持运行
        backend_process.wait()
        
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    launch_fullscreen()
"""
    
    with open('launch_fullscreen.py', 'w', encoding='utf-8') as f:
        f.write(launcher_script)
    
    os.chmod('launch_fullscreen.py', 0o755)
    print("✅ 全屏启动器创建完成")

def create_kiosk_readme():
    """创建终端使用说明"""
    print("📖 创建使用说明...")
    
    readme_content = """# 🖥️ 唐卡修复大师 - 数字终端使用说明

## 📋 终端特性

### 界面设计
- **现代化Metro风格**: 采用Windows 8/10的Metro风格设计
- **大色块布局**: 适合触摸屏操作的大按钮设计
- **响应式界面**: 自动适配不同尺寸的触摸屏
- **文化元素**: 融入藏传佛教传统色彩和符号

### 功能模块
1. **上传图片** 📷 - 支持拖拽上传唐卡图片
2. **修复模式** ⚙️ - 三种预设修复模式
3. **文化学习** 📚 - 唐卡文化知识展示
4. **我的作品** 🎨 - 修复作品展示
5. **修复历史** 📋 - 修复记录查看
6. **帮助中心** ❓ - 使用帮助和支持

## 🚀 启动方式

### 方式一：直接启动
```bash
python start_mvp_product.py --kiosk-mode
```

### 方式二：全屏启动
```bash
python launch_fullscreen.py
```

### 方式三：桌面快捷方式
- Windows: 双击 `start_kiosk.bat`
- Linux: 双击桌面图标或运行 `./start_kiosk.sh`

## ⚙️ 配置选项

### 终端配置 (kiosk_config.json)
```json
{
  "fullscreen": true,
  "touch_optimized": true,
  "auto_start": true,
  "display_mode": "kiosk",
  "screen_resolution": "1920x1080",
  "touch_sensitivity": "high",
  "ui_scale": 1.2
}
```

### 触摸配置 (touch_config.json)
```json
{
  "min_touch_target": 44,
  "touch_feedback": true,
  "gesture_support": true,
  "double_tap_zoom": true,
  "swipe_navigation": true,
  "haptic_feedback": false
}
```

## 🎯 使用场景

### 博物馆展示
- 文物修复过程展示
- 游客互动体验
- 文化教育传播

### 商场展示
- 产品技术演示
- 用户试用体验
- 品牌推广展示

### 教育机构
- 艺术教学辅助
- 学生实践体验
- 文化传承教育

## 🔧 技术规格

### 硬件要求
- **处理器**: Intel i5 或同等性能
- **内存**: 8GB RAM 或更多
- **存储**: 50GB 可用空间
- **显卡**: 支持OpenGL 3.3
- **触摸屏**: 支持多点触控

### 软件要求
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.9 或更高版本
- **浏览器**: Chrome 90+, Firefox 88+, Safari 14+
- **Node.js**: 16 或更高版本

## 📊 性能优化

### 启动优化
- 预加载关键资源
- 缓存静态文件
- 优化图片压缩

### 运行优化
- 内存使用监控
- CPU使用率控制
- 网络请求优化

### 触摸优化
- 响应时间 < 100ms
- 触摸目标 ≥ 44px
- 手势识别准确率 > 95%

## 🛠️ 故障排除

### 常见问题
1. **触摸不响应**: 检查触摸屏驱动
2. **界面显示异常**: 调整屏幕分辨率
3. **启动失败**: 检查Python环境
4. **网络连接**: 确保网络正常

### 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

## 📞 技术支持

- **开发者**: Wangchuk Mind
- **产品**: 唐卡修复大师数字终端
- **版本**: v1.0
- **更新**: 2024年1月

---

**让AI技术以最直观的方式展示唐卡修复的魅力！**
"""
    
    with open('KIOSK_README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 使用说明创建完成")

def main():
    """主函数"""
    print_banner()
    
    # 检查系统要求
    if not check_system_requirements():
        sys.exit(1)
    
    # 设置终端环境
    setup_kiosk_environment()
    
    # 创建启动脚本
    create_kiosk_startup_script()
    
    # 创建桌面快捷方式
    create_kiosk_desktop_file()
    
    # 优化触摸体验
    optimize_for_touch()
    
    # 创建全屏启动器
    create_fullscreen_launcher()
    
    # 创建使用说明
    create_kiosk_readme()
    
    print("\n" + "="*60)
    print("🎉 数字终端部署完成！")
    print("="*60)
    print()
    print("🚀 启动方式:")
    print("  1. 直接启动: python start_mvp_product.py --kiosk-mode")
    print("  2. 全屏启动: python launch_fullscreen.py")
    print("  3. 桌面快捷方式: 双击启动脚本")
    print()
    print("📱 访问地址:")
    print("  终端界面: http://localhost:3000")
    print("  后端API:  http://localhost:8000")
    print()
    print("📖 详细说明: 查看 KIOSK_README.md")
    print("="*60)

if __name__ == "__main__":
    main()
