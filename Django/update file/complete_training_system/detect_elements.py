#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐卡元素检测和分割脚本 - wangchukMind
"""

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
