# 唐卡修复大师 - Docker镜像
# Multi-stage build for production optimization
# Developed by Wangchuk Mind

# Stage 1: Base image with Python and Node.js
FROM node:18-alpine AS base

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    build-base \
    linux-headers \
    libffi-dev \
    openssl-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    libimagequant-dev \
    libxcb-dev \
    libpng-dev

# Create app directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY client/package*.json ./client/

# Stage 2: Install dependencies
FROM base AS dependencies

# Install Python dependencies
COPY Django/requirements_paddle.txt ./
RUN pip3 install --no-cache-dir -r requirements_paddle.txt

# Install Node.js dependencies
RUN npm ci --only=production
RUN cd client && npm ci --only=production

# Stage 3: Build application
FROM base AS builder

# Copy source code
COPY . .

# Install all dependencies (including dev)
RUN npm ci
RUN cd client && npm ci

# Build client
RUN cd client && npm run build

# Stage 4: Production image
FROM base AS production

# Copy Python dependencies
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy built application
COPY --from=builder /app/client/build ./client/build
COPY --from=builder /app/Django ./Django
COPY --from=builder /app/start_mvp_product.py ./
COPY --from=builder /app/deploy_kiosk.py ./
COPY --from=builder /app/mvp_analytics.py ./

# Copy configuration files
COPY --from=builder /app/package.json ./
COPY --from=builder /app/kiosk_config.json ./
COPY --from=builder /app/touch_config.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S thangka -u 1001

# Set ownership
RUN chown -R thangka:nodejs /app
USER thangka

# Create necessary directories
RUN mkdir -p /app/Django/server/media/mvp_uploads
RUN mkdir -p /app/Django/server/media/mvp_results
RUN mkdir -p /app/Django/server/static/mvp
RUN mkdir -p /app/logs

# Expose ports
EXPOSE 3000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/mvp/stats/ || exit 1

# Environment variables
ENV NODE_ENV=production
ENV PYTHONPATH=/app/Django
ENV DJANGO_SETTINGS_MODULE=server.settings
ENV PADDLE_FRAMEWORK=paddle
ENV PADDLE_DEVICE=cpu
ENV MVP_MODE=true
ENV SIMPLIFIED_UI=true

# Default command
CMD ["python3", "start_mvp_product.py", "--production"]

# Labels for metadata
LABEL maintainer="Wangchuk Mind <wangchukmind@example.com>"
LABEL version="1.0.0"
LABEL description="AI-powered Thangka restoration system"
LABEL org.opencontainers.image.source="https://github.com/WangchukMind/thangka-restoration-ai"
LABEL org.opencontainers.image.licenses="MIT"