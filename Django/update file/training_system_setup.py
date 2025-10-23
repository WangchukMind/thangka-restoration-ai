#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐卡修复模型训练系统设置 - wangchukMind
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class ThangkaTrainingSystem:
    """唐卡训练系统"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.training_dir = self.project_root / "training_system"
        self.datasets_dir = self.training_dir / "datasets"
        self.models_dir = self.training_dir / "models"
        self.checkpoints_dir = self.training_dir / "checkpoints"
        self.logs_dir = self.training_dir / "logs"
        self.configs_dir = self.training_dir / "configs"
        
    def create_training_structure(self):
        """创建训练系统目录结构"""
        print("🔧 创建训练系统目录结构...")
        
        directories = [
            self.training_dir,
            self.datasets_dir,
            self.datasets_dir / "thangka_images",
            self.datasets_dir / "thangka_masks", 
            self.datasets_dir / "thangka_edges",
            self.datasets_dir / "thangka_annotations",
            self.models_dir,
            self.models_dir / "lora",
            self.models_dir / "controlnet",
            self.models_dir / "vae",
            self.models_dir / "text_encoder",
            self.checkpoints_dir,
            self.checkpoints_dir / "lora",
            self.checkpoints_dir / "controlnet",
            self.checkpoints_dir / "vae",
            self.logs_dir,
            self.configs_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建目录: {directory}")
    
    def create_training_configs(self):
        """创建训练配置文件"""
        print("🔧 创建训练配置文件...")
        
        # LoRA训练配置
        lora_config = {
            "model": {
                "base_model": "stabilityai/stable-diffusion-3-medium",
                "target_modules": ["to_k", "to_q", "to_v", "to_out.0"],
                "rank": 16,
                "alpha": 32,
                "dropout": 0.1
            },
            "training": {
                "learning_rate": 1e-4,
                "batch_size": 4,
                "num_epochs": 100,
                "save_steps": 500,
                "eval_steps": 100,
                "gradient_accumulation_steps": 4,
                "max_grad_norm": 1.0,
                "warmup_steps": 100
            },
            "data": {
                "train_data_dir": "./datasets/thangka_images",
                "resolution": 1024,
                "center_crop": True,
                "random_flip": True
            },
            "optimizer": {
                "type": "AdamW",
                "weight_decay": 0.01,
                "beta1": 0.9,
                "beta2": 0.999
            },
            "scheduler": {
                "type": "cosine",
                "warmup_ratio": 0.1
            }
        }
        
        config_path = self.configs_dir / "lora_training_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(lora_config, f, indent=2, ensure_ascii=False)
        
        # ControlNet训练配置
        controlnet_config = {
            "model": {
                "base_model": "stabilityai/stable-diffusion-3-medium",
                "controlnet_model": "lllyasviel/control_v11p_sd15_canny",
                "conditioning_scale": 1.0
            },
            "training": {
                "learning_rate": 5e-5,
                "batch_size": 2,
                "num_epochs": 200,
                "save_steps": 1000,
                "eval_steps": 200,
                "gradient_accumulation_steps": 8,
                "max_grad_norm": 1.0
            },
            "data": {
                "train_data_dir": "./datasets/thangka_images",
                "conditioning_data_dir": "./datasets/thangka_edges",
                "resolution": 1024,
                "center_crop": True
            }
        }
        
        config_path = self.configs_dir / "controlnet_training_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(controlnet_config, f, indent=2, ensure_ascii=False)
        
        print("✅ 训练配置文件已创建")
    
    def create_training_scripts(self):
        """创建训练脚本"""
        print("🔧 创建训练脚本...")
        
        # LoRA训练脚本
        lora_training_script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
唐卡LoRA模型训练脚本 - wangchukMind
\"\"\"

import os
import sys
import json
import torch
import paddle
from pathlib import Path
from diffusers import StableDiffusionPipeline, DDPMScheduler
from peft import LoraConfig, get_peft_model, TaskType
from transformers import TrainingArguments, Trainer
from datasets import Dataset
from PIL import Image
import numpy as np

class ThangkaLoRATrainer:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.model = None
        self.trainer = None
        
    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_base_model(self):
        print("🔧 加载基础模型...")
        self.model = StableDiffusionPipeline.from_pretrained(
            self.config['model']['base_model'],
            torch_dtype=torch.float16,
            use_safetensors=True
        )
        print("✅ 基础模型加载完成")
    
    def setup_lora(self):
        print("🔧 设置LoRA...")
        lora_config = LoraConfig(
            r=self.config['model']['rank'],
            lora_alpha=self.config['model']['alpha'],
            target_modules=self.config['model']['target_modules'],
            lora_dropout=self.config['model']['dropout'],
            bias="none",
            task_type=TaskType.DIFFUSION
        )
        
        self.model.unet = get_peft_model(self.model.unet, lora_config)
        print("✅ LoRA设置完成")
    
    def prepare_dataset(self):
        print("🔧 准备训练数据集...")
        # 这里需要实现数据集加载逻辑
        # 返回训练和验证数据集
        pass
    
    def setup_trainer(self, train_dataset, eval_dataset):
        print("🔧 设置训练器...")
        training_args = TrainingArguments(
            output_dir="./checkpoints/lora",
            learning_rate=self.config['training']['learning_rate'],
            per_device_train_batch_size=self.config['training']['batch_size'],
            num_train_epochs=self.config['training']['num_epochs'],
            save_steps=self.config['training']['save_steps'],
            eval_steps=self.config['training']['eval_steps'],
            gradient_accumulation_steps=self.config['training']['gradient_accumulation_steps'],
            max_grad_norm=self.config['training']['max_grad_norm'],
            warmup_steps=self.config['training']['warmup_steps'],
            logging_dir="./logs",
            logging_steps=50,
            evaluation_strategy="steps",
            save_strategy="steps",
            load_best_model_at_end=True,
            metric_for_best_model="loss",
            greater_is_better=False
        )
        
        self.trainer = Trainer(
            model=self.model.unet,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=self.collate_fn
        )
        print("✅ 训练器设置完成")
    
    def collate_fn(self, examples):
        # 实现数据整理函数
        pass
    
    def train(self):
        print("🚀 开始训练LoRA模型...")
        self.load_base_model()
        self.setup_lora()
        
        train_dataset, eval_dataset = self.prepare_dataset()
        self.setup_trainer(train_dataset, eval_dataset)
        
        # 开始训练
        self.trainer.train()
        
        # 保存模型
        self.trainer.save_model()
        print("✅ LoRA模型训练完成")
    
    def save_lora_weights(self, output_path):
        print("💾 保存LoRA权重...")
        self.model.unet.save_pretrained(output_path)
        print(f"✅ LoRA权重已保存到: {output_path}")

def main():
    config_path = "./configs/lora_training_config.json"
    trainer = ThangkaLoRATrainer(config_path)
    trainer.train()
    
    # 保存训练好的LoRA权重
    trainer.save_lora_weights("./models/lora/thangka_artistic_v2.0")

if __name__ == "__main__":
    main()
"""
        
        script_path = self.training_dir / "train_lora.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(lora_training_script)
        
        # ControlNet训练脚本
        controlnet_training_script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
