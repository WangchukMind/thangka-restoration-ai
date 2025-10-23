# AI Studio 快速修复指南

## 问题描述
前端JavaScript解析JSON时遇到错误：`SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON`

## 解决方案

### 方法1：一键修复（推荐）
```bash
python complete_fix_aistudio.py
```

### 方法2：手动修复

#### 步骤1：修复NumPy兼容性
```bash
pip uninstall numpy scikit-image opencv-python imageio -y
pip install 'numpy>=1.21.2,<2.0.0' --force-reinstall
pip install scikit-image==0.21.0 --force-reinstall
pip install opencv-python==4.8.1.78 --force-reinstall
pip install imageio==2.31.1 --force-reinstall
```

#### 步骤2：创建模型目录
```bash
mkdir -p models/finetuned
mkdir -p models/control_v11p_sd21_canny_paddle
```

#### 步骤3：重启服务器
```bash
python start_server_aistudio.py runserver 0.0.0.0:8080
```

#### 步骤4：测试API
```bash
python test_api.py
```

## 验证修复

### 检查API响应
访问 `http://localhost:8080/api/getType` 应该返回JSON数据：
```json
{
  "model": "SD21",
  "type": "inpaint",
  "cnModel": "control_sd2.1_base_canny",
  "loraList": ["thangka_21_Status_140", "thangka_21_ACD_250"],
  "cnList": ["control_v11p_sd21_canny_paddle"]
}
```

### 检查前端
前端应该能正常加载模型类型，不再出现JSON解析错误。

## 常见问题

### 如果API仍然返回HTML
1. 检查Django服务器是否正常运行
2. 检查URL路径是否正确
3. 检查服务器日志中的错误信息

### 如果NumPy错误仍然存在
1. 重启Python环境
2. 清除所有缓存
3. 重新安装所有依赖

## 成功标志
- ✅ 前端不再显示JSON解析错误
- ✅ 模型类型列表正常加载
- ✅ 藏文字体初始化完成
- ✅ 系统可以正常使用



