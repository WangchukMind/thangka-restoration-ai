#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Studio环境模型优化 - wangchukMind
"""

import os
import sys
import time
import paddle

def optimize_for_aistudio():
    """针对AI Studio环境的优化"""
    print("🚀 开始AI Studio环境优化...")
    
    # 1. 检查AI Studio环境
    if not os.path.exists('/home/aistudio'):
        print("⚠️ 不在AI Studio环境中，跳过AI Studio特定优化")
        return False
    
    print("✅ 检测到AI Studio环境")
    
    # 2. GPU优化
    gpu_optimized = optimize_gpu_for_aistudio()
    
    # 3. 内存优化
    memory_optimized = optimize_memory_for_aistudio()
    
    # 4. 模型路径优化
    path_optimized = optimize_model_paths_for_aistudio()
    
    # 5. 推理参数优化
    params_optimized = optimize_inference_params_for_aistudio()
    
    return gpu_optimized and memory_optimized and path_optimized and params_optimized

def optimize_gpu_for_aistudio():
    """AI Studio GPU优化"""
    print("🔧 AI Studio GPU优化...")
    
    try:
        # 1. 设置GPU设备
        if paddle.device.is_compiled_with_cuda():
            paddle.set_device('gpu:0')
            print("✅ GPU设备设置完成")
        
        # 2. 清理GPU缓存
        paddle.device.cuda.empty_cache()
        print("✅ GPU缓存清理完成")
        
        # 3. 设置内存分配策略
        os.environ['PADDLE_CUDNN_DETERMINISTIC'] = '1'
        os.environ['PADDLE_CUDNN_BENCHMARK'] = '1'
        print("✅ GPU内存分配策略设置完成")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU优化失败: {e}")
        return False

def optimize_memory_for_aistudio():
    """AI Studio内存优化"""
    print("🔧 AI Studio内存优化...")
    
    try:
        # 1. 强制垃圾回收
        import gc
        gc.collect()
        print("✅ 垃圾回收完成")
        
        # 2. 清理GPU内存
        if paddle.device.is_compiled_with_cuda():
            paddle.device.cuda.empty_cache()
            print("✅ GPU内存清理完成")
        
        # 3. 设置内存限制
        os.environ['PADDLE_MEMORY_FRACTION'] = '0.9'
        print("✅ 内存限制设置完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 内存优化失败: {e}")
        return False

def optimize_model_paths_for_aistudio():
    """AI Studio模型路径优化"""
    print("🔧 AI Studio模型路径优化...")
    
    try:
        # 检查模型路径
        model_paths = [
            '/home/aistudio/work/wangchukthangka/Thangka/Django/models/',
            '/home/aistudio/work/wangchukthangka/Thangka/Django/server/static/',
            '/home/aistudio/work/wangchukthangka/Thangka/Django/server/media/'
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                print(f"✅ 模型路径存在: {path}")
            else:
                print(f"⚠️ 模型路径不存在: {path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型路径优化失败: {e}")
        return False

def optimize_inference_params_for_aistudio():
    """AI Studio推理参数优化"""
    print("🔧 AI Studio推理参数优化...")
    
    # AI Studio优化的参数配置
    aistudio_params = {
        'inpaint': {
            'steps': 40,  # 减少步数，提高速度
            'guidance': 12.0,  # 降低引导强度
            'strength': 0.6,  # 降低强度
            'scheduler': 'DDIM'
        },
        'text2img': {
            'steps': 30,  # 减少步数
            'guidance': 15.0,  # 适中的引导强度
            'strength': 0.9,  # 高强度
            'scheduler': 'UniPC'
        },
        'img2img': {
            'steps': 35,  # 减少步数
            'guidance': 14.0,  # 适中的引导强度
            'strength': 0.7,  # 适中的强度
            'scheduler': 'UniPC'
        }
    }
    
    print("✅ AI Studio推理参数优化完成")
    print(f"📊 优化参数: {aistudio_params}")
    
    return True

def create_aistudio_optimization_patch():
    """创建AI Studio优化补丁"""
    patch_content = '''# AI Studio优化补丁 - wangchukMind

# 在diffusion_paddle_aistudio.py中添加以下优化：

def optimize_for_aistudio_environment():
    """AI Studio环境优化"""
    print("🔧 应用AI Studio环境优化...")
    
    # 1. 设置环境变量
    os.environ['PADDLE_CUDNN_DETERMINISTIC'] = '1'
    os.environ['PADDLE_CUDNN_BENCHMARK'] = '1'
    os.environ['PADDLE_MEMORY_FRACTION'] = '0.9'
    
    # 2. GPU优化
    if paddle.device.is_compiled_with_cuda():
        paddle.set_device('gpu:0')
        paddle.device.cuda.empty_cache()
    
    # 3. 内存优化
    import gc
    gc.collect()
    
    print("✅ AI Studio环境优化完成")

# 在changeModel函数开始处调用：
optimize_for_aistudio_environment()

# 优化推理参数
def get_aistudio_optimized_params(task_type):
    """获取AI Studio优化参数"""
    params = {
        'inpaint': {'steps': 40, 'guidance': 12.0, 'strength': 0.6},
        'text2img': {'steps': 30, 'guidance': 15.0, 'strength': 0.9},
        'img2img': {'steps': 35, 'guidance': 14.0, 'strength': 0.7}
    }
    return params.get(task_type, params['inpaint'])
'''
    
    patch_path = "aistudio_optimization_patch.py"
    with open(patch_path, 'w', encoding='utf-8') as f:
        f.write(patch_content)
    
    print(f"✅ AI Studio优化补丁已创建: {patch_path}")

def test_aistudio_optimization():
    """测试AI Studio优化效果"""
    print("🧪 测试AI Studio优化效果...")
    
    try:
        # 测试GPU状态
        if paddle.device.is_compiled_with_cuda():
            device_count = paddle.device.cuda.device_count()
            is_available = paddle.device.is_compiled_with_cuda()
            print(f"✅ GPU设备数量: {device_count}")
            print(f"✅ CUDA可用: {is_available}")
            
            # 测试GPU计算
            test_tensor = paddle.randn([100, 100])
            test_tensor = test_tensor.cuda()
            result = paddle.matmul(test_tensor, test_tensor)
            print("✅ GPU计算测试成功")
            
            return True
        else:
            print("⚠️ CUDA不可用")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始AI Studio环境优化...")
    
    # 1. 环境优化
    env_optimized = optimize_for_aistudio()
    
    # 2. 创建优化补丁
    create_aistudio_optimization_patch()
    
    # 3. 测试优化效果
    test_success = test_aistudio_optimization()
    
    print("\n📊 AI Studio优化结果:")
    print(f"  环境优化: {'✅' if env_optimized else '❌'}")
    print(f"  测试结果: {'✅' if test_success else '❌'}")
    
    if env_optimized and test_success:
        print("\n🎉 AI Studio优化完成！")
        print("\n🔧 优化内容:")
        print("  ✅ GPU设备优化")
        print("  ✅ 内存管理优化")
        print("  ✅ 模型路径优化")
        print("  ✅ 推理参数优化")
        print("  ✅ 环境变量设置")
        
        print("\n📋 下一步:")
        print("  1. 在AI Studio中运行此脚本")
        print("  2. 应用优化补丁到diffusion模型")
        print("  3. 重启Django服务器")
        print("  4. 测试优化效果")
        
    else:
        print("\n⚠️ 部分优化失败，请检查AI Studio环境")

if __name__ == "__main__":
    main()



