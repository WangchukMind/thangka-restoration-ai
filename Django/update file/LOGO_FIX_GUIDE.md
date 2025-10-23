# AI Studio Logo显示问题修复指南

## 问题描述
在AI Studio部署后，页面底部的合作方Logo（PaddlePaddle、川大、西藏大学）不显示。

## 问题原因
1. **静态文件未收集**：AI Studio运行在生产模式，需要收集静态文件到`STATIC_ROOT`
2. **URL配置问题**：生产环境使用`STATIC_ROOT`，但静态文件仍在`STATICFILES_DIRS`
3. **路径映射错误**：Django无法正确映射静态文件URL

## 解决方案

### 方法1：一键修复（推荐）
```bash
python fix_static_files.py
```

### 方法2：手动修复

#### 步骤1：收集静态文件
```bash
python manage.py collectstatic --noinput --clear
```

#### 步骤2：验证静态文件
```bash
ls -la staticfiles/images/
# 应该看到：
# paddlepaddle-logo.png
# scu-logo.png
# utibet-logo.png
```

#### 步骤3：重启服务器
```bash
python start_server_aistudio.py runserver 0.0.0.0:8080
```

### 方法3：使用修复后的部署脚本
```bash
python start_server_aistudio.py runserver 0.0.0.0:8080
```
（已包含静态文件收集功能）

## 技术细节

### 修复内容
1. **settings.py**：添加AI Studio环境检测，强制使用`STATICFILES_DIRS`
2. **urls.py**：AI Studio环境使用`STATICFILES_DIRS`而不是`STATIC_ROOT`
3. **start_server_aistudio.py**：添加静态文件收集步骤

### 关键代码修改

#### settings.py
```python
# AI Studio 静态文件配置 - wangchukMind
if os.path.exists('/home/aistudio'):
    # AI Studio环境，强制使用STATICFILES_DIRS
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'server', 'static'),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

#### urls.py
```python
# 添加静态文件支持 - wangchukMind
if settings.DEBUG or os.path.exists('/home/aistudio'):
    # DEBUG模式或AI Studio环境，使用STATICFILES_DIRS
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
```

## 验证修复

### 检查静态文件
1. 访问 `http://localhost:8080/static/images/paddlepaddle-logo.png`
2. 应该能看到PaddlePaddle Logo图片

### 检查页面
1. 打开浏览器开发者工具
2. 查看Network面板
3. 刷新页面，检查是否有404错误

### 成功标志
- ✅ 页面底部显示三个Logo
- ✅ 浏览器开发者工具无404错误
- ✅ 静态文件URL可正常访问

## 常见问题

### 如果Logo仍然不显示
1. 检查浏览器缓存（Ctrl+F5强制刷新）
2. 检查Django服务器日志
3. 确认静态文件路径正确

### 如果出现500错误
1. 检查Django设置是否正确
2. 确认所有依赖已安装
3. 查看详细错误日志

## 文件清单
- `fix_static_files.py` - 静态文件修复脚本
- `start_server_aistudio.py` - 更新的部署脚本（包含静态文件收集）
- `server/settings.py` - 更新的Django设置
- `server/urls.py` - 更新的URL配置



