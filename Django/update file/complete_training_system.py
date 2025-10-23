#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整版唐卡元素精确修复训练系统 - wangchukMind
"""

import os
import sys
import json
import torch
import paddle
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cv2
from typing import Dict, List, Tuple, Any
import random

class ThangkaElementTrainingSystem:
    """唐卡元素精确修复训练系统"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.training_dir = self.project_root / "complete_training_system"
        self.setup_directories()
        
    def setup_directories(self):
        """创建训练目录结构"""
        directories = [
            self.training_dir,
            self.training_dir / "datasets",
            self.training_dir / "datasets" / "thangka_elements",
            self.training_dir / "datasets" / "element_masks",
            self.training_dir / "datasets" / "element_annotations",
            self.training_dir / "datasets" / "damaged_elements",
            self.training_dir / "datasets" / "reference_elements",
            self.training_dir / "models",
            self.training_dir / "models" / "element_lora",
            self.training_dir / "models" / "element_controlnet",
            self.training_dir / "checkpoints",
            self.training_dir / "logs",
            self.training_dir / "configs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def create_element_training_config(self):
        """创建元素训练配置"""
        config = {
            "thangka_elements": {
                "buddha": {
                    "description": "佛陀形象",
                    "key_features": ["坐姿", "手势", "法衣", "光环"],
                    "repair_priority": "highest",
                    "training_samples": 500
                },
                "bodhisattva": {
                    "description": "菩萨形象", 
                    "key_features": ["慈悲相", "装饰", "法器", "姿态"],
                    "repair_priority": "high",
                    "training_samples": 400
                },
                "deity": {
                    "description": "护法神形象",
                    "key_features": ["威严相", "武器", "坐骑", "装饰"],
                    "repair_priority": "high", 
                    "training_samples": 300
                },
                "lotus": {
                    "description": "莲花图案",
                    "key_features": ["花瓣", "花蕊", "茎叶", "色彩"],
                    "repair_priority": "medium",
                    "training_samples": 200
                },
                "mandala": {
                    "description": "曼陀罗图案",
                    "key_features": ["几何形状", "对称性", "色彩", "细节"],
                    "repair_priority": "medium",
                    "training_samples": 300
                },
                "clouds": {
                    "description": "云彩图案",
                    "key_features": ["形状", "层次", "色彩", "流动感"],
                    "repair_priority": "low",
                    "training_samples": 150
                },
                "mountains": {
                    "description": "山峦图案",
                    "key_features": ["轮廓", "层次", "纹理", "色彩"],
                    "repair_priority": "low",
                    "training_samples": 100
                }
            },
            "training_config": {
                "element_detection": {
                    "model": "YOLOv8",
                    "confidence_threshold": 0.7,
                    "iou_threshold": 0.5
                },
                "element_segmentation": {
                    "model": "SAM",
                    "points_per_side": 32,
                    "pred_iou_thresh": 0.88
                },
                "element_inpainting": {
                    "base_model": "stabilityai/stable-diffusion-3-inpainting",
                    "controlnet": "lllyasviel/control_v11p_sd15_canny",
                    "lora_rank": 32,
                    "learning_rate": 1e-4,
                    "batch_size": 2
                }
            }
        }
        
        config_path = self.training_dir / "configs" / "element_training_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 元素训练配置已保存: {config_path}")
    
    def create_element_detection_script(self):
        """创建元素检测脚本"""
        script_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
唐卡元素检测和分割脚本 - wangchukMind
\"\"\"

import cv2
import numpy as np
from PIL import Image
import torch
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor
import json
from pathlib import Path

