from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData


def generate_save_user_token(openid):
    """使用Itsdangrous保存openID，生成access_token"""
    serializer = Serializer(settings.SECRET_KEY, 300)
    # 返回数据 bytes类型
    data = {'openid': openid}
    token = serializer.dumps(data)

    return token


def check_save_user_token(access_token):
    """使用Itsdangrous获取access_token中的openID"""
    # serializer = Serializer(秘钥, 有效期秒)
    serializer = Serializer(settings.SECRET_KEY, 300)

    # 判断是否校验成功
    try:
        data = serializer.loads(access_token)
    except BadData:
        return None
    else:
        return data['openid']

