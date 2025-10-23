#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐卡元素精确修复训练脚本 - wangchukMind
"""

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