class ThangkaElementDetector:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.yolo_model = None
        self.sam_model = None
        self.element_classes = self.config['thangka_elements']
        
    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_models(self):
        # 加载YOLO检测模型
        self.yolo_model = YOLO('yolov8n.pt')
        
        # 加载SAM分割模型
        sam_checkpoint = "sam_vit_h_4b8939.pth"
        model_type = "vit_h"
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self.sam_model = SamPredictor(sam)
        
        print("✅ 检测和分割模型加载完成")
    
    def detect_elements(self, image_path):
        # 使用YOLO检测唐卡元素
        results = self.yolo_model(image_path)
        
        elements = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                element = {
                    'class_id': int(box.cls[0]),
                    'confidence': float(box.conf[0]),
                    'bbox': box.xyxy[0].tolist(),
                    'element_type': self.get_element_type(int(box.cls[0]))
                }
                elements.append(element)
        
        return elements
    
    def segment_elements(self, image, elements):
        # 使用SAM分割检测到的元素
        self.sam_model.set_image(image)
        
        segmented_elements = []
        for element in elements:
            bbox = element['bbox']
            masks, scores, logits = self.sam_model.predict(
                point_coords=None,
                point_labels=None,
                box=bbox,
                multimask_output=False
            )
            
            element['mask'] = masks[0]
            element['segmentation_score'] = float(scores[0])
            segmented_elements.append(element)
        
        return segmented_elements
    
    def get_element_type(self, class_id):
        element_types = list(self.element_classes.keys())
        if class_id < len(element_types):
            return element_types[class_id]
        return "unknown"
    
    def process_thangka_image(self, image_path, output_dir):
        # 处理单张唐卡图像
        image = cv2.imread(str(image_path))
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 检测元素
        elements = self.detect_elements(image_path)
        
        # 分割元素
        segmented_elements = self.segment_elements(image_rgb, elements)
        
        # 保存结果
        self.save_element_data(image_path, segmented_elements, output_dir)
        
        return segmented_elements
    
    def save_element_data(self, image_path, elements, output_dir):
        # 保存元素数据
        image_name = Path(image_path).stem
        
        for i, element in enumerate(elements):
            element_data = {
                'image_path': str(image_path),
                'element_id': i,
                'element_type': element['element_type'],
                'confidence': element['confidence'],
                'bbox': element['bbox'],
                'mask_path': f"{output_dir}/masks/{image_name}_element_{i}.npy"
            }
            
            # 保存遮罩
            mask_path = Path(element_data['mask_path'])
            mask_path.parent.mkdir(parents=True, exist_ok=True)
            np.save(mask_path, element['mask'])
            
            # 保存元素数据
            element_json_path = f"{output_dir}/annotations/{image_name}_element_{i}.json"
            with open(element_json_path, 'w', encoding='utf-8') as f:
                json.dump(element_data, f, indent=2, ensure_ascii=False)

def main():
    config_path = "configs/element_training_config.json"
    detector = ThangkaElementDetector(config_path)
    detector.load_models()
    
    # 处理图像
    image_path = "datasets/thangka_elements/sample.jpg"
    output_dir = "datasets/element_annotations"
    detector.process_thangka_image(image_path, output_dir)

if __name__ == "__main__":
    main()
