#!/usr/bin/env python3
"""
修复AI Studio中静态文件显示问题的脚本
解决Logo不显示的问题
"""
import os
import sys
import shutil
import subprocess

def fix_static_files():
    """修复静态文件问题"""
    print("🔧 修复静态文件显示问题...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置Django环境
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    sys.path.insert(0, current_dir)
    
    try:
        import django
        django.setup()
        
        # 方法1: 使用Django的collectstatic命令
        print("📁 方法1: 使用Django collectstatic命令...")
        from django.core.management import call_command
        call_command('collectstatic', '--noinput', '--clear')
        print("✅ Django collectstatic 完成")
        
    except Exception as e:
        print(f"❌ Django collectstatic 失败: {e}")
        
        # 方法2: 手动复制静态文件
        print("📁 方法2: 手动复制静态文件...")
        try:
            static_source = os.path.join(current_dir, "server", "static")
            static_dest = os.path.join(current_dir, "staticfiles")
            
            if os.path.exists(static_source):
                if os.path.exists(static_dest):
                    shutil.rmtree(static_dest)
                shutil.copytree(static_source, static_dest)
                print("✅ 静态文件手动复制完成")
            else:
                print(f"❌ 静态文件源目录不存在: {static_source}")
                return False
                
        except Exception as e2:
            print(f"❌ 手动复制失败: {e2}")
            return False
    
    # 验证静态文件
    print("\n🔍 验证静态文件...")
    # AI Studio环境使用完整绝对路径
    static_dest = '/home/aistudio/work/wangchukthangka/Thangka/Django/staticfiles'
    images_dir = os.path.join(static_dest, "images")
    
    if os.path.exists(images_dir):
        logo_files = [
            "paddlepaddle-logo.png",
            "scu-logo.png", 
            "utibet-logo.png"
        ]
        
        for logo_file in logo_files:
            logo_path = os.path.join(images_dir, logo_file)
            if os.path.exists(logo_path):
                print(f"✅ Logo文件存在: {logo_file}")
            else:
                print(f"❌ Logo文件缺失: {logo_file}")
    else:
        print(f"❌ 图片目录不存在: {images_dir}")
        return False
    
    return True

def create_static_url_fix():
    """创建静态URL修复"""
    print("🔧 创建静态URL修复...")
    
    # 修改settings.py以强制使用STATICFILES_DIRS
    settings_file = "server/settings.py"
    if os.path.exists(settings_file):
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加AI Studio特殊配置
        ai_studio_config = '''
# AI Studio 静态文件配置 - wangchukMind
if os.path.exists('/home/aistudio'):
    # AI Studio环境，强制使用STATICFILES_DIRS
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'server', 'static'),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
'''
        
        if 'AI Studio 静态文件配置' not in content:
            # 在STATIC_URL配置后添加
            content = content.replace(
                "STATIC_URL = '/static/'",
                f"STATIC_URL = '/static/'\n{ai_studio_config}"
            )
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ settings.py 已更新")
        else:
            print("✅ settings.py 已包含AI Studio配置")
    
    return True

def main():
    """主函数"""
    print("🚀 修复AI Studio静态文件显示问题")
    print("=" * 50)
    
    # 步骤1: 修复静态文件
    print("\n📋 步骤1: 收集静态文件")
    if not fix_static_files():
        print("❌ 静态文件修复失败")
        return False
    
    # 步骤2: 创建静态URL修复
    print("\n📋 步骤2: 修复静态URL配置")
    if not create_static_url_fix():
        print("❌ 静态URL配置失败")
        return False
    
    print("\n🎉 静态文件修复完成！")
    print("\n📋 下一步操作:")
    print("1. 重启Django服务器")
    print("2. 检查Logo是否正常显示")
    print("3. 如果仍有问题，检查浏览器开发者工具的网络面板")
    
    return True

if __name__ == "__main__":
    if main():
        print("\n✅ 修复成功！")
    else:
        print("\n❌ 修复失败！")
        sys.exit(1)
