# shared/decorators.py
import logging
from rest_framework.response import Response
from rest_framework import status
from .exceptions import AIRequestError

logger = logging.getLogger(__name__)

def handle_view_exception(view_func):
    """处理视图异常的装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except AIRequestError as e:
            logger.error(f"AI请求异常: {str(e)}")
            return Response(
                {"error": "AI服务暂时不可用，请稍后再试"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.exception("处理请求时发生未预期错误")
            return Response(
                {"error": "服务器内部错误"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper
