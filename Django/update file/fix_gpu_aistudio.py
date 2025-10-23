#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复AI Studio环境中的GPU使用问题 - wangchukMind
确保模型在推理时正确使用GPU
"""

import os
import sys

def fix_diffusion_paddle_gpu_aistudio():
    """修复diffusion_paddle.py中的GPU使用问题 - AI Studio版本"""
    print("🔧 修复diffusion_paddle.py中的GPU使用问题 (AI Studio版本)...")
    
    file_path = "server/models/diffusion_paddle.py"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复1: 在changeModel函数末尾添加GPU设置
    gpu_fix_1 = '''    # 确保pipe在GPU上 - wangchukMind
    if pipe is not None and paddle.device.is_compiled_with_cuda():
        try:
            # 将pipe的所有组件移动到GPU - 修复设备名称
            if hasattr(pipe, 'unet') and pipe.unet is not None:
                pipe.unet.to('cuda:0')
                print("✅ UNet已移动到GPU")
            if hasattr(pipe, 'vae') and pipe.vae is not None:
                pipe.vae.to('cuda:0')
                print("✅ VAE已移动到GPU")
            if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
                pipe.text_encoder.to('cuda:0')
                print("✅ Text Encoder已移动到GPU")
            if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
                pipe.controlnet.to('cuda:0')
                print("✅ ControlNet已移动到GPU")
        except Exception as e:
            print(f"⚠️ 移动模型到GPU失败: {e}")
    
    # 强制设置GPU设备 - wangchukMind
    if paddle.device.is_compiled_with_cuda():
        paddle.set_device('cuda:0')
        print("✅ 强制设置GPU设备: gpu:0")'''
    
    # 检查是否已经添加了GPU设置
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
    else:
        print("✅ GPU设置已存在")
    
    # 修复2: 在推理函数中强制使用GPU
    inference_fix = '''    # 强制使用GPU进行推理 - wangchukMind
    if paddle.device.is_compiled_with_cuda():
        paddle.set_device('cuda:0')
        print("🔧 推理前强制设置GPU设备: gpu:0")
        
        # 确保所有输入数据在GPU上
        if hasattr(pipe, 'unet') and pipe.unet is not None:
            pipe.unet.to('cuda:0')
        if hasattr(pipe, 'vae') and pipe.vae is not None:
            pipe.vae.to('cuda:0')
        if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
            pipe.text_encoder.to('cuda:0')
        if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
            pipe.controlnet.to('cuda:0')
    '''
    
    # 检查是否已经添加了推理GPU设置
    if "强制使用GPU进行推理 - wangchukMind" not in content:
        # 在inpaint函数中添加GPU设置
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
    else:
        print("✅ 推理GPU设置已存在")
    
    # 修复3: 在text2img和img2img函数中也添加GPU设置
    text2img_fix = '''    # 强制使用GPU进行推理 - wangchukMind
    if paddle.device.is_compiled_with_cuda():
        paddle.set_device('cuda:0')
        print("🔧 text2img推理前强制设置GPU设备: gpu:0")
        
        # 确保所有输入数据在GPU上
        if hasattr(pipe, 'unet') and pipe.unet is not None:
            pipe.unet.to('cuda:0')
        if hasattr(pipe, 'vae') and pipe.vae is not None:
            pipe.vae.to('cuda:0')
        if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
            pipe.text_encoder.to('cuda:0')
        if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
            pipe.controlnet.to('cuda:0')
    '''
    
    # 在text2img函数中添加GPU设置
    if "text2img推理前强制设置GPU设备" not in content:
        text2img_start = content.find("    if CNImgName:")
        if text2img_start != -1:
            # 在CNImgName检查之前插入GPU设置
            new_content = content[:text2img_start] + text2img_fix + "\n    " + content[text2img_start:]
            
            # 保存修改后的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ 已添加GPU设置到text2img函数")
        else:
            print("⚠️ 未找到text2img函数")
    else:
        print("✅ text2img GPU设置已存在")
    
    # 修复4: 在img2img函数中也添加GPU设置
    img2img_fix = '''    # 强制使用GPU进行推理 - wangchukMind
    if paddle.device.is_compiled_with_cuda():
        paddle.set_device('cuda:0')
        print("🔧 img2img推理前强制设置GPU设备: gpu:0")
        
        # 确保所有输入数据在GPU上
        if hasattr(pipe, 'unet') and pipe.unet is not None:
            pipe.unet.to('cuda:0')
        if hasattr(pipe, 'vae') and pipe.vae is not None:
            pipe.vae.to('cuda:0')
        if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
            pipe.text_encoder.to('cuda:0')
        if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
            pipe.controlnet.to('cuda:0')
    '''
    
    # 在img2img函数中添加GPU设置
    if "img2img推理前强制设置GPU设备" not in content:
        img2img_start = content.find("    init_image = Image.open")
        if img2img_start != -1:
            # 在init_image之前插入GPU设置
            new_content = content[:img2img_start] + img2img_fix + "\n    " + content[img2img_start:]
            
            # 保存修改后的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ 已添加GPU设置到img2img函数")
        else:
            print("⚠️ 未找到img2img函数")
    else:
        print("✅ img2img GPU设置已存在")
    
    return True

def create_gpu_monitor_script():
    """创建GPU监控脚本"""
    print("🔧 创建GPU监控脚本...")
    
    monitor_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU使用监控脚本 - wangchukMind
实时监控GPU使用情况
"""

