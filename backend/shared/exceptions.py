class AIRequestError(Exception):
    """AI服务请求异常"""
    pass


class FileProcessingError(Exception):
    """文件处理异常"""
    pass


def handle_view_exception(view_func):
    """处理视图异常的装饰器"""
    from functools import wraps
    from django.http import JsonResponse

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except AIRequestError as e:
            return JsonResponse({'error': str(e)}, status=503)
        except Exception as e:
            return JsonResponse({'error': '服务器内部错误'}, status=500)

    return wrapper
