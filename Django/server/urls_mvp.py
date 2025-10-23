"""
MVP产品URL配置 - 唐卡修复大师
简化用户体验，专注核心功能
Developed by Wangchuk Mind
"""

from django.urls import path
from .views import mvp_views

urlpatterns = [
    # 修复相关API
    path('api/mvp/modes/', mvp_views.get_repair_modes, name='mvp_modes'),
    path('api/mvp/analyze/', mvp_views.analyze_image, name='mvp_analyze'),
    path('api/mvp/repair/start/', mvp_views.start_repair, name='mvp_start_repair'),
    path('api/mvp/repair/progress/', mvp_views.get_repair_progress, name='mvp_progress'),
    path('api/mvp/repair/result/', mvp_views.get_repair_result, name='mvp_result'),
    path('api/mvp/repair/stream/', mvp_views.stream_repair, name='mvp_stream_repair'),
    
    # 文化知识API
    path('api/mvp/knowledge/', mvp_views.get_cultural_knowledge, name='mvp_knowledge'),
    
    # 用户历史API
    path('api/mvp/history/save/', mvp_views.save_repair_history, name='mvp_save_history'),
    path('api/mvp/history/', mvp_views.get_user_history, name='mvp_get_history'),
    
    # 统计信息API
    path('api/mvp/stats/', mvp_views.get_app_statistics, name='mvp_stats'),
]
