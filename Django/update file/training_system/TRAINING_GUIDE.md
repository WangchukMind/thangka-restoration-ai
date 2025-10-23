# 唐卡修复模型训练指南 - wangchukMind

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