import paddle
import time
import subprocess
import os

def get_gpu_info():
    """获取GPU信息"""
    try:
        # 使用nvidia-smi获取GPU信息
        result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\\n')
            gpu_info = []
            for i, line in enumerate(lines):
                parts = line.split(', ')
                if len(parts) >= 4:
                    gpu_info.append({
                        'gpu_id': i,
                        'utilization': int(parts[0]),
                        'memory_used': int(parts[1]),
                        'memory_total': int(parts[2]),
                        'temperature': int(parts[3])
                    })
            return gpu_info
        else:
            return None
    except Exception as e:
        print(f"⚠️ 无法获取GPU信息: {e}")
        return None

def monitor_gpu():
    """监控GPU使用情况"""
    print("🔍 开始监控GPU使用情况...")
    print("按Ctrl+C停止监控\\n")
    
    try:
        while True:
            # 获取GPU信息
            gpu_info = get_gpu_info()
            if gpu_info:
                print("\\r" + " " * 100, end="")  # 清空当前行
                for gpu in gpu_info:
                    memory_percent = (gpu['memory_used'] / gpu['memory_total']) * 100
                    print(f"\\rGPU {gpu['gpu_id']}: 利用率 {gpu['utilization']:3d}% | 显存 {gpu['memory_used']:5d}MB/{gpu['memory_total']:5d}MB ({memory_percent:5.1f}%) | 温度 {gpu['temperature']:3d}°C", end="")
            else:
                print("\\r无法获取GPU信息", end="")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\\n\\n✅ 监控已停止")

if __name__ == "__main__":
    monitor_gpu()
'''
    
    with open("monitor_gpu.py", 'w', encoding='utf-8') as f:
        f.write(monitor_script)
    
    print("✅ GPU监控脚本已创建: monitor_gpu.py")
    return True

def create_gpu_test_script():
    """创建GPU测试脚本"""
    print("🔧 创建GPU测试脚本...")
    
    test_script = '''#!/usr/bin/env python3
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
    paddle.set_device('cuda:0')
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
        
        return True
        
    except Exception as e:
        print(f"❌ GPU计算测试失败: {e}")
        import traceback
        traceback.print_exc()
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
    print("🚀 开始修复AI Studio环境中的GPU使用问题...")
    
    # 1. 修复diffusion_paddle.py
    if not fix_diffusion_paddle_gpu_aistudio():
        print("❌ diffusion_paddle.py修复失败")
        return False
    
    # 2. 创建监控脚本
    if not create_gpu_monitor_script():
        print("❌ 监控脚本创建失败")
        return False
    
    # 3. 创建测试脚本
    if not create_gpu_test_script():
        print("❌ 测试脚本创建失败")
        return False
    
    print("\\n🎉 AI Studio GPU使用问题修复完成！")
    print("\\n📋 修复内容:")
    print("1. ✅ 在changeModel函数中添加GPU设置")
    print("2. ✅ 在inpaint函数中添加GPU设置")
    print("3. ✅ 在text2img函数中添加GPU设置")
    print("4. ✅ 在img2img函数中添加GPU设置")
    print("5. ✅ 创建GPU监控脚本")
    print("6. ✅ 创建GPU测试脚本")
    
    print("\\n🔧 使用方法:")
    print("1. 在AI Studio中运行: python fix_gpu_aistudio.py")
    print("2. 测试GPU: python test_gpu_usage.py")
    print("3. 监控GPU: python monitor_gpu.py")
    print("4. 重启Django服务器")
    print("5. 进行图像修复测试")
    
    return True

if __name__ == "__main__":
    main()
