#!/bin/bash
# 先进唐卡系统部署脚本 - wangchukMind

set -e

echo "🚀 开始部署先进唐卡系统..."

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查NVIDIA Docker支持
if ! docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi &> /dev/null; then
    echo "⚠️ NVIDIA Docker支持未检测到，将使用CPU模式"
fi

# 创建必要目录
mkdir -p models logs cache temp ssl

# 构建镜像
echo "🔧 构建Docker镜像..."
docker-compose -f docker-compose.advanced.yml build

# 启动服务
echo "🚀 启动服务..."
docker-compose -f docker-compose.advanced.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.advanced.yml ps

# 检查健康状态
echo "🏥 检查健康状态..."
curl -f http://localhost:8080/health || echo "⚠️ 健康检查失败"

echo "✅ 部署完成！"
echo "🌐 访问地址: http://localhost:8080"
echo "📊 监控地址: http://localhost:8080/admin"