唐卡ControlNet模型训练脚本 - wangchukMind
\"\"\"

import os
import sys
import json
import torch
from pathlib import Path
from diffusers import StableDiffusionPipeline, ControlNetModel, StableDiffusionControlNetPipeline
from transformers import TrainingArguments, Trainer
from datasets import Dataset
from PIL import Image
import numpy as np

class ThangkaControlNetTrainer:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.model = None
        self.trainer = None
        
    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_models(self):
        print("🔧 加载模型...")
        # 加载基础模型
        self.base_model = StableDiffusionPipeline.from_pretrained(
            self.config['model']['base_model'],
            torch_dtype=torch.float16
        )
        
        # 加载ControlNet
        self.controlnet = ControlNetModel.from_pretrained(
            self.config['model']['controlnet_model'],
            torch_dtype=torch.float16
        )
        
        # 创建ControlNet管道
        self.model = StableDiffusionControlNetPipeline.from_pretrained(
            self.config['model']['base_model'],
            controlnet=self.controlnet,
            torch_dtype=torch.float16
        )
        
        print("✅ 模型加载完成")
    
    def prepare_dataset(self):
        print("🔧 准备训练数据集...")
        # 实现数据集加载逻辑
        pass
    
    def setup_trainer(self, train_dataset, eval_dataset):
        print("🔧 设置训练器...")
        training_args = TrainingArguments(
            output_dir="./checkpoints/controlnet",
            learning_rate=self.config['training']['learning_rate'],
            per_device_train_batch_size=self.config['training']['batch_size'],
            num_train_epochs=self.config['training']['num_epochs'],
            save_steps=self.config['training']['save_steps'],
            eval_steps=self.config['training']['eval_steps'],
            gradient_accumulation_steps=self.config['training']['gradient_accumulation_steps'],
            max_grad_norm=self.config['training']['max_grad_norm'],
            logging_dir="./logs",
            logging_steps=50,
            evaluation_strategy="steps",
            save_strategy="steps"
        )
        
        self.trainer = Trainer(
            model=self.model.controlnet,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=self.collate_fn
        )
        print("✅ 训练器设置完成")
    
    def collate_fn(self, examples):
        # 实现数据整理函数
        pass
    
    def train(self):
        print("🚀 开始训练ControlNet模型...")
        self.load_models()
        
        train_dataset, eval_dataset = self.prepare_dataset()
        self.setup_trainer(train_dataset, eval_dataset)
        
        # 开始训练
        self.trainer.train()
        
        # 保存模型
        self.trainer.save_model()
        print("✅ ControlNet模型训练完成")
    
    def save_controlnet(self, output_path):
        print("💾 保存ControlNet模型...")
        self.model.controlnet.save_pretrained(output_path)
        print(f"✅ ControlNet模型已保存到: {output_path}")

