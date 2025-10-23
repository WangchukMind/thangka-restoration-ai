#!/usr/bin/env python3
"""
快速修复API_BASE_URL未定义错误
"""
import os
import re

def fix_api_error():
    """修复API_BASE_URL未定义错误"""
    print("🔧 修复API_BASE_URL未定义错误...")
    
    template_file = "server/templates/index.html"
    if not os.path.exists(template_file):
        print(f"❌ 模板文件不存在: {template_file}")
        return False
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 确保API配置在第一个script标签中
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
        # 在第一个script标签后添加API配置
        if 'const API_BASE_URL' not in content[:match.end() + 1000]:  # 检查前1000个字符
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
    
    # 删除重复的API配置
    # 查找并删除页面底部的重复配置
    footer_pattern = r'</footer>\s*<script>\s*// 动态API配置.*?</script>'
    content = re.sub(footer_pattern, '</footer>\n    <script>', content, flags=re.DOTALL)
    
    # 写回文件
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ API错误修复完成")
    return True

def main():
    """主函数"""
    print("🚀 快速修复API错误")
    print("=" * 30)
    
    if fix_api_error():
        print("\n🎉 修复完成！")
        print("📋 现在刷新页面，API调用应该正常工作了")
    else:
        print("\n❌ 修复失败！")

if __name__ == "__main__":
    main()



