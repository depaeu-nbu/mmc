from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

# 获取配置文件中定义的logger,用来记录日志
logger = logging.getLogger('django')

def exception_handler(exc, context):
    """自定义异常处理方法"""
    # 调用drf原生异常处理方法
    response = drf_exception_handler(exc, context)

    if response is None:
        # 用户访问的视图
        view = context['view']
        # 判断是否是数据库的异常
        if isinstance(exc, DatabaseError) or isinstance(RedisError):
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
            return response