def main():
    config_path = "./configs/controlnet_training_config.json"
    trainer = ThangkaControlNetTrainer(config_path)
    trainer.train()
    
    # 保存训练好的ControlNet
    trainer.save_controlnet("./models/controlnet/thangka_canny_v1.0")

if __name__ == "__main__":
    main()
"""
        
        script_path = self.training_dir / "train_controlnet.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(controlnet_training_script)
        
        print("✅ 训练脚本已创建")
    
    def create_data_preparation_scripts(self):
        """创建数据准备脚本"""
        print("🔧 创建数据准备脚本...")
        
        data_prep_script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
唐卡训练数据准备脚本 - wangchukMind
\"\"\"

import os
import json
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from skimage.feature import canny

class ThangkaDataPreparer:
    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def prepare_images(self):
        print("🔧 准备图像数据...")
        # 1. 调整图像尺寸到1024x1024
        # 2. 转换为RGB格式
        # 3. 保存到训练目录
        pass
    
    def generate_masks(self):
        print("🔧 生成遮罩数据...")
        # 1. 自动生成损坏区域遮罩
        # 2. 手动标注重要区域
        # 3. 保存遮罩文件
        pass
    
    def generate_edges(self):
        print("🔧 生成边缘数据...")
        # 1. 使用Canny算法生成边缘
        # 2. 优化边缘质量
        # 3. 保存边缘文件
        pass
    
    def create_annotations(self):
        print("🔧 创建标注数据...")
        # 1. 创建图像描述文本
        # 2. 标注佛教元素
        # 3. 保存JSON标注文件
        pass
    
    def prepare_all_data(self):
        print("🚀 开始准备所有训练数据...")
        self.prepare_images()
        self.generate_masks()
        self.generate_edges()
        self.create_annotations()
        print("✅ 数据准备完成")

def main():
    input_dir = "./datasets/raw_thangka"
    output_dir = "./datasets/thangka_images"
    
    preparer = ThangkaDataPreparer(input_dir, output_dir)
    preparer.prepare_all_data()

if __name__ == "__main__":
    main()
"""
        
        script_path = self.training_dir / "prepare_data.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(data_prep_script)
        
        print("✅ 数据准备脚本已创建")
    
    def create_training_requirements(self):
        """创建训练依赖文件"""
        print("🔧 创建训练依赖文件...")
        
        requirements = [
            "torch>=2.1.0",
            "torchvision>=0.16.0",
            "paddlepaddle-gpu>=2.6.0",
            "diffusers>=0.24.0",
            "transformers>=4.35.0",
            "accelerate>=0.24.0",
            "peft>=0.6.0",
            "datasets>=2.14.0",
            "opencv-python>=4.8.0",
            "Pillow>=10.0.0",
            "numpy>=1.24.0",
            "scikit-image>=0.21.0",
            "safetensors>=0.4.0",
            "wandb>=0.16.0",
            "tensorboard>=2.15.0",
            "tqdm>=4.66.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0"
        ]
        
        requirements_path = self.training_dir / "requirements_training.txt"
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write('\\n'.join(requirements))
        
        print(f"✅ 训练依赖文件已保存: {requirements_path}")
    
    def create_training_guide(self):
        """创建训练指南"""
        print("🔧 创建训练指南...")
        
        guide_content = """# 唐卡修复模型训练指南 - wangchukMind

## 🎯 训练概述

本指南将帮助您训练专门用于唐卡修复的AI模型。

## 📋 训练步骤

### 1. 数据准备
```bash
# 准备原始唐卡图像
mkdir -p datasets/raw_thangka
# 将唐卡图像放入该目录

# 运行数据准备脚本
python prepare_data.py
```

### 2. LoRA模型训练
```bash
# 训练唐卡艺术风格LoRA
python train_lora.py
```

### 3. ControlNet模型训练
```bash
# 训练唐卡边缘控制模型
python train_controlnet.py
```

## 📊 训练数据要求

### 图像数据
- **分辨率**: 1024x1024像素
- **格式**: PNG或JPG
- **数量**: 至少1000张高质量唐卡图像
- **质量**: 清晰、无模糊、色彩丰富

### 标注数据
- **图像描述**: 详细的唐卡内容描述
- **佛教元素**: 佛陀、菩萨、护法神等标注
- **艺术风格**: 传统唐卡风格特征标注
- **修复区域**: 需要修复的区域标注

## 🔧 训练配置

### LoRA训练参数
- **学习率**: 1e-4
- **批次大小**: 4
- **训练轮数**: 100
- **Rank**: 16
- **Alpha**: 32

### ControlNet训练参数
- **学习率**: 5e-5
- **批次大小**: 2
- **训练轮数**: 200
- **条件尺度**: 1.0

## 📈 训练监控

### 使用Weights & Biases
```bash
# 安装wandb
pip install wandb

# 登录wandb
wandb login

# 训练时会自动记录指标
```

### 使用TensorBoard
```bash
# 启动TensorBoard
tensorboard --logdir=./logs

# 在浏览器中查看训练进度
# http://localhost:6006
```

## 🎯 训练目标

### LoRA模型目标
- 学习唐卡独特的艺术风格
- 掌握传统色彩搭配
- 理解佛教图像学特征
- 保持文化准确性

### ControlNet模型目标
- 精确控制边缘结构
- 保持图像细节
- 支持多种控制条件
- 提高修复质量

## 🚀 开始训练

1. **准备环境**
```bash
pip install -r requirements_training.txt
```

2. **准备数据**
```bash
python prepare_data.py
```

3. **开始训练**
```bash
python train_lora.py
python train_controlnet.py
```

4. **监控进度**
```bash
tensorboard --logdir=./logs
```

## 📝 注意事项

1. **数据质量**: 确保训练数据质量高
2. **硬件要求**: 需要强大的GPU支持
3. **训练时间**: 完整训练可能需要数天
4. **模型保存**: 定期保存检查点
5. **验证测试**: 定期验证模型效果

## 🎉 训练完成

训练完成后，您将获得：
- 唐卡专用LoRA模型
- 唐卡ControlNet模型
- 训练日志和指标
- 模型评估报告

这些模型将显著提升唐卡修复的质量和准确性！
"""
        
        guide_path = self.training_dir / "TRAINING_GUIDE.md"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"✅ 训练指南已保存: {guide_path}")
    
    def setup_training_system(self):
        """设置完整训练系统"""
        print("🚀 设置唐卡训练系统...")
        
        try:
            # 1. 创建目录结构
            self.create_training_structure()
            
            # 2. 创建配置文件
            self.create_training_configs()
            
            # 3. 创建训练脚本
            self.create_training_scripts()
            
            # 4. 创建数据准备脚本
            self.create_data_preparation_scripts()
            
            # 5. 创建依赖文件
            self.create_training_requirements()
            
            # 6. 创建训练指南
            self.create_training_guide()
            
            print("✅ 唐卡训练系统设置完成！")
            print(f"📁 训练系统目录: {self.training_dir}")
            
            print("\\n📋 下一步操作:")
            print("1. 准备唐卡训练数据")
            print("2. 安装训练依赖: pip install -r training_system/requirements_training.txt")
            print("3. 运行数据准备: python training_system/prepare_data.py")
            print("4. 开始训练: python training_system/train_lora.py")
            
        except Exception as e:
            print(f"❌ 训练系统设置失败: {e}")

def main():
    trainer = ThangkaTrainingSystem()
    trainer.setup_training_system()

if __name__ == "__main__":
    main()



