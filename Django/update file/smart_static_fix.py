#!/usr/bin/env python3
"""
智能静态文件修复脚本
自动检测环境并修复静态文件问题
"""
import os
import sys
import shutil
import subprocess

def detect_environment():
    """检测当前环境"""
    print("🔍 检测当前环境...")
    
    # 检查是否在AI Studio
    if os.path.exists('/home/aistudio'):
        print("✅ 检测到AI Studio环境")
        return 'aistudio'
    else:
        print("✅ 检测到本地环境")
        return 'local'

def find_static_files():
    """查找静态文件位置"""
    print("🔍 查找静态文件位置...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(current_dir, "server", "static"),
        os.path.join(current_dir, "static"),
        "/home/aistudio/work/wangchukthangka/Thangka/Django/server/static",
        "/home/aistudio/work/wangchukthangka/Thangka/Django/static"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            images_dir = os.path.join(path, "images")
            if os.path.exists(images_dir):
                logo_files = ["paddlepaddle-logo.png", "scu-logo.png", "utibet-logo.png"]
                all_exist = all(os.path.exists(os.path.join(images_dir, f)) for f in logo_files)
                if all_exist:
                    print(f"✅ 找到静态文件目录: {path}")
                    return path
    
    print("❌ 未找到静态文件目录")
    return None

def fix_settings_py(static_path, environment):
    """修复settings.py文件"""
    print("🔧 修复settings.py文件...")
    
    settings_file = "server/settings.py"
    if not os.path.exists(settings_file):
        print(f"❌ settings.py文件不存在: {settings_file}")
        return False
    
    # 读取当前内容
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建新的静态文件配置
    if environment == 'aistudio':
        new_config = f'''# AI Studio 静态文件配置 - wangchukMind
if os.path.exists('/home/aistudio'):
    # AI Studio环境，使用检测到的路径
    STATICFILES_DIRS = [
        '{static_path}',
    ]
    STATIC_ROOT = '/home/aistudio/work/wangchukthangka/Thangka/Django/staticfiles'
else:
    # 本地环境
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'server', 'static'),
    ]'''
    else:
        new_config = f'''# 本地环境静态文件配置 - wangchukMind
STATICFILES_DIRS = [
    '{static_path}',
]'''
    
    # 替换配置
    if 'AI Studio 静态文件配置' in content:
        # 更新现有配置
        start_marker = '# AI Studio 静态文件配置'
        end_marker = 'else:\n    # 本地环境\n    STATICFILES_DIRS = [\n        os.path.join(BASE_DIR, \'server\', \'static\'),\n    ]'
        
        if end_marker in content:
            old_config = content[content.find(start_marker):content.find(end_marker) + len(end_marker)]
            content = content.replace(old_config, new_config)
        else:
            # 如果格式不匹配，直接替换整个静态文件配置部分
            content = content.replace('# AI Studio 静态文件配置', new_config)
    else:
        # 添加新配置
        content = content.replace(
            "STATICFILES_DIRS = [\n    os.path.join(BASE_DIR, 'server', 'static'),\n]",
            new_config
        )
    
    # 写回文件
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ settings.py已更新")
    return True

def fix_urls_py(static_path, environment):
    """修复urls.py文件"""
    print("🔧 修复urls.py文件...")
    
    urls_file = "server/urls.py"
    if not os.path.exists(urls_file):
        print(f"❌ urls.py文件不存在: {urls_file}")
        return False
    
    # 读取当前内容
    with open(urls_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建新的URL配置
    if environment == 'aistudio':
        new_url_config = f'''# 添加静态文件支持 - wangchukMind
if settings.DEBUG or os.path.exists('/home/aistudio'):
    # DEBUG模式或AI Studio环境，使用检测到的路径
    if os.path.exists('/home/aistudio'):
        # AI Studio环境，使用检测到的路径
        static_root = '{static_path}'
    else:
        # 本地DEBUG模式
        static_root = settings.STATICFILES_DIRS[0]
    
    urlpatterns += static(settings.STATIC_URL, document_root=static_root)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 生产环境使用STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''
    else:
        new_url_config = f'''# 添加静态文件支持 - wangchukMind
if settings.DEBUG:
    # DEBUG模式，使用检测到的路径
    urlpatterns += static(settings.STATIC_URL, document_root='{static_path}')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 生产环境使用STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''
    
    # 替换现有配置
    if '# 添加静态文件支持' in content:
        # 找到并替换现有配置
        start_marker = '# 添加静态文件支持'
        end_marker = 'urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'
        
        if end_marker in content:
            old_config = content[content.find(start_marker):content.find(end_marker) + len(end_marker)]
            content = content.replace(old_config, new_url_config)
        else:
            # 如果格式不匹配，尝试其他方式
            lines = content.split('\n')
            new_lines = []
            skip_until_end = False
            
            for line in lines:
                if '# 添加静态文件支持' in line:
                    skip_until_end = True
                    new_lines.append(new_url_config)
                elif skip_until_end and 'urlpatterns += static(settings.MEDIA_URL' in line:
                    skip_until_end = False
                    continue
                elif not skip_until_end:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
    else:
        # 添加新配置
        content += f'\n\n{new_url_config}'
    
    # 写回文件
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ urls.py已更新")
    return True

def collect_static_files(static_path, environment):
    """收集静态文件"""
    print("📁 收集静态文件...")
    
    try:
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        import django
        django.setup()
        
        # 使用Django的collectstatic命令
        from django.core.management import call_command
        call_command('collectstatic', '--noinput', '--clear')
        print("✅ Django collectstatic完成")
        return True
        
    except Exception as e:
        print(f"❌ Django collectstatic失败: {e}")
        print("💡 尝试手动复制...")
        
        # 手动复制静态文件
        try:
            if environment == 'aistudio':
                static_dest = '/home/aistudio/work/wangchukthangka/Thangka/Django/staticfiles'
            else:
                static_dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles')
            
            if os.path.exists(static_dest):
                shutil.rmtree(static_dest)
            shutil.copytree(static_path, static_dest)
            print("✅ 静态文件手动复制完成")
            return True
            
        except Exception as e2:
            print(f"❌ 手动复制失败: {e2}")
            return False

def test_static_files(static_path):
    """测试静态文件访问"""
    print("🧪 测试静态文件访问...")
    
    images_dir = os.path.join(static_path, "images")
    logo_files = ["paddlepaddle-logo.png", "scu-logo.png", "utibet-logo.png"]
    
    for logo_file in logo_files:
        logo_path = os.path.join(images_dir, logo_file)
        if os.path.exists(logo_path):
            print(f"✅ {logo_file} 存在")
        else:
            print(f"❌ {logo_file} 缺失")
    
    return True

def main():
    """主函数"""
    print("🚀 智能静态文件修复脚本")
    print("=" * 50)
    
    # 步骤1: 检测环境
    environment = detect_environment()
    
    # 步骤2: 查找静态文件
    static_path = find_static_files()
    if not static_path:
        print("❌ 未找到静态文件，请检查文件结构")
        return False
    
    # 步骤3: 修复settings.py
    if not fix_settings_py(static_path, environment):
        print("❌ settings.py修复失败")
        return False
    
    # 步骤4: 修复urls.py
    if not fix_urls_py(static_path, environment):
        print("❌ urls.py修复失败")
        return False
    
    # 步骤5: 收集静态文件
    if not collect_static_files(static_path, environment):
        print("❌ 静态文件收集失败")
        return False
    
    # 步骤6: 测试静态文件
    test_static_files(static_path)
    
    print("\n🎉 静态文件修复完成！")
    print("\n📋 下一步操作:")
    print("1. 重启Django服务器")
    print("2. 检查Logo是否正常显示")
    print("3. 如果仍有问题，检查浏览器开发者工具")
    
    return True

if __name__ == "__main__":
    if main():
        print("\n✅ 修复成功！")
    else:
        print("\n❌ 修复失败！")
        sys.exit(1)



