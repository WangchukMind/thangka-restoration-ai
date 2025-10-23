"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import RedirectView

def test_image_view(request):
    return render(request, 'test_image.html')
from django.conf import settings
from django.conf.urls.static import static
import time

from .models import thangka_paddle as thangka
from .models import ernie_bot_paddle as ernie_bot

def helloWorld(request):
    return render(request, 'index.html')

def debug_frontend(request):
    from django.http import HttpResponse
    with open('debug_frontend.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content)

def health_check(request):
    """AI Studio健康检查端点"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'thangka-ai',
        'version': '1.0.0',
        'timestamp': time.time()
    })

urlpatterns = [
    path('', helloWorld),
    path('debug/', debug_frontend),
    path('test-image/', test_image_view),
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('api/health', health_check),  # 添加API前缀
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),  # AI Studio健康检查
    path('getToken/', thangka.getToken),
    path('test/', thangka.test),
    path('generate/', thangka.generate),
    path('api/generate', thangka.generate),  # 添加API前缀路径
    path('stream/generate', thangka.generate),  # 使用generate函数，支持流式响应
    path('getImg/', thangka.send_img),
    path('send_img/', thangka.send_img),  # 添加send_img路由
    path('api/getImg', thangka.send_img),  # 添加API前缀
    path('changePipe/', thangka.changePipe),
    path('api/changePipe', thangka.changePipe),  # 添加API前缀
    path('getType/', thangka.getType),
    path('api/getType', thangka.getType),  # 添加API前缀
    path('getPipeType/', thangka.getType),  # 保持向后兼容
    path('edgeInpaint/', thangka.generate_edge),
    path('chat/', ernie_bot.chat),
    path('translate/', ernie_bot.translate),
    path('refine/', ernie_bot.optimize),
    path('getHistory/', thangka.get_history),
    path('setBaseline/', thangka.set_baseline),
    path('copyAsBaseline/', thangka.copy_as_baseline)
]

# 添加静态文件支持 - wangchukMind
if settings.DEBUG:
    # DEBUG模式，使用检测到的路径
    urlpatterns += static(settings.STATIC_URL, document_root='/Users/xiang/SCU/Xiang/Thangka/Paddle 3/Thangka/Django/server/static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 生产环境使用STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
