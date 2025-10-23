# 优化的diffusion_paddle_aistudio.py补丁 - wangchukMind

# 在changeModel函数中添加以下代码：

def optimize_pipe_performance(pipe):
    """优化pipe性能"""
    if pipe is None:
        return pipe
    
    try:
        print("🔧 开始pipe性能优化...")
        
        # 1. 内存优化
        if hasattr(pipe, 'enable_attention_slicing'):
            pipe.enable_attention_slicing()
            print("✅ 启用注意力切片")
        
        # 2. 编译优化
        if hasattr(pipe, 'compile'):
            pipe.compile()
            print("✅ 启用模型编译")
        
        # 3. 缓存优化
        if hasattr(pipe, 'enable_attention_caching'):
            pipe.enable_attention_caching()
            print("✅ 启用注意力缓存")
        
        print("✅ pipe性能优化完成")
        
    except Exception as e:
        print(f"⚠️ pipe性能优化失败: {e}")
    
    return pipe

# 在changeModel函数的return语句前添加：
pipe = optimize_pipe_performance(pipe)
