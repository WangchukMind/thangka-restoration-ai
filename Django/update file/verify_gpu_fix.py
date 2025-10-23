#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证GPU修复效果 - wangchukMind
"""

import os

def verify_gpu_fix():
    """验证GPU修复是否已应用"""
    print("🔍 验证GPU修复效果...")
    
    file_path = "server/models/diffusion_paddle_aistudio.py"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查修复内容
    checks = [
        ("确保pipe在GPU上", "确保pipe在GPU上 - wangchukMind" in content),
        ("cuda:0设备名称", "'cuda:0'" in content),
        ("inpaint GPU设置", "inpaint推理前强制设置GPU设备" in content),
        ("text2img GPU设置", "text2img推理前强制设置GPU设备" in content),
        ("img2img GPU设置", "img2img推理前强制设置GPU设备" in content),
        ("UNet GPU移动", "pipe.unet.to('cuda:0')" in content),
        ("VAE GPU移动", "pipe.vae.to('cuda:0')" in content),
        ("Text Encoder GPU移动", "pipe.text_encoder.to('cuda:0')" in content),
        ("ControlNet GPU移动", "pipe.controlnet.to('cuda:0')" in content),
    ]
    
    print("\\n📋 修复检查结果:")
    all_passed = True
    
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}: {'通过' if passed else '失败'}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\\n🎉 所有GPU修复已成功应用！")
        print("\\n🔧 现在需要重启Django服务器:")
        print("python start_server_aistudio.py")
        print("\\n📊 预期效果:")
        print("- GPU利用率: 从0%提升到80-100%")
        print("- 显存使用: 从310MiB提升到8-16GB")
        print("- 推理速度: 显著提升")
    else:
        print("\\n❌ 部分修复未完成，请检查文件内容")
    
    return all_passed

def main():
    """主函数"""
    print("🚀 开始验证GPU修复效果...")
    
    if verify_gpu_fix():
        print("\\n✅ 验证完成！")
    else:
        print("\\n❌ 验证失败！")

if __name__ == "__main__":
    main()



