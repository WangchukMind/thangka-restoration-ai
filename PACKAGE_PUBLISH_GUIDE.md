# 📦 唐卡修复大师 - 包发布指南

## 🎯 发布策略

我们采用多平台发布策略，确保不同用户群体都能方便地使用我们的产品：

### 1. **GitHub Packages** (主要)
- **npm包**: `@wangchukmind/thangka-repair-ai`
- **Docker镜像**: `ghcr.io/wangchukmind/thangka-restoration-ai`
- **优势**: 与代码仓库集成，私有包管理

### 2. **公共npm Registry** (可选)
- **npm包**: `thangka-repair-ai`
- **优势**: 公开可见，便于发现和使用

## 🚀 发布流程

### 自动发布 (推荐)

#### 1. 创建版本标签
```bash
# 更新版本号
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0

# 推送标签
git push origin v1.0.0
```

#### 2. 触发自动发布
- 推送标签后，GitHub Actions会自动：
  - 构建应用
  - 运行测试
  - 发布npm包到GitHub Packages
  - 构建并推送Docker镜像
  - 创建GitHub Release

### 手动发布

#### 1. 发布npm包到GitHub Packages
```bash
# 登录GitHub Packages
npm login --registry=https://npm.pkg.github.com

# 发布包
npm publish
```

#### 2. 发布Docker镜像
```bash
# 构建镜像
docker build -t ghcr.io/wangchukmind/thangka-restoration-ai .

# 登录GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# 推送镜像
docker push ghcr.io/wangchukmind/thangka-restoration-ai
```

#### 3. 发布到公共npm Registry
```bash
# 登录npm
npm login

# 发布到公共registry
npm publish --registry=https://registry.npmjs.org
```

## 📋 发布前检查清单

### 代码质量
- [ ] 所有测试通过
- [ ] 代码lint检查通过
- [ ] 类型检查通过
- [ ] 构建成功

### 版本管理
- [ ] 更新版本号
- [ ] 更新CHANGELOG.md
- [ ] 更新README.md
- [ ] 检查依赖版本

### 文档更新
- [ ] API文档更新
- [ ] 使用说明更新
- [ ] 部署指南更新
- [ ] 示例代码更新

### 安全检查
- [ ] 依赖安全扫描
- [ ] 敏感信息检查
- [ ] 权限配置检查

## 🔧 配置说明

### package.json 关键配置
```json
{
  "name": "@wangchukmind/thangka-repair-ai",
  "publishConfig": {
    "registry": "https://npm.pkg.github.com",
    "@wangchukmind:registry": "https://npm.pkg.github.com"
  }
}
```

### .npmrc 配置
```
@wangchukmind:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}
```

### Docker 配置
```dockerfile
LABEL org.opencontainers.image.source="https://github.com/WangchukMind/thangka-restoration-ai"
LABEL org.opencontainers.image.licenses="MIT"
```

## 📊 使用统计

### npm包使用
```bash
# 查看包信息
npm view @wangchukmind/thangka-repair-ai

# 查看下载统计
npm view @wangchukmind/thangka-repair-ai downloads
```

### Docker镜像使用
```bash
# 查看镜像信息
docker inspect ghcr.io/wangchukmind/thangka-restoration-ai

# 查看镜像标签
docker images ghcr.io/wangchukmind/thangka-restoration-ai
```

## 🎯 用户安装指南

### 方式1: npm包安装
```bash
# 安装包
npm install @wangchukmind/thangka-repair-ai

# 使用
import { ThangkaRepair } from '@wangchukmind/thangka-repair-ai';
```

### 方式2: Docker镜像使用
```bash
# 拉取镜像
docker pull ghcr.io/wangchukmind/thangka-restoration-ai:latest

# 运行容器
docker run -p 3000:3000 -p 8000:8000 ghcr.io/wangchukmind/thangka-restoration-ai:latest
```

### 方式3: 源码安装
```bash
# 克隆仓库
git clone https://github.com/WangchukMind/thangka-restoration-ai.git

# 安装依赖
npm install

# 启动应用
npm start
```

## 🔄 版本管理策略

### 语义化版本 (SemVer)
- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 版本标签
- `latest`: 最新稳定版
- `beta`: 测试版本
- `alpha`: 开发版本

### 分支策略
- `main`: 主分支，发布稳定版本
- `develop`: 开发分支，集成新功能
- `feature/*`: 功能分支
- `hotfix/*`: 热修复分支

## 📈 监控和维护

### 包健康监控
- 下载量统计
- 依赖安全扫描
- 用户反馈收集
- 错误日志监控

### 定期维护
- 依赖更新
- 安全补丁
- 性能优化
- 文档更新

## 🚨 故障排除

### 常见问题

#### 1. 发布失败
```bash
# 检查权限
npm whoami --registry=https://npm.pkg.github.com

# 检查包名
npm view @wangchukmind/thangka-repair-ai
```

#### 2. Docker推送失败
```bash
# 检查登录状态
docker system info

# 检查镜像标签
docker images | grep thangka
```

#### 3. 权限问题
- 确保有GitHub Packages写入权限
- 检查GITHUB_TOKEN配置
- 验证组织权限设置

## 📞 技术支持

- **GitHub Issues**: https://github.com/WangchukMind/thangka-restoration-ai/issues
- **文档**: https://github.com/WangchukMind/thangka-restoration-ai#readme
- **开发者**: Wangchuk Mind

---

**让唐卡修复技术以最便捷的方式传播到全世界！** 🌍
