#!/usr/bin/env python3
"""
修复AI Studio自动生成API地址的问题
动态配置前端API调用URL
"""
import os
import re

def detect_aistudio_environment():
    """检测是否在AI Studio环境"""
    return os.path.exists('/home/aistudio')

def get_base_url():
    """获取基础URL"""
    if detect_aistudio_environment():
        # AI Studio环境，使用相对路径
        return ""
    else:
        # 本地环境，使用相对路径
        return ""

def fix_api_urls():
    """修复API URLs"""
    print("🔧 修复AI Studio API URLs...")
    
    # 检查是否在AI Studio环境
    if not detect_aistudio_environment():
        print("⚠️ 不在AI Studio环境，跳过API URL修复")
        return True
    
    # 修复index.html
    index_file = "server/templates/index.html"
    if os.path.exists(index_file):
        print(f"📝 修复 {index_file}...")
        fix_template_file(index_file)
    
    # 修复index copy.html
    index_copy_file = "server/templates/index copy.html"
    if os.path.exists(index_copy_file):
        print(f"📝 修复 {index_copy_file}...")
        fix_template_file(index_copy_file)
    
    return True

def fix_template_file(file_path):
    """修复模板文件中的API URLs"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义需要修复的API路径
    api_paths = [
        '/api/getType',
        '/stream/generate',
        '/api/getImg',
        '/api/changePipe',
        '/api/generate'
    ]
    
    # 创建动态API配置
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
    
    # 在script标签开始后添加API配置
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

def create_api_config_script():
    """创建API配置脚本"""
    config_script = '''#!/usr/bin/env python3
"""
AI Studio API配置脚本
自动检测并配置正确的API URLs
"""
import os
import re

def get_aistudio_api_url():
    """获取AI Studio API URL"""
    # 检查环境变量
    api_url = os.environ.get('AISTUDIO_API_URL')
    if api_url:
        return api_url
    
    # 检查是否有API URL文件
    api_file = '/home/aistudio/.api_url'
    if os.path.exists(api_file):
        with open(api_file, 'r') as f:
            return f.read().strip()
    
    # 默认返回空（使用相对路径）
    return ""

def update_django_settings():
    """更新Django设置"""
    settings_file = 'server/settings.py'
    if not os.path.exists(settings_file):
        return False
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加AI Studio API URL配置
    api_config = '''
# AI Studio API URL配置
AISTUDIO_API_URL = get_aistudio_api_url()
if AISTUDIO_API_URL:
    ALLOWED_HOSTS = ['*']  # AI Studio需要允许所有主机
    CSRF_TRUSTED_ORIGINS = [AISTUDIO_API_URL]
'''
    
    if 'AISTUDIO_API_URL' not in content:
        content += api_config
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Django设置已更新")
        return True
    
    return True

if __name__ == "__main__":
    update_django_settings()
'''
    
    with open('configure_aistudio_api.py', 'w', encoding='utf-8') as f:
        f.write(config_script)
    
    print("✅ API配置脚本已创建: configure_aistudio_api.py")

def main():
    """主函数"""
    print("🚀 修复AI Studio API URLs")
    print("=" * 50)
    
    # 步骤1: 修复模板文件
    print("\n📋 步骤1: 修复模板文件中的API URLs")
    if not fix_api_urls():
        print("❌ 模板文件修复失败")
        return False
    
    # 步骤2: 创建API配置脚本
    print("\n📋 步骤2: 创建API配置脚本")
    create_api_config_script()
    
    print("\n🎉 AI Studio API URLs修复完成！")
    print("\n📋 下一步操作:")
    print("1. 在AI Studio中运行: python configure_aistudio_api.py")
    print("2. 重启Django服务器")
    print("3. 检查API调用是否正常")
    
    return True

if __name__ == "__main__":
    if main():
        print("\n✅ 修复成功！")
    else:
        print("\n❌ 修复失败！")
        exit(1)



