#!/usr/bin/env python3
"""
修复模型类型API的脚本
解决前端JavaScript解析JSON错误的问题
"""
import os
import sys
import json
from pathlib import Path

def fix_model_type_api():
    """修复模型类型API问题"""
    print("🔧 修复模型类型API问题...")
    
    # 检查并创建必要的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, "models")
    finetuned_dir = os.path.join(models_dir, "finetuned")
    controlnet_dir = os.path.join(models_dir, "control_v11p_sd21_canny_paddle")
    
    print(f"📁 检查模型目录: {models_dir}")
    
    # 创建目录如果不存在
    os.makedirs(finetuned_dir, exist_ok=True)
    os.makedirs(controlnet_dir, exist_ok=True)
    
    # 检查目录是否存在
    if not os.path.exists(models_dir):
        print(f"❌ 模型目录不存在: {models_dir}")
        return False
    
    if not os.path.exists(finetuned_dir):
        print(f"❌ LoRA模型目录不存在: {finetuned_dir}")
        return False
    
    if not os.path.exists(controlnet_dir):
        print(f"❌ ControlNet模型目录不存在: {controlnet_dir}")
        return False
    
    print("✅ 所有必要的模型目录都存在")
    
    # 创建修复后的getModelType函数
    fixed_code = '''
def getModelType():
    """修复后的getModelType函数 - 增强错误处理"""
    try:
        result = {
            'model': modelSet if 'modelSet' in globals() else 'SD21',
            'type': typeSet if 'typeSet' in globals() else 'inpaint', 
            'cnModel': cnModelSet if 'cnModelSet' in globals() else 'control_sd2.1_base_canny',
            'loraList': [],
            'cnList': []
        }
        
        # 安全地获取LoRA模型列表
        try:
            if os.path.exists(lora_model_path):
                loraList = os.listdir(lora_model_path)
                print(f"🔍 LoRA模型目录内容: {loraList}")
                
                for item in loraList:
                    item_path = os.path.join(lora_model_path, item)
                    
                    # 检查.safetensors文件
                    if os.path.isfile(item_path) and item.endswith('.safetensors'):
                        model_name = item.replace('.safetensors', '')
                        result['loraList'].append(model_name)
                        print(f"✅ 找到.safetensors LoRA模型: {model_name}")
                    
                    # 检查.pdparams文件
                    elif os.path.isfile(item_path) and item.endswith('.pdparams'):
                        model_name = item.replace('.pdparams', '')
                        if model_name.endswith('_paddle'):
                            model_name = model_name[:-7]
                        result['loraList'].append(model_name)
                        print(f"✅ 找到.pdparams LoRA模型: {model_name}")
                    
                    # 检查目录格式
                    elif os.path.isdir(item_path):
                        dir_contents = os.listdir(item_path)
                        has_pdparams = any(f.endswith('.pdparams') for f in dir_contents)
                        if has_pdparams:
                            result['loraList'].append(item)
                            print(f"✅ 找到目录格式LoRA模型: {item}")
            else:
                print(f"⚠️ LoRA模型目录不存在: {lora_model_path}")
                # 使用默认LoRA模型列表
                result['loraList'] = ['thangka_21_Status_140', 'thangka_21_ACD_250']
                
        except Exception as e:
            print(f"❌ 读取LoRA模型目录失败: {e}")
            result['loraList'] = ['thangka_21_Status_140', 'thangka_21_ACD_250']
        
        # 安全地获取ControlNet模型列表
        try:
            if os.path.exists(cn_model_path):
                cnList = os.listdir(cn_model_path)
                for item in cnList:
                    item_path = os.path.join(cn_model_path, item)
                    if os.path.isdir(item_path):
                        try:
                            parts = item.split('_')
                            if len(parts) >= 3:
                                version = parts[1]
                                cnType = parts[2]
                                if cnType == 'canny' and version == '2.1':
                                    result['cnList'].append(item)
                                    print(f"✅ 找到ControlNet模型: {item}")
                        except Exception as e:
                            print(f"⚠️ 解析ControlNet模型名称失败: {item}, {e}")
            else:
                print(f"⚠️ ControlNet模型目录不存在: {cn_model_path}")
                result['cnList'] = ['control_v11p_sd21_canny_paddle']
                
        except Exception as e:
            print(f"❌ 读取ControlNet模型目录失败: {e}")
            result['cnList'] = ['control_v11p_sd21_canny_paddle']
        
        print(f"📊 最终结果: {result}")
        return result
        
    except Exception as e:
        print(f"❌ getModelType函数执行失败: {e}")
        # 返回默认结果
        return {
            'model': 'SD21',
            'type': 'inpaint',
            'cnModel': 'control_sd2.1_base_canny',
            'loraList': ['thangka_21_Status_140', 'thangka_21_ACD_250'],
            'cnList': ['control_v11p_sd21_canny_paddle']
        }
'''
    
    # 写入修复后的代码到文件
    fix_file = os.path.join(current_dir, "getModelType_fixed.py")
    with open(fix_file, 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    
    print(f"✅ 修复代码已保存到: {fix_file}")
    print("📋 请将修复后的getModelType函数替换到diffusion_paddle.py中")
    
    return True

if __name__ == "__main__":
    print("🚀 开始修复模型类型API问题...")
    if fix_model_type_api():
        print("🎉 修复完成！")
    else:
        print("❌ 修复失败！")
        sys.exit(1)



