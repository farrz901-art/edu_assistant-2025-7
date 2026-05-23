# backend/shared/middleware.py
import traceback
from django.http import JsonResponse
import logging

logger = logging.getLogger('django')

class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': '服务器发生内部错误'}, status=500)


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            logger.error("未捕获异常：%s", str(e), exc_info=True, extra={'path': request.path})
            raise
