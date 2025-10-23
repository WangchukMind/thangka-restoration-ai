#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐卡元素详细标注脚本 - wangchukMind
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
from pathlib import Path
import random

class ThangkaElementAnnotator:
    def __init__(self):
        self.element_templates = self.load_element_templates()
        
    def load_element_templates(self):
        return {
            "buddha": {
                "key_points": ["头部", "身体", "手臂", "腿部", "手势", "法衣"],
                "colors": ["金色", "红色", "蓝色"],
                "patterns": ["莲花座", "光环", "法轮"]
            },
            "bodhisattva": {
                "key_points": ["头部", "身体", "装饰", "法器", "姿态"],
                "colors": ["白色", "绿色", "黄色"],
                "patterns": ["珠宝装饰", "莲花", "云彩"]
            },
            "lotus": {
                "key_points": ["花瓣", "花蕊", "茎叶", "根部"],
                "colors": ["粉色", "白色", "绿色"],
                "patterns": ["花瓣纹理", "花蕊细节", "叶子脉络"]
            }
        }
    
    def create_detailed_annotation(self, image_path, element_type):
        # 创建详细标注
        image = Image.open(image_path)
        annotation = {
            "image_path": str(image_path),
            "element_type": element_type,
            "key_points": [],
            "color_regions": [],
            "pattern_regions": [],
            "repair_instructions": []
        }
        
        # 标注关键点
        key_points = self.annotate_key_points(image, element_type)
        annotation["key_points"] = key_points
        
        # 标注色彩区域
        color_regions = self.annotate_color_regions(image, element_type)
        annotation["color_regions"] = color_regions
        
        # 标注图案区域
        pattern_regions = self.annotate_pattern_regions(image, element_type)
        annotation["pattern_regions"] = pattern_regions
        
        # 生成修复指令
        repair_instructions = self.generate_repair_instructions(element_type, key_points, color_regions, pattern_regions)
        annotation["repair_instructions"] = repair_instructions
        
        return annotation
    
    def annotate_key_points(self, image, element_type):
        # 标注关键点
        template = self.element_templates[element_type]
        key_points = []
        
        for point_name in template["key_points"]:
            # 这里需要实际的点标注工具
            # 目前使用模拟数据
            point = {
                "name": point_name,
                "x": random.randint(50, image.width - 50),
                "y": random.randint(50, image.height - 50),
                "confidence": random.uniform(0.8, 1.0)
            }
            key_points.append(point)
        
        return key_points
    
    def annotate_color_regions(self, image, element_type):
        # 标注色彩区域
        template = self.element_templates[element_type]
        color_regions = []
        
        for color_name in template["colors"]:
            region = {
                "color_name": color_name,
                "bbox": [random.randint(0, image.width//2), random.randint(0, image.height//2), 
                        random.randint(image.width//2, image.width), random.randint(image.height//2, image.height)],
                "mask_path": f"masks/{element_type}_{color_name}_mask.png"
            }
            color_regions.append(region)
        
        return color_regions
    
    def annotate_pattern_regions(self, image, element_type):
        # 标注图案区域
        template = self.element_templates[element_type]
        pattern_regions = []
        
        for pattern_name in template["patterns"]:
            region = {
                "pattern_name": pattern_name,
                "bbox": [random.randint(0, image.width//2), random.randint(0, image.height//2), 
                        random.randint(image.width//2, image.width), random.randint(image.height//2, image.height)],
                "mask_path": f"masks/{element_type}_{pattern_name}_mask.png"
            }
            pattern_regions.append(region)
        
        return pattern_regions
    
    def generate_repair_instructions(self, element_type, key_points, color_regions, pattern_regions):
        # 生成修复指令
        instructions = []
        
        # 基于关键点的修复指令
        for point in key_points:
            instruction = {
                "type": "key_point_repair",
                "target": point["name"],
                "instruction": f"修复{point['name']}，保持位置在({point['x']}, {point['y']})",
                "priority": "high"
            }
            instructions.append(instruction)
        
        # 基于色彩区域的修复指令
        for region in color_regions:
            instruction = {
                "type": "color_repair",
                "target": region["color_name"],
                "instruction": f"修复{region['color_name']}区域，保持传统色彩",
                "priority": "medium"
            }
            instructions.append(instruction)
        
        # 基于图案区域的修复指令
        for region in pattern_regions:
            instruction = {
                "type": "pattern_repair",
                "target": region["pattern_name"],
                "instruction": f"修复{region['pattern_name']}图案，保持传统样式",
                "priority": "medium"
            }
            instructions.append(instruction)
        
        return instructions
    
    def save_annotation(self, annotation, output_path):
        # 保存标注数据
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(annotation, f, indent=2, ensure_ascii=False)

def main():
    annotator = ThangkaElementAnnotator()
    
    # 处理示例图像
    image_path = "datasets/thangka_elements/sample_buddha.jpg"
    element_type = "buddha"
    
    annotation = annotator.create_detailed_annotation(image_path, element_type)
    
    # 保存标注
    output_path = "datasets/element_annotations/sample_buddha_annotation.json"
    annotator.save_annotation(annotation, output_path)
    
    print(f"✅ 详细标注已保存: {output_path}")

if __name__ == "__main__":
    main()
