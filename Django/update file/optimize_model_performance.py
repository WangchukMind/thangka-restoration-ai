#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐卡修复模型性能优化器 - wangchukMind
"""

import paddle
import time
import gc
import os
from typing import Dict, Any, Optional, Tuple
import numpy as np

class ModelOptimizer:
    """模型优化器"""
    
    def __init__(self):
        self.performance_history = []
        self.optimization_config = {
            'memory_optimization': True,
            'gpu_optimization': True,
            'inference_optimization': True,
            'quality_optimization': True
        }
    
    def optimize_memory_usage(self, pipe) -> bool:
        """优化内存使用"""
        try:
            print("🔧 开始内存优化...")
            
            # 1. 注意力切片
            if hasattr(pipe, 'enable_attention_slicing'):
                pipe.enable_attention_slicing()
                print("✅ 启用注意力切片")
            
            # 2. 内存高效注意力
            if hasattr(pipe, 'enable_xformers_memory_attention'):
                pipe.enable_xformers_memory_attention()
                print("✅ 启用Xformers内存注意力")
            else:
                print("⚠️ Xformers不可用，使用标准注意力")
            
            # 3. 模型卸载（如果显存不足）
            if hasattr(pipe, 'enable_model_cpu_offload'):
                pipe.enable_model_cpu_offload()
                print("✅ 启用模型CPU卸载")
            
            # 4. 清理GPU缓存
            if paddle.device.is_compiled_with_cuda():
                paddle.device.cuda.empty_cache()
                print("✅ 清理GPU缓存")
            
            return True
            
        except Exception as e:
            print(f"❌ 内存优化失败: {e}")
            return False
    
    def optimize_gpu_usage(self) -> bool:
        """优化GPU使用"""
        try:
            print("🔧 开始GPU优化...")
            
            # 1. 设置最优设备
            if paddle.device.is_compiled_with_cuda():
                paddle.set_device('gpu:0')
                print("✅ 设置GPU设备")
            
            # 2. 启用混合精度
            try:
                paddle.amp.auto_cast()
                print("✅ 启用混合精度")
            except:
                print("⚠️ 混合精度不可用")
            
            # 3. 设置最优线程数
            paddle.set_num_threads(4)
            print("✅ 设置线程数: 4")
            
            # 4. 优化内存分配
            paddle.device.cuda.empty_cache()
            print("✅ 优化内存分配")
            
            return True
            
        except Exception as e:
            print(f"❌ GPU优化失败: {e}")
            return False
    
    def get_optimal_parameters(self, task_type: str, image_size: Tuple[int, int], 
                             complexity: str = 'balanced') -> Dict[str, Any]:
        """获取最优参数"""
        
        # 基础参数配置
        base_configs = {
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
        
        # 根据图像大小调整参数
        width, height = image_size
        size_factor = (width * height) / (512 * 512)
        
        config = base_configs[task_type][complexity].copy()
        
        # 调整步数
        if size_factor > 1.5:  # 大图像
            config['steps'] = int(config['steps'] * 1.2)
        elif size_factor < 0.5:  # 小图像
            config['steps'] = int(config['steps'] * 0.8)
        
        # 调整引导强度
        if complexity == 'high':
            config['guidance'] = min(config['guidance'] * 1.1, 25.0)
        
        print(f"🎯 任务类型: {task_type}, 复杂度: {complexity}, 图像大小: {image_size}")
        print(f"📊 优化参数: {config}")
        
        return config
    
    def optimize_inference_speed(self, pipe) -> bool:
        """优化推理速度"""
        try:
            print("🔧 开始推理速度优化...")
            
            # 1. 编译优化
            if hasattr(pipe, 'compile'):
                pipe.compile()
                print("✅ 启用模型编译")
            
            # 2. 缓存优化
            if hasattr(pipe, 'enable_attention_caching'):
                pipe.enable_attention_caching()
                print("✅ 启用注意力缓存")
            
            # 3. 并行优化
            if hasattr(pipe, 'enable_sequential_cpu_offload'):
                pipe.enable_sequential_cpu_offload()
                print("✅ 启用顺序CPU卸载")
            
            return True
            
        except Exception as e:
            print(f"❌ 推理速度优化失败: {e}")
            return False
    
    def optimize_image_preprocessing(self, image, mask=None, task_type='inpaint'):
        """优化图像预处理"""
        try:
            print("🔧 开始图像预处理优化...")
            
            # 1. 图像增强
            if task_type == 'inpaint' and mask is not None:
                # 增强边缘检测
                image = self.enhance_edges(image)
                # 优化遮罩处理
                mask = self.optimize_mask_processing(mask)
            
            # 2. 颜色空间优化
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            print("✅ 图像预处理优化完成")
            return image, mask
            
        except Exception as e:
            print(f"❌ 图像预处理优化失败: {e}")
            return image, mask
    
    def enhance_edges(self, image):
        """增强边缘检测"""
        try:
            import cv2
            import numpy as np
            from PIL import Image, ImageFilter
            
            # 转换为numpy数组
            img_array = np.array(image)
            
            # 应用Canny边缘检测
            edges = cv2.Canny(img_array, 50, 150)
            
            # 增强边缘
            kernel = np.ones((3,3), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
            
            # 转换回PIL图像
            enhanced_image = Image.fromarray(edges)
            
            return enhanced_image
            
        except Exception as e:
            print(f"⚠️ 边缘增强失败: {e}")
            return image
    
    def optimize_mask_processing(self, mask):
        """优化遮罩处理"""
        try:
            import cv2
            import numpy as np
            from PIL import Image
            
            # 转换为numpy数组
            mask_array = np.array(mask)
            
            # 形态学操作
            kernel = np.ones((3,3), np.uint8)
            mask_array = cv2.morphologyEx(mask_array, cv2.MORPH_CLOSE, kernel)
            mask_array = cv2.morphologyEx(mask_array, cv2.MORPH_OPEN, kernel)
            
            # 转换回PIL图像
            optimized_mask = Image.fromarray(mask_array)
            
            return optimized_mask
            
        except Exception as e:
            print(f"⚠️ 遮罩优化失败: {e}")
            return mask
    
    def optimize_post_processing(self, output_image, original_image=None):
        """优化后处理"""
        try:
            print("🔧 开始后处理优化...")
            
            # 1. 颜色匹配
            if original_image is not None:
                output_image = self.match_colors(output_image, original_image)
            
            # 2. 细节增强
            output_image = self.enhance_details(output_image)
            
            # 3. 噪声减少
            output_image = self.reduce_noise(output_image)
            
            print("✅ 后处理优化完成")
            return output_image
            
        except Exception as e:
            print(f"❌ 后处理优化失败: {e}")
            return output_image
    
    def match_colors(self, output_image, original_image):
        """颜色匹配"""
        try:
            from PIL import Image, ImageOps
            
            # 使用直方图匹配
            matched_image = ImageOps.match_histogram(output_image, original_image)
            
            return matched_image
            
        except Exception as e:
            print(f"⚠️ 颜色匹配失败: {e}")
            return output_image
    
    def enhance_details(self, image):
        """细节增强"""
        try:
            from PIL import ImageFilter
            
            # 应用锐化滤镜
            enhanced_image = image.filter(ImageFilter.SHARPEN)
            
            return enhanced_image
            
        except Exception as e:
            print(f"⚠️ 细节增强失败: {e}")
            return image
    
    def reduce_noise(self, image):
        """噪声减少"""
        try:
            from PIL import ImageFilter
            
            # 应用降噪滤镜
            denoised_image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return denoised_image
            
        except Exception as e:
            print(f"⚠️ 噪声减少失败: {e}")
            return image
    
    def log_performance(self, task_type: str, speed: float, quality: float, 
                       memory_usage: float):
        """记录性能指标"""
        self.performance_history.append({
            'task_type': task_type,
            'speed': speed,
            'quality': quality,
            'memory_usage': memory_usage,
            'timestamp': time.time()
        })
        
        print(f"📊 性能记录: {task_type} - 速度: {speed:.2f}s, 质量: {quality:.2f}, 内存: {memory_usage:.2f}GB")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        if not self.performance_history:
            return {}
        
        # 按任务类型分组
        task_stats = {}
        for record in self.performance_history:
            task_type = record['task_type']
            if task_type not in task_stats:
                task_stats[task_type] = {
                    'speed': [],
                    'quality': [],
                    'memory_usage': []
                }
            
            task_stats[task_type]['speed'].append(record['speed'])
            task_stats[task_type]['quality'].append(record['quality'])
            task_stats[task_type]['memory_usage'].append(record['memory_usage'])
        
        # 计算平均值
        summary = {}
        for task_type, stats in task_stats.items():
            summary[task_type] = {
                'avg_speed': np.mean(stats['speed']),
                'avg_quality': np.mean(stats['quality']),
                'avg_memory': np.mean(stats['memory_usage']),
                'count': len(stats['speed'])
            }
        
        return summary
    
    def auto_tune_parameters(self, target_speed: float = 30.0, 
                           target_quality: float = 0.8) -> Dict[str, Any]:
        """自动调优参数"""
        if not self.performance_history:
            print("⚠️ 没有性能数据，无法自动调优")
            return {}
        
        summary = self.get_performance_summary()
        
        # 分析性能数据
        avg_speed = np.mean([stats['avg_speed'] for stats in summary.values()])
        avg_quality = np.mean([stats['avg_quality'] for stats in summary.values()])
        
        # 调整建议
        recommendations = {}
        
        if avg_speed > target_speed * 1.2:
            recommendations['reduce_steps'] = True
            recommendations['steps_factor'] = 0.8
        
        if avg_quality < target_quality * 0.9:
            recommendations['increase_steps'] = True
            recommendations['steps_factor'] = 1.2
        
        print(f"🎯 自动调优建议: {recommendations}")
        return recommendations

def optimize_model_comprehensive(pipe, task_type='inpaint', 
                               image_size=(512, 512), complexity='balanced'):
    """全面优化模型"""
    optimizer = ModelOptimizer()
    
    print("🚀 开始全面模型优化...")
    
    # 1. 内存优化
    optimizer.optimize_memory_usage(pipe)
    
    # 2. GPU优化
    optimizer.optimize_gpu_usage()
    
    # 3. 推理速度优化
    optimizer.optimize_inference_speed(pipe)
    
    # 4. 获取最优参数
    optimal_params = optimizer.get_optimal_parameters(task_type, image_size, complexity)
    
    print("✅ 全面模型优化完成！")
    
    return optimizer, optimal_params

if __name__ == "__main__":
    print("🔧 模型优化器测试...")
    
    # 测试优化器
    optimizer = ModelOptimizer()
    
    # 测试参数优化
    params = optimizer.get_optimal_parameters('inpaint', (512, 512), 'balanced')
    print(f"📊 优化参数: {params}")
    
    # 测试性能记录
    optimizer.log_performance('inpaint', 25.5, 0.85, 8.2)
    optimizer.log_performance('text2img', 15.3, 0.78, 6.1)
    
    # 获取性能摘要
    summary = optimizer.get_performance_summary()
    print(f"📈 性能摘要: {summary}")
    
    print("✅ 模型优化器测试完成！")