"""
        
        script_path = self.training_dir / "detect_elements.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ 元素检测脚本已创建: {script_path}")
    
    def create_element_inpainting_script(self):
        """创建元素修复脚本"""
        script_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
唐卡元素精确修复训练脚本 - wangchukMind
\"\"\"

import torch
import paddle
from diffusers import StableDiffusionInpaintPipeline, ControlNetModel
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments, Trainer
from datasets import Dataset
from PIL import Image
import numpy as np
import json
from pathlib import Path

class ThangkaElementInpainter:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.pipeline = None
        self.controlnet = None
        self.element_lora_models = {}
        
    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_base_models(self):
        # 加载基础修复模型
        self.pipeline = StableDiffusionInpaintPipeline.from_pretrained(
            self.config['training_config']['element_inpainting']['base_model'],
            torch_dtype=torch.float16
        )
        
        # 加载ControlNet
        self.controlnet = ControlNetModel.from_pretrained(
            self.config['training_config']['element_inpainting']['controlnet'],
            torch_dtype=torch.float16
        )
        
        print("✅ 基础模型加载完成")
    
    def create_element_specific_lora(self, element_type):
        # 为特定元素创建LoRA配置
        lora_config = LoraConfig(
            r=self.config['training_config']['element_inpainting']['lora_rank'],
            lora_alpha=32,
            target_modules=["to_k", "to_q", "to_v", "to_out.0"],
            lora_dropout=0.1,
            bias="none"
        )
        
        # 应用LoRA到UNet
        self.pipeline.unet = get_peft_model(self.pipeline.unet, lora_config)
        
        print(f"✅ {element_type} LoRA配置创建完成")
    
    def prepare_element_dataset(self, element_type):
        # 准备特定元素的训练数据
        element_config = self.config['thangka_elements'][element_type]
        
        # 加载元素图像和遮罩
        images = []
        masks = []
        prompts = []
        
        element_dir = Path(f"datasets/thangka_elements/{element_type}")
        
        for image_file in element_dir.glob("*.jpg"):
            # 加载图像
            image = Image.open(image_file)
            images.append(image)
            
            # 加载对应的遮罩
            mask_file = f"datasets/element_masks/{element_type}/{image_file.stem}_mask.png"
            if Path(mask_file).exists():
                mask = Image.open(mask_file)
                masks.append(mask)
            else:
                # 创建默认遮罩
                mask = Image.new('L', image.size, 0)
                masks.append(mask)
            
            # 生成提示词
            prompt = self.generate_element_prompt(element_type, element_config)
            prompts.append(prompt)
        
        return images, masks, prompts
    
    def generate_element_prompt(self, element_type, element_config):
        # 生成元素特定的提示词
        base_prompt = f"修复{element_config['description']}"
        
        features = element_config['key_features']
        feature_prompt = ", ".join(features)
        
        prompt = f"{base_prompt}, {feature_prompt}, 传统唐卡风格, 高质量, 细节丰富"
        
        return prompt
    
    def train_element_lora(self, element_type):
        # 训练特定元素的LoRA模型
        print(f"🚀 开始训练 {element_type} 元素LoRA模型...")
        
        # 创建元素特定LoRA
        self.create_element_specific_lora(element_type)
        
        # 准备数据
        images, masks, prompts = self.prepare_element_dataset(element_type)
        
        # 创建训练数据集
        dataset = self.create_training_dataset(images, masks, prompts)
        
        # 设置训练参数
        training_args = TrainingArguments(
            output_dir=f"checkpoints/element_lora/{element_type}",
            learning_rate=self.config['training_config']['element_inpainting']['learning_rate'],
            per_device_train_batch_size=self.config['training_config']['element_inpainting']['batch_size'],
            num_train_epochs=50,
            save_steps=100,
            eval_steps=50,
            logging_dir=f"logs/element_lora/{element_type}",
            logging_steps=10,
            evaluation_strategy="steps",
            save_strategy="steps"
        )
        
        # 创建训练器
        trainer = Trainer(
            model=self.pipeline.unet,
            args=training_args,
            train_dataset=dataset,
            data_collator=self.collate_fn
        )
        
        # 开始训练
        trainer.train()
        
        # 保存模型
        trainer.save_model()
        
        print(f"✅ {element_type} 元素LoRA模型训练完成")
    
    def create_training_dataset(self, images, masks, prompts):
        # 创建训练数据集
        dataset_data = []
        
        for i, (image, mask, prompt) in enumerate(zip(images, masks, prompts)):
            dataset_data.append({
                'image': image,
                'mask': mask,
                'prompt': prompt,
                'id': i
            })
        
        return Dataset.from_list(dataset_data)
    
    def collate_fn(self, examples):
        # 数据整理函数
        images = [example['image'] for example in examples]
        masks = [example['mask'] for example in examples]
        prompts = [example['prompt'] for example in examples]
        
        return {
            'images': images,
            'masks': masks,
            'prompts': prompts
        }
    
    def repair_element(self, image, mask, element_type, prompt):
        # 使用训练好的模型修复元素
        if element_type in self.element_lora_models:
            # 加载元素特定LoRA
            self.load_element_lora(element_type)
        
        # 执行修复
        result = self.pipeline(
            prompt=prompt,
            image=image,
            mask_image=mask,
            num_inference_steps=50,
            guidance_scale=15.0,
            strength=0.8
        ).images[0]
        
        return result
    
    def load_element_lora(self, element_type):
        # 加载元素特定LoRA权重
        lora_path = f"checkpoints/element_lora/{element_type}"
        if Path(lora_path).exists():
            self.pipeline.unet.load_adapter(lora_path)
            print(f"✅ {element_type} LoRA权重加载完成")

def main():
    config_path = "configs/element_training_config.json"
    inpainter = ThangkaElementInpainter(config_path)
    inpainter.load_base_models()
    
    # 训练所有元素类型
    element_types = ["buddha", "bodhisattva", "deity", "lotus", "mandala", "clouds", "mountains"]
    
    for element_type in element_types:
        inpainter.train_element_lora(element_type)

if __name__ == "__main__":
    main()
"""
        
        script_path = self.training_dir / "train_element_inpainting.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ 元素修复训练脚本已创建: {script_path}")
    
    def create_detailed_annotation_script(self):
        """创建详细标注脚本"""
        script_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
