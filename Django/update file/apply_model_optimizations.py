#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用模型优化到现有代码 - wangchukMind
"""

import os
import sys
import shutil
from datetime import datetime

def backup_original_file(file_path):
    """备份原始文件"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"✅ 已备份原始文件: {backup_path}")
        return backup_path
    return None

def apply_optimizations_to_diffusion_model():
    """应用优化到diffusion_paddle_aistudio.py"""
    
    file_path = "server/models/diffusion_paddle_aistudio.py"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 备份原始文件
    backup_path = backup_original_file(file_path)
    
    try:
        # 读取原始文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 应用优化1: 添加优化器导入
        optimization_import = """
# 模型优化器导入 - wangchukMind
try:
    from .optimize_model_performance import ModelOptimizer, optimize_model_comprehensive
    OPTIMIZATION_AVAILABLE = True
    print("✅ 模型优化器已加载")
except ImportError as e:
    print(f"⚠️ 模型优化器导入失败: {e}")
    OPTIMIZATION_AVAILABLE = False
"""
        
        # 在文件开头添加优化器导入
        if "from .optimize_model_performance import" not in content:
            content = content.replace(
                "import os\nimport subprocess",
                f"import os\nimport subprocess{optimization_import}"
            )
        
        # 应用优化2: 在changeModel函数中添加优化
        optimization_code = """
    # 应用模型优化 - wangchukMind
    if OPTIMIZATION_AVAILABLE and pipe is not None:
        try:
            print("🔧 应用模型优化...")
            optimizer = ModelOptimizer()
            
            # 内存优化
            optimizer.optimize_memory_usage(pipe)
            
            # GPU优化
            optimizer.optimize_gpu_usage()
            
            # 推理速度优化
            optimizer.optimize_inference_speed(pipe)
            
            print("✅ 模型优化完成")
        except Exception as e:
            print(f"⚠️ 模型优化失败: {e}")
"""
        
        # 在changeModel函数的return语句前添加优化代码
        if "应用模型优化" not in content:
            content = content.replace(
                "    return pipe",
                f"{optimization_code}\n    return pipe"
            )
        
        # 应用优化3: 优化参数获取函数
        optimized_params_function = """
def get_optimized_parameters(task_type, image_size=(512, 512), complexity='balanced'):
    \"\"\"获取优化参数 - wangchukMind\"\"\"
    if OPTIMIZATION_AVAILABLE:
        try:
            optimizer = ModelOptimizer()
            return optimizer.get_optimal_parameters(task_type, image_size, complexity)
        except Exception as e:
            print(f"⚠️ 获取优化参数失败: {e}")
    
    # 默认参数
    return {
        'steps': 50,
        'guidance': 15.0,
        'strength': 0.7
    }
"""
        
        # 在文件末尾添加优化参数函数
        if "def get_optimized_parameters" not in content:
            content += f"\n{optimized_params_function}"
        
        # 应用优化4: 在推理函数中使用优化参数
        # 替换inpaint函数中的参数优化部分
        old_inpaint_params = """    # 优化推理参数以提升质量 - 增加步数让用户看到更多中间结果
    optimized_steps = max(60, min(steps * 2, 120))  # 60-120步，让推理过程更长
    optimized_guidance = max(12.0, min(guidance * 1.5, 20.0))  # 12-20
    # 降低strength上限，确保有足够去噪步数，避免出现 steps = 0 的错误
    optimized_strength = max(0.65, min(strength, 0.75))  # 调整为0.65-0.75"""
        
        new_inpaint_params = """    # 使用优化参数 - wangchukMind
    if OPTIMIZATION_AVAILABLE:
        try:
            # 获取优化参数
            image_size = (512, 512)  # 可以根据实际图像大小调整
            complexity = 'balanced'  # 可以根据任务复杂度调整
            optimized_params = get_optimized_parameters('inpaint', image_size, complexity)
            
            optimized_steps = optimized_params['steps']
            optimized_guidance = optimized_params['guidance']
            optimized_strength = optimized_params['strength']
            
            print(f"🎯 使用优化参数: steps={optimized_steps}, guidance={optimized_guidance}, strength={optimized_strength}")
        except Exception as e:
            print(f"⚠️ 获取优化参数失败，使用默认参数: {e}")
            # 回退到默认参数
            optimized_steps = max(60, min(steps * 2, 120))
            optimized_guidance = max(12.0, min(guidance * 1.5, 20.0))
            optimized_strength = max(0.65, min(strength, 0.75))
    else:
        # 默认参数优化
        optimized_steps = max(60, min(steps * 2, 120))
        optimized_guidance = max(12.0, min(guidance * 1.5, 20.0))
        optimized_strength = max(0.65, min(strength, 0.75))"""
        
        content = content.replace(old_inpaint_params, new_inpaint_params)
        
        # 应用优化5: 添加性能监控
        performance_monitoring = """
    # 性能监控 - wangchukMind
    start_time = time.time()
    if OPTIMIZATION_AVAILABLE:
        try:
            optimizer = ModelOptimizer()
        except:
            optimizer = None
    else:
        optimizer = None
"""
        
        # 在inpaint函数开始处添加性能监控
        if "性能监控" not in content:
            content = content.replace(
                "    # 确保参数类型正确",
                f"{performance_monitoring}\n    # 确保参数类型正确"
            )
        
        # 应用优化6: 添加性能记录
        performance_logging = """
    # 记录性能指标 - wangchukMind
    if optimizer is not None:
        try:
            end_time = time.time()
            inference_time = end_time - start_time
            
            # 估算质量分数（可以根据实际需求调整）
            quality_score = min(1.0, optimized_steps / 100.0)
            
            # 估算内存使用（可以根据实际需求调整）
            memory_usage = 8.0  # GB
            
            optimizer.log_performance('inpaint', inference_time, quality_score, memory_usage)
        except Exception as e:
            print(f"⚠️ 性能记录失败: {e}")
"""
        
        # 在inpaint函数结束前添加性能记录
        if "记录性能指标" not in content:
            content = content.replace(
                "    print(f\"✅ 实际保存的文件名: {actual_filename}\")",
                f"    print(f\"✅ 实际保存的文件名: {actual_filename}\")\n{performance_logging}"
            )
        
        # 写入优化后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 模型优化应用成功！")
        print(f"📁 原始文件已备份到: {backup_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 应用优化失败: {e}")
        # 恢复原始文件
        if backup_path and os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            print("🔄 已恢复原始文件")
        return False

