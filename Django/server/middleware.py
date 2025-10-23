"""
自定义中间件，确保API端点始终返回JSON响应
"""

import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JsonResponseMiddleware(MiddlewareMixin):
    """
    确保API端点始终返回JSON响应，即使发生错误
    """
    
    def process_exception(self, request, exception):
        """
        处理异常，确保API端点返回JSON错误响应
        """
        # 只对API端点应用此中间件
        api_endpoints = [
            '/generate/',
            '/changePipe/',
            '/getType/',
            '/test/',
            '/getImg/',
            '/getToken/',
            '/getPipeType/',
            '/edgeInpaint/',
            '/chat/',
            '/translate/',
            '/refine/',
            '/getHistory/',
            '/setBaseline/',
            '/copyAsBaseline/',
            '/send_img/'
        ]
        
        # 检查是否是API端点
        is_api_endpoint = any(request.path.startswith(endpoint) for endpoint in api_endpoints)
        
        if is_api_endpoint:
            # 返回JSON错误响应
            error_response = {
                'msg': 'error',
                'error': str(exception),
                'error_type': type(exception).__name__
            }
            
            return JsonResponse(error_response, status=500)
        
        # 对于非API端点，返回None让Django处理
        return None

    def process_response(self, request, response):
        """
        确保API端点始终返回JSON响应，即使视图返回了非JSON响应
        """
        api_endpoints = [
            '/generate/',
            '/changePipe/',
            '/getType/',
            '/test/',
            '/getImg/',
            '/getToken/',
            '/getPipeType/',
            '/edgeInpaint/',
            '/chat/',
            '/translate/',
            '/refine/',
            '/getHistory/',
            '/setBaseline/',
            '/copyAsBaseline/',
            '/send_img/'
        ]
        
        is_api_endpoint = any(request.path.startswith(endpoint) for endpoint in api_endpoints)

        if is_api_endpoint and not response.headers.get('content-type', '').startswith('application/json'):
            # 检查是否有跳过JSON转换的标记
            if hasattr(response, '_skip_json_conversion') and response._skip_json_conversion:
                return response
                
            # 如果是API端点但响应不是JSON，尝试转换为JSON
            try:
                # 尝试从响应内容中获取错误信息或默认信息
                content = response.content.decode('utf-8')
                error_msg = "未知错误" # 默认错误信息

                # 尝试解析HTML获取错误信息
                if "<!DOCTYPE html>" in content or "<html>" in content:
                    # 这是一个HTML页面，我们不能直接解析，所以返回通用错误
                    error_msg = "服务器返回了非JSON响应，可能是HTML错误页面。"
                else:
                    # 尝试解析为文本
                    error_msg = content

                error_response = {
                    'msg': 'error',
                    'error': error_msg,
                    'error_type': 'NonJsonResponse'
                }
                return JsonResponse(error_response, status=response.status_code)
            except Exception as e:
                # 如果转换失败，返回通用JSON错误
                return JsonResponse({'msg': 'error', 'error': f'Middleware JSON conversion failed: {e}', 'error_type': 'MiddlewareError'}, status=500)

        return response
