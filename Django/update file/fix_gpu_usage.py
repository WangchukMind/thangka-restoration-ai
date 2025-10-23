#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复GPU使用问题 - wangchukMind
确保模型在推理时正确使用GPU
"""

import os
import sys
import paddle

def fix_gpu_usage():
    """修复GPU使用问题"""
    print("🔧 修复GPU使用问题...")
    
    # 1. 检查GPU状态
    print(f"🔍 GPU设备数量: {paddle.device.cuda.device_count()}")
    print(f"🔍 CUDA是否可用: {paddle.device.is_compiled_with_cuda()}")
    
    if paddle.device.is_compiled_with_cuda():
        # 2. 强制设置GPU设备
        paddle.set_device('gpu:0')
        print("✅ 强制设置GPU设备: gpu:0")
        
        # 3. 检查当前设备
        current_device = paddle.get_device()
        print(f"✅ 当前设备: {current_device}")
        
        # 4. 测试GPU计算
        try:
            # 创建一个简单的tensor在GPU上
            test_tensor = paddle.to_tensor([1.0, 2.0, 3.0], place='gpu:0')
            result = paddle.sum(test_tensor)
            print(f"✅ GPU计算测试成功: {result.numpy()}")
        except Exception as e:
            print(f"❌ GPU计算测试失败: {e}")
            return False
            
        # 5. 检查GPU内存
        try:
            gpu_memory = paddle.device.cuda.memory_allocated()
            gpu_memory_gb = gpu_memory / (1024**3)
            print(f"✅ GPU内存使用: {gpu_memory_gb:.2f} GB")
        except Exception as e:
            print(f"⚠️ 无法获取GPU内存信息: {e}")
            
        return True
    else:
        print("❌ CUDA不可用，无法使用GPU")
        return False

def fix_diffusion_paddle_gpu():
    """修复diffusion_paddle.py中的GPU使用问题"""
    print("🔧 修复diffusion_paddle.py中的GPU使用问题...")
    
    file_path = "server/models/diffusion_paddle.py"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复1: 确保pipe在GPU上
    gpu_fix_1 = '''    # 确保pipe在GPU上 - wangchukMind
    if pipe is not None and paddle.device.is_compiled_with_cuda():
        try:
            # 将pipe的所有组件移动到GPU
            if hasattr(pipe, 'unet') and pipe.unet is not None:
                pipe.unet.to('gpu:0')
                print("✅ UNet已移动到GPU")
            if hasattr(pipe, 'vae') and pipe.vae is not None:
                pipe.vae.to('gpu:0')
                print("✅ VAE已移动到GPU")
            if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
                pipe.text_encoder.to('gpu:0')
                print("✅ Text Encoder已移动到GPU")
            if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
                pipe.controlnet.to('gpu:0')
                print("✅ ControlNet已移动到GPU")
        except Exception as e:
            print(f"⚠️ 移动模型到GPU失败: {e}")
    
    # 强制设置GPU设备 - wangchukMind
    if paddle.device.is_compiled_with_cuda():
        paddle.set_device('gpu:0')
        print("✅ 强制设置GPU设备: gpu:0")'''
    
    # 在changeModel函数末尾添加GPU设置
    if "确保pipe在GPU上 - wangchukMind" not in content:
        # 找到changeModel函数的结尾
        change_model_end = content.find("    return pipe")
        if change_model_end != -1:
            # 在return pipe之前插入GPU设置
            new_content = content[:change_model_end] + gpu_fix_1 + "\n\n    " + content[change_model_end:]
            
            # 保存修改后的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ 已添加GPU设置到changeModel函数")
        else:
            print("⚠️ 未找到changeModel函数结尾")
    
    # 修复2: 在推理函数中强制使用GPU
    inference_fix = '''    # 强制使用GPU进行推理 - wangchukMind
    if paddle.device.is_compiled_with_cuda():
        paddle.set_device('gpu:0')
        print("🔧 推理前强制设置GPU设备: gpu:0")
        
        # 确保所有输入数据在GPU上
        if hasattr(pipe, 'unet') and pipe.unet is not None:
            pipe.unet.to('gpu:0')
        if hasattr(pipe, 'vae') and pipe.vae is not None:
            pipe.vae.to('gpu:0')
        if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
            pipe.text_encoder.to('gpu:0')
        if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
            pipe.controlnet.to('gpu:0')
    '''
    
    # 在inpaint函数中添加GPU设置
    if "强制使用GPU进行推理 - wangchukMind" not in content:
        inpaint_start = content.find("    if progress_callback:")
        if inpaint_start != -1:
            # 在progress_callback之前插入GPU设置
            new_content = content[:inpaint_start] + inference_fix + "\n    " + content[inpaint_start:]
            
            # 保存修改后的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ 已添加GPU设置到inpaint函数")
        else:
            print("⚠️ 未找到inpaint函数")
    
    return True

def create_gpu_test_script():
    """创建GPU测试脚本"""
    print("🔧 创建GPU测试脚本...")
    
    test_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU使用测试脚本 - wangchukMind
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
        # 创建大矩阵进行GPU计算
        size = 1000
        a = paddle.randn([size, size], place='gpu:0')
        b = paddle.randn([size, size], place='gpu:0')
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ GPU计算测试失败: {e}")
        return False

if __name__ == "__main__":
    test_gpu_usage()
'''
    
    with open("test_gpu_usage.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ GPU测试脚本已创建: test_gpu_usage.py")
    return True

def main():
    """主函数"""
    print("🚀 开始修复GPU使用问题...")
    
    # 1. 修复GPU使用
    if not fix_gpu_usage():
        print("❌ GPU使用修复失败")
        return False
    
    # 2. 修复diffusion_paddle.py
    if not fix_diffusion_paddle_gpu():
        print("❌ diffusion_paddle.py修复失败")
        return False
    
    # 3. 创建测试脚本
    if not create_gpu_test_script():
        print("❌ 测试脚本创建失败")
        return False
    
    print("\\n🎉 GPU使用问题修复完成！")
    print("\\n📋 修复内容:")
    print("1. ✅ 强制设置GPU设备")
    print("2. ✅ 确保模型组件在GPU上")
    print("3. ✅ 在推理时强制使用GPU")
    print("4. ✅ 创建GPU测试脚本")
    
    print("\\n🔧 使用方法:")
    print("1. 运行测试: python test_gpu_usage.py")
    print("2. 重启Django服务器")
    print("3. 进行图像修复测试")
    
    return True

if __name__ == "__main__":
    main()