唐卡元素详细标注脚本 - wangchukMind
\"\"\"

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
"""
        
        script_path = self.training_dir / "annotate_elements.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ 详细标注脚本已创建: {script_path}")
    
    def create_complete_training_guide(self):
        """创建完整训练指南"""
        guide_content = """# 完整版唐卡元素精确修复训练指南 - wangchukMind

## 🎯 训练目标

训练能够精确修复唐卡特定元素和细节的AI模型，包括：

### 1. 核心元素类型
- **佛陀形象**: 坐姿、手势、法衣、光环
- **菩萨形象**: 慈悲相、装饰、法器、姿态  
- **护法神形象**: 威严相、武器、坐骑、装饰
- **莲花图案**: 花瓣、花蕊、茎叶、色彩
- **曼陀罗图案**: 几何形状、对称性、色彩、细节
- **云彩图案**: 形状、层次、色彩、流动感
- **山峦图案**: 轮廓、层次、纹理、色彩

### 2. 修复精度要求
- **像素级精度**: 精确到像素级别的修复
- **细节保持**: 保持传统唐卡的精细细节
- **风格一致**: 保持传统艺术风格的一致性
- **文化准确**: 确保修复结果符合文化传统

## 🏗️ 训练系统架构

### 1. 元素检测和分割
```python
# 使用YOLO检测唐卡元素
yolo_model = YOLO('yolov8n.pt')
elements = yolo_model.detect_elements(image)

# 使用SAM精确分割元素
sam_model = SamPredictor(sam)
masks = sam_model.segment_elements(image, elements)
```

### 2. 元素特定LoRA训练
```python
# 为每个元素类型训练专用LoRA
for element_type in ["buddha", "bodhisattva", "lotus"]:
    train_element_lora(element_type)
```

### 3. 精确修复管道
```python
# 使用元素特定模型进行修复
result = element_inpainter.repair_element(
    image=image,
    mask=element_mask,
    element_type="buddha",
    prompt="修复佛陀形象，保持传统风格"
)
```

## 📊 训练数据要求

### 1. 图像数据
- **分辨率**: 1024x1024像素
- **数量**: 每个元素类型至少500张图像
- **质量**: 高清、无模糊、色彩丰富
- **多样性**: 包含不同风格和时期的唐卡

### 2. 标注数据
- **关键点标注**: 标注元素的关键特征点
- **色彩区域标注**: 标注不同色彩区域
- **图案区域标注**: 标注装饰图案区域
- **修复指令**: 详细的修复指导说明

### 3. 遮罩数据
- **元素遮罩**: 精确的元素轮廓遮罩
- **损坏区域遮罩**: 需要修复的区域遮罩
- **参考区域遮罩**: 用于参考的完整区域

## 🔧 训练流程

### 1. 数据准备阶段
```bash
# 1. 收集唐卡图像
mkdir -p datasets/thangka_elements
# 将唐卡图像按元素类型分类存放

# 2. 检测和分割元素
python detect_elements.py

# 3. 创建详细标注
python annotate_elements.py
```

### 2. 模型训练阶段
```bash
# 1. 训练元素检测模型
python train_element_detection.py

# 2. 训练元素分割模型  
python train_element_segmentation.py

# 3. 训练元素修复模型
python train_element_inpainting.py
```

