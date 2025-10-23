#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU使用测试脚本 - wangchukMind (修复版)
测试GPU计算性能
"""

import paddle
import time
import numpy as np

def test_gpu_usage():
    """测试GPU使用情况"""
    print("🔍 开始GPU使用测试...")
    
    # 1. 检查GPU状态
    print(f"GPU设备数量: {paddle.device.cuda.device_count()}")
    print(f"CUDA是否可用: {paddle.device.is_compiled_with_cuda()}")
    
    if not paddle.device.is_compiled_with_cuda():
        print("❌ CUDA不可用")
        return False
    
    # 2. 设置GPU设备
    paddle.set_device('gpu:0')
    print(f"当前设备: {paddle.get_device()}")
    
    # 3. 测试GPU计算
    print("\\n🧪 测试GPU计算...")
    try:
        # 创建大矩阵进行GPU计算 - 修复PaddlePaddle API
        size = 1000
        
        # 方法1: 先创建tensor再移动到GPU
        a = paddle.randn([size, size])
        b = paddle.randn([size, size])
        
        # 移动到GPU
        a = a.cuda()
        b = b.cuda()
        
        start_time = time.time()
        c = paddle.matmul(a, b)
        end_time = time.time()
        
        print(f"✅ GPU矩阵乘法测试成功")
        print(f"   矩阵大小: {size}x{size}")
        print(f"   计算时间: {end_time - start_time:.3f}秒")
        print(f"   结果形状: {c.shape}")
        
        # 4. 检查GPU内存使用
        gpu_memory = paddle.device.cuda.memory_allocated()
        gpu_memory_gb = gpu_memory / (1024**3)
        print(f"✅ GPU内存使用: {gpu_memory_gb:.2f} GB")
        
        # 5. 测试更复杂的GPU计算
        print("\\n🧪 测试复杂GPU计算...")
        d = paddle.randn([size, size]).cuda()
        e = paddle.randn([size, size]).cuda()
        
        start_time = time.time()
        f = paddle.matmul(paddle.matmul(a, b), paddle.matmul(d, e))
        end_time = time.time()
        
        print(f"✅ 复杂GPU计算测试成功")
        print(f"   计算时间: {end_time - start_time:.3f}秒")
        print(f"   结果形状: {f.shape}")
        
        # 6. 最终GPU内存检查
        final_gpu_memory = paddle.device.cuda.memory_allocated()
        final_gpu_memory_gb = final_gpu_memory / (1024**3)
        print(f"✅ 最终GPU内存使用: {final_gpu_memory_gb:.2f} GB")
        
        # 7. 测试GPU性能基准
        print("\\n🧪 测试GPU性能基准...")
        sizes = [500, 1000, 2000]
        for test_size in sizes:
            try:
                test_a = paddle.randn([test_size, test_size]).cuda()
                test_b = paddle.randn([test_size, test_size]).cuda()
                
                start_time = time.time()
                test_c = paddle.matmul(test_a, test_b)
                end_time = time.time()
                
                print(f"   矩阵 {test_size}x{test_size}: {end_time - start_time:.3f}秒")
                
                # 清理内存
                del test_a, test_b, test_c
                paddle.device.cuda.empty_cache()
                
            except Exception as e:
                print(f"   矩阵 {test_size}x{test_size}: 失败 - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU计算测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gpu_memory():
    """测试GPU内存管理"""
    print("\\n🧪 测试GPU内存管理...")
    
    try:
        # 测试内存分配
        initial_memory = paddle.device.cuda.memory_allocated()
        print(f"初始GPU内存: {initial_memory / (1024**2):.2f} MB")
        
        # 分配大块内存
        large_tensor = paddle.randn([2000, 2000]).cuda()
        after_allocation = paddle.device.cuda.memory_allocated()
        print(f"分配后GPU内存: {after_allocation / (1024**2):.2f} MB")
        print(f"内存增长: {(after_allocation - initial_memory) / (1024**2):.2f} MB")
        
        # 清理内存
        del large_tensor
        paddle.device.cuda.empty_cache()
        
        after_cleanup = paddle.device.cuda.memory_allocated()
        print(f"清理后GPU内存: {after_cleanup / (1024**2):.2f} MB")
        print(f"内存释放: {(after_allocation - after_cleanup) / (1024**2):.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU内存测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始GPU使用测试...")
    
    # 基本GPU测试
    if test_gpu_usage():
        print("\\n✅ 基本GPU测试通过")
    else:
        print("\\n❌ 基本GPU测试失败")
    
    # GPU内存测试
    if test_gpu_memory():
        print("\\n✅ GPU内存测试通过")
    else:
        print("\\n❌ GPU内存测试失败")
    
    print("\\n🎉 GPU测试完成！")



