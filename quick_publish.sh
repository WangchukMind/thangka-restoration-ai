#!/bin/bash
# 唐卡修复大师 - 快速发布脚本
# 一键发布npm包和Docker镜像
# Developed by Wangchuk Mind

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印横幅
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║              📦 唐卡修复大师 - 快速发布工具 📦                ║"
    echo "║                                                              ║"
    echo "║        一键发布npm包和Docker镜像到GitHub Packages            ║"
    echo "║                                                              ║"
    echo "║  🚀 自动构建  📦 包发布  🐳 镜像推送  🏷️ 版本管理            ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 检查依赖
check_dependencies() {
    echo -e "${YELLOW}🔍 检查依赖...${NC}"
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js 未安装${NC}"
        exit 1
    fi
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm 未安装${NC}"
        exit 1
    fi
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker 未安装${NC}"
        exit 1
    fi
    
    # 检查Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git 未安装${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 依赖检查通过${NC}"
}

# 检查Git状态
check_git_status() {
    echo -e "${YELLOW}🔍 检查Git状态...${NC}"
    
    # 检查是否有未提交的更改
    if ! git diff-index --quiet HEAD --; then
        echo -e "${RED}❌ 有未提交的更改，请先提交${NC}"
        git status
        exit 1
    fi
    
    # 检查是否在main分支
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "main" ]; then
        echo -e "${YELLOW}⚠️  当前分支: $current_branch，建议在main分支发布${NC}"
        read -p "是否继续? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✅ Git状态检查通过${NC}"
}

# 运行测试
run_tests() {
    echo -e "${YELLOW}🧪 运行测试...${NC}"
    
    # 安装依赖
    echo "📦 安装依赖..."
    npm install
    cd client && npm install && cd ..
    
    # 运行测试
    echo "🔬 运行测试..."
    npm run test || {
        echo -e "${RED}❌ 测试失败${NC}"
        exit 1
    }
    
    echo -e "${GREEN}✅ 测试通过${NC}"
}

# 构建应用
build_application() {
    echo -e "${YELLOW}🔨 构建应用...${NC}"
    
    # 构建前端
    echo "🎨 构建前端..."
    cd client
    npm run build
    cd ..
    
    # 构建后端
    echo "⚙️ 构建后端..."
    npm run build:server
    
    echo -e "${GREEN}✅ 构建完成${NC}"
}

# 发布npm包
publish_npm() {
    echo -e "${YELLOW}📦 发布npm包...${NC}"
    
    # 登录GitHub Packages
    echo "🔐 登录GitHub Packages..."
    npm login --registry=https://npm.pkg.github.com
    
    # 发布包
    echo "🚀 发布包..."
    npm publish --registry=https://npm.pkg.github.com
    
    echo -e "${GREEN}✅ npm包发布成功${NC}"
}

# 发布Docker镜像
publish_docker() {
    echo -e "${YELLOW}🐳 发布Docker镜像...${NC}"
    
    # 获取版本号
    version=$(node -p "require('./package.json').version")
    image_name="ghcr.io/wangchukmind/thangka-restoration-ai"
    
    # 构建镜像
    echo "🔨 构建Docker镜像..."
    docker build -t $image_name:$version .
    docker build -t $image_name:latest .
    
    # 登录GitHub Container Registry
    echo "🔐 登录GitHub Container Registry..."
    echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin
    
    # 推送镜像
    echo "🚀 推送镜像..."
    docker push $image_name:$version
    docker push $image_name:latest
    
    echo -e "${GREEN}✅ Docker镜像发布成功${NC}"
}

# 创建Git标签
create_git_tag() {
    echo -e "${YELLOW}🏷️ 创建Git标签...${NC}"
    
    # 获取版本号
    version=$(node -p "require('./package.json').version")
    tag="v$version"
    
    # 创建标签
    git tag -a $tag -m "Release $tag"
    git push origin $tag
    
    echo -e "${GREEN}✅ Git标签创建成功: $tag${NC}"
}

# 显示发布信息
show_publish_info() {
    echo -e "${GREEN}"
    echo "🎉 发布完成！"
    echo "=" * 50
    echo "📦 npm包: @wangchukmind/thangka-repair-ai"
    echo "🐳 Docker镜像: ghcr.io/wangchukmind/thangka-restoration-ai"
    echo "🏷️ 版本: $(node -p "require('./package.json').version")"
    echo "=" * 50
    echo -e "${NC}"
}

# 主函数
main() {
    print_banner
    
    # 检查参数
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "用法: $0 [选项]"
        echo "选项:"
        echo "  --help, -h     显示帮助信息"
        echo "  --skip-tests   跳过测试"
        echo "  --npm-only     只发布npm包"
        echo "  --docker-only  只发布Docker镜像"
        exit 0
    fi
    
    # 检查依赖
    check_dependencies
    
    # 检查Git状态
    check_git_status
    
    # 运行测试（除非跳过）
    if [ "$1" != "--skip-tests" ]; then
        run_tests
    fi
    
    # 构建应用
    build_application
    
    # 发布npm包（除非只发布Docker）
    if [ "$1" != "--docker-only" ]; then
        publish_npm
    fi
    
    # 发布Docker镜像（除非只发布npm）
    if [ "$1" != "--npm-only" ]; then
        publish_docker
    fi
    
    # 创建Git标签
    create_git_tag
    
    # 显示发布信息
    show_publish_info
}

# 运行主函数
main "$@"
