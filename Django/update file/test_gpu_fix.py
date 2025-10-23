#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GPU修复效果 - wangchukMind
"""

import paddle

def test_gpu_setup():
    """测试GPU设置"""
    print("🔍 测试GPU设置...")
    
    # 1. 检查GPU状态
    print(f"GPU设备数量: {paddle.device.cuda.device_count()}")
    print(f"CUDA是否可用: {paddle.device.is_compiled_with_cuda()}")
    
    if not paddle.device.is_compiled_with_cuda():
        print("❌ CUDA不可用")
        return False
    
    # 2. 测试设备设置
    try:
        paddle.set_device('gpu:0')
        print("✅ paddle.set_device('gpu:0') 成功")
    except Exception as e:
        print(f"❌ paddle.set_device('gpu:0') 失败: {e}")
        return False
    
    # 3. 测试tensor创建
    try:
        # 创建tensor在GPU上
        a = paddle.randn([100, 100])
        a = a.cuda()
        print("✅ tensor.cuda() 成功")
    except Exception as e:
        print(f"❌ tensor.cuda() 失败: {e}")
        return False
    
    # 4. 测试计算
    try:
        b = paddle.randn([100, 100]).cuda()
        c = paddle.matmul(a, b)
        print("✅ GPU计算成功")
    except Exception as e:
        print(f"❌ GPU计算失败: {e}")
        return False
    
    print("🎉 GPU设置测试通过！")
    return True

def main():
    """主函数"""
    print("🚀 开始测试GPU修复效果...")
    
    if test_gpu_setup():
        print("\\n✅ 所有测试通过！")
        print("\\n🔧 现在可以重启Django服务器:")
        print("python start_server_aistudio.py")
    else:
        print("\\n❌ 测试失败！")

if __name__ == "__main__":
    main()



