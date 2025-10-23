from django.apps import AppConfig
import os

class ServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server"
    
    def ready(self):
        # 只在主进程中运行，避免在worker进程中重复加载
        if os.environ.get("RUN_MAIN", None) != "true":
            return
            
        # 检查是否跳过模型加载
        if os.environ.get("SKIP_MODEL_LOADING") == "1":
            print("跳过模型加载")
            return
            
        try:
            print("正在预加载AI模型...")
            # 使用PaddlePaddle版本的模型
            from .models import diffusion_paddle as diffusion
            
            # 预加载默认的inpaint模型
            diffusion.loadModel("inpaint", "SD21", None)
            print("✅ AI模型预加载完成 (PaddlePaddle版本)")
            
        except Exception as e:
            print(f"⚠️ AI模型预加载失败: {e}")
            print("模型将在首次使用时动态加载")
