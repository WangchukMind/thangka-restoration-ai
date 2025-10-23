#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复GPU测试脚本 - wangchukMind
"""

import os

def fix_test_gpu_script():
    """修复test_gpu_usage.py脚本"""
    print("🔧 修复GPU测试脚本...")
    
    # 检查文件是否存在
    if not os.path.exists("test_gpu_usage.py"):
        print("❌ test_gpu_usage.py 不存在")
        return False
    
    # 读取原文件
    with open("test_gpu_usage.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复randn()调用
    old_code = "        a = paddle.randn([size, size], place='gpu:0')\n        b = paddle.randn([size, size], place='gpu:0')"
    new_code = """        # 先创建tensor再移动到GPU
        a = paddle.randn([size, size])
        b = paddle.randn([size, size])
        
        # 移动到GPU
        a = a.cuda()
        b = b.cuda()"""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ 已修复randn()调用")
    else:
        print("⚠️ 未找到需要修复的randn()调用")
    
    # 添加更详细的错误处理
    error_handling = """        import traceback
        traceback.print_exc()"""
    
    if "traceback.print_exc()" not in content:
        content = content.replace("        return False", error_handling + "\n        return False")
        print("✅ 已添加详细错误处理")
    
    # 保存修复后的文件
    with open("test_gpu_usage.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ GPU测试脚本修复完成")
    return True

def main():
    """主函数"""
    print("🚀 开始修复GPU测试脚本...")
    
    if fix_test_gpu_script():
        print("\\n🎉 修复完成！")
        print("\\n🔧 现在可以运行:")
        print("python test_gpu_usage.py")
    else:
        print("\\n❌ 修复失败")

if __name__ == "__main__":
    main()
