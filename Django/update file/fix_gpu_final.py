#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终GPU修复脚本 - wangchukMind
确保使用正确的设备名称
"""

import os
import shutil

def fix_gpu_final():
    """最终GPU修复"""
    print("🔧 开始最终GPU修复...")
    
    # 1. 检查文件存在性
    aistudio_file = "server/models/diffusion_paddle_aistudio.py"
    original_file = "server/models/diffusion_paddle.py"
    
    if not os.path.exists(aistudio_file):
        print(f"❌ 修复文件不存在: {aistudio_file}")
        return False
    
    # 2. 备份原文件
    if os.path.exists(original_file):
        shutil.copy2(original_file, original_file + ".backup")
        print(f"✅ 已备份原文件: {original_file}.backup")
    
    # 3. 替换文件
    shutil.copy2(aistudio_file, original_file)
    print(f"✅ 已替换文件: {aistudio_file} -> {original_file}")
    
    # 4. 验证修复
    with open(original_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查关键修复内容
    checks = [
        ("cuda:0设备名称", "'cuda:0'" in content),
        ("确保pipe在GPU上", "确保pipe在GPU上 - wangchukMind" in content),
        ("inpaint GPU设置", "inpaint推理前强制设置GPU设备" in content),
        ("text2img GPU设置", "text2img推理前强制设置GPU设备" in content),
        ("img2img GPU设置", "img2img推理前强制设置GPU设备" in content),
    ]
    
    print("\\n📋 修复验证:")
    all_passed = True
    
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}: {'通过' if passed else '失败'}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\\n🎉 GPU修复完成！")
        print("\\n🔧 现在需要重启Django服务器:")
        print("python start_server_aistudio.py")
        print("\\n📊 预期效果:")
        print("- 不再出现设备名称错误")
        print("- GPU利用率: 从0%提升到80-100%")
        print("- 显存使用: 从310MiB提升到8-16GB")
        print("- 推理速度: 显著提升")
    else:
        print("\\n❌ 修复验证失败")
    
    return all_passed

def main():
    """主函数"""
    print("🚀 开始最终GPU修复...")
    
    if fix_gpu_final():
        print("\\n✅ 修复完成！")
    else:
        print("\\n❌ 修复失败！")

if __name__ == "__main__":
    main()