### 3. 模型验证阶段
```bash
# 1. 验证检测精度
python validate_detection.py

# 2. 验证分割精度
python validate_segmentation.py

# 3. 验证修复质量
python validate_inpainting.py
```

## 📈 训练配置

### 1. 元素检测配置
```json
{
  "element_detection": {
    "model": "YOLOv8",
    "confidence_threshold": 0.7,
    "iou_threshold": 0.5,
    "input_size": 640
  }
}
```

### 2. 元素分割配置
```json
{
  "element_segmentation": {
    "model": "SAM",
    "points_per_side": 32,
    "pred_iou_thresh": 0.88,
    "stability_score_thresh": 0.95
  }
}
```

### 3. 元素修复配置
```json
{
  "element_inpainting": {
    "base_model": "stabilityai/stable-diffusion-3-inpainting",
    "controlnet": "lllyasviel/control_v11p_sd15_canny",
    "lora_rank": 32,
    "learning_rate": 1e-4,
    "batch_size": 2,
    "num_epochs": 50
  }
}
```

## 🎯 训练目标

### 1. 检测精度目标
- **mAP@0.5**: >0.9
- **检测速度**: <100ms
- **元素覆盖率**: >95%

### 2. 分割精度目标
- **IoU**: >0.85
- **边界精度**: 像素级
- **分割速度**: <200ms

### 3. 修复质量目标
- **PSNR**: >30dB
- **SSIM**: >0.9
- **用户满意度**: >95%

## 🚀 开始训练

### 1. 环境准备
```bash
# 安装依赖
pip install -r requirements_training.txt

# 下载预训练模型
python download_pretrained_models.py
```

### 2. 数据准备
```bash
# 准备训练数据
python prepare_training_data.py

# 验证数据质量
python validate_training_data.py
```

### 3. 开始训练
```bash
# 训练所有元素类型
python train_all_elements.py

# 或训练特定元素
python train_element_inpainting.py --element_type buddha
```

### 4. 模型评估
```bash
# 评估模型性能
python evaluate_models.py

# 生成修复示例
python generate_repair_examples.py
```

## 📝 注意事项

1. **数据质量**: 确保训练数据质量高，标注准确
2. **硬件要求**: 需要强大的GPU支持（推荐RTX 4090或A100）
3. **训练时间**: 完整训练可能需要数周时间
4. **模型保存**: 定期保存检查点和最终模型
5. **验证测试**: 定期验证模型效果和修复质量

## 🎉 训练完成

训练完成后，您将获得：

- **元素检测模型**: 精确检测唐卡中的各种元素
- **元素分割模型**: 精确分割元素轮廓
- **元素修复模型**: 高质量修复特定元素
- **修复质量评估**: 详细的性能指标和评估报告

这些模型将能够精确修复唐卡的每个细节，为唐卡艺术保护提供最先进的技术支持！
"""
        
        guide_path = self.training_dir / "COMPLETE_TRAINING_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"✅ 完整训练指南已保存: {guide_path}")
    
    def setup_complete_training_system(self):
        """设置完整训练系统"""
        print("🚀 设置完整版唐卡元素精确修复训练系统...")
        
        try:
            # 1. 创建元素训练配置
            self.create_element_training_config()
            
            # 2. 创建元素检测脚本
            self.create_element_detection_script()
            
            # 3. 创建元素修复脚本
            self.create_element_inpainting_script()
            
            # 4. 创建详细标注脚本
            self.create_detailed_annotation_script()
            
            # 5. 创建完整训练指南
            self.create_complete_training_guide()
            
            print("✅ 完整版训练系统设置完成！")
            print(f"📁 训练系统目录: {self.training_dir}")
            
            print("\\n📋 下一步操作:")
            print("1. 准备唐卡元素训练数据")
            print("2. 运行元素检测: python complete_training_system/detect_elements.py")
            print("3. 创建详细标注: python complete_training_system/annotate_elements.py")
            print("4. 开始元素训练: python complete_training_system/train_element_inpainting.py")
            
        except Exception as e:
            print(f"❌ 完整训练系统设置失败: {e}")

def main():
    trainer = ThangkaElementTrainingSystem()
    trainer.setup_complete_training_system()

if __name__ == "__main__":
    main()



