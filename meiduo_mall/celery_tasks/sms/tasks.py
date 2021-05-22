import logging

from celery_tasks.main import app
from . yuntongxun.sms import CCP
from . import constants

# logger = logging.getLogger("django")
#
# @app.task(name="send_sms_code")
# def send_sms_code(mobile, sms_code):
#     """短信验证码异步任务请求"""
#     ccp = CCP()
#     ccp = CCP(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
#
#     logger.debug("%s:%s" % (mobile, sms_code))

logger = logging.getLogger("django")

@app.task(name="send_sms_code")
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码的异步任务
    :param mobile: 手机号码
    :param sms_code: 短信验证码
    :return:
    """
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
    logger.debug("%s:%s" % (mobile, sms_code))