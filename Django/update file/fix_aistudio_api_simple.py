#!/usr/bin/env python3
"""
修复AI Studio自动生成API地址的问题 - 简化版
"""
import os
import re

def fix_template_file(file_path):
    """修复模板文件中的API URLs"""
    print(f"🔧 修复 {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加动态API配置
    api_config = """
    // 动态API配置 - AI Studio兼容
    const API_BASE_URL = window.location.origin;
    const API_ENDPOINTS = {
        getType: API_BASE_URL + '/api/getType',
        generate: API_BASE_URL + '/stream/generate',
        getImg: API_BASE_URL + '/api/getImg',
        changePipe: API_BASE_URL + '/api/changePipe',
        generateDirect: API_BASE_URL + '/api/generate'
    };
    """
    
    # 在第一个script标签后添加API配置
    if 'const API_BASE_URL' not in content:
        content = content.replace(
            '<script>',
            f'<script>\n{api_config}'
        )
    
    # 替换硬编码的API路径
    replacements = {
        "fetch('/api/getType'": "fetch(API_ENDPOINTS.getType",
        "fetch('/stream/generate'": "fetch(API_ENDPOINTS.generate",
        "fetch('/api/getImg'": "fetch(API_ENDPOINTS.getImg",
        "fetch('/api/changePipe'": "fetch(API_ENDPOINTS.changePipe",
        "fetch('/api/generate'": "fetch(API_ENDPOINTS.generateDirect",
        "const testUrl = `/api/getImg?filename=${filename}&path=output`": "const testUrl = `${API_ENDPOINTS.getImg}?filename=${filename}&path=output`"
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} 修复完成")

def main():
    """主函数"""
    print("🚀 修复AI Studio API URLs")
    print("=" * 50)
    
    # 修复index.html
    if os.path.exists("server/templates/index.html"):
        fix_template_file("server/templates/index.html")
    
    # 修复index copy.html
    if os.path.exists("server/templates/index copy.html"):
        fix_template_file("server/templates/index copy.html")
    
    print("\n🎉 AI Studio API URLs修复完成！")
    print("\n📋 说明:")
    print("1. 前端现在使用动态API URLs")
    print("2. 自动适配AI Studio的自动生成API地址")
    print("3. 本地环境也能正常工作")
    
    return True

if __name__ == "__main__":
    main()



