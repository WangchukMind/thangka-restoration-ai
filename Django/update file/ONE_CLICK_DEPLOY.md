# AI Studio 一键部署指南

## 概述
`start_server_aistudio.py` 是一个完全独立的一键部署脚本，**不需要**任何外部文件（如`requirements.txt`）。

## 使用方法

### 在AI Studio中部署
```bash
# 1. 上传项目文件到AI Studio
# 2. 进入Django目录
cd Django

# 3. 一键部署（仅需一个命令）
python start_server_aistudio.py runserver 0.0.0.0:8080
```

## 脚本功能

### 🔧 自动完成的任务
1. **环境检测**：自动检测AI Studio环境
2. **依赖安装**：自动安装所有必要的Python包
3. **NumPy修复**：自动修复NumPy兼容性问题
4. **模型下载**：自动下载AI模型文件
5. **Django配置**：自动设置Django环境
6. **静态文件**：自动收集静态文件
7. **服务器启动**：自动启动Django服务器

### 📦 内置的依赖包
脚本内置了所有必要的依赖，包括：
- PaddlePaddle深度学习框架
- Django Web框架
- 图像处理库（OpenCV, Pillow等）
- 数值计算库（NumPy, SciPy等）
- 其他必要的工具库

### 🛠️ 自动修复的问题
- NumPy 2.x兼容性问题
- 静态文件显示问题
- 模型加载问题
- API响应问题

## 部署步骤

### 步骤1：准备环境
```bash
# 在AI Studio中创建新项目
# 上传项目文件
```

### 步骤2：一键部署
```bash
cd Django
python start_server_aistudio.py runserver 0.0.0.0:8080
```

### 步骤3：访问应用
- 打开AI Studio的Web服务
- 访问 `http://0.0.0.0:8080`
- 开始使用唐卡修复系统

## 优势

### ✅ 完全独立
- 不需要`requirements.txt`
- 不需要手动安装依赖
- 不需要复杂配置

### ✅ 自动修复
- 自动处理环境问题
- 自动修复兼容性问题
- 自动配置所有组件

### ✅ 一键完成
- 单个命令完成所有部署
- 自动检测和修复问题
- 详细的进度显示

## 注意事项

### ⚠️ 重要提醒
1. **不需要**上传`requirements.txt`文件
2. **不需要**手动安装任何依赖
3. **不需要**修改任何配置文件
4. 脚本会自动处理所有问题

### 📋 文件清单
只需要上传这些文件：
- `start_server_aistudio.py` - 一键部署脚本
- `server/` - Django应用目录
- `models/` - AI模型目录（可选，脚本会自动下载）

## 故障排除

### 如果部署失败
1. 检查Python版本（需要3.8+）
2. 检查网络连接（需要下载依赖和模型）
3. 查看脚本输出的错误信息
4. 重新运行部署命令

### 如果Logo不显示
脚本已包含Logo显示修复，如果仍有问题：
```bash
python smart_static_fix.py
```

## 总结
`start_server_aistudio.py` 是一个真正的"一键部署"解决方案，**完全不需要**`requirements.txt`或其他外部配置文件。只需要运行一个命令，就能完成整个系统的部署和配置。



