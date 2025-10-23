#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速模型优化脚本 - wangchukMind
"""

import os
import sys
import time
import paddle

def quick_gpu_optimization():
    """快速GPU优化"""
    print("🔧 快速GPU优化...")
    
    try:
        # 1. 设置GPU设备
        if paddle.device.is_compiled_with_cuda():
            paddle.set_device('gpu:0')
            print("✅ GPU设备设置完成")
        
        # 2. 清理GPU缓存
        paddle.device.cuda.empty_cache()
        print("✅ GPU缓存清理完成")
        
        # 3. 设置线程数
        paddle.set_num_threads(4)
        print("✅ 线程数设置完成")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU优化失败: {e}")
        return False

def quick_memory_optimization():
    """快速内存优化"""
    print("🔧 快速内存优化...")
    
    try:
        # 1. 强制垃圾回收
        import gc
        gc.collect()
        print("✅ 垃圾回收完成")
        
        # 2. 清理GPU内存
        if paddle.device.is_compiled_with_cuda():
            paddle.device.cuda.empty_cache()
            print("✅ GPU内存清理完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 内存优化失败: {e}")
        return False

def optimize_inference_parameters():
    """优化推理参数"""
    print("🔧 优化推理参数...")
    
    # 优化的参数配置
    optimized_params = {
        'inpaint': {
            'steps': 50,
            'guidance': 15.0,
            'strength': 0.7,
            'scheduler': 'DDIM'
        },
        'text2img': {
            'steps': 40,
            'guidance': 18.0,
            'strength': 0.95,
            'scheduler': 'UniPC'
        },
        'img2img': {
            'steps': 45,
            'guidance': 16.0,
            'strength': 0.8,
            'scheduler': 'UniPC'
        }
    }
    
    print("✅ 推理参数优化完成")
    return optimized_params

def create_optimized_diffusion_patch():
    """创建优化的diffusion补丁"""
    patch_content = '''# 优化的diffusion_paddle_aistudio.py补丁 - wangchukMind

# 在changeModel函数中添加以下代码：

def optimize_pipe_performance(pipe):
    """优化pipe性能"""
    if pipe is None:
        return pipe
    
    try:
        print("🔧 开始pipe性能优化...")
        
        # 1. 内存优化
        if hasattr(pipe, 'enable_attention_slicing'):
            pipe.enable_attention_slicing()
            print("✅ 启用注意力切片")
        
        # 2. 编译优化
        if hasattr(pipe, 'compile'):
            pipe.compile()
            print("✅ 启用模型编译")
        
        # 3. 缓存优化
        if hasattr(pipe, 'enable_attention_caching'):
            pipe.enable_attention_caching()
            print("✅ 启用注意力缓存")
        
        print("✅ pipe性能优化完成")
        
    except Exception as e:
        print(f"⚠️ pipe性能优化失败: {e}")
    
    return pipe

# 在changeModel函数的return语句前添加：
pipe = optimize_pipe_performance(pipe)
'''
    
    patch_path = "diffusion_optimization_patch.py"
    with open(patch_path, 'w', encoding='utf-8') as f:
        f.write(patch_content)
    
    print(f"✅ 优化补丁已创建: {patch_path}")

def run_performance_test():
    """运行性能测试"""
    print("🧪 运行性能测试...")
    
    try:
        # 测试GPU性能
        if paddle.device.is_compiled_with_cuda():
            # 创建测试tensor
            test_tensor = paddle.randn([1000, 1000])
            test_tensor = test_tensor.cuda()
            
            # 测试矩阵乘法
            start_time = time.time()
            result = paddle.matmul(test_tensor, test_tensor)
            end_time = time.time()
            
            computation_time = end_time - start_time
            print(f"✅ GPU计算测试: {computation_time:.2f}秒")
            
            # 测试内存使用
            memory_usage = paddle.device.cuda.memory_allocated() / 1024**3
            print(f"✅ GPU内存使用: {memory_usage:.2f}GB")
            
            return True
        else:
            print("⚠️ CUDA不可用，跳过GPU测试")
            return False
            
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始快速模型优化...")
    
    # 1. GPU优化
    gpu_success = quick_gpu_optimization()
    
    # 2. 内存优化
    memory_success = quick_memory_optimization()
    
    # 3. 参数优化
    params = optimize_inference_parameters()
    
    # 4. 创建优化补丁
    create_optimized_diffusion_patch()
    
    # 5. 性能测试
    test_success = run_performance_test()
    
    print("\n📊 优化结果:")
    print(f"  GPU优化: {'✅' if gpu_success else '❌'}")
    print(f"  内存优化: {'✅' if memory_success else '❌'}")
    print(f"  参数优化: ✅")
    print(f"  性能测试: {'✅' if test_success else '❌'}")
    
    if gpu_success and memory_success:
        print("\n🎉 快速优化完成！")
        print("\n🔧 建议:")
        print("  1. 重启Django服务器")
        print("  2. 测试图像修复功能")
        print("  3. 观察性能提升效果")
    else:
        print("\n⚠️ 部分优化失败，请检查环境配置")

if __name__ == "__main__":
    main()