def create_optimization_config():
    """创建优化配置文件"""
    config_content = """# 模型优化配置文件 - wangchukMind

# 内存优化配置
MEMORY_OPTIMIZATION = {
    'enable_attention_slicing': True,
    'enable_xformers_memory_attention': True,
    'enable_model_cpu_offload': False,  # 如果显存不足，设置为True
    'enable_sequential_cpu_offload': False
}

# GPU优化配置
GPU_OPTIMIZATION = {
    'device': 'gpu:0',
    'mixed_precision': True,
    'num_threads': 4,
    'memory_fraction': 0.9
}

# 推理参数优化配置
INFERENCE_OPTIMIZATION = {
    'inpaint': {
        'fast': {'steps': 30, 'guidance': 12.0, 'strength': 0.6},
        'balanced': {'steps': 50, 'guidance': 15.0, 'strength': 0.7},
        'high': {'steps': 80, 'guidance': 18.0, 'strength': 0.8}
    },
    'text2img': {
        'fast': {'steps': 20, 'guidance': 15.0, 'strength': 0.9},
        'balanced': {'steps': 40, 'guidance': 18.0, 'strength': 0.95},
        'high': {'steps': 60, 'guidance': 20.0, 'strength': 0.98}
    },
    'img2img': {
        'fast': {'steps': 25, 'guidance': 14.0, 'strength': 0.7},
        'balanced': {'steps': 45, 'guidance': 16.0, 'strength': 0.8},
        'high': {'steps': 70, 'guidance': 18.0, 'strength': 0.9}
    }
}

# 性能监控配置
PERFORMANCE_MONITORING = {
    'enable_logging': True,
    'target_speed': 30.0,  # 目标推理时间（秒）
    'target_quality': 0.8,  # 目标质量分数
    'max_memory_usage': 16.0  # 最大内存使用（GB）
}
"""
    
    config_path = "server/models/optimization_config.py"
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ 优化配置文件已创建: {config_path}")

def main():
    """主函数"""
    print("🚀 开始应用模型优化...")
    
    # 1. 应用优化到diffusion模型
    success = apply_optimizations_to_diffusion_model()
    
    if success:
        # 2. 创建优化配置文件
        create_optimization_config()
        
        print("\n🎉 模型优化应用完成！")
        print("\n📋 优化内容:")
        print("  ✅ 内存优化")
        print("  ✅ GPU优化")
        print("  ✅ 推理速度优化")
        print("  ✅ 参数优化")
        print("  ✅ 性能监控")
        print("  ✅ 配置文件")
        
        print("\n🔧 下一步:")
        print("  1. 重启Django服务器")
        print("  2. 测试优化效果")
        print("  3. 根据性能数据调整参数")
        
    else:
        print("❌ 模型优化应用失败！")

if __name__ == "__main__":
    main()



