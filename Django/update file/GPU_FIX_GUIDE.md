# GPU使用问题修复指南 - wangchukMind

## 🔍 问题分析

从你提供的截图可以看出，在AI Studio上确实没有充分利用GPU：

- **GPU利用率**: 0% (完全没有使用)
- **显存使用**: 310MiB / 32768MiB (仅使用0.9%)
- **功耗**: 59W / 300W (仅使用19.6%)
- **进程列表**: 空 (没有GPU进程在运行)

虽然PaddlePaddle检测到了GPU，但实际推理时可能没有使用GPU加速。

## 🔧 修复方案

### 1. 在AI Studio中运行修复脚本

```bash
# 在AI Studio终端中运行
python fix_gpu_aistudio.py
```

### 2. 测试GPU使用

```bash
# 测试GPU计算性能
python test_gpu_usage.py

# 实时监控GPU使用情况
python monitor_gpu.py
```

### 3. 重启Django服务器

```bash
# 重启服务器
python start_server_aistudio.py
```

## 📋 修复内容

### 1. 模型加载时强制使用GPU

在 `changeModel` 函数中添加：

```python
# 确保pipe在GPU上 - wangchukMind
if pipe is not None and paddle.device.is_compiled_with_cuda():
    try:
        # 将pipe的所有组件移动到GPU
        if hasattr(pipe, 'unet') and pipe.unet is not None:
            pipe.unet.to('gpu:0')
            print("✅ UNet已移动到GPU")
        if hasattr(pipe, 'vae') and pipe.vae is not None:
            pipe.vae.to('gpu:0')
            print("✅ VAE已移动到GPU")
        if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
            pipe.text_encoder.to('gpu:0')
            print("✅ Text Encoder已移动到GPU")
        if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
            pipe.controlnet.to('gpu:0')
            print("✅ ControlNet已移动到GPU")
    except Exception as e:
        print(f"⚠️ 移动模型到GPU失败: {e}")

# 强制设置GPU设备 - wangchukMind
if paddle.device.is_compiled_with_cuda():
    paddle.set_device('gpu:0')
    print("✅ 强制设置GPU设备: gpu:0")
```

### 2. 推理时强制使用GPU

在所有推理函数（inpaint、text2img、img2img）中添加：

```python
# 强制使用GPU进行推理 - wangchukMind
if paddle.device.is_compiled_with_cuda():
    paddle.set_device('gpu:0')
    print("🔧 推理前强制设置GPU设备: gpu:0")
    
    # 确保所有输入数据在GPU上
    if hasattr(pipe, 'unet') and pipe.unet is not None:
        pipe.unet.to('gpu:0')
    if hasattr(pipe, 'vae') and pipe.vae is not None:
        pipe.vae.to('gpu:0')
    if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
        pipe.text_encoder.to('gpu:0')
    if hasattr(pipe, 'controlnet') and pipe.controlnet is not None:
        pipe.controlnet.to('gpu:0')
```

## 🎯 预期效果

修复后，你应该看到：

1. **GPU利用率**: 从0%提升到80-100%
2. **显存使用**: 从310MiB提升到8-16GB
3. **功耗**: 从59W提升到200-300W
4. **进程列表**: 显示Python进程在使用GPU

## 🔍 验证方法

### 1. 运行GPU测试

```bash
python test_gpu_usage.py
```

应该看到：
```
✅ GPU矩阵乘法测试成功
   矩阵大小: 1000x1000
   计算时间: 0.123秒
   结果形状: [1000, 1000]
✅ GPU内存使用: 2.34 GB
```

### 2. 监控GPU使用

```bash
python monitor_gpu.py
```

应该看到：
```
GPU 0: 利用率  85% | 显存 12345MB/32768MB ( 37.7%) | 温度  65°C
```

### 3. 进行图像修复测试

在Web界面中上传图像进行修复，应该看到：

1. **推理速度**: 明显加快（从几分钟缩短到几十秒）
2. **GPU利用率**: 实时显示高利用率
3. **显存使用**: 显存使用量大幅增加

## ⚠️ 注意事项

1. **AI Studio环境**: 这些修复只在AI Studio环境中有效
2. **本地环境**: 本地环境没有GPU，会继续使用CPU
3. **内存管理**: 修复后GPU内存使用会增加，注意监控
4. **性能提升**: 修复后推理速度应该显著提升

## 🚀 快速修复

如果只想快速修复，可以直接在AI Studio中运行：

```bash
# 一键修复
python fix_gpu_aistudio.py

# 重启服务器
python start_server_aistudio.py
```

然后进行图像修复测试，观察GPU使用情况。



