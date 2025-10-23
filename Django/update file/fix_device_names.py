#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复设备名称问题 - wangchukMind
将gpu:0改为cuda:0
"""

import os

def fix_device_names():
    """修复diffusion_paddle.py中的设备名称"""
    print("🔧 修复设备名称问题...")
    
    file_path = "server/models/diffusion_paddle.py"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复设备名称
    old_device = "'gpu:0'"
    new_device = "'cuda:0'"
    
    if old_device in content:
        content = content.replace(old_device, new_device)
        print(f"✅ 已修复设备名称: {old_device} -> {new_device}")
    else:
        print("⚠️ 未找到需要修复的设备名称")
    
    # 保存修改后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 设备名称修复完成")
    return True

def main():
    """主函数"""
    print("🚀 开始修复设备名称问题...")
    
    if fix_device_names():
        print("\\n🎉 修复完成！")
        print("\\n🔧 现在需要重启Django服务器:")
        print("python start_server_aistudio.py")
    else:
        print("\\n❌ 修复失败")

if __name__ == "__main__":
    main()



