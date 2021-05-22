import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt认证成功返回数据"""

    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
    }

def get_user_by_account(account):
    """根据账号信息获取用户"""
    try:
        if re.match('^1[3-9]\d{9}$', account):
            user = User.objects.filter(mobile=account).first()
        else:
            user = User.objects.filter(username=account).first()
    except User.DoesNotExist:
        # 找不到对应的用户
        return None

    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """自定义用户认证"""

        user = get_user_by_account(username)
        # 检查用户名和密码
        if user is not None and user.check_password(password):
            return user

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from users import constants


def generate_save_user_token_url(user):
    """使用itsdangrous保存openid，生成access_token"""
    # 设置邮件有效期
    serializer = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)

    data = {'user_id': user.id}
    token = serializer.dumps(data)
    token = token.decode()

    # 拼接url地址
    verify_url = settings.VERIFY_EMAIL_HTML+ '?token=' + token

    return verify_url
