#!/usr/bin/env python3
"""
最终修复API配置问题
确保API_BASE_URL正确定义
"""
import os
import re

def fix_api_config():
    """修复API配置问题"""
    print("🔧 最终修复API配置问题...")
    
    template_file = "server/templates/index.html"
    if not os.path.exists(template_file):
        print(f"❌ 模板文件不存在: {template_file}")
        return False
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 正确的API配置
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
    
    # 查找第一个script标签
    script_pattern = r'<script>\s*'
    match = re.search(script_pattern, content)
    
    if match:
        # 检查是否已经有API配置
        if 'const API_BASE_URL' not in content[:match.end() + 2000]:  # 检查前2000个字符
            # 在第一个script标签后添加API配置
            content = content.replace(
                match.group(0),
                f'<script>{api_config}\n'
            )
            print("✅ API配置已添加到第一个script标签")
        else:
            print("✅ API配置已存在")
    else:
        print("❌ 未找到script标签")
        return False
    
    # 确保所有API调用都使用正确的端点
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
    
    # 删除重复的API配置（页面底部的）
    footer_pattern = r'</footer>\s*<script>\s*// 动态API配置.*?</script>'
    content = re.sub(footer_pattern, '</footer>\n    <script>', content, flags=re.DOTALL)
    
    # 写回文件
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ API配置修复完成")
    return True

def main():
    """主函数"""
    print("🚀 最终修复API配置问题")
    print("=" * 40)
    
    if fix_api_config():
        print("\n🎉 修复完成！")
        print("📋 现在刷新页面，API_BASE_URL应该正确定义了")
    else:
        print("\n❌ 修复失败！")

if __name__ == "__main__":
    main()



